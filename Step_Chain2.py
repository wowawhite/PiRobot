#!/usr/bin/python3
from time import sleep
import pigpio
import xbox
import numpy as np

# Code where you want to test the error status.
pigpio.exceptions = True

#bcm pin mode
DIR = 20     # Direction GPIO Pin
STEP = 21    # Step GPIO Pin
SWITCH = 16  # GPIO pin of switch, on/off with physical button?

# Stepper parameter
_DEGREE_PER_STEP_ = 1.8
_MAX_RPM_ = 25
_MIN_RPM_ = 1
_RESOLUTION_TEMP_ = 1.0
duration_type = {'time', 'steps', 'continuous'}


# Connect to joystick
joy = xbox.Joystick()

# Connect to pigpiod daemon
pi = pigpio.pi()

# Set up pins as an output
pi.set_mode(DIR, pigpio.OUTPUT)
pi.set_mode(STEP, pigpio.OUTPUT)

# Set up input switch
pi.set_mode(SWITCH, pigpio.INPUT)
pi.set_pull_up_down(SWITCH, pigpio.PUD_UP)  # pulldown up?

MODE = (14, 15, 18)   # Microstep Resolution GPIO Pins, tuple, for both steppers
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}
for i in range(3):
    pi.write(MODE[i], RESOLUTION['Full'][i])

def joystick_conversion():
    x_stick = joy.leftX() * 100
    y_stick = joy.leftY() * 100
    x_stickInt = int(x_stick)
    y_stickInt = int(y_stick)
    x_stickInv = 0 - x_stickInt
    u = (100 - abs(x_stickInv)) * y_stickInt / 100 + y_stickInt
    v = (100 - abs(y_stick)) * x_stickInv / 100 + x_stickInv
    rightVector = (u + v) / 2
    leftVector = (u - v) / 2
    turboButton = joy.leftTrigger()  # does this work?


def pulse_creator(pulses, delay):
    pi.wave_clear()
    wf = []
    wid = [-1] * 100
    wf.append(pigpio.pulse(1 << STEP, 0, delay))  # pulse on
    wf.append(pigpio.pulse(0, 1 << STEP, delay))  # pulse off
    pi.wave_add_generic(wf)
    wid[i] = pi.wave_create()


def drive_steppers(rightVector, leftVector, turboButton):
	#do stuff
    pass

def generate_ramp(ramp):
    """Generate ramp wave forms.
    ramp:  List of [Frequency, Steps]
    """
    pi.wave_clear()     # clear existing waves
    length = len(ramp)  # number of ramp levels
    wid = [-1] * length # list is as long as ramp elements

    # Generate a wave per ramp level
    for i in range(length):
        frequency = ramp[i][0]
        micros = int(500000 / frequency)
        """
        micros, Frequencies, steps
        1562, [320, 200],
        1000, [500, 200],
        625,  [800, 200],
        500,  [1000, 200],
        312,  [1600, 200],
        250,  [2000, 200]
        """

        """
        pigpio.pulse(gpio_on, gpio_off, delay)
        gpio_on:= the GPIO to switch on at the start of the pulse.
        gpio_off:= the GPIO to switch off at the start of the pulse.
        delay:= the delay in microseconds before the next pulse.
        """
        wf = []
        wf.append(pigpio.pulse(1 << STEP, 0, micros))  # pulse on
        wf.append(pigpio.pulse(0, 1 << STEP, micros))  # pulse off
        pi.wave_add_generic(wf)
        wid[i] = pi.wave_create()

    # Generate a chain of waves
    chain = []
    for i in range(length):
        steps = ramp[i][1]
        x = steps & 255 # for what?
        y = steps >> 8 #=0

    """
    Loop Start:	255 0 - Identify start of a wave block
    Loop Repeat:	255 1 x y - loop x + y*256 times
    Delay:	255 2 x y - delay x + y*256 microseconds
    Loop Forever:	255 3 - loop forever
    """

    chain += [255, 0, wid[i], 255, 1, x, y]

    pi.wave_chain(chain)  # Transmit chain.



#runtime loop
try:
    while True:

        pi.write(DIR, pi.read(SWITCH))  # Set direction
        # Ramp up, [frequency, steps]
        generate_ramp([[320, 200],
                       [500, 400],
                       [800, 600],
                       [1000, 800],
                       [1600, 1000],
                       [2000, 2000]])
        sleep(.1) #for what?
except KeyboardInterrupt:
    print ("\nCtrl-C pressed.  Stopping PIGPIO and exiting...")
finally:
    pi.set_PWM_dutycycle(STEP, 0)  # PWM off
    pi.stop()
    #kill joystick
    joy.close()