#! /usr/bin/python

import RPi.GPIO as GPIO
import time

from audio import fft_split_average, fft_split, FREQUENCIES

# The GPIO pins for each colour LED
RED = 2
YELLOW = 3
BLUE = 4
GREEN = 17
WHITE = 27

# The order of LEDS from representing highest to lowest frequencies
LEDS = (RED, YELLOW, BLUE, GREEN, WHITE)

def gpio_setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

def set_output(pin: int):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

def led_setup(leds: list[int] = LEDS):
    gpio_setup()
    for led in leds:
        set_output(led)

def led_clear(leds: list[int] = LEDS):
    for led in leds:
        GPIO.output(led, False)

def blink(pin: int, interval: int):
    GPIO.output(pin, True)
    time.sleep(interval/1000)
    GPIO.output(pin, False)

def blink_fft(fft_data: tuple, leds: list[int] = LEDS):
    amplitudes = fft_split(fft_data)
    averages = fft_split_average(amplitudes)
    print(averages)
