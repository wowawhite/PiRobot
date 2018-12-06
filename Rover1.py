#!/usr/bin/env python
# -*- coding: utf-8 -*-

############### file info ######################################################
#
#
#
#
#
#
################################################################################


import xbox
if __debug__:pass
else:
	import RPi.GPIO as pi


PWM_duty = 50 #%

#Servo Left
MS1_LeftPin
MS2_LeftPin
MS3_LeftPin
Dir_LeftPin
Step_LeftPin
Enable_LeftPin

#Servo Right defs
MS1_LeftPin
MS2_LeftPin
MS3_LeftPin
Dir_LeftPin
Step_LeftPin
Enable_LeftPin

#def controls
joystick = xbox.Joystick()
Xstick = joystick.leftX()
Ystick = joystick.leftY()
u = ((100-abs(Xstick))*Ystick/100+Ystick)
v = ((100-abs(Ystick))*Xstick/100+Xstick)
rightVector = (u+v)/2
leftVector = (u-v)/2

