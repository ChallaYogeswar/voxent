"""
Advanced Gender Classification for VOXENT
Uses multiple acoustic features instead of pitch alone

This fixes the critical limitation of pitch-only classification.
"""

import numpy as np
import librosa
import logging
from typing import Tuple, Dict

logger = logging.getLogger(__name__)

# Try to import Parselmouth for advanced formant extraction
try:
    import parselmouth
    from parselmouth.praat import call
    PARSELMOUTH_AVAILABLE = True
except ImportError:
    PARSELMOUTH_AVAILABLE = False
    logger.warning("Parselmouth not available. Install with: pip install praat-parselmouth")

from scipy.signal import find_peaks


class MultiFeatureGenderClassifier:
    """Advanced gender classifier using multiple acoustic features."""
    
    def __init__(self):
        self.feature_weights = {
            'pitch': 0.20,
            'formants': 0.30,
            'spectral': 0.20,
            'mfcc': 0.15,
            'hnr': 0.15
        }
    
    def extract_formants(self, audio: np.ndarray, sr: int) -> Tuple[float, float, float]:
        """
        Extract formant frequencies (F1, F2, F3).
        Formants are vocal tract resonances - more reliable than pitch.
        """
        try:
            if not PARSELMOUTH_AVAILABLE:
                return self._estimate_formants_fallback(audio, sr)
            
            # Use Parselmouth (Praat interface) for formant extraction
            sound = parselmouth.Sound(audio, sampling_frequency=sr)
            
            # Extract formants
            formant = call(sound, "To Formant (burg)", 0.0, 5, 5500, 0.025, 50)
            
            # Get mean formants
            f1_list = []
            f2_list = []
            f3_list = []
            
            duration = sound.duration
            num_frames = int(duration / 0.01)  # 10ms frames
            
            for i in range(1, num_frames):
                try:
                    f1 = call(formant, "Get value at time", 1, i * 0.01)
                    f2 = call(formant, "Get value at time", 2, i * 0.01)
                    f3 = call(formant, "Get value at time", 3, i * 0.01)
                    
                    if not np.isnan(f1) and f1 > 0:
                        f1_list.append(f1)
                    if not np.isnan(f2) and f2 > 0:
                        f2_list.append(f2)
                    if not np.isnan(f3) and f3 > 0:
                        f3_list.append(f3)
                except:
                    pass
            
            f1_mean = np.mean(f1_list) if f1_list else 0
            f2_mean = np.mean(f2_list) if f2_list else 0
            f3_mean = np.mean(f3_list) if f3_list else 0
            
            return f1_mean, f2_mean, f3_mean
            
        except Exception as e:
            logger.warning(f"Formant extraction failed: {e}, using fallback")
            return self._estimate_formants_fallback(audio, sr)
    
    def _estimate_formants_fallback(self, audio: np.ndarray, sr: int) -> Tuple[float, float, float]:
        """Fallback formant estimation using LPC."""
        from scipy.signal import lfilter
        
        # Pre-emphasis
        pre_emphasis = 0.97
        emphasized = np.append(audio[0], audio[1:] - pre_emphasis * audio[:-1])
        
        # LPC analysis
        order = 12
        a = librosa.lpc(emphasized, order=order)
        
        # Find formants from LPC roots
        roots = np.roots(a)
        roots = roots[np.imag(roots) >= 0]
        
        # Convert to frequencies
        angles = np.arctan2(np.imag(roots), np.real(roots))
        freqs = sorted(angles * (sr / (2 * np.pi)))
        
        # Return first 3 formants
        formants = [f for f in freqs if 90 < f < 5000][:3]
        
        while len(formants) < 3:
            formants.append(0)
        
        return tuple(formants[:3])
    
    def calculate_harmonic_to_noise_ratio(self, audio: np.ndarray, sr: int) -> float:
        """
        Calculate Harmonics-to-Noise Ratio (HNR).
        Higher HNR = clearer, more periodic voice (typically higher in females).
        """
        try:
            if not PARSELMOUTH_AVAILABLE:
                return self._estimate_hnr_fallback(audio, sr)
            
            sound = parselmouth.Sound(audio, sampling_frequency=sr)
            harmonicity = call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
            hnr = call(harmonicity, "Get mean", 0, 0)
            return hnr if not np.isnan(hnr) else 0
        except Exception as e:
            logger.warning(f"HNR calculation failed: {e}")
            return self._estimate_hnr_fallback(audio, sr)
    
    def _estimate_hnr_fallback(self, audio: np.ndarray, sr: int) -> float:
        """Fallback: Estimate HNR from autocorrelation."""
        autocorr = np.correlate(audio, audio, mode='full')
        autocorr = autocorr[len(autocorr)//2:]
        
        # Find peaks
        peaks, _ = find_peaks(autocorr, height=0)
        
        if len(peaks) > 1:
            harmonic_power = autocorr[peaks[0]]
            noise_power = np.sum(autocorr) - harmonic_power
            hnr = 10 * np.log10(harmonic_power / (noise_power + 1e-10))
            return hnr if not np.isnan(hnr) else 0
        
        return 0
    
    def extract_all_features(self, audio: np.ndarray, sr: int) -> Dict[str, float]:
        """Extract comprehensive voice features."""
        
        # 1. PITCH FEATURES
        pitches, magnitudes = librosa.piptrack(y=audio, sr=sr, fmin=75, fmax=400)
        pitch_values = pitches[magnitudes > np.max(magnitudes) * 0.1]
        pitch_mean = np.mean(pitch_values[pitch_values > 0]) if len(pitch_values) > 0 else 0
        pitch_std = np.std(pitch_values[pitch_values > 0]) if len(pitch_values) > 0 else 0
        
        # 2. FORMANT FEATURES (MOST IMPORTANT!)
        f1, f2, f3 = self.extract_formants(audio, sr)
        
        # 3. SPECTRAL FEATURES
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio, sr=sr))
        spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=audio, sr=sr))
        spectral_bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=audio, sr=sr))
        
        # 4. MFCC FEATURES (Voice texture)
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
        mfcc_mean = np.mean(mfcc, axis=1)
        
        # 5. VOICE QUALITY
        zcr = np.mean(librosa.feature.zero_crossing_rate(audio))
        hnr = self.calculate_harmonic_to_noise_ratio(audio, sr)
        
        return {
            'pitch_mean': pitch_mean,
            'pitch_std': pitch_std,
            'formant_f1': f1,
            'formant_f2': f2,
            'formant_f3': f3,
            'spectral_centroid': spectral_centroid,
            'spectral_rolloff': spectral_rolloff,
            'spectral_bandwidth': spectral_bandwidth,
            'mfcc_mean_0': mfcc_mean[0] if len(mfcc_mean) > 0 else 0,
            'mfcc_mean_1': mfcc_mean[1] if len(mfcc_mean) > 1 else 0,
            'mfcc_mean_2': mfcc_mean[2] if len(mfcc_mean) > 2 else 0,
            'zero_crossing_rate': zcr,
            'hnr': hnr
        }
    
    def classify_by_rules(self, features: Dict[str, float]) -> Tuple[str, float]:
        """
        Rule-based classification using multiple features.
        More robust than pitch alone.
        """
        
        # Initialize scores
        male_score = 0.0
        female_score = 0.0
        
        # 1. PITCH SCORING (20% weight)
        pitch = features['pitch_mean']
        if pitch > 0:
            if pitch < 120:
                male_score += 0.20 * 0.8
                female_score += 0.20 * 0.2
            elif pitch > 180:
                male_score += 0.20 * 0.2
                female_score += 0.20 * 0.8
            elif 120 <= pitch < 155:
                male_score += 0.20 * 0.6
                female_score += 0.20 * 0.4
            elif 165 <= pitch <= 180:
                male_score += 0.20 * 0.3
                female_score += 0.20 * 0.7
            else:
                male_score += 0.20 * 0.5
                female_score += 0.20 * 0.5
        
        # 2. FORMANT SCORING (30% weight) - MOST RELIABLE!
        f1 = features['formant_f1']
        f2 = features['formant_f2']
        
        if f1 > 0 and f2 > 0:
            # Male typical: F1~500Hz, F2~1500Hz
            # Female typical: F1~650Hz, F2~1850Hz
            
            # F1 distance scoring
            f1_male_dist = abs(f1 - 500)
            f1_female_dist = abs(f1 - 650)
            
            if f1_male_dist < f1_female_dist:
                male_score += 0.30 * (1 - f1_male_dist / 500)
                female_score += 0.30 * 0.2
            else:
                male_score += 0.30 * 0.2
                female_score += 0.30 * (1 - f1_female_dist / 500)
            
            # F2 distance scoring
            f2_male_dist = abs(f2 - 1500)
            f2_female_dist = abs(f2 - 1850)
            
            if f2_male_dist < f2_female_dist:
                male_score += 0.30 * (1 - f2_male_dist / 1500)
                female_score += 0.30 * 0.2
            else:
                male_score += 0.30 * 0.2
                female_score += 0.30 * (1 - f2_female_dist / 1850)
        
        # 3. SPECTRAL FEATURES (20% weight)
        spectral_centroid = features['spectral_centroid']
        if spectral_centroid > 0:
            # Females typically have higher spectral centroid
            if spectral_centroid < 2000:
                male_score += 0.20 * 0.7
                female_score += 0.20 * 0.3
            elif spectral_centroid > 3000:
                male_score += 0.20 * 0.3
                female_score += 0.20 * 0.7
            else:
                male_score += 0.20 * 0.5
                female_score += 0.20 * 0.5
        
        # 4. HNR (15% weight)
        hnr = features['hnr']
        if hnr > 0:
            # Higher HNR often indicates female voice
            if hnr > 10:
                male_score += 0.15 * 0.3
                female_score += 0.15 * 0.7
            elif hnr < 5:
                male_score += 0.15 * 0.7
                female_score += 0.15 * 0.3
            else:
                male_score += 0.15 * 0.5
                female_score += 0.15 * 0.5
        
        # 5. MFCC (15% weight)
        mfcc_0 = features['mfcc_mean_0']
        if abs(mfcc_0) > 0:
            # MFCC coefficient patterns differ by gender
            if mfcc_0 < -50:
                male_score += 0.15 * 0.6
                female_score += 0.15 * 0.4
            elif mfcc_0 > -30:
                male_score += 0.15 * 0.4
                female_score += 0.15 * 0.6
            else:
                male_score += 0.15 * 0.5
                female_score += 0.15 * 0.5
        
        # Calculate confidence and label
        total_score = male_score + female_score
        
        if total_score > 0:
            male_confidence = (male_score / total_score) * 100
            female_confidence = (female_score / total_score) * 100
            
            if male_score > female_score:
                return "male", male_confidence
            else:
                return "female", female_confidence
        else:
            return "uncertain", 50.0
    
    def classify(self, audio: np.ndarray, sr: int) -> Tuple[str, float]:
        """
        Main classification method.
        Uses multiple features for robust classification.
        """
        try:
            # Extract all features
            features = self.extract_all_features(audio, sr)
            
            # Classify using rules
            label, confidence = self.classify_by_rules(features)
            
            logger.debug(f"Advanced classification: {label} ({confidence:.1f}%)")
            logger.debug(f"Features - Pitch: {features['pitch_mean']:.1f}Hz, F1: {features['formant_f1']:.1f}Hz, F2: {features['formant_f2']:.1f}Hz")
            
            return label, confidence
            
        except Exception as e:
            logger.error(f"Advanced classification error: {e}")
            return "uncertain", 50.0


