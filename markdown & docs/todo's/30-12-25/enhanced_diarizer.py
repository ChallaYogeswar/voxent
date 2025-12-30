"""
Enhanced Speaker Diarization Module
Separates speakers in audio files and organizes by gender

Key Features:
- Uses pyannote.audio v3.1 for speaker diarization
- Extracts individual speaker segments
- Classifies speakers by gender
- Organizes outputs into gender folders (male/, female/)
- Preserves speaker metadata
"""

import os
import torch
import torchaudio
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import json
from datetime import datetime

# Check if pyannote is available
try:
    from pyannote.audio import Pipeline
    PYANNOTE_AVAILABLE = True
except ImportError:
    PYANNOTE_AVAILABLE = False
    print("WARNING: pyannote.audio not installed. Install with: pip install pyannote.audio")


class EnhancedSpeakerDiarizer:
    """
    Advanced speaker diarization with gender classification and organization
    """
    
    def __init__(self, config: Dict):
        """
        Initialize diarizer with configuration
        
        Args:
            config: Configuration dictionary with diarization settings
        """
        self.config = config
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.pipeline = None
        
        # Extract config parameters
        self.min_speakers = config.get('min_speakers', 2)
        self.max_speakers = config.get('max_speakers', 2)
        self.use_auth_token = config.get('hf_token', None)
        
        print(f"Initializing Enhanced Diarizer on device: {self.device}")
        
    def initialize_pipeline(self):
        """Initialize pyannote diarization pipeline"""
        if not PYANNOTE_AVAILABLE:
            raise ImportError("pyannote.audio is required. Install with: pip install pyannote.audio")
        
        if self.use_auth_token is None:
            raise ValueError(
                "HuggingFace token required for pyannote.audio v3.1\n"
                "Get token from: https://huggingface.co/settings/tokens\n"
                "Accept pyannote/speaker-diarization-3.1 model card at:\n"
                "https://huggingface.co/pyannote/speaker-diarization-3.1"
            )
        
        print("Loading pyannote speaker-diarization-3.1 pipeline...")
        self.pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=self.use_auth_token
        )
        self.pipeline.to(self.device)
        print("Pipeline loaded successfully!")
        
    def diarize_audio(self, audio_path: str) -> Dict:
        """
        Perform speaker diarization on audio file
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Dictionary with speaker segments and timestamps
        """
        if self.pipeline is None:
            self.initialize_pipeline()
        
        print(f"Diarizing: {audio_path}")
        
        # Run diarization
        diarization = self.pipeline(
            audio_path,
            min_speakers=self.min_speakers,
            max_speakers=self.max_speakers
        )
        
        # Extract speaker segments
        segments = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            segments.append({
                'speaker': speaker,
                'start': turn.start,
                'end': turn.end,
                'duration': turn.end - turn.start
            })
        
        return {
            'audio_path': audio_path,
            'num_speakers': len(set([s['speaker'] for s in segments])),
            'segments': segments,
            'total_duration': max([s['end'] for s in segments]) if segments else 0
        }
    
    def extract_speaker_segments(
        self, 
        audio_path: str, 
        diarization_result: Dict,
        output_dir: str
    ) -> List[Dict]:
        """
        Extract individual speaker segments from audio
        
        Args:
            audio_path: Path to original audio file
            diarization_result: Diarization output from diarize_audio()
            output_dir: Directory to save speaker segments
            
        Returns:
            List of extracted segment info
        """
        # Load audio
        waveform, sample_rate = torchaudio.load(audio_path)
        
        # Ensure mono audio
        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=True)
        
        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Extract each segment
        extracted_segments = []
        base_filename = Path(audio_path).stem
        
        for idx, segment in enumerate(diarization_result['segments']):
            # Calculate sample indices
            start_sample = int(segment['start'] * sample_rate)
            end_sample = int(segment['end'] * sample_rate)
            
            # Extract segment
            segment_waveform = waveform[:, start_sample:end_sample]
            
            # Create filename
            speaker_label = segment['speaker'].replace('SPEAKER_', 'speaker_')
            segment_filename = f"{base_filename}_{speaker_label}_seg{idx:03d}.wav"
            segment_path = os.path.join(output_dir, segment_filename)
            
            # Save segment
            torchaudio.save(segment_path, segment_waveform, sample_rate)
            
            # Store segment info
            extracted_segments.append({
                'segment_path': segment_path,
                'speaker': segment['speaker'],
                'start_time': segment['start'],
                'end_time': segment['end'],
                'duration': segment['duration'],
                'sample_rate': sample_rate,
                'filename': segment_filename
            })
            
        print(f"Extracted {len(extracted_segments)} speaker segments")
        return extracted_segments
    
    def classify_speaker_gender(self, segment_path: str) -> Tuple[str, float]:
        """
        Classify speaker gender using pitch analysis
        
        Args:
            segment_path: Path to speaker segment audio
            
        Returns:
            Tuple of (gender, confidence)
        """
        # Load audio
        waveform, sample_rate = torchaudio.load(segment_path)
        
        # Ensure mono
        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=True)
        
        # Convert to numpy
        audio_np = waveform.squeeze().numpy()
        
        # Calculate fundamental frequency (F0) using autocorrelation
        f0 = self._estimate_pitch(audio_np, sample_rate)
        
        # Gender classification based on pitch
        # Male: 85-180 Hz, Female: 165-255 Hz
        if f0 < 150:
            gender = "male"
            confidence = min(1.0, (150 - f0) / 65)  # Normalize confidence
        elif f0 > 180:
            gender = "female"
            confidence = min(1.0, (f0 - 180) / 75)  # Normalize confidence
        else:
            # Ambiguous range (150-180 Hz)
            if f0 < 165:
                gender = "male"
                confidence = 0.5
            else:
                gender = "female"
                confidence = 0.5
        
        return gender, float(confidence)
    
    def _estimate_pitch(self, audio: np.ndarray, sample_rate: int) -> float:
        """
        Estimate pitch using autocorrelation method
        
        Args:
            audio: Audio waveform as numpy array
            sample_rate: Sample rate in Hz
            
        Returns:
            Estimated fundamental frequency (F0) in Hz
        """
        # Normalize audio
        audio = audio / (np.max(np.abs(audio)) + 1e-8)
        
        # Define pitch range to search (50-400 Hz for human voice)
        min_pitch = 50
        max_pitch = 400
        
        # Calculate lag range
        min_lag = int(sample_rate / max_pitch)
        max_lag = int(sample_rate / min_pitch)
        
        # Compute autocorrelation
        autocorr = np.correlate(audio, audio, mode='full')
        autocorr = autocorr[len(autocorr)//2:]  # Keep positive lags only
        
        # Find peak in valid lag range
        autocorr_range = autocorr[min_lag:max_lag]
        
        if len(autocorr_range) == 0:
            return 150.0  # Default to ambiguous pitch
        
        peak_lag = np.argmax(autocorr_range) + min_lag
        
        # Convert lag to frequency
        f0 = sample_rate / peak_lag
        
        return f0
    
    def organize_by_gender(
        self, 
        segments: List[Dict], 
        base_output_dir: str
    ) -> Dict[str, List[str]]:
        """
        Organize speaker segments into gender-based folders
        
        Args:
            segments: List of segment dictionaries with gender classification
            base_output_dir: Base directory for organized output
            
        Returns:
            Dictionary mapping gender to list of file paths
        """
        organized = {'male': [], 'female': [], 'unknown': []}
        
        # Create gender folders
        male_dir = os.path.join(base_output_dir, 'male')
        female_dir = os.path.join(base_output_dir, 'female')
        unknown_dir = os.path.join(base_output_dir, 'unknown')
        
        os.makedirs(male_dir, exist_ok=True)
        os.makedirs(female_dir, exist_ok=True)
        os.makedirs(unknown_dir, exist_ok=True)
        
        # Copy segments to appropriate folders
        for segment in segments:
            gender = segment.get('gender', 'unknown')
            source_path = segment['segment_path']
            
            if gender == 'male':
                dest_path = os.path.join(male_dir, os.path.basename(source_path))
            elif gender == 'female':
                dest_path = os.path.join(female_dir, os.path.basename(source_path))
            else:
                dest_path = os.path.join(unknown_dir, os.path.basename(source_path))
            
            # Copy file (or move if preferred)
            import shutil
            shutil.copy2(source_path, dest_path)
            organized[gender].append(dest_path)
        
        print(f"Organized segments: {len(organized['male'])} male, "
              f"{len(organized['female'])} female, {len(organized['unknown'])} unknown")
        
        return organized
    
    def process_audio_file(
        self, 
        audio_path: str, 
        output_base_dir: str,
        organize_by_gender: bool = True
    ) -> Dict:
        """
        Complete pipeline: diarize, extract, classify, and organize
        
        Args:
            audio_path: Path to input audio file
            output_base_dir: Base directory for all outputs
            organize_by_gender: Whether to organize by gender folders
            
        Returns:
            Dictionary with processing results and metadata
        """
        print(f"\n{'='*60}")
        print(f"Processing: {audio_path}")
        print(f"{'='*60}")
        
        # Step 1: Diarization
        print("\n[1/4] Running speaker diarization...")
        diarization_result = self.diarize_audio(audio_path)
        print(f"  ✓ Found {diarization_result['num_speakers']} speakers")
        print(f"  ✓ Total segments: {len(diarization_result['segments'])}")
        
        # Step 2: Extract segments
        print("\n[2/4] Extracting speaker segments...")
        segments_dir = os.path.join(output_base_dir, 'segments')
        extracted_segments = self.extract_speaker_segments(
            audio_path, 
            diarization_result,
            segments_dir
        )
        print(f"  ✓ Extracted {len(extracted_segments)} segments")
        
        # Step 3: Gender classification
        print("\n[3/4] Classifying speaker gender...")
        for segment in extracted_segments:
            gender, confidence = self.classify_speaker_gender(segment['segment_path'])
            segment['gender'] = gender
            segment['gender_confidence'] = confidence
            print(f"  ✓ {segment['speaker']}: {gender} ({confidence:.2%} confidence)")
        
        # Step 4: Organize by gender
        organized_paths = None
        if organize_by_gender:
            print("\n[4/4] Organizing by gender...")
            organized_paths = self.organize_by_gender(extracted_segments, output_base_dir)
        
        # Save metadata
        metadata = {
            'audio_file': audio_path,
            'processing_timestamp': datetime.now().isoformat(),
            'num_speakers': diarization_result['num_speakers'],
            'total_segments': len(extracted_segments),
            'segments': extracted_segments,
            'organized_paths': organized_paths
        }
        
        metadata_path = os.path.join(output_base_dir, 'metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\n✅ Processing complete!")
        print(f"   Metadata saved: {metadata_path}")
        
        return metadata


def main():
    """Example usage"""
    
    # Configuration
    config = {
        'min_speakers': 2,
        'max_speakers': 2,
        'hf_token': None  # Set your HuggingFace token here
    }
    
    # Initialize diarizer
    diarizer = EnhancedSpeakerDiarizer(config)
    
    # Process audio file
    audio_path = "path/to/your/audio.wav"
    output_dir = "output/speaker_separation"
    
    result = diarizer.process_audio_file(
        audio_path=audio_path,
        output_base_dir=output_dir,
        organize_by_gender=True
    )
    
    print(f"\nResults: {result}")


if __name__ == "__main__":
    main()
