# VOXENT Improvement Plan
Date: December 29, 2024  
Status: Production Readiness Roadmap  
Priority: Critical Fixes + Architecture Optimization

---

## Executive Summary

VOXENT has achieved 85-95% MVP completion but requires three critical fixes before production deployment:

1. Speaker Separation - Currently separates vocals from music, but not speaker A from speaker B
2. Batch Folder Organization - Files need physical folder grouping by duration before processing
3. Diarization Integration - RTTM timestamps must drive segment extraction per speaker

Estimated Time to Production: 2-3 days of focused development

---

## Critical Issue #1: Speaker Separation Not Working

### Current Problem
```python
# What's happening now:
Input: call_recording.wav (Agent + Customer mixed)
   ↓ [Demucs Vocal Separation]
Output: vocals.wav (Agent + Customer STILL MIXED)
        accompaniment.wav (background noise/music)
```

Root Cause: Demucs separates vocal vs instrumental, not speaker A vs speaker B. You need speaker diarization → segment extraction, not source separation.

### Solution: Implement True Speaker Segmentation

```python
# What should happen:
Input: call_recording.wav (Agent + Customer)
   ↓ [Step 1: Speaker Diarization with pyannote]
RTTM Output:
  SPEAKER file1 0.0 3.5 SPEAKER_00  # Agent speaks 0-3.5s
  SPEAKER file1 3.5 7.2 SPEAKER_01  # Customer speaks 3.5-7.2s
  SPEAKER file1 7.2 12.8 SPEAKER_00 # Agent speaks 7.2-12.8s
   ↓ [Step 2: Extract segments per speaker]
Output: 
  agent_segment_001.wav (0-3.5s audio)
  customer_segment_001.wav (3.5-7.2s audio)
  agent_segment_002.wav (7.2-12.8s audio)
```

### Implementation Steps

#### Step 1: Fix `diarization/diarizer.py`

```python
"""
Enhanced Speaker Diarization with Segment Extraction
Properly integrates pyannote.audio to get RTTM-style output
"""

import os
import torch
import numpy as np
import soundfile as sf
from pyannote.audio import Pipeline
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

def diarize_and_extract_speakers(audio_path: str, hf_token: str) -> List[Dict]:
    """
    Perform speaker diarization and extract individual speaker segments.
    
    Returns:
        List of dicts with keys:
        - speaker: Speaker ID (SPEAKER_00, SPEAKER_01, etc.)
        - start: Start time in seconds
        - end: End time in seconds
        - audio: Extracted audio segment (numpy array)
        - duration: Segment duration
    """
    try:
        # Load diarization pipeline
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=hf_token
        )
        
        # Move to GPU if available
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        pipeline = pipeline.to(device)
        
        logger.info(f"Running diarization on {audio_path}...")
        
        # Run diarization
        diarization = pipeline(audio_path)
        
        # Load audio for segment extraction
        audio, sr = sf.read(audio_path)
        
        # Extract segments per speaker
        segments = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            start_sample = int(turn.start  sr)
            end_sample = int(turn.end  sr)
            
            # Extract audio segment
            segment_audio = audio[start_sample:end_sample]
            
            segments.append({
                'speaker': speaker,
                'start': turn.start,
                'end': turn.end,
                'duration': turn.end - turn.start,
                'audio': segment_audio,
                'sample_rate': sr
            })
        
        logger.info(f"Extracted {len(segments)} speaker segments")
        
        # Group by speaker for summary
        speaker_stats = {}
        for seg in segments:
            spk = seg['speaker']
            if spk not in speaker_stats:
                speaker_stats[spk] = {'count': 0, 'total_duration': 0}
            speaker_stats[spk]['count'] += 1
            speaker_stats[spk]['total_duration'] += seg['duration']
        
        logger.info(f"Speaker summary: {speaker_stats}")
        
        return segments
        
    except Exception as e:
        logger.error(f"Diarization failed: {e}")
        # Fallback: return entire audio as single speaker
        audio, sr = sf.read(audio_path)
        duration = len(audio) / sr
        return [{
            'speaker': 'SPEAKER_00',
            'start': 0.0,
            'end': duration,
            'duration': duration,
            'audio': audio,
            'sample_rate': sr
        }]


def save_speaker_segments(segments: List[Dict], output_dir: str, 
                         source_filename: str) -> List[str]:
    """
    Save extracted speaker segments to files.
    
    Returns:
        List of saved file paths
    """
    saved_files = []
    base_name = os.path.splitext(source_filename)[0]
    
    for idx, segment in enumerate(segments):
        speaker = segment['speaker']
        start = segment['start']
        end = segment['end']
        
        # Create speaker-specific directory
        speaker_dir = os.path.join(output_dir, f"speakers_{speaker}")
        os.makedirs(speaker_dir, exist_ok=True)
        
        # Generate filename with timing info
        filename = f"{base_name}_{speaker}_seg{idx:03d}_t{start:.1f}-{end:.1f}s.wav"
        filepath = os.path.join(speaker_dir, filename)
        
        # Save audio segment
        sf.write(filepath, segment['audio'], segment['sample_rate'])
        saved_files.append(filepath)
        
        logger.debug(f"Saved: {filename}")
    
    return saved_files
```

