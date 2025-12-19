# EchoForge: Voice Data Collection Research Tool

## Project Vision Reframe

Original Concept: Production-grade speaker separation API for call center analytics

Actual Purpose: Research tool for extracting and curating high-quality voice datasets from call recordings for downstream voice AI model training

---
### Project Strucure

voxent/
├── config/
│   └── config.yaml
│
├── data/
│   ├── input_calls/
│   ├── processed_audio/
│   └── voice_dataset/
│       ├── male/
│       ├── female/
│       ├── uncertain/
│       └── metadata.csv
│
├── preprocessing/
│   ├── audio_loader.py
│   ├── normalize.py
│   ├── vad.py
│
├── diarization/
│   ├── diarizer.py
│   └── segments.py
│
├── classification/
│   ├── pitch_gender.py
│   └── confidence.py
│
├── dataset/
│   ├── organizer.py
│   └── metadata.py
│
├── engine/
│   ├── batch_runner.py
│   └── logger.py
│
├── utils/
│   ├── audio_utils.py
│   └── file_utils.py
│
├── requirements.txt
└── run_pipeline.py

## Core Objective

Build an automated pipeline that transforms raw call recordings into a clean, labeled voice dataset suitable for training custom text-to-speech models, voice assistants, and agent-based voice AI systems.

### Primary Goal

- Input: Collection of call recordings (mixed audio with multiple speakers)
- Output: Organized dataset of isolated speaker segments with accurate gender/voice-type labels
- End Use: Training data for custom voice synthesis and cloning projects

---

## Why This Approach Differs from Production Systems

| Production System | Research Tool |
|-------------------|---------------|
| API-first architecture | Batch processing scripts |
| Real-time processing requirements | Offline processing acceptable |
| Scalability for thousands of users | Single-user, repeated use |
| High availability & error recovery | Manual intervention acceptable |
| Automated everything | Human-in-the-loop verification |
| Generic use cases | Specialized for dataset creation |

---

## System Architecture

### Research-Focused Pipeline

```
Call Recordings
      ↓
[1] Source Separation 
    - Isolate vocals from background noise/music
    - Use when: Recordings contain non-speech audio
    - Skip when: Clean call center recordings
      ↓
[2] Audio Preprocessing
    - Format standardization (mono, consistent sample rate)
    - Voice Activity Detection (remove silence)
    - Loudness normalization
      ↓
[3] Speaker Diarization
    - Identify "who spoke when"
    - Extract temporal segments per speaker
    - Fixed speaker count for consistency
      ↓
[4] Gender/Voice Classification
    - Initial automated labeling (pitch-based or ML)
    - Confidence scoring for review prioritization
    - Manual verification loop
      ↓
[5] Dataset Organization
    - Gender-segregated folders
    - Metadata generation (duration, confidence, source)
    - Quality filtering and augmentation
      ↓
Curated Voice Dataset
```

---

## What We're Building

### Core Components

#### 1. Batch Processing Engine

Purpose: Process multiple call recordings sequentially without user interaction

Key Features:

- File discovery and queuing system
- Progress tracking and logging
- Graceful handling of problematic files
- Resume capability for interrupted runs

NOT Included:

- Web interface or REST API
- Real-time status updates
- Multi-user job management
- Cloud deployment infrastructure

---

#### 2. Audio Preprocessing Module

Purpose: Standardize audio format for consistent downstream processing

Essential Operations:

- Convert any audio format to standard format
- Mono channel conversion
- Resampling to target rate (for ML model compatibility)
- Amplitude normalization

Optional Enhancements:

- Voice Activity Detection (VAD) to remove silence
- Spectral noise reduction
- Source separation for noisy recordings

Output: Clean, normalized audio ready for diarization

---

#### 3. Speaker Diarization Engine

Purpose: Identify distinct speakers and their speech segments

Implementation Strategy:

- Use pre-trained state-of-the-art models (pyannote.audio)
- Hard-code expected speaker count (for call recordings)
- Extract segment timestamps with speaker IDs

Output: List of temporal segments with speaker assignments
```
[
  {start: 0.0s, end: 3.2s, speaker: "SPEAKER_00"},
  {start: 3.2s, end: 7.8s, speaker: "SPEAKER_01"},
  ...
]
```

