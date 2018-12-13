#!/usr/bin/python3
import numpy as np

def ramfoo():
	ramp = ([[320, 200],
		 [500, 200],
		 [800, 200],
		 [1000, 200],
		 [1600, 200],
		 [2000, 200]])
	for i in range(len(ramp)):
		frequency = ramp[i][0]
		micros = int(500000 / frequency)
		print(micros, " = ", micros & 225, " , ", end=" ")


def nearest_ten(x):
	return int(np.round(x / 10.0)) * 10



#
def lcm(values):
	## input is a set
	if values and 0 not in values:
		n = n0 = max(values)
		print()
		values.remove(n)
		while any(n % m for m in values):
			n += n0
		return n
	return 0

print(lcm([5,10,20,7]))