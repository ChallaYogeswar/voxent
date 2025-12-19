import os
import soundfile as sf

def save_sample(audio, sr, label, filename, base_path):
    path = os.path.join(base_path, label)
    os.makedirs(path, exist_ok=True)
    sf.write(os.path.join(path, filename), audio, sr)
