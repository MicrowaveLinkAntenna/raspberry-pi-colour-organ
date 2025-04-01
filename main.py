import sys
import numpy as np
#import librosa
#import pyaudio
import wave
import scipy.fftpack
import pydub.playback

from led import led_setup, led_clear, blink, LEDS
from audio import load_file, fft

def main(audio_file: str):
    print(f"Reading {audio_file}")
    led_setup(LEDS)
    audio, sample_rate = load_file(audio_file)
    audio_length = len(audio)
    block_size = 1024
    for i in range(0, audio_length, block_size):
        audio_block = audio[i:i+block_size]
        print(fft(audio_block, sample_rate))

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
        led_clear(LEDS)
