import numpy as np
import librosa

def load_file(path: str):
    return librosa.load(path)

