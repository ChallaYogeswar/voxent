#!/usr/bin/env python3
"""
VOXENT Quick Start Script

Simplifies the first-time setup and testing of the VOXENT pipeline.
Run this to verify everything is working correctly.
"""

import os
import sys
import subprocess

def run_command(cmd, description):
    """Run a command and print results."""
    print(f"\n{'='*60}")
    print(f"[RUNNING] {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("[WARNINGS/ERRORS]")
            print(result.stderr[:500])  # Limit output
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("[TIMEOUT] Command timed out")
        return False
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def main():
    print("\n" + "="*60)
    print("VOXENT Quick Start Setup")
    print("="*60)
    
    # Step 1: Verify installation
    print("\nStep 1: Verify Installation")
    print("-" * 60)
    if not run_command("python verify_installation.py", "Running installation verification"):
        print("\nWARNING: Some dependencies are missing!")
        print("\nPlease install PyTorch using conda:")
        print("   conda install pytorch torchvision torchaudio cpuonly -c pytorch -y")
        print("\nThen run this script again.")
        return False
    
    # Step 2: Check project structure
    print("\nStep 2: Checking Project Structure")
    print("-" * 60)
    
    required_dirs = [
        'data/input_calls',
        'data/voice_dataset/male',
        'data/voice_dataset/female',
        'data/voice_dataset/uncertain',
        'config',
        'models',
        'logs'
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"[OK] {dir_path}")
        else:
            os.makedirs(dir_path, exist_ok=True)
            print(f"[CREATED] {dir_path}")
    
    # Step 3: Test imports
    print("\nStep 3: Testing Core Imports")
    print("-" * 60)
    
    imports_to_test = [
        ("librosa", "Audio processing"),
        ("numpy", "Numerical operations"),
        ("sklearn", "Machine learning"),
        ("pandas", "Data handling"),
        ("flask", "Web framework"),
        ("yaml", "Config parsing"),
    ]
    
    all_imports_ok = True
    for module, description in imports_to_test:
        try:
            __import__(module)
            print(f"[OK] {module:20} ({description})")
        except ImportError:
            print(f"[FAIL] {module:20} ({description}) - NOT INSTALLED")
            all_imports_ok = False
    
    if not all_imports_ok:
        print("\nWARNING: Some imports failed. Install missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    # Step 4: Test module imports
    print("\nStep 4: Testing VOXENT Modules")
    print("-" * 60)
    
    voxent_tests = [
        ("from preprocessing.audio_loader import load_audio", "Audio loader"),
        ("from preprocessing.normalize import normalize", "Audio normalizer"),
        ("from classification.pitch_gender import PitchGenderClassifier", "Pitch classifier"),
        ("from classification import IntegratedGenderClassifier", "Integrated classifier"),
        ("from dataset.metadata import append_metadata", "Metadata handler"),
        ("from quality_assurance.metrics import QualityMetrics", "Quality metrics"),
    ]
    
    all_modules_ok = True
    for import_str, description in voxent_tests:
        try:
            exec(import_str)
            print(f"[OK] {description}")
        except Exception as e:
            print(f"[FAIL] {description}: {str(e)[:50]}")
            all_modules_ok = False
    
    if not all_modules_ok:
        print("\nWARNING: Some VOXENT modules failed to import.")
        print("   Check the errors above and fix import paths if needed.")
        return False
    
    # Step 5: Quick syntax check
    print("\nStep 5: Validating Python Syntax")
    print("-" * 60)
    
    files_to_check = [
        'classification/__init__.py',
        'classification/ml_classifier.py',
        'quality_assurance/metrics.py',
        'tests/test_pipeline.py',
        'engine/batch_runner.py',
    ]
    
    all_syntax_ok = True
    for file_path in files_to_check:
        result = subprocess.run(
            f"python -m py_compile {file_path}",
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print(f"[OK] {file_path}")
        else:
            print(f"[FAIL] {file_path}: Syntax error")
            all_syntax_ok = False
    
    if not all_syntax_ok:
        return False
    
    # Final success message
    print("\n" + "="*60)
    print("ALL CHECKS PASSED!")
    print("="*60)
    
    print("\nYou're ready to use VOXENT!")
    print("\nNext steps:")
    print("1. Place your audio files in: data/input_calls/")
    print("2. Configure settings in: config/config.yaml")
    print("3. Run the pipeline: python config/run_pipeline.py")
    print("4. Or start the web UI: python web_app.py")
    
    print("\nFor more information:")
    print("   - See README.md for documentation")
    print("   - Check MARKDOWN FILES/ for architecture and guides")
    print("   - Review ERROR_RESOLUTION_GUIDE.md if issues occur")
    
    print("\nTroubleshooting:")
    print("   - Run 'python verify_installation.py' anytime to check your setup")
    print("   - Check config/config.yaml for configuration options")
    print("   - Review logs in logs/ directory for detailed error messages")
    
    print("\n" + "="*60 + "\n")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
