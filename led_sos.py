#! /usr/bin/python

import RPi.GPIO as GPIO
import time

LED_PIN = 12

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def flash_slow():
    GPIO.output(LED_PIN, True)
    time.sleep(0.5)
    GPIO.output(LED_PIN, False)
    time.sleep(0.5)
    
def flash_fast():
    GPIO.output(LED_PIN, True)
    time.sleep(0.2)
    GPIO.output(LED_PIN, False)
    time.sleep(0.2)

while True:
    flash_fast()
    flash_fast()
    flash_fast()
    
    flash_slow()
    flash_slow()
    flash_slow()
    
    flash_fast()
    flash_fast()
    flash_fast()

    
    
    
    
