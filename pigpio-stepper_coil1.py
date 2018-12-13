#!/usr/bin/python
# from https://github.com/stripcode/pigpio-stepper-motor/blob/master/PigpioStepperMotor.py
import pigpio
from time import sleep
from collections import deque



fullStepSequence = (
  (1, 0, 0, 0),
  (0, 1, 0, 0),
  (0, 0, 1, 0),
  (0, 0, 0, 1)
)



halfStepSequence = (
  (1, 0, 0, 0),
  (1, 1, 0, 0),
  (0, 1, 0, 0),
  (0, 1, 1, 0),
  (0, 0, 1, 0),
  (0, 0, 1, 1),
  (0, 0, 0, 1),
  (1, 0, 0, 1)
)



class StepperMotor:

  def __init__(self, pi, pin1, pin2, pin3, pin4, sequence = halfStepSequence, delayAfterStep = 0.0025):
    if not isinstance(pi, pigpio.pi):
      raise TypeError("Is not pigpio.pi instance.")
    pi.set_mode(pin1, pigpio.OUTPUT)
    pi.set_mode(pin2, pigpio.OUTPUT)
    pi.set_mode(pin3, pigpio.OUTPUT)
    pi.set_mode(pin4, pigpio.OUTPUT)
    self.pin1 = pin1
    self.pin2 = pin2
    self.pin3 = pin3
    self.pin4 = pin4
    self.pi = pi
    self.delayAfterStep = delayAfterStep
    self.deque = deque(sequence)



  def doСounterclockwiseStep(self):
    self.deque.rotate(-1)
    self.doStepAndDelay(self.deque[0])



  def doСlockwiseStep(self):
    self.deque.rotate(1)
    self.doStepAndDelay(self.deque[0])



  def doStepAndDelay(self, step):
    self.pi.write(self.pin1, step[0])
    self.pi.write(self.pin2, step[1])
    self.pi.write(self.pin3, step[2])
    self.pi.write(self.pin4, step[3])
    sleep(self.delayAfterStep)