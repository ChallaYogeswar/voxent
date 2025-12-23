import unittest
import os
import tempfile
import shutil
import numpy as np
from preprocessing.audio_loader import load_audio
from preprocessing.normalize import normalize
from classification.pitch_gender import estimate_pitch

class TestPipeline(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
        self.sample_rate = 16000

        # Create a simple test audio signal (1 second of 440Hz sine wave)
        duration = 1.0
        frequency = 440.0
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        self.test_audio = np.sin(frequency * 2 * np.pi * t).astype(np.float32)

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_audio_loading(self):
        """Test audio loading functionality."""
        # This would require actual audio files, so we'll skip for now
        pass

    def test_normalize(self):
        """Test audio normalization."""
        normalized = normalize(self.test_audio)
        self.assertIsInstance(normalized, np.ndarray)
        # Check that values are within [-1, 1]
        self.assertTrue(np.all(normalized >= -1.0))
        self.assertTrue(np.all(normalized <= 1.0))

    def test_pitch_estimation(self):
        """Test pitch estimation."""
        pitch = estimate_pitch(self.test_audio, self.sample_rate)
        self.assertIsInstance(pitch, (int, float))
        self.assertGreater(pitch, 0)

    def test_config_validation(self):
        """Test configuration validation."""
        from engine.batch_runner import validate_config

        # Valid config
        valid_config = {
            'sample_rate': 16000,
            'min_segment_duration': 1.0,
            'male_pitch_threshold': 165,
            'female_pitch_threshold': 255,
            'confidence_margin': 20
        }
        self.assertTrue(validate_config(valid_config))

        # Invalid config - missing key
        invalid_config = valid_config.copy()
        del invalid_config['sample_rate']
        with self.assertRaises(ValueError):
            validate_config(invalid_config)

        # Invalid config - negative sample rate
        invalid_config = valid_config.copy()
        invalid_config['sample_rate'] = -1
        with self.assertRaises(ValueError):
            validate_config(invalid_config)

if __name__ == '__main__':
    unittest.main()
