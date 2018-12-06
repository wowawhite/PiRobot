#!/usr/bin/python
# ========================================================
# Python module for controlling Raspberry Pi robot PiBot-B
# by Thomas Schoch - www.retas.de
# ========================================================

import sys
import os

sys.path.append('/home/pi/lib/WiringPi-Python')
import wiringpi

# ========================================================
# Constants
# ========================================================

# GPIO pin numbers
MOTOR_LEFT_A  = 22
MOTOR_LEFT_B  = 23
MOTOR_RIGHT_A = 10
MOTOR_RIGHT_B = 24
PWM_VALUE     = 18
PWM_LEFT      = 17
PWM_RIGHT     = 27

# GPIO pin modes
MODE_IN  = 0
MODE_OUT = 1
MODE_PWM = 2

# Logic levels
HIGH = 1
LOW  = 0

# movements
LEFT  = 0
RIGHT = 1
BOTH  = 2
FWD   = 0
BWD   = 1
STOP  = -1

# ========================================================
# Initialization
# ========================================================

def init():

    # setup class wiringpi with GPIO pin numbering
    wiringpi.wiringPiSetupGpio()

    # motor right
    wiringpi.pinMode(MOTOR_RIGHT_A, MODE_OUT)
    wiringpi.pinMode(MOTOR_RIGHT_B, MODE_OUT)

    # motor left
    wiringpi.pinMode(MOTOR_LEFT_A, MODE_OUT)
    wiringpi.pinMode(MOTOR_LEFT_B, MODE_OUT)

    # PWM side control (or-gate)
    wiringpi.pinMode(PWM_LEFT,  MODE_OUT)
    wiringpi.pinMode(PWM_RIGHT, MODE_OUT)

    # PWM value
    wiringpi.pinMode(PWM_VALUE, MODE_PWM)

# ========================================================
# GPIO output
# ========================================================

# PWM control
#
def setpwm(side, value):

    # set inputs of or-gates
    if (side == BOTH):
        wiringpi.digitalWrite(PWM_LEFT,  LOW)
        wiringpi.digitalWrite(PWM_RIGHT, LOW)
    elif (side == LEFT):
        wiringpi.digitalWrite(PWM_LEFT,  LOW)
        wiringpi.digitalWrite(PWM_RIGHT, HIGH)
    elif (side == RIGHT):
        wiringpi.digitalWrite(PWM_LEFT,  HIGH)
        wiringpi.digitalWrite(PWM_RIGHT, LOW)

    # set pwm value
    wiringpi.pwmWrite(PWM_VALUE, value)

# Motor control
#
def motor(side, direction):

    # which motor to control
    if (side == RIGHT):
        MOTOR_A = MOTOR_RIGHT_A
        MOTOR_B = MOTOR_RIGHT_B
    elif (side == LEFT):
        MOTOR_A = MOTOR_LEFT_A
        MOTOR_B = MOTOR_LEFT_B

    # GPIO output to inputs of L293D
    if (direction == FWD):
        wiringpi.digitalWrite(MOTOR_A, HIGH)
        wiringpi.digitalWrite(MOTOR_B, LOW)
    elif (direction == BWD):
        wiringpi.digitalWrite(MOTOR_A, LOW)
        wiringpi.digitalWrite(MOTOR_B, HIGH)
    elif (direction == STOP):
        wiringpi.digitalWrite(MOTOR_A, LOW)
        wiringpi.digitalWrite(MOTOR_B, LOW)

# ========================================================
# Movements
# ========================================================

def straight(direction, pwm):
    setpwm(BOTH, pwm)
    motor (LEFT,  direction)
    motor (RIGHT, direction)

def rotate(rotation, pwm):
    setpwm(BOTH, pwm)
    motor (rotation, BWD)
    motor (not(rotation), FWD)

def turn(rotation, direction, pwm):
    setpwm(not(rotation), pwm)
    motor (rotation, STOP)
    motor (not(rotation), direction)

def curve(rotation, direction, pwm):
    setpwm(rotation, pwm)
    motor (LEFT, direction)
    motor (RIGHT, direction)

def stop():
    motor (LEFT, STOP)
    motor (RIGHT, STOP)

# ========================================================
