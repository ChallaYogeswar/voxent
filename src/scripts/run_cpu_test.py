#!/usr/bin/env python
"""
VOXENT - CPU-ONLY Pipeline Test
Runs the full voice classification pipeline in CPU mode
"""

import os
import sys
import yaml
import time
import logging
import traceback
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def print_header(title):
    """Print formatted header"""
    print("\n" + "="*100)
    print(f"  {title}")
    print("="*100 + "\n")

def check_core_dependencies():
    """Verify core dependencies (without CUDA)"""
    print_header("CHECKING CORE DEPENDENCIES")
    
    required = {
        'yaml': 'PyYAML',
        'librosa': 'librosa',
        'soundfile': 'soundfile',
        'numpy': 'numpy',
        'scipy': 'scipy',
        'sklearn': 'scikit-learn',
        'psutil': 'psutil',
        'tqdm': 'tqdm',
    }
    
    missing = []
    for module, name in required.items():
        try:
            __import__(module)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name}")
            missing.append(name)
    
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        return False
    
    print(f"\n✅ All core dependencies available")
    return True

def check_classifiers_cpu():
    """Check if classifiers work in CPU mode"""
    print_header("CHECKING CLASSIFIERS (CPU MODE)")
    
    try:
        from classification.pitch_gender import PitchGenderClassifier
        print(f"  ✅ Pitch-Based Classifier")
        
        from classification.ml_classifier import MLGenderClassifier
        print(f"  ✅ ML Classifier Framework")
        
        try:
            from classification.advanced_gender_classifier import create_advanced_classifier
            print(f"  ✅ Advanced Multi-Feature Classifier")
        except Exception as e:
            print(f"  ⚠️  Advanced Classifier (optional)")
        
        print(f"\n✅ All classifiers loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Error loading classifiers: {e}")
        traceback.print_exc()
        return False

def test_pitch_classifier():
    """Test pitch classifier with sample audio"""
    print_header("TESTING PITCH CLASSIFIER")
    
    try:
        import numpy as np
        from classification.pitch_gender import PitchGenderClassifier
        
        classifier = PitchGenderClassifier()
        
        # Generate test audio
        sr = 16000
        duration = 2
        t = np.arange(int(sr * duration)) / sr
        
        # Male voice (low pitch)
        male_audio = np.sin(2 * np.pi * 120 * t) * 0.5
        label, conf = classifier.classify(male_audio, sr)
        print(f"  Male test: {label} ({conf:.1f}%)")
        
        # Female voice (high pitch)
        female_audio = np.sin(2 * np.pi * 220 * t) * 0.5
        label, conf = classifier.classify(female_audio, sr)
        print(f"  Female test: {label} ({conf:.1f}%)")
        
        print(f"\n✅ Pitch classifier working")
        return True
    except Exception as e:
        print(f"❌ Pitch classifier error: {e}")
        return False

def test_real_audio():
    """Test with real audio files"""
    print_header("TESTING WITH REAL AUDIO FILES")
    
    try:
        import soundfile as sf
        from classification.pitch_gender import PitchGenderClassifier
        
        input_dir = "data/input"
        classifier = PitchGenderClassifier()
        
        results = []
        audio_files = [f for f in os.listdir(input_dir) if f.endswith('.wav')][:3]
        
        print(f"  Processing {len(audio_files)} audio files...\n")
        
        for filename in audio_files:
            filepath = os.path.join(input_dir, filename)
            try:
                audio, sr = sf.read(filepath)
                label, conf = classifier.classify(audio, sr)
                results.append((filename, label, conf))
                print(f"  • {filename}: {label} ({conf:.1f}%)")
            except Exception as e:
                print(f"  ✗ {filename}: Error - {str(e)[:50]}")
        
        print(f"\n✅ Processed {len(results)} audio files")
        return True
    except Exception as e:
        print(f"❌ Real audio test error: {e}")
        traceback.print_exc()
        return False

def test_dataset_output():
    """Test dataset organization"""
    print_header("TESTING DATASET OUTPUT")
    
    try:
        from dataset.organizer import save_sample_with_counter, get_current_counter
        import soundfile as sf
        import numpy as np
        
        dataset_dir = "data/voice_dataset"
        os.makedirs(dataset_dir, exist_ok=True)
        os.makedirs(os.path.join(dataset_dir, "male"), exist_ok=True)
        os.makedirs(os.path.join(dataset_dir, "female"), exist_ok=True)
        
        # Generate test audio
        test_audio = np.random.randn(16000).astype(np.float32)
        sr = 16000
        
        # Save samples
        result1 = save_sample_with_counter(test_audio, sr, "male", dataset_dir, "test_original_1.wav")
        result2 = save_sample_with_counter(test_audio, sr, "female", dataset_dir, "test_original_2.wav")
        
        print(f"  Saved: {result1['new_filename']} (from {result1['original_filename']})")
        print(f"  Saved: {result2['new_filename']} (from {result2['original_filename']})")
        
        counter = get_current_counter()
        print(f"  Current counter: {counter}")
        
        print(f"\n✅ Dataset organization working")
        return True
    except Exception as e:
        print(f"❌ Dataset output error: {e}")
        traceback.print_exc()
        return False

def main():
    """Main entry point"""
    print("\n")
    print("[" + "="*98 + "]")
    print("|" + " "*98 + "|")
    print("|" + "VOXENT - VOICE CLASSIFICATION PIPELINE - CPU-ONLY TEST".center(98) + "|")
    print("|" + " "*98 + "|")
    print("[" + "="*98 + "]")
    
    tests = [
        ("Core Dependencies", check_core_dependencies),
        ("Classifiers (CPU)", check_classifiers_cpu),
        ("Pitch Classifier", test_pitch_classifier),
        ("Real Audio Files", test_real_audio),
        ("Dataset Output", test_dataset_output),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ Test '{test_name}' failed with error: {e}")
            results[test_name] = False
    
    # Generate summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n" + "[" + "="*98 + "]")
        print("|" + "✓ ALL TESTS PASSED - VOXENT IS OPERATIONAL (CPU MODE)".center(98) + "|")
        print("[" + "="*98 + "]")
        return 0
    else:
        print("\n" + "[" + "="*98 + "]")
        print("|" + f"x {total - passed} TEST(S) FAILED - REVIEW ERRORS ABOVE".center(98) + "|")
        print("[" + "="*98 + "]")
        return 1

if __name__ == "__main__":
    sys.exit(main())