#### Step 2: Update `engine/batch_runner.py` to use proper diarization

```python
# Replace the vocal separation section with:

from diarization.diarizer import diarize_and_extract_speakers, save_speaker_segments

def process_file(file_path, cfg, separator=None):
    """Process file using SPEAKER DIARIZATION, not vocal separation"""
    
    try:
        logger.info(f"Processing: {os.path.basename(file_path)}")
        
        # Get HuggingFace token
        hf_token = os.getenv("HF_TOKEN")
        if not hf_token:
            logger.error("HF_TOKEN required for diarization")
            return {"error": "Missing HF_TOKEN"}
        
        # Step 1: Speaker Diarization + Segment Extraction
        segments = diarize_and_extract_speakers(file_path, hf_token)
        
        if not segments:
            logger.warning("No segments extracted")
            return {"segments_processed": 0}
        
        # Step 2: Process each speaker segment
        classifier = get_classifier(cfg)
        processed_segments = 0
        
        for segment in segments:
            audio = segment['audio']
            sr = segment['sample_rate']
            speaker = segment['speaker']
            duration = segment['duration']
            
            # Skip short segments
            if duration < cfg['min_segment_duration']:
                continue
            
            # Normalize audio
            audio = normalize(audio)
            
            # Classify gender
            gender, confidence = classifier.classify(audio, sr)
            
            # Save to dataset
            base_name = os.path.basename(file_path).replace('.wav', '').replace('.mp3', '')
            filename = f"{base_name}_{speaker}_t{segment['start']:.1f}s_{gender[0].upper()}_conf{int(confidence)}.wav"
            
            saved_path = save_sample(audio, sr, gender, filename, "data/voice_dataset")
            
            # Quality assessment
            quality_metrics = QualityMetrics(sr).assess_audio_quality(saved_path)
            
            # Metadata
            append_metadata("data/voice_dataset/metadata.csv", {
                "file": filename,
                "source": os.path.basename(file_path),
                "speaker": speaker,
                "start_time": segment['start'],
                "end_time": segment['end'],
                "duration": duration,
                "label": gender,
                "confidence": confidence,
                "quality_score": quality_metrics["quality_score"],
                "snr": quality_metrics["snr"]
            })
            
            processed_segments += 1
            logger.info(f"Processed {speaker}: {gender} ({confidence:.1f}%)")
        
        return {
            "file": os.path.basename(file_path),
            "segments_processed": processed_segments,
            "total_speakers": len(set(s['speaker'] for s in segments))
        }
        
    except Exception as e:
        logger.error(f"Processing error: {e}")
        return {"error": str(e)}
```

---

## Critical Issue #2: Batch Folder Organization

### Current Problem
Duration-based batching exists in code but doesn't create physical folders:
```
data/input_calls/
  ├── file1.wav (30s)
  ├── file2.wav (45s)
  ├── file3.wav (90s)
  └── file4.wav (120s)
```

### Solution: Create Physical Batch Folders

