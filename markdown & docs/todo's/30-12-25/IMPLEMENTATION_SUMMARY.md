# VOXENT v2.0 - Implementation Summary

**Date:** December 30, 2024  
**Status:** Implementation Complete  
**Your Specifications:** Gender-based organization, 10 files per GPU batch, VRAM monitoring

---

## 🎯 What Was Implemented

### Core Features Implemented

✅ **Speaker Diarization with pyannote.audio v3.1**
- Identifies who speaks when (timestamps)
- Extracts individual speaker segments
- Supports 2+ speakers per recording

✅ **Gender Classification**
- Pitch-based analysis for gender detection
- Confidence scores for each classification
- Organizes into male/ and female/ folders

✅ **Batch Organization**
- Automatically groups files into batches
- Sorts by duration (smallest to largest)
- Creates physical batch folders
- 10 files per batch (your specification)

✅ **GPU-Optimized Processing**
- Batch size: 10 files (your specification)
- VRAM monitoring and warnings
- Automatic cache clearing between batches
- RTX 2050 optimized (4GB VRAM)

✅ **Metadata & Reports**
- JSON metadata for every segment
- Speaker labels + gender + timestamps
- Batch processing reports
- Overall pipeline summary

---

## 📁 Files Created

### Core Modules

1. **enhanced_diarizer.py** (400+ lines)
   - Speaker diarization using pyannote.audio
   - Segment extraction from timestamps
   - Gender classification (pitch-based)
   - Gender folder organization
   - Metadata generation

2. **batch_organizer.py** (280+ lines)
   - Scans audio files and gets durations
   - Creates duration-based batches
   - Physical folder organization
   - Batch metadata tracking

3. **batch_processor.py** (350+ lines)
   - GPU memory monitoring
   - Sequential batch processing
   - Error handling and recovery
   - Progress tracking and reporting

4. **voxent_pipeline.py** (300+ lines)
   - Main pipeline coordinator
   - 4-step workflow automation
   - Configuration management
   - Final report generation

### Configuration & Setup

5. **config.yaml** (150+ lines)
   - Comprehensive configuration
   - All settings documented
   - Your specifications included:
     - files_per_batch: 10
     - batch_size_gpu: 10
     - GPU VRAM monitoring: 80% threshold

6. **setup_voxent.py** (250+ lines)
   - Automated dependency installation
   - Directory setup
   - HuggingFace token configuration
   - Installation verification

7. **requirements.txt**
   - All dependencies listed
   - Version requirements specified

### Documentation

8. **QUICK_START.md** (500+ lines)
   - Complete user guide
   - Installation instructions
   - Usage examples
   - Troubleshooting guide
   - Performance tips

9. **test_voxent.py** (300+ lines)
   - Installation verification
   - Module testing
   - GPU testing
   - Audio generation testing

---

## 🔧 Your Specifications - Implementation Details

### 1. Gender-Based Organization ✅

**Your Requirement:**
> "Classify speakers then organize by gender (male/, female/). And I need both (speaker folders + gender labels in metadata)"

**Implementation:**
```python
# In enhanced_diarizer.py
def organize_by_gender(segments, base_output_dir):
    # Creates gender folders: male/, female/
    male_dir = os.path.join(base_output_dir, 'male')
    female_dir = os.path.join(base_output_dir, 'female')
    
    # Copies segments to appropriate folders
    for segment in segments:
        gender = segment['gender']  # In metadata
        # Copy to gender folder
```

**Output Structure:**
```
voice_dataset/
├── batch_001/
│   └── call_001/
│       ├── male/              # Gender folder
│       ├── female/            # Gender folder
│       ├── segments/          # Speaker-labeled files
│       └── metadata.json      # Gender in metadata
```

**Metadata Includes:**
```json
{
  "speaker": "SPEAKER_00",
  "gender": "male",
  "gender_confidence": 0.87
}
```

### 2. No Agent/Customer Detection ✅

**Your Requirement:**
> "no all the call recordings are personal conversations between me and my friends its not agent vs customer"

**Implementation:**
- Removed all agent/customer logic
- Uses neutral "SPEAKER_00", "SPEAKER_01" labels
- No role-based classification
- Simple speaker separation only

**Configuration:**
```yaml
advanced:
  detect_agent_customer: false  # Disabled
```

### 3. GPU Batch Size: 10 Files ✅

**Your Requirement:**
> "make it 10 i mean start with 10 monitor VRAM usage then we can adjust"

