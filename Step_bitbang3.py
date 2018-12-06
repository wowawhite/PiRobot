import RPi.GPIO as GPIO
import time
import threading

class Stepper:

  def __init__(self, steps_per_rotation, A1, A2, B1, B2, E):

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    self.steps_per_rotation = steps_per_rotation
    self.coil_A_1_pin = A1
    self.coil_A_2_pin = A2
    self.coil_B_1_pin = B1
    self.coil_B_2_pin = B2
    self.enable_pin   = E

    GPIO.setup(self.coil_A_1_pin, GPIO.OUT)
    GPIO.setup(self.coil_A_2_pin, GPIO.OUT)
    GPIO.setup(self.coil_B_1_pin, GPIO.OUT)
    GPIO.setup(self.coil_B_2_pin, GPIO.OUT)
    GPIO.setup(self.enable_pin, GPIO.OUT)

  def set_step(self, w1, w2, w3, w4):
    GPIO.output(self.coil_A_1_pin, w1)
    GPIO.output(self.coil_A_2_pin, w2)
    GPIO.output(self.coil_B_1_pin, w3)
    GPIO.output(self.coil_B_2_pin, w4)

  def enable(self):
    GPIO.output(self.enable_pin, 1)

  def disable(self):
    GPIO.output(self.enable_pin, 0)

  def forward_rotation(self, delay, rotation):
    steps = rotation * self.steps_per_rotation
    delay = delay/1000
    self.enable()
    for i in range(0, steps):
      self.set_step(1, 0, 1, 0)
      time.sleep(delay)
      self.set_step(0, 1, 1, 0)
      time.sleep(delay)
      self.set_step(0, 1, 0, 1)
      time.sleep(delay)
      self.set_step(1, 0, 0, 1)
      time.sleep(delay)
    self.disable()

  def backward_rotation(self, delay, rotation):
    steps = rotation * self.steps_per_rotation
    delay = delay/1000
    self.enable()
    for i in range(0, steps):
      self.set_step(1, 0, 0, 1)
      time.sleep(delay)
      self.set_step(0, 1, 0, 1)
      time.sleep(delay)
      self.set_step(0, 1, 1, 0)
      time.sleep(delay)
      self.set_step(1, 0, 1, 0)
      time.sleep(delay)
    self.disable()

  def forward_time(self, delay, second):
    delay = delay/1000
    self.enable()
    timeout = time.time() + second
    while time.time() < timeout:
      self.set_step(1, 0, 1, 0)
      time.sleep(delay)
      self.set_step(0, 1, 1, 0)
      time.sleep(delay)
      self.set_step(0, 1, 0, 1)
      time.sleep(delay)
      self.set_step(1, 0, 0, 1)
      time.sleep(delay)
    self.disable()

  def backward_time(self, delay, second):
    delay = delay/1000
    self.enable()
    timeout = time.time() + second
    while time.time() < timeout:
      self.set_step(1, 0, 0, 1)
      time.sleep(delay)
      self.set_step(0, 1, 0, 1)
      time.sleep(delay)
      self.set_step(0, 1, 1, 0)
      time.sleep(delay)
      self.set_step(1, 0, 1, 0)
      time.sleep(delay)
    self.disable()

  def forwards(self, delay, steps = 1):
    delay = delay/1000
    self.enable()
    for i in range(0, steps):
      self.set_step(1, 0, 1, 0)
      time.sleep(delay)
      self.set_step(0, 1, 1, 0)
      time.sleep(delay)
      self.set_step(0, 1, 0, 1)
      time.sleep(delay)
      self.set_step(1, 0, 0, 1)
      time.sleep(delay)
    self.disable()

  def backwards(self, delay, steps = 1):
    delay = delay/1000
    self.enable()
    for i in range(0, steps):
      self.set_step(1, 0, 0, 1)
      time.sleep(delay)
      self.set_step(0, 1, 0, 1)
      time.sleep(delay)
      self.set_step(0, 1, 1, 0)
      time.sleep(delay)
      self.set_step(1, 0, 1, 0)
      time.sleep(delay)
    self.disable()