```python
# Create this new file: engine/batch_organizer.py

"""
Batch Organizer - Creates physical folders for duration-based batches
Organizes input files before processing
"""

import os
import shutil
import librosa
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

def organize_files_into_batches(input_dir: str, batch_dir: str, 
                                batch_size_minutes: int = 2,
                                files_per_batch: int = 10) -> Dict[str, List[str]]:
    """
    Organize audio files into batch folders based on duration.
    
    Args:
        input_dir: Source directory with audio files
        batch_dir: Target directory for batch folders
        batch_size_minutes: Duration threshold for batching
        files_per_batch: Maximum files per batch (for GPU memory)
    
    Returns:
        Dictionary mapping batch names to file lists
    """
    logger.info("Organizing files into batch folders...")
    
    # Get all audio files with durations
    files_with_duration = []
    for filename in os.listdir(input_dir):
        if not filename.endswith(('.wav', '.mp3')):
            continue
        
        filepath = os.path.join(input_dir, filename)
        try:
            duration = librosa.get_duration(filename=filepath)
            files_with_duration.append((filename, filepath, duration))
        except Exception as e:
            logger.warning(f"Could not get duration for {filename}: {e}")
    
    # Sort by duration (smallest first)
    files_with_duration.sort(key=lambda x: x[2])
    
    logger.info(f"Found {len(files_with_duration)} audio files")
    
    # Create batches
    batches = {}
    current_batch = []
    current_batch_duration = 0
    batch_num = 1
    
    for filename, filepath, duration in files_with_duration:
        # Check if adding this file exceeds batch limits
        if (len(current_batch) >= files_per_batch or 
            current_batch_duration + duration > batch_size_minutes  60):
            
            # Save current batch
            if current_batch:
                batch_name = f"batch_{batch_num:03d}"
                batches[batch_name] = current_batch
                batch_num += 1
                current_batch = []
                current_batch_duration = 0
        
        # Add file to current batch
        current_batch.append((filename, filepath, duration))
        current_batch_duration += duration
    
    # Add final batch
    if current_batch:
        batch_name = f"batch_{batch_num:03d}"
        batches[batch_name] = current_batch
    
    # Create physical batch folders
    os.makedirs(batch_dir, exist_ok=True)
    
    for batch_name, files in batches.items():
        batch_folder = os.path.join(batch_dir, batch_name)
        os.makedirs(batch_folder, exist_ok=True)
        
        total_duration = sum(f[2] for f in files)
        logger.info(f"Creating {batch_name}: {len(files)} files, "
                   f"{total_duration:.1f}s total duration")
        
        # Copy files to batch folder
        for filename, filepath, duration in files:
            dest_path = os.path.join(batch_folder, filename)
            if not os.path.exists(dest_path):
                shutil.copy2(filepath, dest_path)
                logger.debug(f"  → {filename} ({duration:.1f}s)")
    
    return batches


def get_batch_folders(batch_dir: str) -> List[str]:
    """Get list of batch folders in order."""
    if not os.path.exists(batch_dir):
        return []
    
    batches = [d for d in os.listdir(batch_dir) 
               if os.path.isdir(os.path.join(batch_dir, d)) 
               and d.startswith('batch_')]
    
    return sorted(batches)
```

#### Update `engine/batch_runner.py` to use batch folders:

```python
from engine.batch_organizer import organize_files_into_batches, get_batch_folders

def run(config_path):
    """Main pipeline with batch folder organization"""
    
    cfg = yaml.safe_load(open(config_path))
    
    input_dir = "data/input_calls"
    batch_dir = "data/batches"
    output_dir = "data/voice_dataset"
    
    # Step 1: Organize files into batch folders
    logger.info("Step 1: Organizing files into batches...")
    batches = organize_files_into_batches(
        input_dir=input_dir,
        batch_dir=batch_dir,
        batch_size_minutes=cfg.get('batch_size_minutes', 2),
        files_per_batch=cfg.get('files_per_batch', 10)
    )
    
    # Step 2: Process each batch folder sequentially
    batch_folders = get_batch_folders(batch_dir)
    logger.info(f"Found {len(batch_folders)} batches to process")
    
    all_results = []
    for batch_name in batch_folders:
        logger.info(f"\n{'='60}")
        logger.info(f"Processing {batch_name}")
        logger.info(f"{'='60}")
        
        batch_folder = os.path.join(batch_dir, batch_name)
        files = [os.path.join(batch_folder, f) 
                for f in os.listdir(batch_folder) 
                if f.endswith(('.wav', '.mp3'))]
        
        # Process batch
        batch_results = []
        for file_path in tqdm(files, desc=f"{batch_name}"):
            result = process_file(file_path, cfg)
            batch_results.append(result)
        
        all_results.extend(batch_results)
        
        # Clear GPU cache between batches
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            logger.info(f"Cleared GPU cache after {batch_name}")
    
    # Summary
    successful = len([r for r in all_results if "error" not in r])
    failed = len([r for r in all_results if "error" in r])
    
    logger.info(f"\nProcessing complete: {successful} successful, {failed} failed")
    
    return {
        "status": "completed",
        "total_batches": len(batch_folders),
        "total_files": len(all_results),
        "successful": successful,
        "failed": failed
    }
```

