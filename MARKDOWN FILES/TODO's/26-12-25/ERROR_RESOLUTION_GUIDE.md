# VOXENT Error Resolution Guide

## Critical Errors - Must Fix Immediately

### Error 1: PyTorch DLL Loading Failure ⚠️⚠️⚠️

Error Message:
```
OSError: Could not load library: libtorchaudio.pyd
Could not find module 'C:\Users\...\torchcodec\libtorchcodec_core7.dll'
```

Root Cause: Windows DLL dependency issues with PyTorch 2.9.1 + TorchAudio 2.8.0

Solution Path A: Conda (RECOMMENDED for Windows)

```bash
# Step 1: Install Miniconda (if not already installed)
# Download from: https://docs.conda.io/en/latest/miniconda.html

# Step 2: Create new environment
conda create -n voxent python=3.11 -y
conda activate voxent

# Step 3: Install PyTorch with conda (CRITICAL - use conda, not pip)
# For CPU only:
conda install pytorch torchvision torchaudio cpuonly -c pytorch -y

# For GPU (if you have NVIDIA GPU):
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia -y

# Step 4: Install other dependencies
pip install pyannote.audio librosa soundfile pydub speechbrain scikit-learn pandas tqdm PyYAML Flask werkzeug joblib psutil

# Step 5: Test installation
python -c "import torch; import torchaudio; print('Success!')"
```

Solution Path B: Specific pip versions

```bash
# Step 1: Uninstall existing PyTorch
pip uninstall torch torchaudio torchvision -y

# Step 2: Install specific working versions
pip install torch==2.1.0+cpu torchaudio==2.1.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

# For GPU:
pip install torch==2.1.0+cu118 torchaudio==2.1.0+cu118 -f https://download.pytorch.org/whl/torch_stable.html

# Step 3: Test
python -c "import torch; import torchaudio; print(torch.__version__)"
```

Solution Path C: WSL2 (Best long-term solution)

```bash
# Step 1: Install WSL2 on Windows
wsl --install

# Step 2: Open Ubuntu terminal and install Python
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip ffmpeg -y

# Step 3: Clone your project
cd /mnt/c/Users/YOUR_USERNAME/Downloads/PROJECTS/
git clone [your-repo] voxent-wsl
cd voxent-wsl

# Step 4: Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# Step 5: Install dependencies (Linux has better PyTorch support)
pip install --upgrade pip
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt

# Step 6: Test
python -c "import torch; import torchaudio; print('WSL Success!')"
```

Verification:
```python
# test_pytorch.py
import torch
import torchaudio

print(f"PyTorch version: {torch.__version__}")
print(f"TorchAudio version: {torchaudio.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")

# Test audio loading
waveform, sample_rate = torchaudio.load("test.wav")
print(f"Audio loaded successfully: {waveform.shape}")
```

---

### Error 2: HuggingFace Authentication ⚠️⚠️⚠️

Error Message:
```
403 Client Error. Cannot access gated repo
Access to model pyannote/speaker-diarization-community-1 is restricted
```

Solution:

```bash
# Step 1: Create HuggingFace account
# Go to: https://huggingface.co/join

# Step 2: Accept model terms
# Visit: https://huggingface.co/pyannote/speaker-diarization-community-1
# Click "Agree and access repository"

# Step 3: Get access token
# Go to: https://huggingface.co/settings/tokens
# Click "New token" → Create token with "read" access
# Copy the token (starts with "hf_...")

# Step 4: Set environment variable

# Windows PowerShell:
$env:HF_TOKEN="hf_your_token_here"
# Or permanently:
[System.Environment]::SetEnvironmentVariable('HF_TOKEN', 'hf_your_token_here', 'User')

# Windows CMD:
setx HF_TOKEN "hf_your_token_here"

# Linux/WSL/Mac:
export HF_TOKEN="hf_your_token_here"
# Or add to ~/.bashrc:
echo 'export HF_TOKEN="hf_your_token_here"' >> ~/.bashrc
source ~/.bashrc

# Step 5: Verify
echo $env:HF_TOKEN  # Windows PowerShell
echo $HF_TOKEN      # Linux/Mac
```

