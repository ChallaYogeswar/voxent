"""
Source separation module using Demucs.
Separates vocals from accompaniment in audio files.
This enables gender classification on pure vocal tracks.
"""

import os
import numpy as np
import torch
import torchaudio
import logging
from demucs.pretrained import get_model
from demucs.apply import apply_model
from demucs.audio import convert_audio

logger = logging.getLogger(__name__)


class VocalSeparator:
    """Separates vocals from accompaniment using Demucs."""
    
    def __init__(self, model_name: str = "htdemucs", device: str = None):
        """
        Initialize vocal separator with Demucs model.
        
        Args:
            model_name: Demucs model to use (default: "htdemucs" - high-quality)
            device: torch device ("cpu" or "cuda", auto-detect if None)
        """
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.sample_rate = 44100  # Demucs default sample rate
        
        try:
            logger.info(f"Loading Demucs model '{model_name}' on {self.device}...")
            self.model = get_model(model_name).to(self.device)
            self.model.eval()
            logger.info(f"Demucs model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Demucs model: {e}")
            raise
    
    def separate_vocals(self, audio: np.ndarray, sample_rate: int) -> dict:
        """
        Separate vocals from accompaniment.
        
        Args:
            audio: Audio waveform (numpy array, mono or stereo)
            sample_rate: Sample rate of audio
        
        Returns:
            Dictionary with keys:
            - 'vocals': separated vocal track (numpy array)
            - 'accompaniment': separated accompaniment (numpy array)
            - 'confidence': separation confidence score
        """
        try:
            # Convert to torch tensor
            if audio.ndim == 1:
                # Mono to stereo
                audio_tensor = torch.from_numpy(audio).float().unsqueeze(0)
                audio_tensor = audio_tensor.repeat(2, 1)
            else:
                audio_tensor = torch.from_numpy(audio).float()
            
            # Ensure correct format for Demucs (channels x samples)
            if audio_tensor.shape[0] != 2:
                # If not stereo, convert
                if audio_tensor.shape[0] > 2:
                    audio_tensor = audio_tensor[:2]
                else:
                    audio_tensor = audio_tensor.repeat(2, 1)
            
            # Convert sample rate if needed (Demucs expects 44100 Hz)
            model_sr = 44100  # Demucs fixed sample rate
            if sample_rate != model_sr:
                audio_tensor = convert_audio(audio_tensor, sample_rate, model_sr, channels_first=True)
                sr = model_sr
            else:
                sr = sample_rate
            
            # Move to device
            audio_tensor = audio_tensor.to(self.device)
            
            # Apply separation model
            logger.debug(f"Separating vocals from {audio_tensor.shape} tensor...")
            with torch.no_grad():
                sources = apply_model(self.model, audio_tensor, device=self.device, progress=False)
            
            # Extract vocals and accompaniment
            # Demucs returns: [drums, bass, other, vocals]
            vocals = sources[-1]  # Last source is vocals
            accompaniment = sources[:-1].sum(dim=0)  # Sum other sources
            
            # Convert back to numpy (take first channel for mono)
            vocals_np = vocals[0].cpu().numpy() if vocals.shape[0] > 1 else vocals.cpu().numpy()
            accomp_np = accompaniment[0].cpu().numpy() if accompaniment.shape[0] > 1 else accompaniment.cpu().numpy()
            
            # Convert back to original sample rate if needed
            if sr != sample_rate:
                # Simple resampling using linear interpolation
                factor = sample_rate / sr
                original_len = int(len(audio) * factor / len(vocals_np))
                
                vocals_np = np.interp(
                    np.linspace(0, len(vocals_np) - 1, int(len(vocals_np) * factor))[:len(audio)],
                    np.arange(len(vocals_np)),
                    vocals_np
                )[:len(audio)]
                
                accomp_np = np.interp(
                    np.linspace(0, len(accomp_np) - 1, int(len(accomp_np) * factor))[:len(audio)],
                    np.arange(len(accomp_np)),
                    accomp_np
                )[:len(audio)]
            
            # Ensure same length as input
            if len(vocals_np) != len(audio):
                if len(vocals_np) > len(audio):
                    vocals_np = vocals_np[:len(audio)]
                    accomp_np = accomp_np[:len(audio)]
                else:
                    pad_len = len(audio) - len(vocals_np)
                    vocals_np = np.pad(vocals_np, (0, pad_len), mode='constant')
                    accomp_np = np.pad(accomp_np, (0, pad_len), mode='constant')
            
            # Normalize to prevent clipping
            max_val = max(np.abs(vocals_np).max(), np.abs(accomp_np).max())
            if max_val > 1.0:
                vocals_np = vocals_np / max_val * 0.95
                accomp_np = accomp_np / max_val * 0.95
            
            # Calculate confidence based on vocal energy ratio
            vocal_energy = np.mean(vocals_np ** 2)
            total_energy = vocal_energy + np.mean(accomp_np ** 2)
            confidence = (vocal_energy / total_energy) if total_energy > 0 else 0.5
            
            logger.info(f"Vocal separation complete - vocal confidence: {confidence:.2%}")
            
            return {
                "vocals": vocals_np,
                "accompaniment": accomp_np,
                "confidence": confidence
            }
            
        except Exception as e:
            logger.error(f"Error during vocal separation: {e}")
            # Return original audio as vocals as fallback
            return {
                "vocals": audio,
                "accompaniment": np.zeros_like(audio),
                "confidence": 0.0
            }


def separate_vocals_from_file(file_path: str, sample_rate: int = 16000, model_name: str = "htdemucs") -> dict:
    """
    Convenience function to separate vocals from an audio file.
    
    Args:
        file_path: Path to audio file
        sample_rate: Target sample rate for processing
        model_name: Demucs model name
    
    Returns:
        Dictionary with 'vocals', 'accompaniment', and 'confidence' keys
    """
    separator = VocalSeparator(model_name=model_name)
    
    # Load audio
    try:
        audio_tensor, sr = torchaudio.load(file_path)
        # Convert to mono
        if audio_tensor.shape[0] > 1:
            audio_tensor = audio_tensor.mean(dim=0, keepdim=True)
        
        # Resample if needed
        if sr != sample_rate:
            resampler = torchaudio.transforms.Resample(sr, sample_rate)
            audio_tensor = resampler(audio_tensor)
        
        audio_np = audio_tensor.squeeze().numpy()
    except Exception as e:
        logger.error(f"Failed to load audio file {file_path}: {e}")
        raise
    
    return separator.separate_vocals(audio_np, sample_rate)


if __name__ == "__main__":
    # Test example
    import sys
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
        if os.path.exists(test_file):
            result = separate_vocals_from_file(test_file)
            print(f"Separation complete!")
            print(f"Vocals shape: {result['vocals'].shape}")
            print(f"Accompaniment shape: {result['accompaniment'].shape}")
            print(f"Vocal confidence: {result['confidence']:.2%}")
        else:
            print(f"File not found: {test_file}")
    else:
        print("Usage: python source_separator.py <audio_file>")
