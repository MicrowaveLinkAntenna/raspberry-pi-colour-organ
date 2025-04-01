import sys
import numpy as np
#import librosa
#import pyaudio
import wave
import scipy.fftpack

from led import led_setup, led_clear, blink, LEDS
from audio import load_file

def main(audio_file: str):
    print(f"Reading {audio_file}")
    led_setup(LEDS)
    audio = load_file(audio_file)
    print(audio)

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
