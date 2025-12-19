import librosa

def remove_silence(audio, sr):
    intervals = librosa.effects.split(audio, top_db=30)
    return [audio[start:end] for start, end in intervals]
