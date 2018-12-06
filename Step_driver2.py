#!/usr/bin/env python3
# from https://github.com/gavinlyonsrepo/RpiMotorLib/blob/master/Documentation/Nema11A4988.md
import RpiMotorLib
import RPi.GPIO as GPIO
#define GPIO pins
#bcm mode
GPIO_pins = (14, 15, 18) # Microstep Resolution MS1-MS3 -> GPIO Pin
direction= 20       # Direction -> GPIO Pin
step = 21      # Step -> GPIO Pin

mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")
# call the function, pass the arguments
#arguments(clockwise?, steptype, steps, stepdelay, verbose, init delay )
mymotortest.motor_go(False, "Half", 500, .005, False, .05)

# good practise to cleanup GPIO at some point before exit
GPIO.cleanup()

"""The library file RpiMotorLib.py contains the class which controls the motor. The class is called A4988Nema.

The class is initialized with three arguments. (direction_pin, step_pin, mode_pins):

direction type=int , help=GPIO pin connected to DIR pin of IC.
step_pin type=int , help=GPIO pin connected to STEP of IC.
mode_pins type=tuple of 3 ints, help=GPIO pins connected to, Microstep Resolution pins MS1-MS3 of IC.
motor_type type=string, help= type of motor, two options "A4988" or "DRV8825"
The main method that moves motor is called motor_go, takes 6 inputs. motor_go(clockwise, steptype, steps, stepdelay, verbose, initdelay):

clockwise, type=bool default=False help="Turn stepper counterclockwise"

steptype, type=string , default=Full help= type of drive to step motor 5 options. (Full, Half, 1/4, 1/8, 1/16)

steps, type=int, default=200, help=Number of steps sequence's to execute. Default is one revolution , 200 in Full mode.

stepdelay, type=float, default=0.05, help=Time to wait (in seconds) between steps.

verbose, type=bool type=bool default=False help="Write pin actions",

initdelay, type=float, default=1mS, help= Intial delay after GPIO pins initialized but before motor is moved.

Example: Should do a 180 degree turn. To run A stepper motor clockwise in Full mode for 100 steps. for step delay of .01 second. verbose output off , with 50mS init delay."""