#!/usr/bin/env python3
"""
VOXENT Code Fixes - Automated Patching Script

This script automatically fixes all known code quality issues in the VOXENT project.
Run this before attempting to execute the pipeline.

Usage:
    python apply_fixes.py [--dry-run]
"""

import os
import re
import sys
import argparse
from pathlib import Path

class CodeFixer:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.fixes_applied = 0
        self.files_modified = []
    
    def fix_file(self, filepath, fixes):
        """Apply fixes to a single file."""
        if not os.path.exists(filepath):
            print(f"⚠️  File not found: {filepath}")
            return False
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        for pattern, replacement, description in fixes:
            if re.search(pattern, content):
                content = re.sub(pattern, replacement, content)
                self.fixes_applied += 1
                print(f"  ✓ {description}")
        
        if content != original_content:
            if not self.dry_run:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.files_modified.append(filepath)
            return True
        
        return False
    
    def fix_classification_init(self):
        """Fix classification/__init__.py logging issues."""
        print("\n📝 Fixing classification/__init__.py...")
        
        fixes = [
            (
                r'logger\.debug\("\\.1f"\)',
                'logger.debug(f"ML classification: {ml_label} with confidence {ml_confidence:.1f}%")',
                "Fixed ML classification debug log"
            ),
            (
                r'logger\.debug\("\\.1f"\)\s*\n\s*else:',
                'logger.debug(f"ML confidence too low ({ml_confidence:.1f}%), falling back to pitch-based")\n        else:',
                "Fixed ML fallback debug log"
            ),
            (
                r'logger\.debug\("\\.1f"\)\s*\n\s*return pitch_label',
                'logger.debug(f"Pitch classification: {pitch_label} with confidence {pitch_confidence:.1f}%")\n        return pitch_label',
                "Fixed pitch classification debug log"
            ),
        ]
        
        return self.fix_file('classification/__init__.py', fixes)
    
    def fix_ml_classifier(self):
        """Fix classification/ml_classifier.py logging issues."""
        print("\n📝 Fixing classification/ml_classifier.py...")
        
        fixes = [
            (
                r'logger\.info\("\\.2%"\)',
                'logger.info(f"Model training completed with accuracy: {accuracy:.2%}")',
                "Fixed training completion log"
            ),
            (
                r'print\("\\.3f"\)',
                'print(f"  {metric}: {value:.3f}")',
                "Fixed metric printing"
            ),
        ]
        
        return self.fix_file('classification/ml_classifier.py', fixes)
    
    def fix_quality_metrics(self):
        """Fix quality_assurance/metrics.py printing issues."""
        print("\n📝 Fixing quality_assurance/metrics.py...")
        
        fixes = [
            (
                r'print\("\\.2f"\)',
                'print(f"Average quality score: {summary[\'average_quality_score\']:.2f}")',
                "Fixed quality score printing"
            ),
        ]
        
        return self.fix_file('quality_assurance/metrics.py', fixes)
    
    def fix_batch_runner_imports(self):
        """Fix engine/batch_runner.py to add MP3 conversion."""
        print("\n📝 Fixing engine/batch_runner.py...")
        
        # Check if conversion function already exists
        with open('engine/batch_runner.py', 'r') as f:
            content = f.read()
        
        if 'convert_mp3_to_wav_if_needed' in content:
            print("  ℹ️  MP3 conversion already implemented")
            return False
        
        # Add conversion function before run()
        conversion_code = '''
def convert_mp3_to_wav_if_needed(input_dir):
    """Automatically convert MP3 files to WAV before processing."""
    from pydub import AudioSegment
    import glob
    
    mp3_files = glob.glob(os.path.join(input_dir, '*.mp3'))
    
    if not mp3_files:
        return
    
    logger.info(f"Converting {len(mp3_files)} MP3 files to WAV...")
    
    for mp3_file in mp3_files:
        wav_file = mp3_file.replace('.mp3', '.wav')
        
        if os.path.exists(wav_file):
            logger.debug(f"Skipping {mp3_file} (WAV exists)")
            continue
        
        try:
            audio = AudioSegment.from_mp3(mp3_file)
            audio = audio.set_channels(1).set_frame_rate(16000)
            audio.export(wav_file, format='wav')
            logger.info(f"Converted: {os.path.basename(mp3_file)}")
        except Exception as e:
            logger.error(f"Failed to convert {mp3_file}: {e}")

'''
        
        # Insert before def run(config_path):
        pattern = r'(def run\(config_path\):)'
        replacement = conversion_code + r'\1'
        
        content = re.sub(pattern, replacement, content)
        
        # Add call to conversion in run() function
        pattern = r'(input_dir = "data/input_calls"\s+)(os\.makedirs)'
        replacement = r'\1\n    # Auto-convert MP3 files\n    convert_mp3_to_wav_if_needed(input_dir)\n    \n    \2'
        
        content = re.sub(pattern, replacement, content)
        
        if not self.dry_run:
            with open('engine/batch_runner.py', 'w') as f:
                f.write(content)
            self.files_modified.append('engine/batch_runner.py')
        
        print("  ✓ Added MP3 auto-conversion")
        self.fixes_applied += 1
        return True
    
    def fix_test_pipeline(self):
        """Fix tests/test_pipeline.py type issues."""
        print("\n📝 Fixing tests/test_pipeline.py...")
        
        fixes = [
            (
                r'self\.assertIsInstance\(pitch, \(int, float\)\)',
                'self.assertIsInstance(pitch, (int, float, np.floating))',
                "Fixed pitch type assertion"
            ),
            (
                r'self\.assertGreater\(pitch, 0\)',
                'self.assertGreater(float(pitch), 0)',
                "Fixed pitch comparison"
            ),
        ]
        
        # Add numpy import if missing
        with open('tests/test_pipeline.py', 'r') as f:
            content = f.read()
        
        if 'import numpy as np' not in content:
            content = content.replace(
                'import unittest',
                'import unittest\nimport numpy as np'
            )
            if not self.dry_run:
                with open('tests/test_pipeline.py', 'w') as f:
                    f.write(content)
            print("  ✓ Added numpy import")
            self.fixes_applied += 1
        
        return self.fix_file('tests/test_pipeline.py', fixes)
    
    def fix_web_app_classifier_status(self):
        """Fix web_app.py classifier status endpoint."""
        print("\n📝 Fixing web_app.py...")
        
        with open('web_app.py', 'r') as f:
            content = f.read()
        
        # Check if fix already applied
        if 'config_path = "config/config.yaml"' in content and '@app.route(\'/classifier-status\')' in content:
            # Find the classifier-status function
            pattern = r'(@app\.route\(\'/classifier-status\'\)\s+def get_classifier_status\(\):.*?)(from classification import get_classifier)'
            
            if re.search(pattern, content, re.DOTALL):
                replacement = r'\1# Load config first\n        config_path = "config/config.yaml"\n        if os.path.exists(config_path):\n            with open(config_path, \'r\') as f:\n                config = yaml.safe_load(f)\n        else:\n            config = {}\n        \n        from classification import get_classifier'
                
                content = re.sub(pattern, replacement, content, flags=re.DOTALL)
                
                if not self.dry_run:
                    with open('web_app.py', 'w') as f:
                        f.write(content)
                    self.files_modified.append('web_app.py')
                
                print("  ✓ Fixed classifier status endpoint")
                self.fixes_applied += 1
                return True
        
        print("  ℹ️  No changes needed")
        return False
    
    def create_verification_script(self):
        """Create installation verification script."""
        print("\n📝 Creating verify_installation.py...")
        
        script_content = '''#!/usr/bin/env python3
"""
VOXENT Installation Verification Script

Checks that all required dependencies are installed and configured correctly.
"""

import sys
import os

def check_installation():
    """Verify all components are installed correctly."""
    issues = []
    
    print("\\n🔍 VOXENT Installation Verification\\n")
    print("="*50)
    
    # Check Python version
    if sys.version_info < (3, 10):
        issues.append("❌ Python version too old. Need 3.10+")
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Check PyTorch
    try:
        import torch
        import torchaudio
        print(f"✅ PyTorch {torch.__version__}")
        print(f"✅ TorchAudio {torchaudio.__version__}")
        
        if torch.cuda.is_available():
            print(f"✅ CUDA available: {torch.cuda.get_device_name(0)}")
    except Exception as e:
        issues.append(f"❌ PyTorch/TorchAudio: {e}")
    
    # Check HuggingFace Token
    if os.getenv("HF_TOKEN"):
        token = os.getenv("HF_TOKEN")
        print(f"✅ HF_TOKEN set ({token[:10]}...)")
    else:
        issues.append("❌ HF_TOKEN not set")
    
    # Check pyannote
    try:
        from pyannote.audio import Pipeline
        print("✅ pyannote.audio installed")
        
        # Try to load pipeline (requires token)
        if os.getenv("HF_TOKEN"):
            try:
                pipeline = Pipeline.from_pretrained(
                    "pyannote/speaker-diarization-community-1",
                    use_auth_token=os.getenv("HF_TOKEN")
                )
                print("✅ Diarization pipeline accessible")
            except Exception as e:
                issues.append(f"⚠️  Diarization pipeline: {str(e)[:50]}...")
    except Exception as e:
        issues.append(f"❌ pyannote.audio: {e}")
    
    # Check other dependencies
    deps = {
        'librosa': 'Audio processing',
        'soundfile': 'Audio I/O',
        'pydub': 'Audio conversion',
        'flask': 'Web interface',
        'pandas': 'Data handling',
        'sklearn': 'ML models',
        'numpy': 'Numerical computing',
        'tqdm': 'Progress bars',
        'yaml': 'Configuration',
    }
    
    for dep, description in deps.items():
        try:
            __import__(dep)
            print(f"✅ {dep} ({description})")
        except ImportError:
            issues.append(f"❌ {dep} not installed")
    
    # Check FFmpeg
    import subprocess
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True,
            check=True
        )
        version_line = result.stdout.split('\\n')[0]
        print(f"✅ FFmpeg installed ({version_line})")
    except:
        issues.append("⚠️  FFmpeg not installed (optional but recommended)")
    
    # Check directories
    required_dirs = [
        'data/input_calls',
        'data/voice_dataset',
        'config',
        'models'
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ Directory exists: {dir_path}")
        else:
            print(f"⚠️  Creating directory: {dir_path}")
            os.makedirs(dir_path, exist_ok=True)
    
    # Summary
    print("\\n" + "="*50)
    
    if issues:
        print("\\n❌ ISSUES FOUND:\\n")
        for issue in issues:
            print(f"  {issue}")
        print("\\n⚠️  Fix these issues before running the pipeline.")
        print("\\n📖 See ERROR_RESOLUTION_GUIDE.md for detailed instructions.")
        return False
    else:
        print("\\n✅ ALL CHECKS PASSED!")
        print("\\n🚀 You're ready to run VOXENT!")
        print("\\n   Next steps:")
        print("   1. Place audio files in data/input_calls/")
        print("   2. Run: python config/run_pipeline.py")
        print("   3. Or start web UI: python web_app.py")
        return True

if __name__ == "__main__":
    success = check_installation()
    sys.exit(0 if success else 1)
'''
        
        if not self.dry_run:
            with open('verify_installation.py', 'w') as f:
                f.write(script_content)
            os.chmod('verify_installation.py', 0o755)
            self.files_modified.append('verify_installation.py')
        
        print("  ✓ Created verification script")
        self.fixes_applied += 1
        return True
    
    def create_quickstart_script(self):
        """Create quickstart setup script."""
        print("\n📝 Creating quickstart.sh...")
        
        script_content = '''#!/bin/bash
# VOXENT Quickstart Setup Script

set -e

echo "🚀 VOXENT Quickstart Setup"
echo "=========================="
echo ""

# Check if conda is available
if command -v conda &> /dev/null; then
    echo "✅ Conda found"
    USE_CONDA=true
else
    echo "⚠️  Conda not found - using pip (less reliable on Windows)"
    USE_CONDA=false
fi

# Create environment
if [ "$USE_CONDA" = true ]; then
    echo "📦 Creating conda environment..."
    conda create -n voxent python=3.11 -y
    source $(conda info --base)/etc/profile.d/conda.sh
    conda activate voxent
    
    echo "📦 Installing PyTorch with conda..."
    conda install pytorch torchaudio cpuonly -c pytorch -y
else
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    
    echo "📦 Installing PyTorch with pip..."
    pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
fi

# Install other dependencies
echo "📦 Installing other dependencies..."
pip install pyannote.audio librosa soundfile pydub speechbrain \\
    scikit-learn pandas tqdm PyYAML Flask werkzeug joblib psutil

# Set up HuggingFace token
echo ""
echo "🔑 HuggingFace Setup"
echo "==================="
echo ""
echo "You need a HuggingFace token to use speaker diarization."
echo "1. Create account at https://huggingface.co/join"
echo "2. Accept terms at https://huggingface.co/pyannote/speaker-diarization-community-1"
echo "3. Get token from https://huggingface.co/settings/tokens"
echo ""
read -p "Enter your HuggingFace token (or press Enter to skip): " hf_token

if [ ! -z "$hf_token" ]; then
    export HF_TOKEN="$hf_token"
    echo "export HF_TOKEN=\\"$hf_token\\"" >> ~/.bashrc
    echo "✅ HF_TOKEN set"
else
    echo "⚠️  Skipped HF_TOKEN setup - you'll need to set it later"
fi

# Create directories
echo ""
echo "📁 Creating directories..."
mkdir -p data/input_calls data/voice_dataset models logs

# Run verification
echo ""
echo "🔍 Running installation verification..."
python verify_installation.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Place audio files in data/input_calls/"
echo "2. Run: python config/run_pipeline.py"
echo "3. Or start web UI: python web_app.py"
'''
        
        if not self.dry_run:
            with open('quickstart.sh', 'w') as f:
                f.write(script_content)
            os.chmod('quickstart.sh', 0o755)
            self.files_modified.append('quickstart.sh')
        
        print("  ✓ Created quickstart script")
        self.fixes_applied += 1
        return True
    
    def run_all_fixes(self):
        """Apply all fixes."""
        print("="*60)
        print("VOXENT Automated Code Fixes")
        print("="*60)
        
        if self.dry_run:
            print("\n🔍 DRY RUN MODE - No files will be modified\n")
        
        # Apply fixes
        self.fix_classification_init()
        self.fix_ml_classifier()
        self.fix_quality_metrics()
        self.fix_batch_runner_imports()
        self.fix_test_pipeline()
        self.fix_web_app_classifier_status()
        
        # Create helper scripts
        self.create_verification_script()
        self.create_quickstart_script()
        
        # Summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"\n✓ Applied {self.fixes_applied} fixes")
        
        if self.files_modified:
            print(f"✓ Modified {len(self.files_modified)} files:")
            for filepath in self.files_modified:
                print(f"  - {filepath}")
        
        if self.dry_run:
            print("\n⚠️  DRY RUN - Run without --dry-run to apply changes")
        else:
            print("\n✅ All fixes applied successfully!")
            print("\n📖 Next steps:")
            print("   1. Run: python verify_installation.py")
            print("   2. Fix any installation issues")
            print("   3. Run: python config/run_pipeline.py")
        
        return True

def main():
    parser = argparse.ArgumentParser(description='Apply automated fixes to VOXENT code')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without modifying files')
    args = parser.parse_args()
    
    fixer = CodeFixer(dry_run=args.dry_run)
    
    try:
        fixer.run_all_fixes()
        return 0
    except Exception as e:
        print(f"\n❌ Error applying fixes: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
