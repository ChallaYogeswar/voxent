#!/usr/bin/env python3
"""
VOXENT Installation Verification Script

Checks that all required dependencies are installed and configured correctly.
Run this before attempting to execute the pipeline.
"""

import sys
import os
import subprocess

def check_installation():
    """Verify all components are installed correctly."""
    issues = []
    warnings = []
    
    print("\n" + "="*60)
    print("VOXENT Installation Verification")
    print("="*60 + "\n")
    
    # Check Python version
    if sys.version_info < (3, 10):
        issues.append(f"[FAIL] Python version too old: {sys.version_info.major}.{sys.version_info.minor} (need 3.10+)")
    else:
        print(f"[OK] Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Check PyTorch/TorchAudio
    try:
        import torch
        import torchaudio
        print(f"[OK] PyTorch {torch.__version__}")
        print(f"[OK] TorchAudio {torchaudio.__version__}")
        
        if torch.cuda.is_available():
            print(f"[OK] CUDA available: {torch.cuda.get_device_name(0)}")
        else:
            print("[WARNING] CUDA not available (CPU-only mode)")
    except ImportError as e:
        issues.append(f"[FAIL] PyTorch/TorchAudio not installed: {e}")
    
    # Check HuggingFace Token
    if os.getenv("HF_TOKEN"):
        token = os.getenv("HF_TOKEN")
        print(f"[OK] HF_TOKEN configured ({token[:10]}...)")
    else:
        warnings.append("[WARNING] HF_TOKEN not set (diarization will fail)")
    
    # Check critical dependencies
    critical_deps = {
        'librosa': 'Audio feature extraction',
        'soundfile': 'Audio file I/O',
        'pyannote': 'Speaker diarization',
        'flask': 'Web interface',
        'pandas': 'Data handling',
        'sklearn': 'ML models',
        'numpy': 'Numerical operations',
        'tqdm': 'Progress tracking',
        'yaml': 'Config parsing',
    }
    
    print("\nCritical dependencies:")
    for dep, description in critical_deps.items():
        try:
            __import__(dep)
            print(f"[OK] {dep:15} ({description})")
        except ImportError:
            issues.append(f"[FAIL] {dep} not installed ({description})")
    
    # Check optional but recommended
    optional_deps = {
        'pydub': 'MP3 conversion',
        'requests': 'HTTP operations',
        'dotenv': 'Environment variables',
    }
    
    print("\nOptional dependencies:")
    for dep, description in optional_deps.items():
        try:
            __import__(dep)
            print(f"[OK] {dep:15} ({description})")
        except ImportError:
            warnings.append(f"[WARNING] {dep} not installed ({description})")
    
    # Check FFmpeg
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            check=True,
            timeout=5
        )
        version_line = result.stdout.split('\n')[0]
        print(f"\n[OK] FFmpeg installed")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        warnings.append("[WARNING] FFmpeg not found (required for audio conversion)")
    
    # Check directory structure
    print("\nDirectory structure:")
    required_dirs = {
        'data/input': 'Input audio directory',
        'data/voice_dataset': 'Output dataset directory',
        'config': 'Configuration directory',
        'models': 'Models directory',
        'logs': 'Logs directory',
    }
    
    for dir_path, description in required_dirs.items():
        if os.path.exists(dir_path):
            print(f"[OK] {dir_path:25} exists")
        else:
            os.makedirs(dir_path, exist_ok=True)
            print(f"[CREATED] {dir_path:25}")
    
    # Summary
    print("\n" + "="*60)
    
    if issues:
        print("\nCRITICAL ISSUES FOUND:\n")
        for issue in issues:
            print(f"  {issue}")
        print("\nThese must be fixed before running VOXENT")
        print("See ERROR_RESOLUTION_GUIDE.md for solutions")
        return False
    
    if warnings:
        print("\nWARNINGS:\n")
        for warning in warnings:
            print(f"  {warning}")
        print("\nYou can proceed, but some features may be limited")
    
    if not issues and not warnings:
        print("\nALL CHECKS PASSED!")
    
    print("\nNEXT STEPS:")
    print("   1. Place audio files in: data/input/")
    print("   2. Review config: config/config.yaml")
    print("   3. Run pipeline: python config/run_pipeline.py")
    print("   4. Or start web UI: python web_app.py")
    print("="*60 + "\n")
    
    return True

if __name__ == "__main__":
    success = check_installation()
    sys.exit(0 if success else 1)
