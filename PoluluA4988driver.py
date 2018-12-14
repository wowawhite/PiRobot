#!/usr/bin/python3
# from https://raspberrypi.stackexchange.com/questions/88724/add-pulse-object-to-transmitting-pigpio-waveform
from IODevice import IODevice
import numpy as np
import time

_MODE0_ = 0
_MODE1_ = 1
_MODE2_ = 2
_DECAY_ = 3
_DIR_ = 20
_STEP_ = 21 ## must be a Pi GPIO pin
_nENBL_ = 6
_nRESET_ = 7
_nSLEEP_ = 8

_PINS_ = {
        'MODE0': _MODE0_,
        'MODE1': _MODE1_,
        'MODE2': _MODE2_,
        'DECAY': _DECAY_,
        'DIR': _DIR_,
        'STEP': _STEP_,
        'nENBL': _nENBL_,
        'nRESET': _nRESET_,
        'nSLEEP': _nSLEEP_,
        }

_DEGREE_PER_STEP_ = 1.8

_MAX_RPM_ = 100

_NAME_ = 'stepper motor'

class StepperMotorA4988(IODevice):
    def __init__(self, name = _NAME_, pins = _PINS_,
                 degree_per_step = _DEGREE_PER_STEP_,
                 max_rpm = _MAX_RPM_, GPIO = None, pigpio = None,
                 pigpio_pi = None, **kwargs):

        IODevice.__init__(self, name = name, dtype = 'Stepper Motors',
                           display = True, GPIO = GPIO,
                           pigpio = pigpio, pigpio_pi = pigpio_pi)
