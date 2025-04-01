from led import *

def main():
    led_setup(LEDS)
    while True:
        for led in LEDS:
            blink(led, 500)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        led_clear(LEDS)
