from utils.connections.visaCommunication import VisaCommunication
from utils.validation import Validation


class SpectrumAnalyzer(object):
    def __init__(self, gpib_address):
        self.gpib_address = gpib_address
        self.connection = VisaCommunication(gpib_address)
        self.check_identity()

    def check_identity(self, spectrum_name = 'Keysight CXA N9000B'):
        self.print_to_log('Checking Spectrum Identity')
        ans = self.connection.send_receive('*IDN?\r\n')
        if ans.__contains__(spectrum_name):
            self.print_to_log('{} Found and connected properly!')
        else:
            self.print_to_log('{} didnt Found!'.format(spectrum_name))
            raise SpectrumNotFoundException('{} didnt Found!'.format(spectrum_name))

    def reset(self):
        '''
        Resets the SA sets all parameters to default
        :return: None
        '''
        self.print_to_log('Resetting..')
        self.connection.send('*RST\r\n')
        self.print_to_log('Reset finished')

    def set_ref_level(self, ref_level_value):
        '''
        sets the ref level and validate the ref after set
        @:param ref_level_value : ref value
        :return:None
        '''
        self.print_to_log('Set Ref level to {}'.format(ref_level_value))
        Validation.validate_input_parameter_in_range('Spectrum Ref level', ref_level_value, -40.0, 60.0)
        self.connection.send('SPEC:REF {}\r\n'.format(ref_level_value))
        Validation.check_identical_value('Ref level', self.connection.send_receive('SPEC:REF?\r\n'), cast=float)
        self.print_to_log('Ref level is {}!'.format(ref_level_value))

    def set_center_frequency(self, center_freq):
        '''
        sets the center freq and validate the center freq after set
        @:param center_freq : center freq
        @:param center_freq : center freq
        :return: None
        '''
        self.print_to_log('Set Center freq to {}'.format(center_freq))
        Validation.validate_input_parameter_in_range('Center Freq', center_freq, 50, 7*1E9)
        self.connection.send('SPEC:CENT {}\r\n'.format(center_freq))
        Validation.check_identical_value('Center freq', self.connection.send_receive('SPEC:CENT?\r\n'), cast=float)
        self.print_to_log('Center freq is {}!'.format(center_freq))

    def set_span(self, span):
        self.print_to_log('Set span to {}'.format(span))
        Validation.validate_input_parameter_in_range('Span', span, 1, 100E6)
        self.connection.send('SPEC:SPAN {}\r\n'.format(span))
        Validation.check_identical_value('Span', self.connection.send_receive('SPEC:SPAN?\r\n'), cast=float)
        self.print_to_log('Span is {}!'.format(span))

    def get_peak(self):
        self.print_to_log('Get peak..')
        resp = float(self.connection.send_receive('SPEC:PEAK? {}\r\n'))
        self.print_to_log('Peak is {}!'.format(resp))
        return resp

    def close(self):
        self.print_to_log('Closing....')
        self.connection.send('CLOS\r\n')
        self.connection.close()
        self.print_to_log('Closed....')

    def print_to_log(self, msg):
        print(self._format_msg(msg))

    def _format_msg(self, msg):
        return 'Keysight CXA N9000B({}) : {}'.format(self.gpib_address, msg)


class SpectrumNotFoundException(Exception):
    pass