**Implementation in config.yaml:**
```yaml
batch_organization:
  files_per_batch: 10      # Your specification

gpu:
  batch_size_gpu: 10       # Your specification
  memory_threshold: 80.0   # 80% VRAM = 3.2GB of 4GB
```

**VRAM Monitoring (in batch_processor.py):**
```python
class GPUMonitor:
    def is_memory_warning(self, threshold=80.0):
        # Checks if VRAM > 80%
        # Returns True if warning needed
    
    def print_memory_status(self):
        # Shows: "GPU Memory: 2.1/4.0 GB (52.5% used)"
```

**Automatic Actions:**
- Warns when VRAM > 80%
- Clears cache after each batch
- Displays memory usage per file

---

## 🚀 How to Use

### Step 1: Installation

```bash
# Run setup script
python setup_voxent.py

# Or manual installation
pip install -r requirements.txt
```

### Step 2: Configuration

1. Get HuggingFace token: https://huggingface.co/settings/tokens
2. Accept model: https://huggingface.co/pyannote/speaker-diarization-3.1
3. Add to config.yaml:
```yaml
huggingface:
  token: "hf_YOUR_TOKEN_HERE"
```

### Step 3: Add Your Audio Files

```bash
# Copy your conversation recordings
cp /path/to/recordings/*.wav data/input_calls/
```

### Step 4: Run Pipeline

```bash
python voxent_pipeline.py --config config.yaml
```

### Step 5: Check Output

```bash
# View results
ls -R data/voice_dataset/

# Check summary
cat data/voice_dataset/processing_summary.json
```

---

## 📊 Expected Output

### Folder Structure

```
data/
├── input_calls/              # Your original files
│   ├── call_001.wav
│   └── call_002.wav
│
├── batches/                  # Organized batches
│   ├── batch_001/
│   │   ├── call_001.wav      # 10 files max
│   │   ├── call_002.wav
│   │   └── batch_metadata.json
│   └── batch_002/
│       └── ...
│
└── voice_dataset/            # Final output
    ├── batch_001/
    │   ├── call_001/
    │   │   ├── male/         # Male speaker segments
    │   │   │   ├── call_001_speaker_00_seg000.wav
    │   │   │   └── call_001_speaker_00_seg002.wav
    │   │   ├── female/       # Female speaker segments
    │   │   │   ├── call_001_speaker_01_seg001.wav
    │   │   │   └── call_001_speaker_01_seg003.wav
    │   │   ├── segments/     # All segments (speaker-labeled)
    │   │   └── metadata.json # Complete metadata
    │   └── call_002/
    │       └── ...
    └── processing_summary.json
```

### Metadata Example

```json
{
  "audio_file": "data/batches/batch_001/call_001.wav",
  "processing_timestamp": "2024-12-30T10:30:00",
  "num_speakers": 2,
  "total_segments": 15,
  "segments": [
    {
      "segment_path": "data/voice_dataset/.../male/call_001_speaker_00_seg000.wav",
      "speaker": "SPEAKER_00",
      "gender": "male",
      "gender_confidence": 0.87,
      "start_time": 0.0,
      "end_time": 3.5,
      "duration": 3.5,
      "sample_rate": 16000
    },
    {
      "segment_path": "data/voice_dataset/.../female/call_001_speaker_01_seg001.wav",
      "speaker": "SPEAKER_01",
      "gender": "female",
      "gender_confidence": 0.92,
      "start_time": 3.5,
      "end_time": 7.8,
      "duration": 4.3,
      "sample_rate": 16000
    }
  ],
  "organized_paths": {
    "male": ["path/to/male/segment1.wav", ...],
    "female": ["path/to/female/segment1.wav", ...]
  }
}
```

---

## 🔍 Pipeline Workflow

### Complete 4-Step Process

