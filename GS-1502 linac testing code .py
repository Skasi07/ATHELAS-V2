# Servo Control
import time
import wiringpi

# use 'GPIO naming'
wiringpi.wiringPiSetupGpio()

# set #18 to be a PWM output
wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)

# set the PWM mode to milliseconds stype
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

# divide down clock
wiringpi.pwmSetClock(180)
wiringpi.pwmSetRange(1960)

#speed of the devicer can be controlled here
delay_period =0.2
d = 120
dx = 5

# Original start points = 85, 215

while True:
        for d in range(85,215,dx):
                d+=dx
                wiringpi.pwmWrite(18, d)
		print(d)
                time.sleep(delay_period)
		if d == 215: 
			time.sleep(1)
        for d in range(215,85,-dx):
		d-=dx
                wiringpi.pwmWrite(18, d)
		print(d)
                time.sleep(delay_period)
		if d == 85:
			time.sleep(1)
