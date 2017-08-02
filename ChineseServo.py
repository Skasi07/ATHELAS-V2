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
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(1000)


x = input("Where do you want to go")
print (x)
dx = input("Input the imcrement amount")
print (dx)
delay_period = input("Input the delay period")
print (delay_period)
time.sleep(3)
d = 110
while True:
        for d in range(110,200,dx):
                x=x+dx
                wiringpi.pwmWrite(18, x)
                time.sleep(delay_period)
        for d in range(190,110,-dx):
                x=x-dx
                wiringpi.pwmWrite(18, x)
                time.sleep(delay_period)




