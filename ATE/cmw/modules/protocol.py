

import time
from utils.validation import Validation
from ATE.cmw.consts import CmwChannels, CmwStates, CmwRFPaths, CmwAttDirections, CmwAttValues


class CmwProtocol(object):

    def __init__(self, connection, port_name):
        self.connection = connection
        self.port_name = port_name
        self.check_identity()

    def check_identity(self, spectrum_name = "Rohde&Schwarz,CMW"):
        self.print_to_log('Checking CMW Identity')
        ans = self.connection.send_receive('*IDN?\r\n')
        if ans.__contains__(spectrum_name):
            self.print_to_log('{} Found and connected properly!')
        else:
            self.print_to_log('{} didnt Found!'.format(spectrum_name))
            raise CMWNotFound('{} didnt Found!'.format(spectrum_name))

    def _wait_for_state(self, state, command, success_msg, failure_msg, delay, timeout):
        '''
        timeout procedure - been used in several WCDMA procedurs
        @param trigger: represents the stop trigger - when it accoures, the while will end. 
        @param command : the command that query the ATE in order to check the wanted trigger 
        @param success msg : the msg that will be printed at the log when success. 
        @param failure msg : the msg that will be printed at the log when failure. 
        @param delay : the delay between every loop. 
        @raise timeout: the time limit for all while procedure.  
        @return: No return value
        '''
        start = time.time()
        while time.time() - start < timeout:
            ans = (self.connection.send_receive(command)).rstrip()
            if ans == state :
                self.print_to_log(success_msg)
                break
            else:
                time.sleep(delay)
        else:
            self.print_to_log(failure_msg)
            raise Exception(self._format_msg(failure_msg))
        
    def is_rf_on(self, channel):
        '''
        Sets state of needed channel.
        @param channel(CmwChannels): string represents needed channel 
        @param state(Cmwstates): on/off
        @param timeout(int): timeout in seconds
        @raise ConfigException: in case setting failed 
        @return: 
        '''
        Validation.validate_elements_in_list("Channel",channel, CmwChannels.supported_channels)
        self.print_to_log("Getting {} signaling CH{} state".format(self.interface_name, channel))
        ans = self.connection.send_receive(self.QUERY_IS_RF_ON.format(channel)).rstrip()
        ans = ans.split(',')
        self.print_to_log("{} CH{} state is {}".format(self.interface_name, channel, ans[0]))
        return ans[0] == CmwStates.ON
    
    def config_standard_cell_scenario(self, channel, rx_connector, rx_converter, tx_connector, tx_converter):
        '''
        configures the RF routs at the signaling channel 
        @param channel(CmwChannels): string represents needed channel 
        @param rx_connector: the rx connector 
        @param rx_converter: the rx converter 
        @param tx_connector: the tx connector 
        @param tx_converter: the tx converter 
        @raise ConfigException: in case that the configure failed. 
        @return: No return value
        '''
        Validation.validate_elements_in_list("Channel", channel, CmwChannels.supported_channels)
        Validation.validate_elements_in_list("RF Paths", [rx_connector, rx_converter, tx_connector, tx_converter], CmwRFPaths.supported_rf_paths)
        self.print_to_log("Establishing Standard Cell Scenario configured to: {}, {}, {}, {}".format(rx_connector, rx_converter, tx_connector, tx_converter))
        self.connection.send("ROUT:{}:SIGN{}:SCEN:SCEL {}, {}, {}, {}".format(self.interface_name, channel, rx_connector, rx_converter, tx_connector, tx_converter))
        ans = str(self.connection.send_receive("ROUT:{}:SIGN{}:SCEN:SCEL?".format(self.interface_name, channel)).rstrip())
        path_list = ans.split(',')
        Validation.validate_elements_in_list("RF Paths", path_list, CmwRFPaths.supported_rf_paths)
        self.print_to_log("Standard Cell Scenario configured successfully to: {}, {}, {}, {}".format(path_list[0], path_list[1], path_list[2], path_list[3]))

    def set_ext_attenuation(self, channel, attenuation, direction, tolerance = 0.05):
        '''
        configures the RF external attenuation - output or input 
        @param channel(CmwChannels): string represents needed channel 
        @param attenuation(int or float): the attenuation value. Note that attenuation in this ATE can be max with 2 digits after floating point. (value.xx)   
        @param direction(CmwAttDirections): the attenuation direction - output or input  
        @raise ConfigException: in case that the configure failed. 
        @return: No return value
        '''
        Validation.validate_elements_in_list("Channel", channel, CmwChannels.supported_channels)
        Validation.validate_elements_in_list("Direction", direction, CmwAttDirections.supported_att_directions)
        Validation.validate_limits_min_max(attenuation, CmwAttValues.MIN_ATT, CmwAttValues.MAX_ATT, float)
        self.print_to_log("Configuring {}DB {} attenuation to sign channel{}".format(attenuation , direction, channel))
        self.connection.send(self.CMD_SET_EXT_ATTENUATION.format(self.interface_name, channel, direction, attenuation))
        ans = self.connection.send_receive(self.QUERY_SET_EXT_ATTENUATION.format(self.interface_name, channel, direction))
        Validation.validate_limits_abs_tolerance(ans, attenuation, tolerance, float)
        
    def set_channel_state(self, channel, state, timeout = 30):
        '''
        Sets state of needed channel.
        @param channel(CmwChannels): string represents needed channel 
        @param state(Cmwstates): on/off
        @param timeout(int): timeout in seconds
        @raise ConfigException: in case setting failed 
        @return: No return value
        '''
        Validation.validate_elements_in_list("Channel", channel, CmwChannels.supported_channels)
        Validation.validate_elements_in_list("State", state, CmwStates.supported_states)
        self.print_to_log("Establishing {} CH{} set to {}".format(self.interface_name ,channel, state))
        self.connection.send(self.CMD_SET_CHANNEL_STATE.format(self.interface_name, channel, state))
        self._wait_for_state(state, self.QUERY_SET_CHANNEL_STATE.format(self.interface_name, channel), "{} CH{} set to {} successfully".format(self.interface_name, channel, state), "Failed to set {} signaling channel {} to {} - didnt succeded the turn on!".format(self.interface_name, channel, state), 0.1, timeout)

    def print_to_log(self, msg):
        print(self._format_msg(msg))

    def _format_msg(self, msg):
        return 'Rohde&Schwartz CMW500({}) : {}'.format(self.port_name, msg)


class CMWNotFound(Exception):
    pass