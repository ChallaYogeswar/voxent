import numpy as np

def normalize(audio):
    peak = np.max(np.abs(audio))
    return audio if peak == 0 else audio / peak
