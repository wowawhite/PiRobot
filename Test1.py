#!/usr/bin/python3
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