#motor parameters from where?
        self.MCP = None #MCP = motion control product?/parameter?
        self.driver = 'A4988'
        self.pins = pins
        self.degree_per_step = degree_per_step
        self.max_rpm = max_rpm
        self.rpm = 0
        self.direction = 'stopped'
        self.resolution = None
        self.waveform_id = None
        self.waveform = None
        self.continuous_pulse_delay = None
        self.operation_type = None

    global _OPERATION_TYPE_
    _OPERATION_TYPE_ = ['continuous', 'time', 'angle', 'steps']

    global _DIRECTION_DICT_
    _DIRECTION_DICT_ = {'forward': True,
                        'reverse': False}

    def set_resolution(self, resolution):
        """ method to set step resolution """

        resolution_dict = {
                  1.0: {self.pins['MODE0']: False,
                           self.pins['MODE1']: False,
                           self.pins['MODE2']: False},
                  2.0: {self.pins['MODE0']: True,
                           self.pins['MODE1']: False,
                           self.pins['MODE2']: False},
                  4.0: {self.pins['MODE0']: False,
                          self.pins['MODE1']: True,
                          self.pins['MODE2']: False},
                  8.0: {self.pins['MODE0']: True,
                          self.pins['MODE1']: True,
                          self.pins['MODE2']: False},
                  16.0: {self.pins['MODE0']: False,
                           self.pins['MODE1']: False,
                           self.pins['MODE2']: True},
                  32.0: {self.pins['MODE0']: True,
                           self.pins['MODE1']: False,
                           self.pins['MODE2']: True}
                  }

        # error check stepmode
        if resolution in resolution_dict:
            pass
        else:
            print("Invalid resolution: {}".format(resolution))
            quit()

        self.MCP.MCP.output_pins(resolution_dict[resolution])
        self.resolution = resolution
        time.sleep(0.05)

    def calc_pwm_frequency(self, resolution, rpm):
        """ method to calculate pulse frequency in Hz for desired rpm and res """
        if rpm > float(self.max_rpm):
            print('Entered rpm exceeds limit. Setting rpm to: ' + str(self.max_rpm))
            rpm = self.max_rpm
        freq = float(rpm) * 360. * float(resolution) / ( 60. * float(self.degree_per_step) )
        return float(freq), rpm

    def calc_actual_rpm(self, resolution, pulse_delay):
        """ method to calculate actual rpm from pulse_delay in micros """
        # pulse_delay is half the total period of a total cycle
        freq = 1. / (2. * pulse_delay) * 1E6
        actual_rpm = float(freq) / ( 360. * float(resolution) ) *  ( 60. * float(self.degree_per_step) )
        return float(actual_rpm)

    def calc_angle_steps(self, resolution, angle):
        """ method to calculate number of steps for a given angle and resolution """
        steps = resolution * self.degree_per_step
        return float(steps)

    def operate_motor_finite(self, direction, resolution, rpm,
                      duration = {'type': 'time', 'value': 5},
                      setup_delay = 0.2):

        # get list of running motors
        motor_running_dict, pulse_dict, device_list = self.get_motor_running_dict()
        if bool(motor_running_dict):
            print("Can't operate motor in finite stepping mode when another motor is \
                  running.")
            return

        if direction not in _DIRECTION_DICT_.keys():
            raise ValueError('direction must be one of: %r.' % _DIRECTION_DICT_.keys())

        if duration['type'] not in [x for x in _OPERATION_TYPE_ if x != 'continuous']:
            raise ValueError('direction must be one of: %r.' % [x for x in _OPERATION_TYPE_ if x != 'continuous'])

        # set enable pin to low to allow for output
        self.set_output({self.pins['nENBL']: False})
        # set direction
        self.set_output({self.pins['DIR']: _DIRECTION_DICT_[direction]})
        # set resolution
        self.set_resolution(resolution)
        # calculate pwm frequency
        freq, rpm = self.calc_pwm_frequency(resolution, rpm)
        pulse_delay = 1. / (2. * freq) * 1E6 ## microseconds
        # set RPi STEP pin to pigpio output
        self.pigpio_pi.set_mode(self.pins['STEP'], self.pigpio.OUTPUT)
        # setup delay wait
        time.sleep(setup_delay)

        duration_type, duration_value = map(duration.get, ('type', 'value'))

        self.rpm = self.calc_actual_rpm(self.resolution, pulse_delay)
        self.direction = direction
        self.operation_type = duration_type

        if duration_type == 'time':
            waveform = []
            waveform.append(self.pigpio.pulse(1<<self.pins['STEP'], 0, int(pulse_delay)))
            waveform.append(self.pigpio.pulse(0, 1<<self.pins['STEP'], int(pulse_delay)))
            self.pigpio_pi.wave_clear() # clear any existing waveforms
            self.pigpio_pi.wave_add_generic(waveform)
            waveform_id = self.pigpio_pi.wave_create() # create and save id
            self.waveform_id = waveform_id
            self.pigpio_pi.wave_send_repeat(waveform_id)
            time_start = time.time()
            while time.time() - time_start <= duration_value:
                time.sleep(0.1)
            self.pigpio_pi.wave_tx_stop() # stop waveform

        if (duration_type == 'steps' or duration_type == 'angle'):
            if duration_type == 'angle':
                steps = self.calc_angle_steps(resolution, duration_value)
                duration_value = steps
            steps_to_do = duration_value
            while steps_to_do > 0:
                waveform = []
                n_max = 1000 if steps_to_do > 1000 else int(steps_to_do)
                for i in range(n_max):
                    waveform.append(self.pigpio.pulse(1<<self.pins['STEP'], 0, int(pulse_delay)))
                    waveform.append(self.pigpio.pulse(0, 1<<self.pins['STEP'], int(pulse_delay)))
                self.pigpio_pi.wave_add_generic(waveform)
                waveform_id = self.pigpio_pi.wave_create() # create and save id
                self.waveform_id = waveform_id
                self.pigpio_pi.wave_send_once(waveform_id)
                while self.pigpio_pi.wave_tx_busy(): # wait for waveform to be sent
                    time.sleep(0.1)
                self.pigpio_pi.wave_delete(self.waveform_id)
                steps_to_do = steps_to_do - n_max

        # cleanup
        self.stop_motor()

    def operate_motor_continuous(self, direction, resolution, rpm, setup_delay = 0.2):

        if direction not in _DIRECTION_DICT_.keys():
            raise ValueError('direction must be one of: %r.' % _DIRECTION_DICT_.keys())

        # enable
        self.set_output({self.pins['nENBL']: False})
        # set direction
        self.set_output({self.pins['DIR']: _DIRECTION_DICT_[direction]})
        # set resolution
        self.set_resolution(resolution)
        # calculate pwm frequency
        freq, rpm = self.calc_pwm_frequency(resolution, rpm)
        pulse_delay = self.nearest_ten( 1. / (2. * freq) * 1E6 ) ## microseconds
        self.pigpio_pi.set_mode(self.pins['STEP'], self.pigpio.OUTPUT)
        # setup delay wait
        time.sleep(setup_delay)

        # must set object's operation type and
        # continuous_pulse_delay prior to getting pulse_dict
        self.operation_type = 'continuous'
        self.continuous_pulse_delay = pulse_delay

        motor_running_dict, pulse_dict, device_list = self.get_motor_running_dict()

        if bool(motor_running_dict):
            if not all(v == 'continuous' for v in motor_running_dict.values()):
                print("Can't operate motor continuously when another motor is \
                      running in non-continuous mode.")
                return

        new_waveform = self.splice_waveform(pulse_dict)
        print('new waveform length: ' + str(len(new_waveform)))
        for p in new_waveform[0:10]:
            print(p.__dict__)
        new_waveform_id = self.waveform_transition(new_waveform)
        self.update_waveforms(device_list, new_waveform_id, new_waveform)

        self.rpm = self.calc_actual_rpm(self.resolution, pulse_delay)
        self.direction = direction

    def waveform_transition(self, new_waveform):
        old_waveform_id = self.pigpio_pi.wave_tx_at()
        if old_waveform_id in [9998, 9999]: old_waveform_id = None
        self.pigpio_pi.wave_add_generic(new_waveform)
        # create and save id
        new_waveform_id = self.pigpio_pi.wave_create()
        # It is then safe to delete the old wave.
        if old_waveform_id:
            self.pigpio_pi.wave_send_using_mode(
                new_waveform_id, self.pigpio.WAVE_MODE_REPEAT_SYNC)
            # Spin until the new wave has started.
            while self.pigpio_pi.wave_tx_at() != new_waveform_id:
                pass
            self.pigpio_pi.wave_delete(old_waveform_id)
        else:
            self.pigpio_pi.wave_send_repeat(new_waveform_id)
        return new_waveform_id

    def change_motor_speed(self, rpm):

        if self.operation_type != 'continuous':
            raise ValueError('Unable to change speed of motor that is not \
                             operating in continuous mode.')

        # calculate pwm frequency
        freq, rpm = self.calc_pwm_frequency(self.resolution, rpm)
        pulse_delay = self.nearest_ten( 1. / (2. * freq) * 1E6 ) ## microseconds

        self.continuous_pulse_delay = pulse_delay

        # get list of running motors
        motor_running_dict, pulse_dict, device_list = self.get_motor_running_dict()
        if bool(motor_running_dict):
            if not all(v == 'continuous' for v in motor_running_dict.values()):
                print("Can't operate motor continuously when another motor is \
                      running in non-continuous mode.")
                return

        new_waveform = self.splice_waveform(pulse_dict)
        new_waveform_id = self.waveform_transition(new_waveform)
        self.update_waveforms(device_list, new_waveform_id, new_waveform)

        self.rpm = self.calc_actual_rpm(self.resolution, pulse_delay)

    def stop_motor(self):
        motor_running_dict, pulse_dict, device_list = self.get_motor_running_dict()
        if (len(motor_running_dict.keys()) == 1 and self.name in motor_running_dict.keys()):
            ## only this motor is running
            self.shutdown()
            self.pigpio_pi.wave_tx_stop()
            self.pigpio_pi.wave_clear()
        else:
            pulse_dict.pop(self.pins['STEP'])
            new_waveform = self.splice_waveform(pulse_dict)
            new_waveform_id = self.waveform_transition(new_waveform)
            device_list.remove(self)
            self.update_waveforms(device_list, new_waveform_id, new_waveform)
        self.shutdown()

    def shutdown(self):
        self.set_output({self.pins['nENBL']: True})
        time.sleep(0.1)
        self.set_output({self.pins['DIR']: False})
        self.set_resolution(1.0)
        self.rpm = 0.
        self.direction = 'stopped'
        self.waveform_id = None
        self.waveform = None
        self.continuous_pulse_delay = None
        self.operation_type = None

    def set_output(self, output_dict):
        self.MCP.MCP.output_pins(output_dict)

    def get_motor_running_dict(self):
        # running dict is of format {MOTOR_NAME: operation_type}
        # of all motors that are currently running on this MCP
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

    def splice_waveform(self, pulse_dict):
        periods = set([int(2 * t) for t in pulse_dict.values()])
        total_length = self.lcm(periods)
        print(total_length)
        action_list = []
        # each row is pin, action (1 or 0), t_action
        for pin in pulse_dict.keys():
            action_list.append([pin, 1, 0.0])
        for pin, pulse in pulse_dict.items():
            for cycles in range(0, int(total_length / (2. * pulse))):
                action_list.append([pin, 0, cycles * 2.*pulse + pulse])
                action_list.append([pin, 1, cycles * 2.*pulse + 2.*pulse])
        action_array = np.array(action_list)
        action_array = action_array[action_array[:,2] < total_length]
        print(action_array)
        action_array = action_array[action_array[:,2].argsort()]
        waveform = []
        for i in range(0, action_array.shape[0] - 1):
            delay = int(action_array[i + 1,2] - action_array[i,2])
            if bool(action_array[i,1]):
                waveform.append(self.pigpio.pulse(1<<int(action_array[i,0]), 0, delay))
            else:
                waveform.append(self.pigpio.pulse(0, 1<<int(action_array[i,0]), delay))
        delay = int(total_length - action_array[-1,2])
        if bool(action_array[-1,1]):
            waveform.append(self.pigpio.pulse(1<<int(action_array[-1,0]), 0, delay))
        else:
            waveform.append(self.pigpio.pulse(0, 1<<int(action_array[-1,0]), delay))
        return waveform

    def update_waveforms(self, device_list, new_waveform_id, new_waveform):
        for device in device_list:
            device.waveform_id = new_waveform_id
            device.waveform = new_waveform

    def lcm(self, values):
        ## input is a set
        if values and 0 not in values:
            n = n0 = max(values)
            values.remove(n)
            while any( n % m for m in values ):
                n += n0
            return n
        return 0

    def nearest_ten(self, x):
        return int(np.round(x / 10.0)) * 10