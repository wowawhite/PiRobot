# from https://electronics.stackexchange.com/questions/318632/driving-multiple-stepper-motors-with-raspberry-pi
#try implementing bitbang stepper control
from Stepper_Motor import Stepper
import time
from threading import Thread
from queue import Queue

Acoil_A_1_pin = 2
Acoil_A_2_pin = 3
Acoil_B_1_pin = 4
Acoil_B_2_pin = 14
Aenable_pin   = 15


Bcoil_A_1_pin = 18
Bcoil_A_2_pin = 17
Bcoil_B_1_pin = 27
Bcoil_B_2_pin = 22
Benable_pin   = 23

steps_per_rotation = 50

stepper_A = Stepper(steps_per_rotation, Acoil_A_1_pin, Acoil_A_2_pin, Acoil_B_1_pin, Acoil_B_2_pin, Aenable_pin)

stepper_B = stepper = Stepper(steps_per_rotation, Bcoil_A_1_pin, Bcoil_A_2_pin, Bcoil_B_1_pin, Bcoil_B_2_pin, Benable_pin)

#q = Queue()
motor_on_A = False
motor_on_B = False

def spin_A():
    while True:
        if motor_on_A:
            stepper_A.forwards(2)

def spin_B():
    while True:
        if motor_on_B:
            stepper_B.forwards(2)

def control():
    global motor_on_A
    global motor_on_B

    while True:
        user_input = input()

        if user_input == "start_A":
            #q.put("start")
            motor_on_A = True

        elif user_input == "start_B":
            #q.put("start")
            motor_on_B = True

        elif user_input == "start":
            #q.put("start")
            motor_on_A = True
            motor_on_B = True

        elif user_input == "stop_A":
            #q.put("stop")
            motor_on_A = False

        elif user_input == "stop_B":
            #q.put("stop")
            motor_on_B = False

        elif user_input == "stop":
            #q.put("stop")
            motor_on_B = False
            motor_on_A = False


sA = Thread(target = spin_A)
c = Thread(target = control)
sB = Thread(target = spin_B)


sA.start()
sB.start()
c.start()