---

#### 4. Voice Classification System

Purpose: Assign gender/voice-type labels to separated speakers

Phased Approach:

##### Phase 1: Rule-Based Classification (Bootstrap)

- Pitch frequency analysis (F0 calculation)
- Simple threshold-based labeling
- Confidence scoring based on pitch characteristics
- Expected accuracy: 75-85% on clean speech

##### Phase 2: Machine Learning Classification (After Dataset Creation)

- Train custom classifier on verified samples
- Feature extraction: voice embeddings + acoustic features
- Binary classification (male/female voice characteristics)
- Expected accuracy: 90-95% after training

Key Principle: Accept lower initial accuracy, improve through manual verification and retraining

---

#### 5. Dataset Organization System

Purpose: Structure output for efficient use in voice model training

Directory Structure:
```
voice_dataset/
├── male/
│   ├── call_X_speaker_Y_conf_Z.wav
│   └── ...
├── female/
│   ├── call_A_speaker_B_conf_C.wav
│   └── ...
├── uncertain/
│   └── (low confidence samples for review)
└── metadata.csv
```

Metadata Schema:

- File path and identifier
- Source call and speaker number
- Gender label and confidence score
- Duration and audio quality metrics
- Manual verification status

---

## Expected Workflow

### Stage 1: Initial Processing

1. Place call recordings in input directory
2. Run batch processing script
3. System generates initial dataset with automated labels
4. Review high-level statistics (speaker count, duration distribution)

### Stage 2: Manual Verification

1. Sample random files from each gender category
2. Listen and verify label accuracy
3. Move misclassified files to correct folders
4. Flag low-quality samples for exclusion
5. Document verification pass in metadata

### Stage 3: Classifier Training

1. Use verified dataset as training data
2. Extract features from all samples
3. Train supervised classification model
4. Evaluate on held-out test set
5. Save trained model for future use

### Stage 4: Reprocessing & Augmentation

1. Reprocess uncertain samples with trained classifier
2. Apply data augmentation techniques
3. Generate multiple variants per sample
4. Create final curated dataset with metadata
5. Validate dataset quality and distribution

---

## Technology Stack

### Core Libraries

Audio Processing:

- `pydub` - High-level audio manipulation
- `librosa` - Feature extraction and analysis
- `soundfile` - Fast I/O operations
- `ffmpeg` - Format conversion backend

Machine Learning:

- `pyannote.audio` - Speaker diarization models
- `speechbrain` - Voice embedding extraction
- `scikit-learn` - Classifier training
- `torch` - Deep learning inference

Optional:

- `spleeter` - Source separation (if needed)
- `silero-vad` - Voice activity detection
- `audiomentations` - Data augmentation

Utilities:

- `pandas` - Metadata management
- `tqdm` - Progress visualization
- Standard library (`os`, `glob`, `shutil`)

---

## Quality Metrics

### Dataset Quality Indicators

Coverage Metrics:

- Total audio duration per gender category
- Number of unique speakers represented
- Average segment length distribution
- Silence-to-speech ratio

Classification Metrics:

- Initial automated accuracy (pre-verification)
- Post-verification accuracy (ground truth)
- Confidence score distribution
- Uncertain sample percentage

Audio Quality Metrics:

- Signal-to-noise ratio (SNR)
- Clipping/distortion detection
- Frequency response balance
- Consistent loudness levels

### Diarization Performance

Temporal Accuracy:

- Segment boundary precision
- Speaker change detection accuracy
- Overlapping speech handling

Speaker Identification:

- Correct speaker count detection rate
- Speaker consistency across segments
- Cross-talk separation quality

---

## What Success Looks Like

### Immediate Success Criteria (First Run)

- All input files processed without crashes
- Automated labels achieve baseline accuracy
- Output organized in usable directory structure
- Metadata file contains all required fields

### Dataset Quality Criteria (After Verification)

- High confidence samples exceed target accuracy threshold
- Balanced representation across gender categories
- Individual segments meet minimum duration requirements
- Audio quality suitable for model training (no distortion/clipping)

### Long-Term Success Criteria (After Training)