Alternative: Store in config file

```python
# Create: config/hf_token.py
HF_TOKEN = "hf_your_token_here"

# Update: dIarization/diarizer.py
import os
try:
    from config.hf_token import HF_TOKEN
    token = HF_TOKEN
except ImportError:
    token = os.getenv("HF_TOKEN")

if not token:
    raise ValueError("HF_TOKEN not found. Set environment variable or create config/hf_token.py")
```

Verification:
```python
# test_hf_auth.py
import os
from pyannote.audio import Pipeline

token = os.getenv("HF_TOKEN")
if not token:
    print("ERROR: HF_TOKEN not set")
else:
    print(f"Token found: {token[:10]}...")
    try:
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-community-1",
            use_auth_token=token
        )
        print("SUCCESS: Pipeline loaded")
    except Exception as e:
        print(f"ERROR: {e}")
```

---

### Error 3: Flask Not Installed ⚠️⚠️

Error Message:
```
ModuleNotFoundError: No module named 'flask'
```

Solution:

```bash
# Install Flask and dependencies
pip install flask werkzeug flask-socketio

# Verify
python -c "import flask; print(f'Flask {flask.__version__} installed')"
```

---

### Error 4: Metadata File Not Found ⚠️

Error Message:
```
Training failed: Metadata file not found: data/voice_dataset/metadata.csv
```

Root Cause: Pipeline hasn't successfully processed any files yet

Solution: This will automatically resolve once Errors 1-3 are fixed. However, to test:

```bash
# Create dummy metadata for testing
mkdir -p data/voice_dataset/male data/voice_dataset/female

# Create test metadata
cat > data/voice_dataset/metadata.csv << EOL
file,source,speaker,pitch,label,confidence,duration,quality_score,snr,clipping_ratio,silence_ratio
test_male_1.wav,test.wav,SPEAKER_00,120.5,male,85.3,3.2,78.5,15.2,0.005,0.15
test_female_1.wav,test.wav,SPEAKER_01,220.8,female,92.1,2.8,82.3,16.8,0.002,0.12
EOL

# Now test training script
python train_ml_classifier.py --min-confidence 70
```

---

## Code Quality Issues

### Issue 1: String Formatting Bugs

Locations: Multiple files have placeholder strings like `".1f"`, `".2%"`, `".3f"`

Fix 1: classification/__init__.py (lines 61-63)

```python
# BEFORE:
logger.debug(".1f")

# AFTER:
logger.debug(f"ML classification: {ml_label} with confidence {ml_confidence:.1f}%")
logger.debug(f"ML confidence too low ({ml_confidence:.1f}%), falling back to pitch-based")
logger.debug(f"Pitch classification: {pitch_label} with confidence {pitch_confidence:.1f}%")
```

Fix 2: classification/ml_classifier.py (line 134)

```python
# BEFORE:
logger.info(".2%")

# AFTER:
logger.info(f"Model training completed with accuracy: {accuracy:.2%}")
```

Fix 3: classification/ml_classifier.py (line 185)

```python
# BEFORE:
print(".3f")

# AFTER:
print(f"{metric}: {value:.3f}")
```

Fix 4: quality_assurance/metrics.py (line 220)

```python
# BEFORE:
print(".2f")

# AFTER:
print(f"Average quality score: {summary['average_quality_score']:.2f}")
```

Complete Fix File:

```python
# Create: fixes/fix_logging.py
import re
import os

def fix_logging_statements(file_path):
    """Fix placeholder logging statements in a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match incomplete format strings
    patterns = [
        (r'logger\.debug\("\.1f"\)', 'logger.debug(f"Classification complete")'),
        (r'logger\.info\("\.2%"\)', 'logger.info(f"Accuracy: {accuracy:.2%}")'),
        (r'print\("\.3f"\)', 'print(f"Metric: {value:.3f}")'),
        (r'print\("\.2f"\)', 'print(f"Score: {score:.2f}")'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed: {file_path}")

# Run on all affected files
files_to_fix = [
    'classification/__init__.py',
    'classification/ml_classifier.py',
    'quality_assurance/metrics.py'
]

for file in files_to_fix:
    if os.path.exists(file):
        fix_logging_statements(file)
```

