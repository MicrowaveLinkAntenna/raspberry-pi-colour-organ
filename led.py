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

LED_FREQUENCIES = {l: f for l, f in zip(LEDS, FREQUENCIES)}

BLINK_DURATION = 5

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

def blink(pin: int, interval: int = BLINK_DURATION):
    GPIO.output(pin, True)
    time.sleep(interval/1000)
    GPIO.output(pin, False)

def fft_led_state(fft_averages: dict, led_mapping: dict = LED_FREQUENCIES):
    result = {}
    total_average = fft_averages["Total"]
    for led, frequency in led_mapping.items():
        result[led] = fft_averages[frequency] > total_average
    return result

def blink_fft(fft_data: tuple, led_mapping: dict = LED_FREQUENCIES):
    amplitudes = fft_split(fft_data)
    averages = fft_split_average(amplitudes)
    print(averages)
    for led, state in fft_led_state(averages, led_mapping).items():
        if state:
            blink(led)