- Custom classifier outperforms rule-based baseline
- Dataset successfully trains functional TTS model
- Reusable pipeline for additional call batches
- Documented lessons learned and optimization strategies

---

## Implementation Phases

### Phase 1: Minimum Viable Pipeline

Focus: Get something working end-to-end

Deliverables:

- Batch processing script that runs unattended
- Basic preprocessing and diarization
- Rule-based classification system
- Simple file organization

Time Investment: Suitable for rapid prototyping

---

### Phase 2: Quality Enhancement

Focus: Improve accuracy and dataset quality

Deliverables:

- Manual verification workflow
- Cleaned and validated dataset
- Custom classifier training pipeline
- Enhanced metadata tracking

Time Investment: Moderate, requires human review time

---

### Phase 3: Refinement & Augmentation

Focus: Maximize dataset utility for training

Deliverables:

- Data augmentation pipeline
- Quality filtering and outlier removal
- Comprehensive dataset documentation
- Reprocessing with improved models

Time Investment: Extended, includes experimentation

---

## Key Design Principles

### 1. Human-in-the-Loop

Automated systems handle volume, humans handle accuracy. Design for easy manual intervention and verification.

### 2. Iterative Improvement

Accept imperfect initial results. Use verified data to train better models, then reprocess.

### 3. Metadata First

Comprehensive metadata enables filtering, analysis, and debugging. Track everything.

### 4. Reproducibility

Scripts should be deterministic and version-controlled. Document all parameter choices.

### 5. Quality Over Quantity

Better to have fewer high-quality samples than many questionable ones. Be aggressive with filtering.

### 6. Modular Design

Each processing stage should be runnable independently. Enables debugging and selective reprocessing.

---

## Common Pitfalls to Avoid

### Over-Engineering

- ❌ Building REST APIs for personal use
- ❌ Complex deployment infrastructure
- ❌ Over-optimizing for scale you don't need
- ✅ Simple scripts that do one thing well

### Under-Validating

- ❌ Trusting automated labels without verification
- ❌ Assuming diarization is always correct
- ❌ Skipping quality checks on output
- ✅ Sample and verify at each stage

### Wrong Success Metrics

- ❌ Optimizing for processing speed
- ❌ Focusing on system uptime
- ❌ Measuring API response times
- ✅ Measuring dataset quality and label accuracy

### Scope Creep

- ❌ Adding real-time processing
- ❌ Building multi-user features
- ❌ Implementing every possible feature
- ✅ Focusing on dataset quality first

---

## Ethical Considerations

### Data Privacy

- Ensure call recordings are obtained with appropriate consent
- Remove personally identifiable information from metadata
- Implement secure storage for source recordings
- Define data retention and deletion policies

### Gender Classification Limitations

- System infers acoustic characteristics, not gender identity
- Binary classification is a simplification
- Document limitations clearly
- Consider "voice type" terminology over "gender"

### Bias Awareness

- Dataset may reflect biases in source material
- Consider demographic representation in training data
- Test trained models across diverse speakers
- Document dataset limitations for downstream users

---

## Future Extensions

### Once Core Pipeline is Stable

Advanced Classification:

- Age estimation from voice
- Accent/dialect detection
- Emotion recognition
- Speaking style categorization

Dataset Enhancements:

- Multi-speaker conversation dynamics
- Cross-reference with transcripts
- Speaker identity clustering across calls
- Voice similarity metrics

Downstream Integration:

- Direct pipeline to TTS training frameworks
- Voice cloning API integration
- Custom voice profile generation
- Quality-aware sample selection

---

## Documentation Requirements

### For Yourself (Future Reference)

- Command-line usage examples for all scripts
- Parameter explanations and tuning guidelines
- Troubleshooting common errors
- Performance benchmarks on your hardware

### For Dataset Users (If Sharing)

- Dataset composition statistics
- Collection and processing methodology
- Known limitations and biases
- Recommended use cases
- License and attribution requirements

---

## Final Notes

This is a research tool, not a product. Optimize for:

- Data quality over processing speed
- Reproducibility over features
- Simplicity over scalability
- Manual control over automation

The goal is creating a high-quality voice dataset for training AI models, not building production infrastructure. Design decisions should prioritize that outcome above all else.