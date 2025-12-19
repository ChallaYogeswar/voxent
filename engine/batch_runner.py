import os
import yaml
from preprocessing.audio_loader import load_audio
from preprocessing.normalize import normalize
from preprocessing.vad import remove_silence
from dIarization.diarizer import diarize
from dIarization.segments import extract_segment
from classification.pitch_gender import estimate_pitch
from classification.confidence import classify_pitch
from dataset.organizer import save_sample
from dataset.metadata import append_metadata

def run(config_path):
    cfg = yaml.safe_load(open(config_path))
    input_dir = "data/input_calls"
    dataset_dir = "data/voice_dataset"

    for file in os.listdir(input_dir):
        if not file.endswith(".wav"):
            continue

        audio_path = os.path.join(input_dir, file)
        audio = load_audio(audio_path, cfg["sample_rate"])
        audio = normalize(audio)

        segments = diarize(audio_path)

        for i, seg in enumerate(segments):
            clip = extract_segment(audio, cfg["sample_rate"], seg["start"], seg["end"])
            pitch = estimate_pitch(clip, cfg["sample_rate"])
            label, conf = classify_pitch(
                pitch,
                cfg["male_pitch_threshold"],
                cfg["female_pitch_threshold"]
            )

            name = f"{file}_spk{i}_conf{int(conf)}.wav"
            save_sample(clip, cfg["sample_rate"], label, name, dataset_dir)

            append_metadata(
                os.path.join(dataset_dir, "metadata.csv"),
                {
                    "file": name,
                    "source": file,
                    "speaker": seg["speaker"],
                    "pitch": pitch,
                    "label": label,
                    "confidence": conf,
                    "duration": len(clip)/cfg["sample_rate"]
                }
            )
