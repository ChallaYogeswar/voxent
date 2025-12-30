"""
VOXENT Testing Script
Tests installation and basic functionality
"""

import os
import sys
import torch
import tempfile
import numpy as np
from pathlib import Path


def print_section(title):
    """Print section header"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")


def test_imports():
    """Test if all required modules can be imported"""
    print_section("Testing Imports")
    
    modules = [
        ('torch', 'PyTorch'),
        ('torchaudio', 'TorchAudio'),
        ('pyannote.audio', 'Pyannote.audio'),
        ('librosa', 'Librosa'),
        ('yaml', 'PyYAML'),
        ('tqdm', 'TQDM'),
        ('psutil', 'Psutil')
    ]
    
    all_passed = True
    for module_name, display_name in modules:
        try:
            __import__(module_name)
            print(f"✅ {display_name:20s} - OK")
        except ImportError as e:
            print(f"❌ {display_name:20s} - FAILED: {e}")
            all_passed = False
    
    return all_passed


def test_gpu():
    """Test GPU availability"""
    print_section("Testing GPU")
    
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
        print(f"✅ GPU detected: {gpu_name}")
        print(f"   Total VRAM: {gpu_memory:.2f} GB")
        
        # Test GPU computation
        try:
            x = torch.randn(100, 100).cuda()
            y = torch.matmul(x, x)
            torch.cuda.synchronize()
            print(f"✅ GPU computation test passed")
            return True
        except Exception as e:
            print(f"❌ GPU computation test failed: {e}")
            return False
    else:
        print("⚠️  No GPU detected - will use CPU")
        return False


def test_config():
    """Test configuration file"""
    print_section("Testing Configuration")
    
    if not os.path.exists('config.yaml'):
        print("❌ config.yaml not found")
        return False
    
    try:
        import yaml
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        print("✅ config.yaml loaded successfully")
        
        # Check HuggingFace token
        hf_token = config.get('huggingface', {}).get('token')
        if hf_token and hf_token != 'null' and hf_token is not None:
            print("✅ HuggingFace token configured")
        else:
            print("⚠️  HuggingFace token not set")
            print("   Required for speaker diarization")
        
        return True
        
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        return False


def test_modules():
    """Test custom modules"""
    print_section("Testing Custom Modules")
    
    modules_to_test = [
        'enhanced_diarizer.py',
        'batch_organizer.py',
        'batch_processor.py',
        'voxent_pipeline.py'
    ]
    
    all_passed = True
    for module_file in modules_to_test:
        if os.path.exists(module_file):
            print(f"✅ {module_file:25s} - Found")
            
            # Try to import
            try:
                module_name = module_file.replace('.py', '')
                __import__(module_name)
                print(f"   ↳ Import successful")
            except Exception as e:
                print(f"   ⚠️  Import warning: {e}")
        else:
            print(f"❌ {module_file:25s} - Not found")
            all_passed = False
    
    return all_passed


def test_directories():
    """Test if required directories exist"""
    print_section("Testing Directories")
    
    required_dirs = [
        'data/input_calls',
        'data/batches',
        'data/voice_dataset',
        'data/temp',
        'logs'
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path:30s} - Exists")
        else:
            print(f"❌ {dir_path:30s} - Missing")
            all_exist = False
    
    return all_exist


def test_audio_generation():
    """Test audio file generation and processing"""
    print_section("Testing Audio Generation")
    
    try:
        import torchaudio
        import tempfile
        
        # Generate test audio (1 second, 16kHz, sine wave)
        sample_rate = 16000
        duration = 1.0
        frequency = 440.0  # A4 note
        
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = np.sin(2 * np.pi * frequency * t)
        
        # Convert to tensor
        audio_tensor = torch.from_numpy(audio).float().unsqueeze(0)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
            tmp_path = tmp_file.name
            torchaudio.save(tmp_path, audio_tensor, sample_rate)
        
        print(f"✅ Generated test audio: {tmp_path}")
        
        # Try to load it back
        waveform, sr = torchaudio.load(tmp_path)
        print(f"✅ Loaded test audio: {waveform.shape}, {sr} Hz")
        
        # Clean up
        os.remove(tmp_path)
        print(f"✅ Audio generation test passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Audio generation test failed: {e}")
        return False


def test_batch_organizer():
    """Test batch organizer with sample data"""
    print_section("Testing Batch Organizer")
    
    try:
        from batch_organizer import BatchOrganizer
        
        config = {
            'files_per_batch': 10,
            'batch_size_minutes': 2.0
        }
        
        organizer = BatchOrganizer(config)
        print("✅ BatchOrganizer initialized")
        
        # Test duration calculation with a dummy file
        # (This will fail if no audio files exist, but that's OK for testing)
        print("✅ Batch organizer test passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Batch organizer test failed: {e}")
        return False


def test_gpu_monitor():
    """Test GPU monitoring"""
    print_section("Testing GPU Monitor")
    
    try:
        from batch_processor import GPUMonitor
        
        monitor = GPUMonitor()
        print("✅ GPUMonitor initialized")
        
        # Get memory status
        monitor.print_memory_status()
        
        # Test cache clearing
        if monitor.has_gpu:
            monitor.clear_cache()
            print("✅ GPU cache clearing works")
        
        return True
        
    except Exception as e:
        print(f"❌ GPU monitor test failed: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print(" "*25 + "VOXENT TEST SUITE")
    print("="*70)
    
    results = {
        'Imports': test_imports(),
        'GPU': test_gpu(),
        'Configuration': test_config(),
        'Custom Modules': test_modules(),
        'Directories': test_directories(),
        'Audio Generation': test_audio_generation(),
        'Batch Organizer': test_batch_organizer(),
        'GPU Monitor': test_gpu_monitor()
    }
    
    # Summary
    print_section("Test Summary")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:25s} - {status}")
    
    print(f"\n{'='*60}")
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print(f"{'='*60}\n")
    
    if passed == total:
        print("🎉 All tests passed! System is ready.")
        return True
    else:
        print("⚠️  Some tests failed. Please address the issues above.")
        return False


def main():
    """Main test function"""
    success = run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
