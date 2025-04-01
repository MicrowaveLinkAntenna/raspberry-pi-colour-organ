import sys
import numpy as np
import librosa

from led import led_setup, led_clear, blink, LEDS
from audio import load_file

def main(audio_file: str):
    print(f"Reading {audio_file}")
    led_setup(LEDS)
    audio_data, sample_rate = load_file(audio_file)
    fft = np.fft.fft(audio_data)

    print(audio_data, sample_rate, fft)

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
