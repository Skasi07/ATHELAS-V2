#! /usr/bin/python
#This code controllers stepper motors via the Adafruit Raspberry Pit HAT
#This is used primarily for stepper motor functionality and accuracy testing

#Written by: Daniel Beebe
#Athelas --February 2017
#Ver: 0.0.1

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_StepperMotor
from Adafruit_MotorHAT import Adafruit_DCMotor

import time
import atexit

#--------------------Creating motor objects----------------------------#
mh = Adafruit_MotorHAT(addr=0x60)
stepper = mh.getStepper(200, 1)
#stepper.setSpeed(255) #SETTING THE RPM, NOT SURE IF NEEDED

#---------------------------Functions----------------------------------#
#Shut off motor function.
def turnOFF():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
#The turnOFF function is REQUIRED for when motor functions are no longer needed.
#The turnOFF function cuts off all hold current to the motor.
#If motor is meant to be held in place turnOFF should not be called.

#backward is down.
#micro step down function.
def microdown():
    stepper.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.MICROSTEP)
#micro step up function.
def microup():
    stepper.oneStep(Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)
#
#interleave step down function.
def interdown():
    stepper.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.INTERLEAVE)
#interleave step up function.
def interup():
    stepper.oneStep(Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.INTERLEAVE)
#interleave steps are in between micro and double step sizings.

#double step down function.
def doubledown():
    stepper.oneStep(Adafruit_MotorHAT.BACKWARD, Adafruit_MotorHAT.DOUBLE)
#double step up function.
def doubleup():
    stepper.oneStep(Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.DOUBLE)
#double steps are full steps.

#----------------------------MAIN----------------------------------------# 
while True:
    stpz = 0
    step = raw_input('What kind of steps? ')

    #Micro step loop.
    if step == 'u':
        stpz = 0
        while True:
            drct = raw_input('Up or down? Or Exit ')
            if drct == 'u':
                while True:
                    move = raw_input('Press Enter to move and E to exit: ')
                    if move == '': 
                        microup()
                        stpz = stpz + 1
                        print stpz
                    elif move == 'E':
                        turnOFF()
                        break
            if drct == 'd':
                while True:
                    move = raw_input('Press Enter to move and E to exit')
                    if move == '':
                        microdown()
                        stpz= stpz - 1
                        print stpz
                    elif move == 'E':
                        turnOFF()
                        break
            if drct == 'E':
                turnOFF()
                break
    #Interleave step loop.
    if step == 'i':
        stpz = 0
        while True:
            drct = raw_input('Up or down? Or Exit ')
            if drct == 'u':
                while True:
                    move = raw_input('Press Enter to move and E to exit: ')
                    if move == '': 
                        interup()
                        stpz = stpz + 1
                        print stpz
                    elif move == 'E':
                        turnOFF()
                        break
            if drct == 'd':
                while True:
                    move = raw_input('Press Enter to move and E to exit')
                    if move == '':
                        interdown()
                        stpz= stpz - 1
                        print stpz
                    elif move == 'E':
                        turnOFF()
                        break
            if drct == 'E':
                turnOFF()
                break
    #Double step loop.
    if step == 'd':
        stpz = 0
        while True:
            drct = raw_input('Up or down? Or Exit ')
            if drct == 'u':
                while True:
                    move = raw_input('Press Enter to move and E to exit: ')
                    if move == '': 
                        doubleup()
                        stpz = stpz + 1
                        print stpz
                    elif move == 'E':
                        turnOFF()
                        break
            if drct == 'd':
                while True:
                    move = raw_input('Press Enter to move and E to exit')
                    if move == '':
                        doubledown()
                        stpz= stpz - 1
                        print stpz
                    elif move == 'E':
                        turnOFF()
                        break
            if drct == 'E':
                turnOFF()
                break
