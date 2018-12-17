#!/usr/bin/python3
# from https://raspberrypi.stackexchange.com/questions/88724/add-pulse-object-to-transmitting-pigpio-waveform
import PoluluA4988driver as driver

# motor1 parameter

_DEGREE_PER_STEP_ = 1.8
_MAX_RPM_ = 100
_NAME_ = 'left motor'

_MODE0_ = 0
_MODE1_ = 1
_MODE2_ = 2
_DECAY_ = 3
_DIR_ = 20
_STEP_ = 21 ## must be a Pi GPIO pin
_nENBL_ = 6
_nRESET_ = 7
_nSLEEP_ = 8

_PINS_ = {
        'MODE0': _MODE0_,
        'MODE1': _MODE1_,
        'MODE2': _MODE2_,
        'DECAY': _DECAY_,
        'DIR': _DIR_,
        'STEP': _STEP_,
        'nENBL': _nENBL_,
        'nRESET': _nRESET_,
        'nSLEEP': _nSLEEP_,
        }


""" Possible motor parameters
duration = {'type': 'time', 'value': 5},
#_OPERATION_TYPE_ = duration = ['continuous', 'time', 'angle', 'steps']


def operate_motor_continuous(self, direction, resolution, rpm, setup_delay = 0.2):
"""


motor1 = driver.StepperMotorA4988(name = _NAME_, pins = _PINS_, degree_per_step = _DEGREE_PER_STEP_,  max_rpm = _MAX_RPM_)
motor1.operate_motor_finite('forward', 1.0, 20, 'time', 20 )


"""
def operate_motor_finite(self, direction, resolution, rpm,
                      duration = {'type': 'time', 'value': 5},
                      setup_delay = 0.2):
"""