---

### Issue 2: Test Failures

Test 1: test_config_validation

Error: Fails due to HF_TOKEN import issue in validation

Fix:

```python
# In tests/test_pipeline.py

def test_config_validation(self):
    """Test configuration validation."""
    from engine.batch_runner import validate_config
    
    # Mock HF_TOKEN for testing
    import os
    os.environ['HF_TOKEN'] = 'hf_test_token_for_validation'
    
    # Valid config
    valid_config = {
        'sample_rate': 16000,
        'min_segment_duration': 1.0,
        'male_pitch_threshold': 85,
        'female_pitch_threshold': 165,
        'confidence_margin': 20
    }
    self.assertTrue(validate_config(valid_config))
    
    # Invalid config - missing key
    invalid_config = valid_config.copy()
    del invalid_config['sample_rate']
    with self.assertRaises(ValueError):
        validate_config(invalid_config)
```

Test 2: test_pitch_estimation

Error: Type assertion fails (np.float32 vs float)

Fix:

```python
# In tests/test_pipeline.py

def test_pitch_estimation(self):
    """Test pitch estimation."""
    pitch = estimate_pitch(self.test_audio, self.sample_rate)
    
    # Accept both native float and numpy float types
    self.assertIsInstance(pitch, (int, float, np.floating))
    self.assertGreater(float(pitch), 0)
```

---

### Issue 3: Audio Conversion Required

Problem: Input files are MP3, but pipeline expects WAV

Solution: Use the existing `convert_audio.py` script

```bash
# Step 1: Convert all MP3 files to WAV
python convert_audio.py --input data --output data/input_calls --sample-rate 16000

# Step 2: Verify conversion
ls data/input_calls/.wav

# Step 3: Run pipeline
python config/run_pipeline.py
```

Automated Solution: Add pre-processing step to batch_runner.py

```python
# Add to engine/batch_runner.py

def convert_mp3_to_wav_if_needed(input_dir):
    """Automatically convert MP3 files to WAV before processing."""
    from pydub import AudioSegment
    import glob
    
    mp3_files = glob.glob(os.path.join(input_dir, '.mp3'))
    
    if not mp3_files:
        return
    
    logger.info(f"Converting {len(mp3_files)} MP3 files to WAV...")
    
    for mp3_file in mp3_files:
        wav_file = mp3_file.replace('.mp3', '.wav')
        
        if os.path.exists(wav_file):
            logger.info(f"Skipping {mp3_file} (WAV exists)")
            continue
        
        try:
            audio = AudioSegment.from_mp3(mp3_file)
            audio = audio.set_channels(1).set_frame_rate(16000)
            audio.export(wav_file, format='wav')
            logger.info(f"Converted: {os.path.basename(mp3_file)}")
        except Exception as e:
            logger.error(f"Failed to convert {mp3_file}: {e}")

# Add to run() function, before getting files:
def run(config_path):
    # ... existing code ...
    
    input_dir = "data/input_calls"
    
    # NEW: Auto-convert MP3 files
    convert_mp3_to_wav_if_needed(input_dir)
    
    # Get files to process
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".wav")]
    # ... rest of function ...
```

---

## Complete Setup Checklist

### Pre-Flight Checklist

- [ ] Python 3.11 installed (or 3.10)
- [ ] Virtual environment created
- [ ] PyTorch installed via conda (CRITICAL)
- [ ] HuggingFace account created
- [ ] pyannote model access granted
- [ ] HF_TOKEN environment variable set
- [ ] All pip dependencies installed
- [ ] FFmpeg installed (for audio conversion)

### Installation Verification Script

