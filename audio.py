import numpy as np
from pydub import AudioSegment

FREQUENCIES = (
    (4000, 20000),
    (2000, 4000),
    (500, 2000),
    (250, 500),
    (20, 250)
)

def load_file(path: str):
    audio = AudioSegment.from_file(path).set_channels(1)
    return audio.get_array_of_samples(), audio.frame_rate

def fft(audio, sample_rate):
    samples = len(audio)
    period = 1/sample_rate
    return np.fft.fft(audio)
