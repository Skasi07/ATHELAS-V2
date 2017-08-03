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
delay_period = .05
d = 120
dx = 1

# Original start points = 80, 210

while True:
        for d in range(77,230,dx):
                d+=dx
                wiringpi.pwmWrite(18, d)
                print(d)
                time.sleep(delay_period)
                if d == 230:
                        time.sleep(.05)
        for d in range(230,77,-dx):
                d-=dx
                wiringpi.pwmWrite(18, d)
                print(d)
                time.sleep(delay_period)
                if d == 77:
                        time.sleep(.05)


