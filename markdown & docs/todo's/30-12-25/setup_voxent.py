"""
VOXENT Installation and Setup Script
Installs dependencies and sets up the environment
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    print(f"Running: {command}\n")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print(f"✅ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"Error: {e.stderr}")
        return False


def check_python_version():
    """Check Python version"""
    print("\nChecking Python version...")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher required!")
        return False
    
    print("✅ Python version is compatible")
    return True


def check_gpu():
    """Check for GPU availability"""
    print("\nChecking for GPU...")
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            print(f"✅ GPU detected: {gpu_name}")
            return True
        else:
            print("⚠️  No GPU detected - will use CPU (slower)")
            return False
    except ImportError:
        print("⚠️  PyTorch not installed yet")
        return False


def install_dependencies():
    """Install required Python packages"""
    print("\n" + "="*60)
    print("INSTALLING DEPENDENCIES")
    print("="*60)
    
    # Core dependencies
    packages = [
        "torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118",
        "pyannote.audio",
        "librosa",
        "soundfile",
        "pyyaml",
        "tqdm",
        "psutil"
    ]
    
    for package in packages:
        if not run_command(
            f"{sys.executable} -m pip install {package}",
            f"Installing {package.split()[0]}"
        ):
            print(f"⚠️  Failed to install {package}")
    
    print("\n✅ All dependencies installed!")


def setup_directories():
    """Create necessary directories"""
    print("\n" + "="*60)
    print("SETTING UP DIRECTORIES")
    print("="*60)
    
    directories = [
        "data/input_calls",
        "data/batches",
        "data/voice_dataset",
        "data/temp",
        "logs",
        "models"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created: {directory}")
    
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
        token = input("\nPaste your token here (hidden): ")
        
        # Update config.yaml
        try:
            import yaml
            with open('config.yaml', 'r') as f:
                config = yaml.safe_load(f)
            
            config['huggingface']['token'] = token
            
            with open('config.yaml', 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            
            print("✅ Token saved to config.yaml")
        except Exception as e:
            print(f"⚠️  Could not save token automatically: {e}")
            print("   Please manually edit config.yaml and add your token")
    else:
        print("\n⚠️  You'll need to add your token to config.yaml later")
        print("   Edit the file and set: huggingface -> token")


def verify_installation():
    """Verify the installation"""
    print("\n" + "="*60)
    print("VERIFYING INSTALLATION")
    print("="*60)
    
    # Check PyTorch
    try:
        import torch
        print(f"✅ PyTorch version: {torch.__version__}")
        if torch.cuda.is_available():
            print(f"✅ CUDA available: {torch.version.cuda}")
    except ImportError:
        print("❌ PyTorch not installed")
        return False
    
    # Check pyannote.audio
    try:
        import pyannote.audio
        print(f"✅ pyannote.audio installed")
    except ImportError:
        print("❌ pyannote.audio not installed")
        return False
    
    # Check librosa
    try:
        import librosa
        print(f"✅ librosa version: {librosa.__version__}")
    except ImportError:
        print("❌ librosa not installed")
        return False
    
    # Check configuration
    if os.path.exists('config.yaml'):
        print("✅ config.yaml exists")
    else:
        print("❌ config.yaml not found")
        return False
    
    print("\n✅ Installation verified!")
    return True


def print_next_steps():
    """Print next steps for user"""
    print("\n" + "="*60)
    print("SETUP COMPLETE!")
    print("="*60)
    
    print("\n📋 Next steps:")
    print("\n1. Add your audio files to: data/input_calls/")
    print("   - Supported formats: .wav, .mp3, .flac, .m4a")
    print("   - These should be conversation recordings")
    
    print("\n2. Edit config.yaml if needed:")
    print("   - Set HuggingFace token (if not done)")
    print("   - Adjust batch size (currently: 10 files)")
    print("   - Configure GPU settings")
    
    print("\n3. Run the pipeline:")
    print("   python voxent_pipeline.py --config config.yaml")
    
    print("\n4. Find outputs in:")
    print("   - Batches: data/batches/")
    print("   - Voice dataset: data/voice_dataset/")
    print("   - Logs: logs/")
    
    print("\n" + "="*60)
    print("For help: python voxent_pipeline.py --help")
    print("="*60 + "\n")


def main():
    """Main setup function"""
    print("\n" + "="*70)
    print(" "*20 + "VOXENT SETUP")
    print("="*70)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    response = input("\nInstall dependencies? (y/n): ")
    if response.lower() == 'y':
        install_dependencies()
    
    # Check GPU
    check_gpu()
    
    # Setup directories
    setup_directories()
    
    # Setup HuggingFace
    setup_huggingface()
    
    # Verify installation
    if verify_installation():
        print_next_steps()
    else:
        print("\n⚠️  Installation incomplete. Please fix errors and run again.")


if __name__ == "__main__":
    main()
