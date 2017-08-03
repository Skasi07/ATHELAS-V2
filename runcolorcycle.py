import colorschemes
import apa102
import time
import signal
import sys

NUM_LED = 2

color = input("color? (r, g, b, w)")
brightness = int(input("brightness? (0-255)"))

strip = apa102.APA102(num_led=NUM_LED, global_brightness=brightness)

if color == "r":
    for led in range(NUM_LED):
        strip.set_pixel(led, 255, 0,0, bright_percent=100)
elif color == "g":
    for led in range(NUM_LED):
        strip.set_pixel(led, 0 ,255,0, bright_percent=100)
elif color == "b":
    for led in range(NUM_LED):
        strip.set_pixel(led, 0, 0, 255, bright_percent=100)
elif color == "w":
    for led in range(NUM_LED):
        strip.set_pixel(led, 255,255,200, bright_percent=100)

def signal_handler(signal, frame):
    strip.clear_strip()
    strip.cleanup()

signal.signal(signal.SIGINT, signal_handler)

while True:
    strip.show()