# Fallback: If Parselmouth not available, use simplified version
class SimplifiedMultiFeatureClassifier:
    """Simplified version without Praat dependencies."""
    
    def __init__(self):
        pass
    
    def classify(self, audio: np.ndarray, sr: int) -> Tuple[str, float]:
        """Classify using pitch + spectral features only."""
        
        # Extract basic features
        pitches, magnitudes = librosa.piptrack(y=audio, sr=sr)
        pitch_values = pitches[magnitudes > np.max(magnitudes) * 0.1]
        pitch_mean = np.mean(pitch_values[pitch_values > 0]) if len(pitch_values) > 0 else 0
        
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio, sr=sr))
        
        # Simple scoring
        male_score = 0
        female_score = 0
        
        # Pitch scoring
        if pitch_mean < 140:
            male_score += 2
        elif pitch_mean > 180:
            female_score += 2
        else:
            male_score += 1
            female_score += 1
        
        # Spectral scoring
        if spectral_centroid < 2000:
            male_score += 1
        else:
            female_score += 1
        
        # Determine result
        total = male_score + female_score
        if male_score > female_score * 1.3:
            return "male", (male_score / total) * 100
        elif female_score > male_score * 1.3:
            return "female", (female_score / total) * 100
        else:
            return "uncertain", 50.0


# Auto-select best classifier
def create_advanced_classifier():
    """Create the best available classifier."""
    try:
        if PARSELMOUTH_AVAILABLE:
            logger.info("Using MultiFeatureGenderClassifier (with formants)")
            return MultiFeatureGenderClassifier()
    except ImportError:
        pass
    
    logger.warning("Using SimplifiedMultiFeatureClassifier (pitch + spectral only)")
    logger.warning("Install parselmouth-python for better accuracy: pip install praat-parselmouth")
    return SimplifiedMultiFeatureClassifier()


if __name__ == "__main__":
    import soundfile as sf
    
    classifier = create_advanced_classifier()
    
    # Test with sample audio if available
    try:
        audio, sr = sf.read("test.wav")
        label, confidence = classifier.classify(audio, sr)
        print(f"Classification: {label} ({confidence:.1f}% confidence)")
    except FileNotFoundError:
        print("No test.wav file found. Classifier ready for use.")
