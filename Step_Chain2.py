#!/usr/bin/python3
# import here
from time import sleep
import pigpio
#import xbox

# Code where you want to test the error status.

pigpio.exceptions = True

#bcm pin mode
DIR = 20     # Direction GPIO Pin
STEP = 21    # Step GPIO Pin
SWITCH = 16  # GPIO pin of switch

# Connect to pigpiod daemon
pi = pigpio.pi()

# Set up pins as an output
pi.set_mode(DIR, pigpio.OUTPUT)
pi.set_mode(STEP, pigpio.OUTPUT)

# Set up input switch
pi.set_mode(SWITCH, pigpio.INPUT)
pi.set_pull_up_down(SWITCH, pigpio.PUD_UP)#pulldown up?

MODE = (14, 15, 18)   # Microstep Resolution GPIO Pins
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}
for i in range(3):
    pi.write(MODE[i], RESOLUTION['Full'][i])


def generate_ramp(ramp):
    """Generate ramp wave forms.
    ramp:  List of [Frequency, Steps]
    """
    pi.wave_clear()     # clear existing waves
    length = len(ramp)  # number of ramp levels
    wid = [-1] * length

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



        chain += [255, 0, wid[i], 255, 1, x, y]

    pi.wave_chain(chain)  # Transmit chain.


#runtime loop
try:
    while True:
        #joystick parameter hier rein
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