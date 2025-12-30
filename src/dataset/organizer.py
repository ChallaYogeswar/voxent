import os
import soundfile as sf
import json
import logging

logger = logging.getLogger(__name__)

COUNTER_FILE = "data/voice_dataset/.counter.json"

def get_next_counter():
    """Get next sequential file number."""
    try:
        if os.path.exists(COUNTER_FILE):
            with open(COUNTER_FILE, 'r') as f:
                data = json.load(f)
                counter = data.get('counter', 0) + 1
        else:
            counter = 1
        
        # Create directory if needed
        os.makedirs(os.path.dirname(COUNTER_FILE), exist_ok=True)
        
        with open(COUNTER_FILE, 'w') as f:
            json.dump({'counter': counter}, f)
        
        return counter
    except Exception as e:
        logger.warning(f"Error managing counter: {e}")
        return 1

def save_sample(audio, sr, label, filename, base_path):
    """Save sample with sequential naming convention."""
    counter = get_next_counter()
    new_filename = f"voice_sample_{counter:04d}.wav"
    
    path = os.path.join(base_path, label)
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, new_filename)
    sf.write(file_path, audio, sr)
    
    logger.debug(f"Saved: {label}/{new_filename} (source: {filename})")
    
    # Return both new filename and original for metadata tracking
    return new_filename, filename

def save_sample_with_counter(audio, sr, label, base_path, original_filename=""):
    """Save sample with sequential naming and metadata tracking."""
    counter = get_next_counter()
    new_filename = f"voice_sample_{counter:04d}.wav"
    
    path = os.path.join(base_path, label)
    os.makedirs(path, exist_ok=True)
    file_path = os.path.join(path, new_filename)
    sf.write(file_path, audio, sr)
    
    logger.debug(f"Saved: {new_filename} ({label})")
    
    return {
        "new_filename": new_filename,
        "original_filename": original_filename,
        "label": label,
        "counter": counter,
        "file_path": file_path
    }

def reset_counter():
    """Reset the counter (use with caution!)."""
    try:
        if os.path.exists(COUNTER_FILE):
            os.remove(COUNTER_FILE)
        logger.info("Counter reset to 0")
    except Exception as e:
        logger.error(f"Failed to reset counter: {e}")

def get_current_counter():
    """Get current counter value without incrementing."""
    try:
        if os.path.exists(COUNTER_FILE):
            with open(COUNTER_FILE, 'r') as f:
                data = json.load(f)
                return data.get('counter', 0)
        return 0
    except Exception as e:
        logger.warning(f"Error reading counter: {e}")
        return 0
