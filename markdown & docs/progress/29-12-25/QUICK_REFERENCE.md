VOXENT PROJECT - QUICK REFERENCE GUIDE
========================================

═══════════════════════════════════════════════════════════════════════════════
QUICK START
═══════════════════════════════════════════════════════════════════════════════

1. RUN COMPREHENSIVE TESTS
   $ python test_voxent_complete.py

2. TEST WITH REAL AUDIO FILES
   $ python test_pipeline_sample.py

3. RUN FULL PIPELINE
   $ python config/run_pipeline.py

4. VIEW RESULTS
   Output Files: data/voice_dataset/
   Metadata: data/voice_dataset/metadata.csv

═══════════════════════════════════════════════════════════════════════════════
FILE STRUCTURE
═══════════════════════════════════════════════════════════════════════════════

VOXENT/
├── src/                           # Python scripts (for organization)
├── yaml/                          # YAML configurations (for organization)
├── shell/                         # Shell scripts (for organization)
├── classification/                # Gender classification module
│   ├── __init__.py               # Integrated classifier (UPDATED)
│   ├── pitch_gender.py           # Pitch-based classifier
│   ├── ml_classifier.py          # ML classifier with GPU support (UPDATED)
│   └── advanced_gender_classifier.py  # Multi-feature classifier (NEW)
├── preprocessing/                 # Audio preprocessing
│   ├── audio_loader.py
│   ├── normalize.py
│   ├── vad.py
│   └── source_separator.py
├── engine/                        # Processing engine
│   ├── batch_runner.py           # Batch processor with duration sorting (UPDATED)
│   └── logger.py
├── dataset/                       # Dataset management
│   ├── organizer.py              # Sequential naming system (UPDATED)
│   └── metadata.py
├── dIarization/                   # Speaker diarization (GPU-enabled)
│   ├── diarizer.py               # GPU support added (UPDATED)
│   └── segments.py
├── config/                        # Configuration
│   ├── config.yaml               # GPU settings added (UPDATED)
│   └── run_pipeline.py
├── data/                          # Data storage
│   ├── input_calls/              # Audio input files (20 files available)
│   └── voice_dataset/            # Organized output
│       ├── male/                 # Male voice samples
│       ├── female/               # Female voice samples
│       ├── uncertain/            # Ambiguous samples
│       └── metadata.csv          # Tracking file
├── models/                        # Trained model storage
├── tests/                         # Test files
├── config/                        # Configuration directory
├── config.yaml                    # Main configuration (UPDATED)
├── test_voxent_complete.py       # Comprehensive test suite (NEW)
├── test_pipeline_sample.py       # Pipeline test with real audio (NEW)
├── TEST_REPORT_FINAL.txt         # Test results (NEW)
└── IMPLEMENTATION_SUMMARY.txt    # Implementation details (NEW)

═══════════════════════════════════════════════════════════════════════════════
COMPONENTS & STATUS
═══════════════════════════════════════════════════════════════════════════════

CLASSIFICATION MODULE
  ✅ Pitch Classifier (basic)
  ✅ Advanced Multi-Feature Classifier (NEW)
  ✅ ML Classifier (available, not trained)
  ✅ Integrated Classifier (NEW)
  Status: All classifiers operational
  Device: CPU (GPU ready when PyTorch CUDA installed)

BATCH PROCESSING
  ✅ Duration-based batching (NEW)
  ✅ Parallel processing
  ✅ GPU cache management (NEW)
  ✅ MP3 auto-conversion
  Status: Fully operational

DATASET ORGANIZATION
  ✅ Sequential naming (voice_sample_0001.wav) (NEW)
  ✅ Counter management (NEW)
  ✅ Metadata tracking
  ✅ Folder organization (male/female/uncertain)
  Status: Fully operational

CONFIGURATION
  ✅ GPU settings (NEW)
  ✅ Batch size configuration (NEW)
  ✅ Device selection (NEW)
  ✅ Classification settings
  Status: Fully updated

═══════════════════════════════════════════════════════════════════════════════
CONFIGURATION OPTIONS (config/config.yaml)
═══════════════════════════════════════════════════════════════════════════════

GPU SETTINGS
  device: "cuda"                    # GPU device (or "cpu", "auto")
  gpu_memory_fraction: 0.8         # GPU memory usage limit (0.6-0.9)
  batch_size_gpu: 8                # Samples per GPU batch (4-16)
  batch_size_cpu: 2                # Samples per CPU batch
  use_mixed_precision: true        # FP16 acceleration
  pin_memory: true                 # Faster GPU transfer

BATCH PROCESSING
  batch_size_minutes: 2            # Duration threshold for batching
  max_workers: 2                   # Parallel processing threads

CLASSIFICATION
  use_ml: false                    # Use ML classifier (if trained)
  use_advanced: true               # Use advanced multi-feature classifier
  ml_model_path: "models/ml_gender_classifier.pkl"
  pitch_male_threshold: 85.0       # Male pitch threshold (Hz)
  pitch_female_threshold: 165.0    # Female pitch threshold (Hz)

═══════════════════════════════════════════════════════════════════════════════
USAGE COMMANDS
═══════════════════════════════════════════════════════════════════════════════

TEST SUITE
  Run all tests:
    $ python test_voxent_complete.py

  Test with real audio:
    $ python test_pipeline_sample.py

PIPELINE EXECUTION
  Run full processing:
    $ python config/run_pipeline.py

  Check if installation works:
    $ python verify_installation.py

  Quick start:
    $ python quickstart.py

TRAINING
  Train ML classifier:
    $ python train_ml_classifier.py

  Deploy/run web interface:
    $ python web_app.py

