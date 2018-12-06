#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# based on http://home.kendra.com/mauser/joystick.html
from __future__ import print_function
import xbox
import sys
# Format floating point number to string format -x.xxx
def fmtFloat(n):
    return '{:6.3f}'.format(n)

# Print one or more values without a line feed
def show(*args):
    for arg in args:
        print(arg, end="")

# Print true or false value based on a boolean, without linefeed
def showIf(boolean, ifTrue, ifFalse=" "):
    if boolean:
        show(ifTrue)
    else:
        show(ifFalse)
#init joypad
joy = xbox.Joystick()
#exit on joypad
while not joy.X():
	#return from -1.0 to +1.0
	Xstick = joy.leftX()*100
	Ystick = joy.leftY()*100
	XstickInt=int(Xstick)
	YstickInt=int(Ystick)
	XstickInv=0-XstickInt
	u = (100-abs(XstickInv))*YstickInt/100+YstickInt
	v = (100-abs(Ystick))*XstickInv/100+XstickInv
	rightVector = (u+v)/2
	leftVector = (u-v)/2

	#print stuff
	show("X-Button for Exit!  ")
	show(chr(17))
	show(" Left X: ", fmtFloat(joy.leftX()), " Left Y: ", fmtFloat(joy.leftY()))
	show("  Left Vector:",fmtFloat(leftVector), "  Right Vector:", fmtFloat((rightVector)))
	#rewrite line
	show(chr(13))
joy.close()

