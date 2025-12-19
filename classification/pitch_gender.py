import librosa
import numpy as np

def estimate_pitch(audio, sr):
    pitches, mags = librosa.piptrack(y=audio, sr=sr)
    pitch_values = pitches[mags > np.median(mags)]
    return np.mean(pitch_values) if len(pitch_values) else 0
