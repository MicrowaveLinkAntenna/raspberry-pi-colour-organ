#! /usr/bin/python

import RPi.GPIO as GPIO
import time

def gpio_setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

def set_output(pin: int):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

def blink(pin: int, interval: int):
    GPIO.output(pin, True)
    time.sleep(interval)
    GPIO.output(pin, False)