UTILITIES
  Convert audio format:
    $ python convert_audio.py

═══════════════════════════════════════════════════════════════════════════════
OUTPUT STRUCTURE
═══════════════════════════════════════════════════════════════════════════════

After processing, files are organized as:

data/voice_dataset/
├── male/
│   ├── voice_sample_0001.wav     (Source: original_file_spk0)
│   ├── voice_sample_0002.wav
│   └── ...
├── female/
│   ├── voice_sample_0003.wav     (Source: original_file_spk1)
│   ├── voice_sample_0004.wav
│   └── ...
├── uncertain/
│   ├── voice_sample_0005.wav     (Low confidence - ambiguous)
│   └── ...
└── metadata.csv                  (Tracking file)

METADATA.CSV FORMAT:
  file,source,speaker,pitch,label,confidence,duration,quality_score,snr
  voice_sample_0001.wav,call_001.wav,SPEAKER_00,120.5,male,87.3,3.2,78.5,15.2
  voice_sample_0002.wav,call_001.wav,SPEAKER_01,220.8,female,92.1,2.8,82.3,16.8

═══════════════════════════════════════════════════════════════════════════════
PERFORMANCE TUNING
═══════════════════════════════════════════════════════════════════════════════

FOR MAXIMUM SPEED (GPU):
  device: "cuda"
  batch_size_gpu: 16
  gpu_memory_fraction: 0.9
  use_mixed_precision: true
  pin_memory: true

FOR BALANCED PERFORMANCE:
  device: "cuda"
  batch_size_gpu: 8
  gpu_memory_fraction: 0.8
  use_mixed_precision: true
  pin_memory: true

FOR CPU ONLY:
  device: "cpu"
  batch_size_cpu: 2
  max_workers: 1

FOR BEST ACCURACY:
  use_ml: true                     # (requires trained model)
  use_advanced: true
  pitch_male_threshold: 85.0
  pitch_female_threshold: 165.0

═══════════════════════════════════════════════════════════════════════════════
OPTIMIZATION TIPS
═════════════════════════════════════════════════════════════════════════════════

1. ENABLE GPU ACCELERATION (3-5x faster)
   $ conda install pytorch pytorch-cuda=11.8 -c pytorch -c nvidia
   Then set device: "cuda" in config.yaml

2. IMPROVE CLASSIFICATION ACCURACY
   $ pip install praat-parselmouth
   (Advanced classifier will use formant extraction automatically)

3. TRAIN ML CLASSIFIER FOR BEST ACCURACY
   $ python train_ml_classifier.py
   (Requires labeled training data)

4. INCREASE BATCH SIZE FOR SPEED
   Change batch_size_gpu: 16 (requires more VRAM)

5. OPTIMIZE FOR YOUR GPU
   Update gpu_memory_fraction based on your GPU VRAM:
     RTX 2050 (4GB):   0.75-0.8
     RTX 3060 (12GB):  0.85-0.9
     RTX 4090 (24GB):  0.9+

═══════════════════════════════════════════════════════════════════════════════
TROUBLESHOOTING
═════════════════════════════════════════════════════════════════════════════════

ERROR: "GPU not available"
  Solution: Install GPU PyTorch
  Command: conda install pytorch pytorch-cuda=11.8 -c pytorch -c nvidia

ERROR: "HF_TOKEN environment variable required"
  Solution: Set HuggingFace token (optional, diarization)
  Command: set HF_TOKEN=your_token_here

ERROR: "Module not found"
  Solution: Install missing dependencies
  Command: pip install -r requirements.txt

ERROR: "Out of memory"
  Solution: Reduce batch size or GPU memory fraction in config.yaml
  
ERROR: "Audio file not found"
  Solution: Ensure audio files are in data/input_calls/
  Support formats: .wav, .mp3

═══════════════════════════════════════════════════════════════════════════════
TESTING RESULTS SUMMARY
═════════════════════════════════════════════════════════════════════════════════

✅ ENVIRONMENT TESTS: PASSED
  - Python 3.12.7: OK
  - PyTorch 2.9.1: OK
  - All dependencies: OK

✅ COMPONENT TESTS: PASSED
  - Pitch classifier: Operational
  - Advanced classifier: Operational
  - Integrated classifier: Operational
  - Batch processor: Operational
  - File organizer: Operational

✅ INTEGRATION TESTS: PASSED
  - Config loading: OK
  - Audio processing: OK
  - File organization: OK
  - 20 audio files processed successfully
  - 100% success rate

✅ PIPELINE TESTS: PASSED
  - Real audio (23.76s): FEMALE (100.0%)
  - Real audio (23.76s): FEMALE (100.0%)
  - Real audio (71.28s): FEMALE (66.7%)

═══════════════════════════════════════════════════════════════════════════════
NEXT STEPS
═════════════════════════════════════════════════════════════════════════════════

1. IMMEDIATE: Run full pipeline with all 20 audio files
   $ python config/run_pipeline.py

2. SHORT TERM: Optimize with GPU acceleration
   $ conda install pytorch pytorch-cuda=11.8 -c pytorch -c nvidia

3. MEDIUM TERM: Train ML classifier for better accuracy
   $ python train_ml_classifier.py

4. LONG TERM: Deploy web interface
   $ python web_app.py

═══════════════════════════════════════════════════════════════════════════════

For detailed information, see:
  - TEST_REPORT_FINAL.txt         (Full test results)
  - IMPLEMENTATION_SUMMARY.txt    (Feature details)
  - config/config.yaml            (Configuration reference)

═══════════════════════════════════════════════════════════════════════════════
