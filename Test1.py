import Inheritance_Konto1 as konto
import Inheritance1 as erstesahne
"""
k1 = konto.GirokontoMitTagesumsatz("Heinz Meier", 567123, 12350.0)
k2 = konto.GirokontoMitTagesumsatz("Heinz Meier", 567123, 12350.0)
if k1.geldtransfer(k2, 160): print("ok")
"""

Name1 = "Bernd"
Name2 = "Heinz"
Name3 = "Marie"
Name4 = "Anna"



a = 1
b = 2
c = 3
d = 4
e = 5
f = 6
g = 7
h = 8


#print(erstesahne.SuperClass().foo_calculate(c,d))


class ExampleClass():
	def __init__(self, name = Name1):
		self.MCP = None #some kind of object?

	global _OPERATION_TYPE_
	_OPERATION_TYPE_ = ['continuous', 'time', 'angle', 'steps']


	def some_foo(self, input):

		self.MCP.MCP.output_pins(input)
		#should enable the hardware pins

	def another_foo(self):
		# running dict is of format {MOTOR_NAME: operation_type}
		# of all motors that are currently running on this MCP
		running_dict = {}
		# pulse dict is of format {STEP_PIN: pulse_micros}
		# of all motors that are currently running in cont
		pulse_dict = {}
		# device list is a list of all motors running in continuous mode
		device_list = []

		for name, device in self.MCP.devices.items():
			if (device.driver and device.driver == 'A4988'):
				if device.operation_type in _OPERATION_TYPE_:
					running_dict[name] = device.operation_type
				if device.operation_type == 'continuous':
					pulse_dict[device.pins['STEP']] = device.continuous_pulse_delay
					device_list.append(device)
		return running_dict, pulse_dict, device_list


class MCP():
	def __init__(self):
		#somestuff


		self.devices = {'Key1': 1, 'Key2': 2, 'Key3': 3}

	def items(self, name, devices):
		return name, devices

"""
tuple
thistuple = ("apple", "banana", "cherry")

d = {'a':1, 'b':2, 'c':3}
list(d)          # ['a', 'b', 'c']             the keys
list(d.keys())   # ['a', 'b', 'c']             the keys
list(d.values()) # [1, 2, 3]                   the values
list(d.items())  # [('a',1), ('b',2), ('c',3)] a tuple of (key, value)

check
https://stackoverflow.com/questions/24531931/python-dict-with-three-values-in-the-for-loop

"""