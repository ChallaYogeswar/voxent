import os
import soundfile as sf
import warnings
import torch
import logging

logger = logging.getLogger(__name__)

_pipeline = None

def get_pipeline():
    """Get or create the diarization pipeline with GPU support."""
    global _pipeline
    if _pipeline is None:
        token = os.getenv("HF_TOKEN")
        if not token:
            raise ValueError("HF_TOKEN environment variable is required for pyannote/speaker-diarization. Please set it with your Hugging Face token.")
        try:
            # Suppress torchcodec warnings
            warnings.filterwarnings("ignore", message=".*torchcodec.*")
            from pyannote.audio import Pipeline
            _pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-community-1", use_auth_token=token)
            
            # Move to GPU if available
            if torch.cuda.is_available():
                _pipeline = _pipeline.to(torch.device('cuda'))
                logger.info(f"✅ Diarization pipeline moved to GPU: {torch.cuda.get_device_name(0)}")
            else:
                logger.info("ℹ️  Using CPU for diarization (GPU not available)")
                
        except ImportError as e:
            logger.warning(f"pyannote.audio not available: {e}")
            _pipeline = None
        except Exception as e:
            logger.warning(f"Failed to load diarization pipeline: {e}")
            logger.warning("Diarization will be skipped. Files will be processed as single segments.")
            _pipeline = None
    return _pipeline

def diarize(audio_path):
    """Perform speaker diarization on audio file with GPU acceleration."""
    pipeline = get_pipeline()
    
    if pipeline is None:
        # Fallback: return entire file as single segment
        try:
            audio, sr = sf.read(audio_path)
            duration = len(audio) / sr
            return [{"start": 0, "end": duration, "speaker": "unknown"}]
        except Exception as e:
            logger.error(f"Error reading audio for fallback segmentation: {e}")
            return [{"start": 0, "end": 1, "speaker": "unknown"}]
    
    try:
        diarization = pipeline(audio_path)
        segments = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            segments.append({
                "start": turn.start,
                "end": turn.end,
                "speaker": speaker
            })
        return segments if segments else [{"start": 0, "end": 1, "speaker": "unknown"}]
    except Exception as e:
        print(f"Diarization failed for {audio_path}: {e}")
        # Fallback to single segment
        try:
            audio, sr = sf.read(audio_path)
            duration = len(audio) / sr
            return [{"start": 0, "end": duration, "speaker": "unknown"}]
        except:
            return [{"start": 0, "end": 1, "speaker": "unknown"}]
