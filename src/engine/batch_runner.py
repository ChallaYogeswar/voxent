
import os
import sys
import yaml
import logging
import psutil
import time
import numpy as np
import torch
import librosa
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from preprocessing.audio_loader import load_audio
from preprocessing.normalize import normalize
from preprocessing.vad import remove_silence
from preprocessing.source_separator import VocalSeparator
from classification import get_classifier
from dataset.organizer import save_sample
from dataset.metadata import append_metadata
from quality.metrics import QualityMetrics
from data_augmentation.augment import balance_dataset

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_duration_batches(files: list, batch_size_minutes: int = 2) -> dict:
    """
    Sort files into batches by duration.
    
    Args:
        files: List of audio file paths
        batch_size_minutes: Duration threshold for batch assignment (in minutes)
    
    Returns:
        Dictionary mapping batch names to file lists
    """
    logger.info("Creating duration-based batches...")
    batches = {}
    
    for file_path in files:
        try:
            # Get audio duration
            duration = librosa.get_duration(filename=file_path)
            batch_num = int(duration // (batch_size_minutes * 60)) + 1
            batch_key = f"batch_{batch_num}"
            
            if batch_key not in batches:
                batches[batch_key] = []
                
            batches[batch_key].append(file_path)
            logger.debug(f"  {os.path.basename(file_path)}: {duration:.1f}s → {batch_key}")
            
        except Exception as e:
            logger.warning(f"Failed to get duration for {file_path}: {e}, putting in batch_0")
            if "batch_0" not in batches:
                batches["batch_0"] = []
            batches["batch_0"].append(file_path)
    
    # Log batch summary
    for batch_name in sorted(batches.keys()):
        logger.info(f"  {batch_name}: {len(batches[batch_name])} files")
    
    return batches

def convert_mp3_to_wav_if_needed(input_dir):
    """Automatically convert MP3 files to WAV before processing."""
    import glob
    try:
        from pydub import AudioSegment
    except ImportError:
        logger.warning("pydub not installed - MP3 conversion disabled. Install with: pip install pydub")
        return
    
    mp3_files = glob.glob(os.path.join(input_dir, '*.mp3'))
    
    if not mp3_files:
        logger.debug("No MP3 files found to convert")
        return
    
    logger.info(f"Converting {len(mp3_files)} MP3 files to WAV...")
    
    for mp3_file in mp3_files:
        wav_file = mp3_file.replace('.mp3', '.wav')
        
        if os.path.exists(wav_file):
            logger.debug(f"Skipping {mp3_file} (WAV already exists)")
            continue
        
        try:
            audio = AudioSegment.from_mp3(mp3_file)
            # Ensure mono and 16kHz
            audio = audio.set_channels(1).set_frame_rate(16000)
            audio.export(wav_file, format='wav')
            logger.info(f"Converted: {os.path.basename(mp3_file)} → {os.path.basename(wav_file)}")
        except Exception as e:
            logger.error(f"Failed to convert {mp3_file}: {e}")

def validate_config(cfg):
    """Validate configuration parameters."""
    # Check for nested structure first (new format)
    if 'preprocessing' in cfg and 'diarization' in cfg:
        sample_rate = cfg['preprocessing'].get('sample_rate', 16000)
        min_segment_duration = cfg['diarization'].get('min_segment_duration', 1.0)
    else:
        # Fallback to old flat structure
        sample_rate = cfg.get('sample_rate', 16000)
        min_segment_duration = cfg.get('min_segment_duration', 1.0)
    
    if sample_rate <= 0:
        raise ValueError("sample_rate must be positive")
    if min_segment_duration <= 0:
        raise ValueError("min_segment_duration must be positive")

    # Validate classification settings
    if 'classification' in cfg:
        class_cfg = cfg['classification']
        if 'pitch_male_threshold' in class_cfg and 'pitch_female_threshold' in class_cfg:
            if class_cfg['pitch_male_threshold'] >= class_cfg['pitch_female_threshold']:
                raise ValueError("pitch_male_threshold must be less than pitch_female_threshold")

    # Legacy validation for backward compatibility
    if 'male_pitch_threshold' in cfg and 'female_pitch_threshold' in cfg:
        if cfg['male_pitch_threshold'] >= cfg['female_pitch_threshold']:
            raise ValueError("male_pitch_threshold must be less than female_pitch_threshold")

    logger.info("Configuration validation passed")
    return True

def monitor_performance():
    """Monitor system performance during processing."""
    memory = psutil.virtual_memory()
    return {
        "memory_percent": memory.percent,
        "memory_used_gb": memory.used / (1024**3),
        "cpu_percent": psutil.cpu_percent(interval=1)
    }

def get_config_value(cfg, key, default=None):
    """Get config value, handling both nested and flat structures."""
    if 'preprocessing' in cfg and key in cfg['preprocessing']:
        return cfg['preprocessing'][key]
    elif 'diarization' in cfg and key in cfg['diarization']:
        return cfg['diarization'][key]
    else:
        return cfg.get(key, default)

def process_file(file_path, cfg, separator=None):
    """Process a single audio file using source separation."""
    start_time = time.time()

    try:
        logger.info(f"Processing file: {os.path.basename(file_path)}")

        # Load and validate configuration
        validate_config(cfg)

        # Initialize classifier and separator if needed
        classifier = get_classifier(cfg)
        if separator is None:
            separator = VocalSeparator(model_name="htdemucs", device="cpu")

        # Load and preprocess audio
        audio = load_audio(file_path, get_config_value(cfg, "sample_rate", 16000))
        audio = normalize(audio)

        # Monitor memory before separation
        mem_before = monitor_performance()

        # Separate vocals from accompaniment
        logger.info(f"Separating vocals from accompaniment...")
        try:
            separation_result = separator.separate_vocals(audio, get_config_value(cfg, "sample_rate", 16000))
            vocals = separation_result["vocals"]
            accompaniment = separation_result["accompaniment"]
            vocal_confidence = separation_result["confidence"]
        except Exception as e:
            logger.warning(f"Vocal separation failed, using original audio: {e}")
            vocals = audio
            accompaniment = np.zeros_like(audio)
            vocal_confidence = 0.0

        # Track results for male and female samples
        processed_segments = 0
        gender_distribution = {"male": 0, "female": 0, "uncertain": 0}

        # Process vocals track
        logger.info(f"Classifying separated vocal track...")
        try:
            # Classify the vocal track
            vocal_label, vocal_conf = classifier.classify(vocals, get_config_value(cfg, "sample_rate", 16000))
            
            # Skip if too short
            if len(vocals) / get_config_value(cfg, "sample_rate", 16000) >= get_config_value(cfg, "min_segment_duration", 1.0):
                # Estimate pitch for metadata
                from classification.pitch_gender import PitchGenderClassifier
                pitch_estimator = PitchGenderClassifier()
                try:
                    pitch = pitch_estimator.estimate_pitch(vocals, get_config_value(cfg, "sample_rate", 16000))
                except:
                    pitch = 0.0

                # Create filename for separated vocals
                base_name = os.path.basename(file_path).replace('.wav', '').replace('.mp3', '')
                name = f"{base_name}_vocals_gender{vocal_label[0].upper()}_conf{int(vocal_conf)}.wav"
                
                saved_path = save_sample(vocals, get_config_value(cfg, "sample_rate", 16000), vocal_label, name, "data/voice_dataset")

                # Assess audio quality
                quality_metrics = QualityMetrics(cfg["sample_rate"]).assess_audio_quality(saved_path)

                # Append metadata with quality metrics and separation info
                metadata_entry = {
                    "file": name,
                    "source": os.path.basename(file_path),
                    "speaker": f"vocals_{vocal_label}",
                    "pitch": pitch,
                    "label": vocal_label,
                    "confidence": vocal_conf,
                    "duration": len(vocals) / cfg["sample_rate"],
                    "quality_score": quality_metrics["quality_score"],
                    "snr": quality_metrics["snr"],
                    "clipping_ratio": quality_metrics["clipping_ratio"],
                    "silence_ratio": quality_metrics["silence_ratio"],
                    "separation_type": "vocals",
                    "separation_confidence": vocal_confidence
                }

                append_metadata("data/voice_dataset/metadata.csv", metadata_entry)
                gender_distribution[vocal_label] += 1
                processed_segments += 1
                logger.info(f"Saved separated vocals as {vocal_label}: {name}")

        except Exception as e:
            logger.error(f"Error classifying vocal track: {e}")

        # Process accompaniment track if it contains meaningful audio
        if np.mean(accompaniment ** 2) > 0.001:  # Check if accompaniment has energy
            logger.info(f"Classifying separated accompaniment track...")
            try:
                # Classify the accompaniment
                accomp_label, accomp_conf = classifier.classify(accompaniment, get_config_value(cfg, "sample_rate", 16000))
                
                # Skip if too short
                if len(accompaniment) / get_config_value(cfg, "sample_rate", 16000) >= get_config_value(cfg, "min_segment_duration", 1.0):
                    # Estimate pitch for metadata
                    from classification.pitch_gender import PitchGenderClassifier
                    pitch_estimator = PitchGenderClassifier()
                    try:
                        pitch = pitch_estimator.estimate_pitch(accompaniment, get_config_value(cfg, "sample_rate", 16000))
                    except:
                        pitch = 0.0

                    # Create filename for separated accompaniment
                    base_name = os.path.basename(file_path).replace('.wav', '').replace('.mp3', '')
                    name = f"{base_name}_accompaniment_gender{accomp_label[0].upper()}_conf{int(accomp_conf)}.wav"
                    
                    saved_path = save_sample(accompaniment, cfg["sample_rate"], accomp_label, name, "data/voice_dataset")

                    # Assess audio quality
                    quality_metrics = QualityMetrics(cfg["sample_rate"]).assess_audio_quality(saved_path)

                    # Append metadata
                    metadata_entry = {
                        "file": name,
                        "source": os.path.basename(file_path),
                        "speaker": f"accompaniment_{accomp_label}",
                        "pitch": pitch,
                        "label": accomp_label,
                        "confidence": accomp_conf,
                        "duration": len(accompaniment) / cfg["sample_rate"],
                        "quality_score": quality_metrics["quality_score"],
                        "snr": quality_metrics["snr"],
                        "clipping_ratio": quality_metrics["clipping_ratio"],
                        "silence_ratio": quality_metrics["silence_ratio"],
                        "separation_type": "accompaniment",
                        "separation_confidence": vocal_confidence
                    }

                    append_metadata("data/voice_dataset/metadata.csv", metadata_entry)
                    gender_distribution[accomp_label] += 1
                    processed_segments += 1
                    logger.info(f"Saved separated accompaniment as {accomp_label}: {name}")

            except Exception as e:
                logger.error(f"Error classifying accompaniment track: {e}")

        processing_time = time.time() - start_time
        mem_after = monitor_performance()

        logger.info(f"Successfully processed {file_path}: {processed_segments} tracks in {processing_time:.2f}s")
        logger.info(f"Gender distribution: {gender_distribution}")

        return {
            "file": os.path.basename(file_path),
            "segments_processed": processed_segments,
            "gender_distribution": gender_distribution,
            "processing_time": processing_time,
            "memory_delta": mem_after["memory_used_gb"] - mem_before["memory_used_gb"]
        }

    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")
        return {
            "file": os.path.basename(file_path),
            "error": str(e),
            "processing_time": time.time() - start_time
        }

def run_parallel(files, cfg, max_workers=2):
    """Run processing in parallel with shared separator."""
    results = []
    # Create separator once and share across threads
    try:
        separator = VocalSeparator(model_name="htdemucs", device="cpu")
    except Exception as e:
        logger.error(f"Failed to initialize separator: {e}")
        separator = None
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(process_file, file_path, cfg, separator): file_path for file_path in files}

        for future in tqdm(as_completed(future_to_file), total=len(files), desc="Processing files"):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                logger.error(f"Thread execution error: {e}")
                results.append({"error": str(e)})

    return results

