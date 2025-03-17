import time

from serial import SerialException
from utils.connections.serialCommunication import SerialCommunication
from utils.validation import Validation


class TigerUUT(object):
    SYSTEM_RX_MODE = 'SYS_RX'
    SYSTEM_CW_MODE = 'SYS_CW'
    SUPPORTED_SYS_STATES = [SYSTEM_CW_MODE, SYSTEM_RX_MODE]

    def __init__(self, port_name = 'COM33', baud_rate = 115200):
        self.port_name = port_name
        self.baudrate = baud_rate
        self.connection = SerialCommunication(self.port_name, baud_rate)
        self.validate_uut_is_on()

    def validate_uut_is_on(self, timeout = 10):
        self.print_to_log('Validating if UUT is on..')
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                self.print_to_log('trying to get version from uut..')
                resp = self.connection.send_receive('GetVersion\r\n')
                if resp.__contains__('Version:'):
                    self.print_to_log('UUT is up!')
                    break
                else:
                    time.sleep(1)
            except SerialException:
                time.sleep(1)
        else:
            self.print_to_log('UUT is not up after {} seconds, please check your uut manually and validate your setup.'.format(timeout))
            raise UUTConnectionException('UUT is not up after {} seconds, please check your uut manually and validate your setup.'.format(timeout))

    def get_version(self):
        self.print_to_log('Getting UUT version..')
        resp = self.connection.send_receive('GetVersion\r\n')
        self.print_to_log('UUT version is {}'.format(resp))
        return resp

    def set_system_mode(self, mode):
        self.print_to_log('Moving system to {} mode..'.format(mode))
        Validation.validate_elements_in_list('System Mode', [mode], self.SUPPORTED_SYS_STATES)
        self.connection.send('system state {}'.format(mode))
        Validation.check_identical_value('System mode', self.get_system_mode(), mode, cast=str)
        self.print_to_log('UUT system mode is {}'.format(self.get_system_mode()))

    def get_system_mode(self):
        self.print_to_log('getting system mode..')
        resp = self.connection.send_receive('get system mode\r\n')
        self.print_to_log('System mode is {}'.format(resp))
        return resp

    def transmit_cw(self, frequency = 1000000):
        self.print_to_log('Transmit CW..')
        self.connection.send('CW {}\r\n'.format(frequency))
        self.print_to_log('UUT is transmitting CW')

    def close(self):
        self.print_to_log('Closng..')
        self.connection.close()
        self.print_to_log('Closed!')

    def print_to_log(self, msg):
        print(self._format_msg(msg))

    def _format_msg(self, msg):
        return 'TigerUUT({}) : {}'.format(self.port_name, msg)


class UUTConnectionException(Exception):
    pass