```python
# Create: verify_installation.py

import sys

def check_installation():
    """Verify all components are installed correctly."""
    issues = []
    
    # Check Python version
    if sys.version_info < (3, 10):
        issues.append("❌ Python version too old. Need 3.10+")
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Check PyTorch
    try:
        import torch
        import torchaudio
        print(f"✅ PyTorch {torch.__version__}")
        print(f"✅ TorchAudio {torchaudio.__version__}")
    except Exception as e:
        issues.append(f"❌ PyTorch/TorchAudio: {e}")
    
    # Check HuggingFace
    import os
    if os.getenv("HF_TOKEN"):
        print(f"✅ HF_TOKEN set")
    else:
        issues.append("❌ HF_TOKEN not set")
    
    # Check pyannote
    try:
        from pyannote.audio import Pipeline
        print("✅ pyannote.audio installed")
    except Exception as e:
        issues.append(f"❌ pyannote.audio: {e}")
    
    # Check other dependencies
    deps = ['librosa', 'soundfile', 'pydub', 'flask', 'pandas', 'sklearn']
    for dep in deps:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            issues.append(f"❌ {dep} not installed")
    
    # Check FFmpeg
    import subprocess
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("✅ FFmpeg installed")
    except:
        issues.append("❌ FFmpeg not installed")
    
    # Summary
    print("\n" + "="50)
    if issues:
        print("❌ ISSUES FOUND:")
        for issue in issues:
            print(f"  {issue}")
        print("\nFix these issues before running the pipeline.")
        return False
    else:
        print("✅ ALL CHECKS PASSED! Ready to run.")
        return True

if __name__ == "__main__":
    success = check_installation()
    sys.exit(0 if success else 1)
```

### Run Verification

```bash
# Run the verification script
python verify_installation.py

# If all checks pass, test the pipeline with a single file
python config/run_pipeline.py
```

---

## Emergency Troubleshooting

### If Nothing Works

Nuclear Option: Fresh Start

```bash
# Step 1: Backup your data
cp -r data data_backup
cp config/config.yaml config/config_backup.yaml

# Step 2: Delete environment
conda env remove -n voxent
# or
rm -rf .venv

# Step 3: Fresh conda install
conda create -n voxent python=3.11 -y
conda activate voxent
conda install pytorch torchaudio cpuonly -c pytorch -y

# Step 4: Install from requirements
pip install -r requirements.txt

# Step 5: Set HF_TOKEN
export HF_TOKEN="your_token_here"

# Step 6: Test
python verify_installation.py
```

---

## Post-Fix Validation

### After All Fixes Applied

```bash
# 1. Run unit tests
python -m pytest tests/test_pipeline.py -v

# 2. Run integration tests
python -m pytest tests/test_integration.py -v

# 3. Test with real audio
python convert_audio.py --input data --output data/input_calls
python config/run_pipeline.py

# 4. Check outputs
ls -lh data/voice_dataset/male/
ls -lh data/voice_dataset/female/
cat data/voice_dataset/metadata.csv

# 5. Start web app
python web_app.py
# Open: http://localhost:5000
```

---

## Getting Help

### If Issues Persist

1. Check Logs:
   ```bash
   # View recent logs
   tail -n 100 logs/voxent.log
   ```

2. Enable Debug Mode:
   ```python
   # In config/config.yaml
   logging:
     level: DEBUG
   ```

3. Test Individual Components:
   ```bash
   # Test audio loading
   python -c "from preprocessing.audio_loader import load_audio; print(load_audio('test.wav', 16000))"
   
   # Test classification
   python -c "from classification import get_classifier; print(get_classifier())"
   ```

4. Community Support:
   - pyannote.audio: https://github.com/pyannote/pyannote-audio/discussions
   - PyTorch: https://discuss.pytorch.org/
   - HuggingFace: https://discuss.huggingface.co/

---

## Success Indicators

### You Know It's Working When:

✅ No errors during `python verify_installation.py`
✅ Pipeline processes at least one file successfully
✅ metadata.csv is created with valid entries
✅ Audio files appear in male/female directories
✅ Web interface loads without errors
✅ Tests pass: `pytest tests/ -v`

### Expected Output:

```
2025-12-26 10:00:00,000 - INFO - Starting batch processing of 2 files
Processing files: 100%|██████████| 2/2 [00:30<00:00, 15.00s/it]
2025-12-26 10:00:30,000 - INFO - Successfully processed test.wav: 3 segments
2025-12-26 10:00:30,001 - INFO - Batch processing completed: 2 successful, 0 failed
```
