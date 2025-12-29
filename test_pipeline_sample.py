#!/usr/bin/env python
"""
VOXENT Pipeline Test
Test the full pipeline with available audio files
"""

import sys
import os
import logging

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

print("\n" + "="*70)
print("VOXENT PIPELINE TEST")
print("="*70 + "\n")

# Import components
import yaml
import numpy as np
import soundfile as sf
from tqdm import tqdm
from preprocessing.audio_loader import load_audio
from preprocessing.normalize import normalize
from classification import get_classifier
from dataset.organizer import get_current_counter, reset_counter
from dataset.metadata import append_metadata

# Load configuration
try:
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    logger.info("✅ Configuration loaded")
except Exception as e:
    logger.error(f"❌ Failed to load config: {e}")
    sys.exit(1)

# Initialize classifier
try:
    classifier = get_classifier(config)
    logger.info("✅ Classifier initialized")
except Exception as e:
    logger.error(f"❌ Failed to initialize classifier: {e}")
    sys.exit(1)

# Get input files
input_dir = "data/input_calls"
if not os.path.exists(input_dir):
    logger.error(f"❌ Input directory not found: {input_dir}")
    sys.exit(1)

audio_files = [
    os.path.join(input_dir, f) 
    for f in os.listdir(input_dir) 
    if f.endswith('.wav') or f.endswith('.mp3')
]

if not audio_files:
    logger.error("❌ No audio files found in input directory")
    sys.exit(1)

logger.info(f"✅ Found {len(audio_files)} audio files to process")

# Reset counter for fresh test
logger.info("Resetting file counter...")
reset_counter()

# Process files
print("\n[PROCESSING AUDIO FILES]")
print("-" * 70)

results = {
    "total_files": len(audio_files),
    "processed": 0,
    "male": 0,
    "female": 0,
    "uncertain": 0,
    "errors": 0,
    "details": []
}

for idx, file_path in enumerate(audio_files[:3], 1):  # Test with first 3 files
    try:
        filename = os.path.basename(file_path)
        logger.info(f"\n[{idx}/{min(3, len(audio_files))}] Processing: {filename}")
        
        # Load audio
        audio = load_audio(file_path, config["sample_rate"])
        duration = len(audio) / config["sample_rate"]
        logger.info(f"  - Duration: {duration:.2f}s")
        
        # Normalize
        audio = normalize(audio)
        logger.info(f"  - Normalized")
        
        # Classify
        gender, confidence = classifier.classify(audio, config["sample_rate"])
        logger.info(f"  - Classification: {gender.upper()} ({confidence:.1f}% confidence)")
        
        # Save sample (simulated)
        label_dir = {
            "male": "data/voice_dataset/male",
            "female": "data/voice_dataset/female",
            "uncertain": "data/voice_dataset/uncertain"
        }[gender]
        
        os.makedirs(label_dir, exist_ok=True)
        counter = get_current_counter() + 1
        output_file = f"voice_sample_{counter:04d}.wav"
        output_path = os.path.join(label_dir, output_file)
        
        # In a real scenario, would save audio here
        # sf.write(output_path, audio, config["sample_rate"])
        
        logger.info(f"  - Would save to: {label_dir}/{output_file}")
        
        # Update results
        results["processed"] += 1
        results[gender] += 1
        results["details"].append({
            "file": filename,
            "gender": gender,
            "confidence": confidence,
            "duration": duration
        })
        
    except Exception as e:
        logger.error(f"  ❌ Error: {e}")
        results["errors"] += 1

# Print summary
print("\n" + "="*70)
print("TEST RESULTS SUMMARY")
print("="*70)

print(f"\n📊 Processing Results:")
print(f"  ✅ Successfully processed: {results['processed']} files")
print(f"  ❌ Errors: {results['errors']} files")
print(f"\n👥 Gender Classification:")
print(f"  - Male: {results['male']} samples")
print(f"  - Female: {results['female']} samples")
print(f"  - Uncertain: {results['uncertain']} samples")

if results['details']:
    print(f"\n📝 Details:")
    for detail in results['details']:
        print(f"  - {detail['file']}")
        print(f"    ├─ Gender: {detail['gender'].upper()}")
        print(f"    ├─ Confidence: {detail['confidence']:.1f}%")
        print(f"    └─ Duration: {detail['duration']:.2f}s")

# Classifier info
print(f"\n🎯 Classifier Information:")
info = classifier.get_classifier_info()
print(f"  - Device: {info['device']}")
print(f"  - ML Classifier: {'Available' if info['ml_available'] else 'Not available'}")
print(f"  - Advanced Classifier: {'Available' if info['advanced_available'] else 'Not available'}")
print(f"  - Priority: {' → '.join(info['classification_priority'])}")

# Next steps
print(f"\n📋 Next Steps:")
print(f"  1. Run full pipeline: python config/run_pipeline.py")
print(f"  2. Check output: data/voice_dataset/")
print(f"  3. View metadata: data/voice_dataset/metadata.csv")

if not info['ml_available']:
    print(f"\n💡 Optimization Tips:")
    print(f"  - Train ML classifier: python train_ml_classifier.py")
    print(f"  - Install Parselmouth: pip install praat-parselmouth")
    print(f"  - Install GPU PyTorch: conda install pytorch pytorch-cuda=11.8 -c pytorch -c nvidia")

print("\n" + "="*70)
print("✅ PIPELINE TEST COMPLETE")
print("="*70 + "\n")
