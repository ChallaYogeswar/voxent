# VOXENT Quick Start Guide
## Voice Dataset Creation with Speaker Diarization

**Version:** 2.0  
**Updated:** December 30, 2024

---

## 🎯 What This Does

VOXENT automatically:
1. ✅ Separates speakers in conversation recordings
2. ✅ Classifies speakers by gender (male/female)
3. ✅ Organizes output into clean folder structure
4. ✅ Processes files in GPU-optimized batches
5. ✅ Creates metadata for every segment

**Perfect for:** Creating voice datasets from personal conversation recordings, phone calls, podcasts, or any multi-speaker audio.

---

## 🚀 Installation & Setup

### Step 1: Install Dependencies

Run the setup script:
```bash
python setup_voxent.py
```

This will:
- Install PyTorch, pyannote.audio, librosa, and other dependencies
- Create necessary directories
- Help you configure HuggingFace authentication

**Or install manually:**
```bash
# Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install other dependencies
pip install pyannote.audio librosa soundfile pyyaml tqdm psutil
```

### Step 2: Get HuggingFace Token

Required for speaker diarization:

1. Go to: https://huggingface.co/settings/tokens
2. Create a token (read access is enough)
3. Accept the model license at: https://huggingface.co/pyannote/speaker-diarization-3.1
4. Add your token to `config.yaml`:

```yaml
huggingface:
  token: "hf_YOUR_TOKEN_HERE"
```

### Step 3: Configure Settings

Edit `config.yaml` to customize:

**Batch Settings:**
```yaml
batch_organization:
  files_per_batch: 10        # Your setting
  batch_size_minutes: 2.0    # Maximum duration per batch
```

**GPU Settings:**
```yaml
gpu:
  batch_size_gpu: 10         # Your setting
  memory_threshold: 80.0     # Warn at 80% VRAM usage
```

**Speaker Settings:**
```yaml
diarization:
  min_speakers: 2            # For conversations
  max_speakers: 2
```

---

## 📂 Directory Structure

```
VOXENT/
├── data/
│   ├── input_calls/         # 👈 PUT YOUR AUDIO FILES HERE
│   ├── batches/             # Auto-created batch folders
│   └── voice_dataset/       # Final output with separated speakers
├── config.yaml              # Configuration file
├── voxent_pipeline.py       # Main script
├── enhanced_diarizer.py     # Speaker separation module
├── batch_organizer.py       # Batch creation module
├── batch_processor.py       # Processing engine
└── logs/                    # Processing logs and reports
```

---

## 🎬 Usage

### Basic Usage

1. **Add your audio files:**
   ```bash
   # Copy your conversation recordings to:
   cp /path/to/your/recordings/*.wav data/input_calls/
   ```

2. **Run the pipeline:**
   ```bash
   python voxent_pipeline.py --config config.yaml
   ```

3. **Check the output:**
   ```
   data/voice_dataset/
   ├── batch_001/
   │   ├── call_001/
   │   │   ├── male/              # Male speaker segments
   │   │   │   ├── call_001_speaker_00_seg000.wav
   │   │   │   └── call_001_speaker_00_seg002.wav
   │   │   ├── female/            # Female speaker segments
   │   │   │   ├── call_001_speaker_01_seg001.wav
   │   │   │   └── call_001_speaker_01_seg003.wav
   │   │   └── metadata.json      # Segment information
   │   └── batch_results.json     # Batch statistics
   └── processing_summary.json    # Overall results
   ```

### Advanced Usage

**Skip batch organization (if already organized):**
```bash
python voxent_pipeline.py --skip-organize
```

**Process specific batches:**
```python
from batch_processor import IntegratedBatchProcessor
from enhanced_diarizer import EnhancedSpeakerDiarizer

# Initialize
config = {...}
diarizer = EnhancedSpeakerDiarizer(config)
processor = IntegratedBatchProcessor(diarizer, config)

# Process single batch
processor.process_batch_folder(
    batch_folder="data/batches/batch_001",
    output_base_dir="data/voice_dataset"
)
```

---

## 📊 Understanding the Output

### Output Structure

**Gender-based organization (default):**
```
voice_dataset/
└── batch_001/
    └── recording_001/
        ├── male/              # Male speaker segments
        ├── female/            # Female speaker segments
        ├── segments/          # All segments (speaker-labeled)
        └── metadata.json      # Complete metadata
```

### Metadata Format

Each processed file generates metadata:

```json
{
  "audio_file": "path/to/original.wav",
  "processing_timestamp": "2024-12-30T10:30:00",
  "num_speakers": 2,
  "total_segments": 15,
  "segments": [
    {
      "segment_path": "path/to/segment.wav",
      "speaker": "SPEAKER_00",
      "gender": "male",
      "gender_confidence": 0.87,
      "start_time": 0.0,
      "end_time": 3.5,
      "duration": 3.5
    }
  ]
}
```

---

## 🔧 Troubleshooting

### Issue: "HuggingFace token required"

**Solution:**
1. Get token from: https://huggingface.co/settings/tokens
2. Accept model at: https://huggingface.co/pyannote/speaker-diarization-3.1
3. Add to config.yaml

### Issue: GPU out of memory

