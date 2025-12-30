import os
import pandas as pd
import soundfile as sf
import numpy as np
from pydub import AudioSegment
from pydub.playback import play

def play_audio(file_path):
    """Play audio file using pydub."""
    audio = AudioSegment.from_wav(file_path)
    play(audio)

def manual_verification(dataset_dir):
    """Manual verification interface for classified samples."""
    metadata_path = os.path.join(dataset_dir, "metadata.csv")

    if not os.path.exists(metadata_path):
        print("No metadata file found. Run the pipeline first.")
        return

    df = pd.read_csv(metadata_path)

    print("Manual Verification Interface")
    print("=" * 40)

    for idx, row in df.iterrows():
        file_path = os.path.join(dataset_dir, row['label'], row['file'])

        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue

        print(f"\nSample {idx + 1}/{len(df)}")
        print(f"File: {row['file']}")
        print(f"Current label: {row['label']}")
        print(f"Confidence: {row['confidence']:.2f}")
        print(f"Duration: {row['duration']:.2f}s")

        # Play audio
        input("Press Enter to play audio...")
        try:
            play_audio(file_path)
        except Exception as e:
            print(f"Could not play audio: {e}")

        # Get user input
        while True:
            choice = input("Correct label (m/f/u/skip)? ").lower().strip()
            if choice in ['m', 'f', 'u', 'skip']:
                break
            print("Invalid choice. Use m/f/u/skip")

        if choice == 'skip':
            continue

        # Update label
        new_label = {'m': 'male', 'f': 'female', 'u': 'uncertain'}[choice]

        if new_label != row['label']:
            # Move file to correct directory
            old_path = file_path
            new_path = os.path.join(dataset_dir, new_label, row['file'])

            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            os.rename(old_path, new_path)

            # Update metadata
            df.at[idx, 'label'] = new_label
            df.at[idx, 'verified'] = True

            print(f"Updated label from {row['label']} to {new_label}")
        else:
            df.at[idx, 'verified'] = True
            print("Label confirmed")

    # Save updated metadata
    df.to_csv(metadata_path, index=False)
    print(f"\nVerification complete. Updated metadata saved to {metadata_path}")

if __name__ == "__main__":
    manual_verification("data/voice_dataset")
