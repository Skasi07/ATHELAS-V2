import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:

	print('VALUE', GPIO.input(12))
	time.sleep(0.1)

