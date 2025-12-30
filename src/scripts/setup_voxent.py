"""
VOXENT Installation and Setup Script
Installs dependencies and sets up the environment
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path


def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    print(f"Running: {command}\n")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=False)
        if result.returncode != 0:
            print(f"⚠️  Command returned non-zero exit code: {result.returncode}")
            return False
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def check_python_version():
    """Check Python version"""
    print("\nChecking Python version...")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required!")
        return False
    
    print("✅ Python version is compatible")
    return True


def check_gpu():
    """Check for GPU availability"""
    print("\nChecking for GPU...")
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✅ GPU detected: {torch.cuda.get_device_name(0)}")
            print(f"   CUDA Version: {torch.version.cuda}")
            print(f"   Total VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
            return True
        else:
            print("⚠️  No GPU detected. Will use CPU (slower)")
            return False
    except ImportError:
        print("⚠️  PyTorch not installed yet")
        return False


def install_dependencies():
    """Install required Python packages"""
    print("\n" + "="*60)
    print("INSTALLING DEPENDENCIES")
    print("="*60)
    
    # Install PyTorch first (with CUDA support)
    print("\nInstalling PyTorch with CUDA support...")
    pytorch_cmd = (
        "pip install torch torchvision torchaudio "
        "--index-url https://download.pytorch.org/whl/cu118"
    )
    run_command(pytorch_cmd, "Installing PyTorch")
    
    # Core dependencies
    packages = [
        "pyannote.audio",
        "librosa",
        "soundfile",
        "pyyaml",
        "tqdm",
        "psutil",
        "scipy",
        "numpy",
        "pandas",
        "scikit-learn",
        "requests",
        "flask",
        "python-dotenv"
    ]
    
    for package in packages:
        print(f"\nInstalling {package}...")
        run_command(f"pip install {package}", f"Installing {package}")
    
    print("\n✅ All dependencies installed!")


def setup_directories():
    """Create necessary directories"""
    print("\n" + "="*60)
    print("SETTING UP DIRECTORIES")
    print("="*60)
    
    directories = [
        "data/input",
        "data/batches",
        "data/voice_dataset",
        "data/temp",
        "logs",
        "models"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created: {directory}")
    
    print("\n✅ Directories created!")


def setup_huggingface():
    """Guide user through HuggingFace setup"""
    print("\n" + "="*60)
    print("HUGGINGFACE SETUP")
    print("="*60)
    
    print("\nFor speaker diarization, you need a HuggingFace token.")
    print("\nSteps:")
    print("1. Go to: https://huggingface.co/settings/tokens")
    print("2. Create a new token (or use existing)")
    print("3. Accept model terms at: https://huggingface.co/pyannote/speaker-diarization-3.1")
    print("4. Copy your token")
    
    response = input("\nDo you have your HuggingFace token ready? (y/n): ")
    
    if response.lower() == 'y':
        token = input("Paste your HuggingFace token: ").strip()
        
        # Update config.yaml
        try:
            with open('config/config.yaml', 'r') as f:
                content = f.read()
            
            # Replace the token placeholder
            content = content.replace('token: null', f'token: "{token}"')
            
            with open('config/config.yaml', 'w') as f:
                f.write(content)
            
            print("\n✅ HuggingFace token saved to config/config.yaml")
        except Exception as e:
            print(f"❌ Error saving token: {e}")
            print("   You can manually add it to config/config.yaml")
    else:
        print("\n⚠️  You can add the token later by editing config/config.yaml")


def verify_installation():
    """Verify the installation"""
    print("\n" + "="*60)
    print("VERIFYING INSTALLATION")
    print("="*60)
    
    all_good = True
    
    # Check PyTorch
    try:
        import torch
        print("✅ PyTorch installed")
    except ImportError:
        print("❌ PyTorch not installed")
        all_good = False
    
    # Check pyannote.audio
    try:
        import pyannote.audio
        print("✅ pyannote.audio installed")
    except ImportError:
        print("❌ pyannote.audio not installed")
        all_good = False
    
    # Check librosa
    try:
        import librosa
        print("✅ librosa installed")
    except ImportError:
        print("❌ librosa not installed")
        all_good = False
    
    # Check soundfile
    try:
        import soundfile
        print("✅ soundfile installed")
    except ImportError:
        print("❌ soundfile not installed")
        all_good = False
    
    # Check configuration
    if os.path.exists('config/config.yaml'):
        print("✅ Configuration file exists")
    else:
        print("⚠️  Configuration file not found")
        all_good = False
    
    # Check directories
    dirs_ok = all(
        os.path.exists(d) for d in [
            'data/input', 'data/batches', 
            'data/voice_dataset', 'logs'
        ]
    )
    
    if dirs_ok:
        print("✅ All directories created")
    else:
        print("⚠️  Some directories missing")
        all_good = False
    
    print("\n✅ Installation verified!")
    return all_good


def print_next_steps():
    """Print next steps for user"""
    print("\n" + "="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    
    print("\n📋 Next steps:")
    print("\n1. Add your audio files to: data/input/")
    print("   Supported formats: .wav, .mp3, .flac, .m4a")
    
    print("\n2. Verify HuggingFace token in config/config.yaml")
    print("   Look for: huggingface.token")
    
    print("\n3. Run the pipeline:")
    print("   python voxent_pipeline.py --config config/config.yaml")
    
    print("\n4. Check results in: data/voice_dataset/")
    print("   Output includes:")
    print("   - male/ folder with male speaker segments")
    print("   - female/ folder with female speaker segments")
    print("   - metadata.json with speaker information")
    
    print("\n" + "="*60)


def main():
    print("\n" + "="*70)
    print(" "*20 + "VOXENT SETUP WIZARD")
    print("="*70)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check GPU
    check_gpu()
    
    # Install dependencies
    response = input("\nInstall all dependencies? (y/n): ")
    if response.lower() == 'y':
        install_dependencies()
    
    # Setup directories
    setup_directories()
    
    # Setup HuggingFace
    setup_huggingface()
    
    # Verify installation
    verify_installation()
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup error: {e}")
        sys.exit(1)