---

## Critical Issue #3: Code Structure Reorganization

### Current Problem
```
VOXENT/
  ├── many_py_files.py (scattered in root)
  ├── classification/
  ├── preprocessing/
  └── ...
```

### Solution: Proper Module Organization

```
VOXENT/
├── src/                          # ALL Python scripts here
│   ├── __init__.py
│   ├── main.py                  # Main entry point
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── batch_organizer.py
│   │   ├── batch_processor.py
│   │   └── pipeline_runner.py
│   ├── classification/          # Move existing
│   ├── preprocessing/           # Move existing
│   ├── diarization/             # Move existing (rename from dIarization)
│   ├── dataset/                 # Move existing
│   ├── quality/                 # Move existing (rename from quality_assurance)
│   └── utils/
│       ├── audio_utils.py
│       └── file_utils.py
├── config/
│   └── config.yaml
├── scripts/                      # Utility scripts
│   ├── verify_installation.py   # Move from root
│   ├── train_ml_classifier.py   # Move from root
│   └── quickstart.py            # Move from root
├── data/
│   ├── input_calls/             # Original uploads
│   ├── batches/                 # Organized batches (NEW)
│   └── voice_dataset/           # Final output
├── tests/
├── docs/                         # Move from MARKDOWN FILES
│   ├── mvps/
│   ├── progress/
│   └── guides/
└── requirements.txt
```

Migration script:

```python
# scripts/reorganize_project.py

import os
import shutil

def reorganize_project():
    """Reorganize VOXENT project structure"""
    
    # Create new directories
    os.makedirs("src/pipeline", exist_ok=True)
    os.makedirs("scripts", exist_ok=True)
    os.makedirs("docs/mvps", exist_ok=True)
    os.makedirs("docs/progress", exist_ok=True)
    os.makedirs("docs/guides", exist_ok=True)
    os.makedirs("data/batches", exist_ok=True)
    
    # Move root Python files to scripts/
    root_scripts = [
        "verify_installation.py",
        "quickstart.py",
        "train_ml_classifier.py",
        "convert_audio.py",
        "verification.py",
        "generate_test_audio.py"
    ]
    
    for script in root_scripts:
        if os.path.exists(script):
            shutil.move(script, f"scripts/{script}")
            print(f"Moved {script} → scripts/")
    
    # Move markdown docs
    if os.path.exists("MARKDOWN FILES"):
        for item in os.listdir("MARKDOWN FILES"):
            src = os.path.join("MARKDOWN FILES", item)
            if "MVP" in item:
                dest = f"docs/mvps/{item}"
            elif "PROGRESS" in item:
                dest = f"docs/progress/{item}"
            else:
                dest = f"docs/guides/{item}"
            
            if os.path.isfile(src):
                shutil.copy2(src, dest)
                print(f"Copied {item} → docs/")
    
    # Rename dIarization to diarization
    if os.path.exists("dIarization"):
        shutil.move("dIarization", "src/diarization")
        print("Renamed dIarization → src/diarization")
    
    # Move existing modules to src/
    modules = ["classification", "preprocessing", "dataset", 
               "quality_assurance", "engine", "data_augmentation"]
    
    for module in modules:
        if os.path.exists(module):
            dest = f"src/{module}"
            if module == "quality_assurance":
                dest = "src/quality"
            shutil.move(module, dest)
            print(f"Moved {module} → src/")
    
    print("\n✅ Project reorganization complete!")
    print("\nNext steps:")
    print("  1. Update import statements in Python files")
    print("  2. Run: python scripts/verify_installation.py")
    print("  3. Run: python src/main.py")

if __name__ == "__main__":
    reorganize_project()
```

---

## Configuration Updates

Update `config/config.yaml`:

