import time

from ATE.cmw.consts import CmwStates
from utils.validation import Validation
from ATE.cmw.rohdeSchwarzCMW500 import CMW500
from ATE.spectrumAnalyzer import SpectrumAnalyzer
from infra.tigerBastTest import TigerBaseTest
from infra.tigerUUT import TigerUUT


class SystemRFTest(TigerBaseTest):
    CMW_GPIB_ADDRESS = 18
    SPECTRUM_GPIB_ADDRESS = 20
    UUT_COM = 'COM22'
    MIN_PEAK = -10.0
    MAX_PEAK = 20.0
    MIN_SENSE = -75.0
    MAX_SENSE = -78.0

    def get_user_params(self):
        'Get user params from user'

        pass

    def setup(self):
        'Init for all of the test'
        self.print_to_log('Test Setup..')
        self.init_ate_instruments()
        self.init_uut()
        self.init_report()

    def init_ate_instruments(self):
        self.print_to_log('Init instruments')
        self.init_cmw()
        self.init_spectrum_analyzer()

    def init_cmw(self):
        self.print_to_log('Init CMW')
        self.cmw = CMW500(self.CMW_GPIB_ADDRESS)
        self.cmw.preset()

    def init_spectrum_analyzer(self):
        self.print_to_log('Init Spectrum')
        self.spectrum = SpectrumAnalyzer(self.SPECTRUM_GPIB_ADDRESS)
        self.spectrum.reset()

    def _config_spectrum(self):
        self.print_to_log('Config spectrum..')
        self.print_to_log('Here you need to add few commands for configure the spectrum for CW measure..')

    def init_uut(self):
        self.print_to_log('Init uut..')
        self.uut = TigerUUT(self.UUT_COM)

    def init_report(self):
        self.print_to_log('Init report')
        self.print_to_log('Here you need to add CSV file / JSON and add all the data you want to save')
        self.print_to_log('Relevant data: 1. uut_serial_number 2. batch_id 3.fw version 4. test_results(only the relevant), date, pass/fail etc..')

    def body(self):
        self.check_tx_power()

    def check_tx_power(self):
        self.print_to_log('Checking UUT TX power..')
        self.uut.set_system_mode(self.uut.SYSTEM_CW_MODE)
        self.uut.transmit_cw()
        time.sleep(3)
        peak = self.spectrum.get_peak()
        result = Validation.is_limits_min_max(peak, self.MIN_PEAK, self.MAX_PEAK)
        self.print_to_log('Here you need to add the result to the report (numeric and pass/fail)')

    def check_rx_sensetivity(self):
        self.print_to_log('Checking UUT RX Senesetivity..')
        self.cmw.wlan.ext_config_wlan_scenario()
        self.cmw.wlan.set_channel_state(1, CmwStates.ON)
        self.uut.set_system_mode(self.uut.SYSTEM_RX_MODE)
        sens_value = self.cmw.wlan.ext_get_sesetivity_threshold(1, start_power=-70.0, stop_power=-80.0)
        result = Validation.is_limits_min_max(sens_value, self.MIN_SENSE, self.MAX_SENSE)
        self.print_to_log('Here you need to add the result to the report (numeric and pass/fail)')

    def cleanup(self):
        self.close_spectrum()
        self.close_cmw()
        self.close_uut()

    def close_spectrum(self):
        if hasattr(self, 'spectrum'):
            self.spectrum.close()

    def close_cmw(self):
        if hasattr(self, 'cmw'):
            self.cmw.wlan.set_channel_state(1, CmwStates.OFF)
            self.cmw.close()

    def close_uut(self):
        if hasattr(self, 'uut'):
            self.uut.close()

    @staticmethod
    def _format_msg(msg):
        return 'RF Test : {}'.format(msg)