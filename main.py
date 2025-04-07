import sys
import time
import numpy as np
#import librosa
#import pyaudio
import wave
import scipy.fftpack

from led import led_setup, led_clear, blink, blink_fft, LEDS
from audio import load_file, get_processed_fft, async_play

def delay():
    print("File loaded, playing in")
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)

def main(audio_file: str):
    print(f"Reading {audio_file}")
    led_setup()
    audio, sample_rate = load_file(audio_file)
    audio_length = len(audio)

    delay()

    async_play(audio)
    block_size = 64
    for i in range(0, audio_length, block_size):
        audio_block = audio[i:i+block_size]
        fft_data = get_processed_fft(audio_block.get_array_of_samples(), sample_rate)
        blink_fft(fft_data)

def no_audio_file():
    print("No audio file specified, running test sequence.")
    from led_test import main as test
    test()

if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
        no_audio_file()
    except KeyboardInterrupt:
        led_clear()
