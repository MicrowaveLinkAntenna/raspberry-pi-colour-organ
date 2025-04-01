#! /usr/bin/python

import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

def flash(interval):
    GPIO.output(18, True)
    time.sleep(interval)
    GPIO.output(18, False)
    time.sleep(interval)

while True:
    flash(3)
    
    
    
    