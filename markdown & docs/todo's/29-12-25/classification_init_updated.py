"""
Updated classification/__init__.py
Integrates advanced multi-feature classifier with GPU support
"""

import os
import numpy as np
import logging
import torch
from typing import Tuple, Optional

# Try to import advanced classifier
try:
    from .advanced_gender_classifier import create_advanced_classifier
    ADVANCED_AVAILABLE = True
except ImportError:
    ADVANCED_AVAILABLE = False
    logging.warning("Advanced classifier not available, using fallback")

from .pitch_gender import PitchGenderClassifier
from .ml_classifier import MLGenderClassifier, load_ml_classifier

logger = logging.getLogger(__name__)

# Detect GPU
if torch.cuda.is_available():
    DEVICE = torch.device('cuda')
    logger.info(f"🚀 GPU detected: {torch.cuda.get_device_name(0)}")
    logger.info(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
else:
    DEVICE = torch.device('cpu')
    logger.warning("⚠️  GPU not available, using CPU")


class IntegratedGenderClassifier:
    """
    Integrated gender classifier with multiple methods:
    1. ML classifier (if trained) - highest priority
    2. Advanced multi-feature classifier (if available)
    3. Pitch-based classifier (fallback)
    
    With GPU acceleration support.
    """

    def __init__(self, use_ml: bool = True, ml_model_path: str = "models/ml_gender_classifier.pkl",
                 pitch_male_threshold: float = 85.0, pitch_female_threshold: float = 165.0,
                 use_advanced: bool = True):
        """
        Initialize integrated classifier.

        Args:
            use_ml: Whether to use ML classifier (if available)
            ml_model_path: Path to trained ML model
            pitch_male_threshold: Pitch threshold for male classification
            pitch_female_threshold: Pitch threshold for female classification
            use_advanced: Whether to use advanced multi-feature classifier
        """
        self.use_ml = use_ml
        self.use_advanced = use_advanced
        self.ml_model_path = ml_model_path
        self.device = DEVICE
        
        # Initialize classifiers
        self.pitch_classifier = PitchGenderClassifier(pitch_male_threshold, pitch_female_threshold)
        self.ml_classifier = None
        self.advanced_classifier = None

        # Try to load ML classifier
        if self.use_ml:
            try:
                if os.path.exists(self.ml_model_path):
                    self.ml_classifier = load_ml_classifier(self.ml_model_path)
                    logger.info(f"✅ ML classifier loaded from {self.ml_model_path}")
                else:
                    logger.info(f"ℹ️  ML model not found at {self.ml_model_path}")
            except Exception as e:
                logger.warning(f"Failed to load ML classifier: {e}")

        # Try to load advanced classifier
        if self.use_advanced and ADVANCED_AVAILABLE:
            try:
                self.advanced_classifier = create_advanced_classifier()
                logger.info("✅ Advanced multi-feature classifier loaded")
            except Exception as e:
                logger.warning(f"Failed to load advanced classifier: {e}")

    def classify(self, audio: np.ndarray, sr: int) -> Tuple[str, float]:
        """
        Classify gender using best available method.

        Priority:
        1. ML classifier (if available and trained)
        2. Advanced multi-feature classifier (if available)
        3. Pitch-based classifier (fallback)

        Returns:
            Tuple of (gender_label, confidence_score)
        """
        
        # Method 1: Try ML classification first (if trained)
        if self.ml_classifier and self.ml_classifier.is_trained:
            try:
                # Resample audio if necessary
                if sr != self.ml_classifier.sample_rate:
                    import librosa
                    audio_resampled = librosa.resample(audio, orig_sr=sr, target_sr=self.ml_classifier.sample_rate)
                else:
                    audio_resampled = audio

                ml_label, ml_confidence = self.ml_classifier.predict(audio_resampled)

                # If ML confidence is high, use it
                if ml_confidence >= 70.0:
                    logger.debug(f"ML classification: {ml_label} with confidence {ml_confidence:.1f}%")
                    return ml_label, ml_confidence
                else:
                    logger.debug(f"ML confidence too low ({ml_confidence:.1f}%), trying advanced classifier")

            except Exception as e:
                logger.warning(f"ML classification failed: {e}, falling back")

        # Method 2: Try advanced multi-feature classifier
        if self.advanced_classifier:
            try:
                adv_label, adv_confidence = self.advanced_classifier.classify(audio, sr)
                
                if adv_confidence >= 60.0:
                    logger.debug(f"Advanced classification: {adv_label} with confidence {adv_confidence:.1f}%")
                    return adv_label, adv_confidence
                else:
                    logger.debug(f"Advanced confidence too low ({adv_confidence:.1f}%), falling back to pitch")

            except Exception as e:
                logger.warning(f"Advanced classification failed: {e}, falling back to pitch")

        # Method 3: Fall back to pitch-based classification
        pitch_label, pitch_confidence = self.pitch_classifier.classify(audio, sr)
        logger.debug(f"Pitch classification: {pitch_label} with confidence {pitch_confidence:.1f}%")
        return pitch_label, pitch_confidence

    def classify_batch(self, audio_batch: list, sr: int) -> list:
        """
        Classify multiple audio samples (GPU-accelerated if available).
        
        Args:
            audio_batch: List of audio arrays
            sr: Sample rate
            
        Returns:
            List of (label, confidence) tuples
        """
        if self.device.type == 'cuda' and len(audio_batch) > 1:
            logger.info(f"🚀 GPU batch classification: {len(audio_batch)} samples")
            
            # Use ML classifier for batch if available
            if self.ml_classifier and self.ml_classifier.is_trained:
                try:
                    results = []
                    for audio in audio_batch:
                        result = self.ml_classifier.predict(audio)
                        results.append(result)
                    return results
                except Exception as e:
                    logger.warning(f"Batch ML classification failed: {e}")
        
        # Fallback: Process individually
        results = []
        for audio in audio_batch:
            result = self.classify(audio, sr)
            results.append(result)
        
        return results

    def is_ml_available(self) -> bool:
        """Check if ML classifier is available and trained."""
        return self.ml_classifier is not None and self.ml_classifier.is_trained

    def is_advanced_available(self) -> bool:
        """Check if advanced classifier is available."""
        return self.advanced_classifier is not None

    def get_classifier_info(self) -> dict:
        """Get information about available classifiers."""
        return {
            "device": str(self.device),
            "ml_available": self.is_ml_available(),
            "advanced_available": self.is_advanced_available(),
            "ml_model_path": self.ml_model_path if self.is_ml_available() else None,
            "pitch_thresholds": {
                "male": self.pitch_classifier.male_threshold,
                "female": self.pitch_classifier.female_threshold
            },
            "classification_priority": self._get_priority_list()
        }
    
    def _get_priority_list(self) -> list:
        """Get list of classifiers in priority order."""
        priority = []
        if self.is_ml_available():
            priority.append("ML Classifier (trained)")
        if self.is_advanced_available():
            priority.append("Advanced Multi-Feature Classifier")
        priority.append("Pitch-Based Classifier (fallback)")
        return priority


def create_classifier(config: dict) -> IntegratedGenderClassifier:
    """Factory function to create classifier from configuration."""
    use_ml = config.get('classification', {}).get('use_ml', True)
    ml_model_path = config.get('classification', {}).get('ml_model_path', 'models/ml_gender_classifier.pkl')
    pitch_male_threshold = config.get('classification', {}).get('pitch_male_threshold', 85.0)
    pitch_female_threshold = config.get('classification', {}).get('pitch_female_threshold', 165.0)
    use_advanced = config.get('classification', {}).get('use_advanced', True)

    return IntegratedGenderClassifier(
        use_ml=use_ml,
        ml_model_path=ml_model_path,
        pitch_male_threshold=pitch_male_threshold,
        pitch_female_threshold=pitch_female_threshold,
        use_advanced=use_advanced
    )


# Global classifier instance
_classifier_instance = None

def get_classifier(config: dict = None) -> IntegratedGenderClassifier:
    """Get or create global classifier instance."""
    global _classifier_instance

    if _classifier_instance is None:
        if config is None:
            # Default configuration
            config = {
                'classification': {
                    'use_ml': True,
                    'ml_model_path': 'models/ml_gender_classifier.pkl',
                    'pitch_male_threshold': 85.0,
                    'pitch_female_threshold': 165.0,
                    'use_advanced': True
                }
            }
        _classifier_instance = create_classifier(config)
        
        # Log classifier info
        info = _classifier_instance.get_classifier_info()
        logger.info(f"Classifier initialized on {info['device']}")
        logger.info(f"Classification priority: {' → '.join(info['classification_priority'])}")

    return _classifier_instance
