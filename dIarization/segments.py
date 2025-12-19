import soundfile as sf

def extract_segment(audio, sr, start, end):
    return audio[int(start*sr):int(end*sr)]