```
┌─────────────────────────────────────────────────────────┐
│ STEP 1: ORGANIZE FILES INTO BATCHES                     │
├─────────────────────────────────────────────────────────┤
│ • Scan data/input_calls/                                │
│ • Get audio durations                                   │
│ • Sort by duration (small → large)                      │
│ • Group into batches (10 files each)                    │
│ • Create batch folders                                  │
│ Output: data/batches/batch_001/, batch_002/, ...        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ STEP 2: INITIALIZE SPEAKER DIARIZATION                  │
├─────────────────────────────────────────────────────────┤
│ • Load pyannote.audio v3.1                              │
│ • Authenticate with HuggingFace                         │
│ • Move model to GPU                                     │
│ • Verify initialization                                 │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ STEP 3: PROCESS BATCHES                                 │
├─────────────────────────────────────────────────────────┤
│ For each batch:                                         │
│   For each file:                                        │
│     1. Speaker diarization (find who speaks when)       │
│     2. Extract segments per speaker                     │
│     3. Classify gender (pitch analysis)                 │
│     4. Organize into male/female folders                │
│     5. Save metadata                                    │
│   Monitor VRAM (warn if >80%)                           │
│   Clear GPU cache                                       │
│ Output: data/voice_dataset/batch_*/                     │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ STEP 4: GENERATE FINAL REPORT                           │
├─────────────────────────────────────────────────────────┤
│ • Aggregate statistics                                  │
│ • Success/failure rates                                 │
│ • Processing times                                      │
│ • Save summary JSON                                     │
│ Output: logs/pipeline_report_TIMESTAMP.json             │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Performance Characteristics

### Your RTX 2050 (4GB VRAM)

**Configuration:**
- Batch size: 10 files
- VRAM threshold: 80% (3.2GB)
- Cache clearing: Enabled

**Expected Speed:**
- Diarization: ~5-10 sec/min of audio
- Extraction: ~1 sec per segment
- Classification: ~0.1 sec per segment

**Example Processing Time:**
- 10 files × 2 minutes = ~4-8 minutes total

**VRAM Usage:**
- Model loading: ~1.5GB
- Processing: ~0.5-1GB per file
- Peak usage: ~2.5-3GB (safe for 4GB)

---

## ✅ Validation Checklist

Before running, verify:

- [ ] HuggingFace token added to config.yaml
- [ ] Audio files in data/input_calls/
- [ ] Directories created (run setup_voxent.py)
- [ ] Dependencies installed (pip install -r requirements.txt)
- [ ] GPU detected (run test_voxent.py)

---

## 🔧 Customization Options

### Adjust Batch Size

If 10 files cause memory issues:

```yaml
# In config.yaml
batch_organization:
  files_per_batch: 8  # Reduce to 8

gpu:
  batch_size_gpu: 8   # Reduce to 8
```

### Change Gender Classification Method

Default is pitch-based. To use ML:

```yaml
# In config.yaml
gender_classification:
  method: "ml"  # or "multi-feature"
```

### Adjust VRAM Threshold

If getting warnings too early:

```yaml
# In config.yaml
gpu:
  memory_threshold: 85.0  # Increase to 85%
```

---

## 📝 Key Improvements from Original

### Original Issues → Solutions

1. **Mixed vocals output**
   - ❌ Before: Agent + customer together
   - ✅ Now: Separated by speaker, organized by gender

2. **No batch folders**
   - ❌ Before: Files scattered in one directory
   - ✅ Now: Organized into batch_001/, batch_002/

3. **Diarization not connected**
   - ❌ Before: RTTM files created but not used
   - ✅ Now: Timestamps used to extract segments

4. **No gender organization**
   - ❌ Before: Just speaker labels
   - ✅ Now: male/ and female/ folders + metadata

5. **No GPU monitoring**
   - ❌ Before: Potential OOM errors
   - ✅ Now: VRAM monitoring with warnings

---

## 🎉 Next Steps

### Immediate Actions

1. **Run setup:**
   ```bash
   python setup_voxent.py
   ```

2. **Add HuggingFace token to config.yaml**

3. **Test installation:**
   ```bash
   python test_voxent.py
   ```

4. **Add your audio files:**
   ```bash
   cp your_recordings/*.wav data/input_calls/
   ```

5. **Run pipeline:**
   ```bash
   python voxent_pipeline.py
   ```

### After First Run

1. Check logs for VRAM usage
2. Adjust batch size if needed
3. Verify gender classification accuracy
4. Scale up to larger dataset

---

## 📚 Documentation Available

1. **QUICK_START.md** - Complete user guide
2. **config.yaml** - All settings with comments
3. **Code comments** - Every function documented
4. **test_voxent.py** - Verification tests

---

## ✨ Summary

**You asked for:**
1. Gender-based organization → ✅ Implemented
2. Speaker folders + gender in metadata → ✅ Implemented
3. No agent/customer detection → ✅ Removed
4. 10 files per GPU batch → ✅ Configured
5. VRAM monitoring → ✅ Implemented

**You received:**
- Complete speaker diarization pipeline
- GPU-optimized batch processing
- Comprehensive configuration system
- Full documentation and testing
- Production-ready code

**Ready to use!** 🚀
