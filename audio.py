import math
import threading
import numpy as np
from pydub import AudioSegment
from pydub.playback import play

# Everything higher than this value will be grouped together
# Prevents the amplitudes of the highest frequencies from always being 0
FREQUENCY_SECOND_HIGHEST_CUTOFF = 20000

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

def highest_frequency(fft_data) -> float:
    result = 0
    for amplitude, frequency in zip(fft_data[0], fft_data[1]):
        if amplitude > 0 and frequency > result:
            result = frequency
    return result

def create_frequency_ranges(fft_data, number_of_ranges: int, cutoff: int = FREQUENCY_SECOND_HIGHEST_CUTOFF) -> list[tuple[int, int]]:
    result = []
    fft_amplitudes, fft_frequencies = fft_data
    sorted_frequencies = np.sort(fft_frequencies)
    length = len(fft_frequencies)
    min = sorted_frequencies[0]
    max = highest_frequency(fft_data)
    range_size = cutoff / (number_of_ranges - 1)
    for i in range(number_of_ranges):
        if 1 != number_of_ranges - 1:
            result.append((float(range_size*i), float(range_size*(i+1))))
        else:
            result.append((cutoff, max))

    return result

def fft_split(fft_data: tuple, number_of_ranges: int) -> dict:
    frequency_ranges = create_frequency_ranges(fft_data, number_of_ranges)
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
