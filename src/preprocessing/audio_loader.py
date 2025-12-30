import librosa

def load_audio(path, sr):
    audio, _ = librosa.load(path, sr=sr, mono=True)
    return audio