def run(config_path):
    """Main processing function with duration-based batching and GPU support."""
    try:
        # Load and validate configuration
        cfg = yaml.safe_load(open(config_path))
        validate_config(cfg)

        # Log GPU status
        if torch.cuda.is_available():
            logger.info(f"🚀 GPU detected: {torch.cuda.get_device_name(0)}")
            device = torch.device('cuda')
        else:
            logger.info("⚠️  GPU not available, using CPU")
            device = torch.device('cpu')

        # Set up directories
        input_dir = "data/input"
        dataset_dir = "data/voice_dataset"

        os.makedirs(input_dir, exist_ok=True)
        os.makedirs(dataset_dir, exist_ok=True)
        os.makedirs(os.path.join(dataset_dir, "male"), exist_ok=True)
        os.makedirs(os.path.join(dataset_dir, "female"), exist_ok=True)
        os.makedirs(os.path.join(dataset_dir, "uncertain"), exist_ok=True)

        # Convert MP3 files to WAV
        convert_mp3_to_wav_if_needed(input_dir)

        # Get files to process (both .wav and .mp3)
        wav_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".wav")]
        mp3_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".mp3")]
        
        files = wav_files + mp3_files

        if not files:
            logger.warning("No audio files found in input directory")
            return {"status": "no_files", "message": "No audio files found"}

        logger.info(f"Starting batch processing of {len(files)} files ({len(wav_files)} WAV, {len(mp3_files)} MP3)")

        # Create duration-based batches
        batches = create_duration_batches(files, batch_size_minutes=cfg.get('batch_size_minutes', 2))
        logger.info(f"Created {len(batches)} batches based on audio duration")
        
        # Process batches in order (smallest first)
        all_results = []
        for batch_name in sorted(batches.keys()):
            batch_files = batches[batch_name]
            logger.info(f"Processing {batch_name}: {len(batch_files)} files")
            
            # Use GPU batch processing if available
            if device.type == 'cuda':
                logger.info(f"  🚀 Using GPU acceleration for batch")
                torch.cuda.empty_cache()
            
            results = run_parallel(batch_files, cfg, max_workers=cfg.get('max_workers', 2))
            all_results.extend(results)
            
            # Clear GPU cache between batches
            if device.type == 'cuda':
                torch.cuda.empty_cache()

        # Generate summary

        # Initialize separator once for better performance
        try:
            separator = VocalSeparator(model_name="htdemucs", device="cpu")
        except Exception as e:
            logger.error(f"Failed to initialize separator: {e}")
            separator = None

        # Choose processing method based on file count
        if len(files) <= 2:
            # Sequential processing for small batches
            results = []
            for file_path in tqdm(files, desc="Processing files"):
                result = process_file(file_path, cfg, separator)
                results.append(result)
        else:
            # Parallel processing for larger batches
            max_workers = min(cfg.get("parallel_workers", 2), len(files))
            results = run_parallel(files, cfg, max_workers)

        # Data augmentation if enabled
        if cfg.get("enable_augmentation", False):
            logger.info("Running data augmentation...")
            try:
                balance_dataset(dataset_dir, cfg)
                logger.info("Data augmentation completed")
            except Exception as e:
                logger.error(f"Data augmentation failed: {e}")

        # Summary
        successful = len([r for r in results if "error" not in r])
        failed = len([r for r in results if "error" in r])

        logger.info(f"Batch processing completed: {successful} successful, {failed} failed")

        return {
            "status": "completed",
            "total_files": len(files),
            "successful": successful,
            "failed": failed,
            "results": results
        }

    except Exception as e:
        logger.error(f"Batch processing failed: {e}")
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python batch_runner.py <config_path>")
        sys.exit(1)

    result = run(sys.argv[1])
    print(f"Processing result: {result}")
