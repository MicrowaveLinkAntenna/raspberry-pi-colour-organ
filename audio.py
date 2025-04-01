import math
import numpy as np
from pydub import AudioSegment

FREQUENCIES = (
    (4000, 20000),
    (2000, 4000),
    (500, 2000),
    (250, 500),
    (20, 250),
    (0, 0) # Placeholder for frequencies out of range to prevent index errors
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

def frequency_in_range(frequency: float, frequencies: tuple = FREQUENCIES):
    for frequency_range in frequencies:
        if frequency_range[0] <= frequency <= frequency_range[1]:
            return frequency_range
    return (0, 0)

def fft_split(fft_data: tuple, frequencies: tuple = FREQUENCIES) -> dict:
    frequency_ranges = {frequency: [] for frequency in frequencies}

    for amplitude, frequency in zip(fft_data[0], fft_data[1]):
        if amplitude != np.float64(np.inf):
            frequency_ranges[frequency_in_range(frequency, frequencies)].append(amplitude)
    return frequency_ranges

def float_or_zero(value: np.float64):
    result = float(value)
    return 0 if math.isnan(result) else result

def fft_split_average(fft_split_data: dict):
    result = {}
    for frequency, amplitudes in fft_split_data.items():
        average = np.mean(amplitudes)
        result[frequency] = float_or_zero(average)
    total_average = np.mean(list(result.values()))
    result["Total"] = float_or_zero(total_average)

    return result

