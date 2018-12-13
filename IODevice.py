class IODevice():
	def __init__(self):()

	self, name = _NAME_, pins = _PINS_,
	degree_per_step = _DEGREE_PER_STEP_,
	max_rpm = _MAX_RPM_, GPIO = None, pigpio = None,
	pigpio_pi = None, ** kwargs):

	#das soll in IODevice rein?
	IODevice.__init__(self, name=name, dtype='Stepper Motors',
	display = True, GPIO = GPIO,
	pigpio = pigpio, pigpio_pi = pigpio_pi)


#unbekannte

	_OPERATION_TYPE_
	_DIRECTION_DICT_

	def set_resolution(self, resolution):
	pass

	def get_motor_running_dict(self):
		# running dict is of format {MOTOR_NAME: operation_type}
		# of all motors that are currently running on this MCP
		# MCP = None
		running_dict = {}
		# pulse dict is of format {STEP_PIN: pulse_micros}
		# of all motors that are currently running in cont
		pulse_dict = {}
		# device list is a list of all motors running in continuous mode
		device_list = []
		for name, device in self.MCP.devices.items():
			if (device.driver and device.driver == 'DRV8825'):
				if device.operation_type in _OPERATION_TYPE_:
					running_dict[name] = device.operation_type
				if device.operation_type == 'continuous':
					pulse_dict[device.pins['STEP']] = device.continuous_pulse_delay
					device_list.append(device)
		return running_dict, pulse_dict, device_list

