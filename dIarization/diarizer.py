import os
from pyannote.audio import Pipeline

token = os.getenv("HF_TOKEN")
if not token:
    raise ValueError("HF_TOKEN environment variable is required for pyannote/speaker-diarization. Please set it with your Hugging Face token.")
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-community-1", token=token)

def diarize(audio_path):
    diarization = pipeline(audio_path)
    segments = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        segments.append({
            "start": turn.start,
            "end": turn.end,
            "speaker": speaker
        })
    return segments
