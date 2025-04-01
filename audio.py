import math
import threading
import numpy as np
from pydub import AudioSegment
from pydub.playback import play

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

def frequency_in_range(frequency: float, frequencies: tuple[int, int]):
    for frequency_range in frequencies:
        if frequency_range[0] <= frequency <= frequency_range[1]:
            return frequency_range
    return (0, 0)

def create_frequency_ranges(fft_frequencies, number_of_ranges: int) -> list[tuple[int, int]]:
    result = []
    sorted_frequencies = np.sort(fft_frequencies)
    length = len(fft_frequencies)
    max = sorted_frequencies[-1]
    min = sorted_frequencies[0]
    range_size = (max - min) / number_of_ranges
    for i in range(number_of_ranges):
        result.append((float(range_size*i), float(range_size*(i+1))))
    print(result)
    return result

def fft_split(fft_data: tuple, number_of_ranges: int) -> dict:
    frequency_ranges = create_frequency_ranges(fft_data[1], number_of_ranges)
    frequency_amplitudes = {frequency: [] for frequency in frequency_ranges}

    for amplitude, frequency in zip(fft_data[0], fft_data[1]):
        if amplitude != np.float64(np.inf):
            frequency_range = frequency_in_range(frequency, frequency_ranges)
            if frequency_range != (0, 0):
                frequency_amplitudes[frequency_range].append(amplitude)
    return frequency_amplitudes

def float_or_zero(value: np.float64):
    result = float(value)
    return 0 if math.isnan(result) else result

def fft_split_average(fft_split_data: dict):
    result = {}
    for frequency, amplitudes in fft_split_data.items():
        average = np.mean(amplitudes)
        result[frequency] = float_or_zero(average)
    total_average = np.mean(list(result.values()))

    return result, float_or_zero(total_average)

def async_play(audio):
    audio_thread = threading.Thread(target=play, args=(audio,))
    audio_thread.start()
