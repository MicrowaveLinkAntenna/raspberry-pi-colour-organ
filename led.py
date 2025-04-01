#! /usr/bin/python

import RPi.GPIO as GPIO
import time

# The GPIO pins for each colour LED
RED = 2
YELLOW = 3
BLUE = 4
GREEN = 17
WHITE = 27

# The order of LEDS from representing highest to lowest frequencies
LEDS = [RED, YELLOW, BLUE, GREEN, WHITE]

def gpio_setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

def set_output(pin: int):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

def led_setup(leds: list[int]):
    gpio_setup()
    for led in leds:
        set_output(led)

def led_clear(leds: list[int]):
    for led in leds:
        GPIO.output(led, False)

def blink(pin: int, interval: int):
    GPIO.output(pin, True)
    time.sleep(1000)
    GPIO.output(pin, False)

