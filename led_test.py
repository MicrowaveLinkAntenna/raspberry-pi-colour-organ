from led import *

def main():
    led_setup(LEDS)
    try:
        while True:
            for led in LEDS:
                blink(led, 500)
    except KeyboardInterrupt:
        led_clear(LEDS)

if __name__ == "__main__":
    main()
