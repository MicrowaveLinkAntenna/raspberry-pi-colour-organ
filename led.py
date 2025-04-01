#! /usr/bin/python

import RPi.GPIO as GPIO
import time
import threading

from audio import fft_split_average, fft_split

# The GPIO pins for each colour LED
RED = 2
YELLOW = 3
BLUE = 4
GREEN = 17
WHITE = 27

# The order of LEDS from representing highest to lowest frequencies
LEDS = (RED, YELLOW, BLUE, GREEN, WHITE)

# Multipliers used to adjust the weights of the frequency ranges so no one LED is always on or off
LED_MULTIPLIERS = (1, 1, 0.5, 1, 0.5)

# How long in miliseconds to keep the LED on for
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

def async_blink(pin: int, interval: int = BLINK_DURATION):
    thread = threading.Thread(target=blink, args=(pin, interval))
    thread.start()

def fft_led_state(fft_averages: dict, total_average: float):
    result = {}
    frequency_ranges = sorted(list(fft_averages.keys()), key=lambda x: x[1])
    for led, multiplier, frequency in zip(LEDS, LED_MULTIPLIERS, frequency_ranges):
        result[led] = fft_averages[frequency]*multiplier > total_average
    return result

def blink_fft(fft_data: tuple):
    amplitudes = fft_split(fft_data, len(LEDS))
    averages, total_average = fft_split_average(amplitudes)
    print(averages)
    for led, state in fft_led_state(averages, total_average).items():
        if state:
            async_blink(led)
