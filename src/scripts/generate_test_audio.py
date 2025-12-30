#!/usr/bin/env python
"""Generate test audio files for VOXENT pipeline"""

import numpy as np
import soundfile as sf
import os
from scipy import signal

def generate_test_audio(duration=3, gender="male", sr=16000):
    """Generate synthetic test audio with voice-like characteristics"""
    
    # Generate time array
    t = np.arange(int(sr * duration)) / sr
    
    if gender == "male":
        # Male voice: lower pitch (100-150 Hz fundamental)
        f0 = 120  # Fundamental frequency
    else:
        # Female voice: higher pitch (200-250 Hz fundamental)
        f0 = 220
    
    # Generate fundamental and harmonics
    signal_out = np.zeros_like(t)
    
    for harmonic in range(1, 6):
        freq = f0 * harmonic
        signal_out += (1.0 / harmonic) * np.sin(2 * np.pi * freq * t)
    
    # Add amplitude modulation (simulate speech)
    envelope = 0.3 + 0.3 * signal.sawtooth(2 * np.pi * 2 * t)
    signal_out = signal_out * envelope
    
    # Add background noise
    noise = 0.02 * np.random.randn(len(signal_out))
    signal_out = signal_out + noise
    
    # Normalize
    signal_out = signal_out / (np.max(np.abs(signal_out)) + 1e-7) * 0.9
    
    return signal_out.astype(np.float32)

# Create input directory
input_dir = "data/input"
os.makedirs(input_dir, exist_ok=True)

# Generate test audio files
print("\n" + "="*80)
print("GENERATING TEST AUDIO FILES")
print("="*80)

test_cases = [
    ("test_male_001.wav", "male", 3),
    ("test_female_001.wav", "female", 3),
    ("test_male_002.wav", "male", 2),
    ("test_female_002.wav", "female", 2),
    ("test_uncertain.wav", "male", 1.5),  # Short to test minimum duration
]

for filename, gender, duration in test_cases:
    filepath = os.path.join(input_dir, filename)
    
    # Skip if already exists
    if os.path.exists(filepath):
        print(f"  ✓ {filename} (already exists)")
        continue
    
    audio = generate_test_audio(duration, gender)
    sf.write(filepath, audio, 16000)
    print(f"  ✓ {filename} ({gender}, {duration}s)")

print(f"\n✅ Test audio files ready in {input_dir}")
print("="*80)
