import RPi.GPIO as GPIO
import sys
import time

GPIO.setmode(GPIO.BCM)

PIN_LIVING = 20
GPIO.setup(PIN_LIVING, GPIO.OUT)
living = GPIO.PWM(PIN_LIVING, 110)
living.start(0)
#dc = 0
#dx = 10
#delay = 1
#living.ChangeDutyCycle(dc)

#while True:
#       for dc in range (0, 100, dx):
#               dc += dx
#               living.ChangeDutyCycle(dc)
#               time.sleep(delay)
#               print (dc)
#        for dc in range (100, 0, -dx):
#                dc -= dx
#               living.ChangeDutyCycle(dc)
#                time.sleep(delay)
#                print (dc)


brightness = input('Enter the value of the brightness')
while brightness > 0:
        living.ChangeDutyCycle(brightness)