**Solutions:**
1. Reduce batch size in config.yaml:
   ```yaml
   gpu:
     batch_size_gpu: 5  # Reduce from 10
   ```

2. Enable cache clearing:
   ```yaml
   gpu:
     clear_cache_between_batches: true
   ```

3. Use mixed precision:
   ```yaml
   gpu:
     use_mixed_precision: true
   ```

### Issue: Speaker separation not working

**Check:**
- Are input files conversation recordings (multi-speaker)?
- Is the diarization model loaded correctly?
- Check logs for errors: `logs/voxent.log`

### Issue: No audio files found

**Solution:**
1. Check audio files are in: `data/input_calls/`
2. Supported formats: .wav, .mp3, .flac, .m4a
3. Verify file permissions

### Issue: Gender classification incorrect

**Solution:**
The pitch-based method has limitations. To improve:
1. Use longer audio segments (better pitch estimation)
2. Consider implementing ML-based classification
3. Manually review and correct if needed

---

## 📈 Performance Tips

### Optimize GPU Usage

**Your RTX 2050 (4GB VRAM):**
- Start with 10 files per batch ✅
- Monitor VRAM in logs
- Adjust if you see memory warnings

**Check GPU status:**
```python
import torch
print(f"GPU: {torch.cuda.get_device_name(0)}")
print(f"Memory: {torch.cuda.mem_get_info()[0] / 1e9:.2f} GB free")
```

### Batch Size Guidelines

| Total Audio Duration | Recommended Batch Size |
|---------------------|------------------------|
| < 20 minutes        | All files (no batching)|
| 20-60 minutes       | 10 files per batch    |
| 60-120 minutes      | 8 files per batch     |
| > 120 minutes       | 5 files per batch     |

### Processing Speed

**Approximate times (RTX 2050):**
- Diarization: ~5-10 seconds per minute of audio
- Segment extraction: ~1 second per segment
- Gender classification: ~0.1 seconds per segment

**Example:** 10 files × 2 minutes each = ~4-8 minutes processing time

---

## 🎯 Use Cases

### 1. Personal Voice Dataset
You want to create a dataset from conversations with friends:
- ✅ Automatically separates your voice from friends
- ✅ Organizes by gender
- ✅ Ready for ML training

### 2. Podcast Processing
Extract individual speaker segments from podcast episodes:
- ✅ Identifies host vs guest
- ✅ Creates clean speaker segments
- ✅ Maintains timing metadata

### 3. Interview Analysis
Process interview recordings:
- ✅ Separates interviewer from interviewee
- ✅ Analyzes speaking patterns
- ✅ Creates searchable segments

---

## 📝 Configuration Reference

### Key Settings Explained

**files_per_batch:** Number of audio files to process together before clearing GPU cache. You set this to **10**.

**batch_size_minutes:** Maximum total duration for files in one batch. Helps prevent GPU memory overflow.

**batch_size_gpu:** How many files to load into GPU memory simultaneously. You set this to **10**.

**memory_threshold:** VRAM usage percentage that triggers a warning (80% = 3.2GB of 4GB).

**clear_cache_between_batches:** Clears GPU memory between batches to prevent accumulation.

**min/max_speakers:** Expected number of speakers in each recording (2 for conversations).

---

## 🆘 Getting Help

### Check Logs
All processing details are logged:
```bash
# View recent logs
cat logs/voxent.log

# View processing summary
cat data/voice_dataset/processing_summary.json
```

### Common Error Messages

**"CUDA out of memory"**
→ Reduce batch_size_gpu in config

**"No audio files found"**
→ Add files to data/input_calls/

**"Token required"**
→ Add HuggingFace token to config

**"Speaker diarization failed"**
→ Check audio quality and format

---

## 🎉 Success Indicators

Pipeline is working correctly when you see:

✅ Batches created in `data/batches/`  
✅ Gender folders (male/, female/) in output  
✅ Metadata files generated  
✅ Success rate > 90% in summary  
✅ No "out of memory" errors  

---

## 📚 Next Steps

After successful processing:

1. **Verify output quality:**
   - Listen to a few segments
   - Check gender classification accuracy
   - Verify speaker separation

2. **Adjust configuration:**
   - Fine-tune batch sizes based on logs
   - Adjust gender classification thresholds if needed

3. **Scale up:**
   - Process larger datasets
   - Experiment with different audio types

---

## 🔄 Workflow Summary

```
INPUT FILES (data/input_calls/)
    ↓
[Batch Organization]
    ↓
BATCHES (data/batches/batch_001, batch_002, ...)
    ↓
[Speaker Diarization]
    ↓
SPEAKER SEGMENTS (timestamps identified)
    ↓
[Gender Classification]
    ↓
ORGANIZED OUTPUT (data/voice_dataset/male/, female/)
    ↓
METADATA & REPORTS (JSON files)
```

---

## 📞 Support

For issues or questions:
1. Check logs: `logs/voxent.log`
2. Review configuration: `config.yaml`
3. Check documentation in code files
4. Verify HuggingFace setup

---

**Ready to start? 🚀**

```bash
# Add your files
cp your_recordings/*.wav data/input_calls/

# Run pipeline
python voxent_pipeline.py

# Check results
ls -R data/voice_dataset/
```

Good luck with your voice dataset creation!
