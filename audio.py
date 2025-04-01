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
    return audio, audio.frame_rate

def positive_frequencies(frequencies, samples: int):
    """
    Returns the positive frequencies.
    :return: The first half of the fft_frequencies
    """
    half_samples = samples//2
    return frequencies[:half_samples]

def sample_count(audio):
    return len(audio)

def period(sample_rate: int):
    return 1/sample_rate

def fft(audio, sample_rate: int, samples: int):
    fft_result = np.fft.fft(audio)
    fft_frequencies = np.fft.fftfreq(samples, period(sample_rate))
    return fft_result, fft_frequencies

def fft_normalize(fft_result, samples: int):
    absolute_values = np.abs(fft_result)
    fft_scaled = 1/(samples*absolute_values)
    return 2*fft_scaled

def get_processed_fft(audio, sample_rate: int):
    samples = sample_count(audio)
    fft_result, fft_frequencies = fft(audio, sample_rate, samples)
    fft_normalized = fft_normalize(fft_result, samples)
    return fft_normalized, fft_frequencies

