import sys
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# setup GPIO
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, True)
# dict resolution
stepdelay=(0.000001) #in seconds, max stepdelay=(0.000001) bullshit timer, half speed of arduino
#time.sleep(0.05)
try:
	while True:
		GPIO.output(21, True)
		time.sleep(stepdelay)
		GPIO.output(21, False)
		time.sleep(stepdelay)
except KeyboardInterrupt:
	GPIO.output(21, False)
	GPIO.cleanup()