```yaml
# Audio Processing
sample_rate: 16000
min_segment_duration: 1.0

# Batch Organization
batch_size_minutes: 2          # Duration threshold for batches
files_per_batch: 10            # Max files per batch (GPU memory)
batch_directory: "data/batches"

# Speaker Diarization
diarization:
  model: "pyannote/speaker-diarization-3.1"
  min_speakers: 2              # Minimum speakers (agent + customer)
  max_speakers: 2              # Maximum speakers
  min_segment_duration: 1.0    # Skip segments shorter than this

# Classification
classification:
  use_ml: false
  use_advanced: true
  pitch_male_threshold: 85.0
  pitch_female_threshold: 165.0

# GPU Settings
device: "cuda"
batch_size_gpu: 8
gpu_memory_fraction: 0.8
use_mixed_precision: true

# Output
output:
  dataset_dir: "data/voice_dataset"
  metadata_file: "data/voice_dataset/metadata.csv"
  save_speaker_folders: true   # Save by speaker ID
  save_gender_folders: true    # Save by gender
```

---

## Testing Plan

### Test 1: Speaker Diarization
```bash
# Create test with 2-speaker audio
python scripts/test_diarization.py --input test_2speakers.wav

# Expected output:
# Extracted 5 segments:
#   SPEAKER_00: 3 segments (15.2s total)
#   SPEAKER_01: 2 segments (12.8s total)
```

### Test 2: Batch Organization
```bash
# Organize existing files
python scripts/test_batch_organization.py

# Expected output:
# Created batch_001: 8 files, 95.3s total
# Created batch_002: 12 files, 118.7s total
# Created batch_003: 6 files, 87.2s total
```

### Test 3: End-to-End Pipeline
```bash
# Process with new structure
python src/main.py --config config/config.yaml

# Expected output:
# Processing batch_001 (8 files)
# - file1.wav: 2 speakers, 4 segments extracted
# - file2.wav: 2 speakers, 3 segments extracted
# ...
# Batch complete: 32 segments processed
```

---

## Additional Recommendations

### 1. Add RTTM Export
```python
def export_rttm(segments: List[Dict], output_file: str):
    """Export diarization results in RTTM format for analysis"""
    with open(output_file, 'w') as f:
        for seg in segments:
            # RTTM format: SPEAKER filename 1 start duration <NA> <NA> speaker <NA> <NA>
            f.write(f"SPEAKER {seg['source']} 1 {seg['start']:.3f} "
                   f"{seg['duration']:.3f} <NA> <NA> {seg['speaker']} <NA> <NA>\n")
```

### 2. Add Speaker Consistency Tracking
```python
def track_speaker_consistency(metadata_df):
    """Analyze speaker patterns across files"""
    # Track which speaker tends to be agent vs customer
    # Based on segment counts, durations, speech patterns
    pass
```

### 3. Add Quality Filters for Segments
```python
def filter_segments_by_quality(segments: List[Dict], min_snr: float = 10.0):
    """Filter out low-quality speaker segments"""
    filtered = []
    for seg in segments:
        snr = calculate_snr(seg['audio'])
        if snr >= min_snr and seg['duration'] >= 1.0:
            filtered.append(seg)
    return filtered
```

### 4. Add GPU Memory Management
```python
# In batch processing loop:
if torch.cuda.is_available():
    # Monitor GPU memory
    allocated = torch.cuda.memory_allocated() / 1e9
    reserved = torch.cuda.memory_reserved() / 1e9
    logger.info(f"GPU Memory: {allocated:.2f}GB allocated, {reserved:.2f}GB reserved")
    
    # Clear cache if usage > 80%
    if allocated / 4.0 > 0.8:  # RTX 2050 has 4GB
        torch.cuda.empty_cache()
```

---

## Success Metrics

Before Improvements:
- ❌ Outputs: Mixed vocals (agent + customer together)
- ❌ Organization: Files scattered in single directory
- ❌ Processing: Sequential without batch awareness

After Improvements:
- ✅ Outputs: Separated segments per speaker (agent_001.wav, customer_001.wav)
- ✅ Organization: Batch folders (batch_001/, batch_002/, ...)
- ✅ Processing: Batch-aware with GPU optimization
- ✅ Metadata: RTTM timestamps for each speaker turn

---

