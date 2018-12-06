#original script from
#http://www.elektronx.de/tutorials/schrittmotorsteuerung-mit-dem-raspberry-pi/
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)


A=18
B=23
C=24
D=25
time = 0.05


GPIO.setup(A,GPIO.OUT)
GPIO.setup(B,GPIO.OUT)
GPIO.setup(C,GPIO.OUT)
GPIO.setup(D,GPIO.OUT)
GPIO.output(A, False)
GPIO.output(B, False)
GPIO.output(C, False)
GPIO.output(D, False)

# Schritte 1 - 8 festlegen
def Step1():
    GPIO.output(A, True)
    GPIO.output(B, False)
    GPIO.output(C, False)
    GPIO.output(D, False)
    sleep(time)
def Step2():
    GPIO.output(A, True)
    GPIO.output(B, True)
    GPIO.output(C, False)
    GPIO.output(D, False)
    sleep(time)
def Step3():
    GPIO.output(A, False)
    GPIO.output(B, True)
    GPIO.output(C, False)
    GPIO.output(D, False)
    sleep(time)
def Step4():
    GPIO.output(A, False)
    GPIO.output(B, True)
    GPIO.output(C, True)
    GPIO.output(D, False)
    sleep(time)
def Step5():
    GPIO.output(A, False)
    GPIO.output(B, False)
    GPIO.output(C, True)
    GPIO.output(D, False)
    sleep(time)
def Step6():
    GPIO.output(A, False)
    GPIO.output(B, False)
    GPIO.output(C, True)
    GPIO.output(D, True)
    sleep(time)
def Step7():
    GPIO.output(A, False)
    GPIO.output(B, False)
    GPIO.output(C, False)
    GPIO.output(D, True)
    sleep(time)
def Step8():
    GPIO.output(A, True)
    GPIO.output(B, False)
    GPIO.output(C, False)
    GPIO.output(D, True)
    sleep(time)
# Volle Umdrehung
for i in range (200):
    Step1()
    Step2()
    Step3()
    Step4()
    Step5()
    Step6()
    Step7()
    Step8()
    print (i)

GPIO.cleanup()