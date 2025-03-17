
import time

from ATE.cmw.consts import CmwChannels, CmwWLANSecurityModes, CmwWLANIPTypes, CmwWLANChannels, CmwWLANStandards, \
    CmwWLANAPPower, CmwRMCdomains, CmwSpecialWLANMessages, CmwWLANOperationMode, CmwPowerRange, CmwRFPaths, \
    CmwAttDirections
from ATE.cmw.modules.protocol import CmwProtocol
from utils.validation import Validation


class WLAN(CmwProtocol):
    
    QUERY_IS_RF_ON = "SOUR:WLAN:SIGN{}:STAT?"
    CMD_SET_EXT_ATTENUATION = "CONF:{}:SIGN{}:RFS:EATT:{} {}"
    QUERY_SET_EXT_ATTENUATION = "CONF:{}:SIGN{}:RFS:EATT:{}?"
    CMD_SET_CHANNEL_STATE = "SOUR:{}:SIGN{}:STAT {}"
    QUERY_SET_CHANNEL_STATE = "SOUR:{}:SIGN{}:STAT?"

    def __init__(self, connection, port_name):
        CmwProtocol.__init__(self, connection, port_name)
        self.interface_name = "WLAN"
    
    def _format_msg(self, msg):
        return "CMW500 ({}) (WLAN): {}".format(self.port_name, msg)

    def set_security_and_password(self, channel, security_mode, last_digit_password = 0):
        '''
        Sets wlan security mode, and the last digit of the password. (at the cmw you can only configure the last digit of 1234567x - x is the last digit. example: 12345673 - the last digit is 3. 
        this procedure must be done when the signaling channel state is OFF. 
        @param channel(CmwChannels): string represents needed channel 
        @param security_mode(CmwWLANSecurityModes): the type of security mode
        @param last_digit_password(int): the last digit of the password you want - relevant only to WPA or WPER
        @raise ConfigException: in case that the sign channel state is ON 
        @return: No return value
        '''
        Validation.validate_elements_in_list("Channel", channel, CmwChannels.supported_channels)
        Validation.validate_elements_in_list("Security last digit password", last_digit_password, range(0, 10))
        Validation.validate_elements_in_list("Security mode", security_mode, CmwWLANSecurityModes.supported_wlan_security_modes)
        self.print_to_log("Configuring at signaling channel{} security mode to {} and last digit password to {}".format(channel, security_mode, last_digit_password))
        if not self.is_rf_on(channel):
            self.connection.send('CONF:WLAN:SIGN{}:CONN:SEC:TYPE {}, "{}"'.format(channel, security_mode, last_digit_password))
            ans = self.connection.send_receive("CONF:WLAN:SIGN{}:CONN:SEC:TYPE?".format(channel))
            Validation.check_identical_value("WLAN security and password at signaling ch{}".format(channel), ans, security_mode + "," +'{}'.format(last_digit_password), str)
        else:
            self.print_to_log("The Security config failed! please turn Off the RF!!")
            raise Exception("The WLAN security and password at signaling channel {} wernet been configured because the channel is ON!. please turn OFF the channel.".format(channel))
            
    def set_ssid(self, channel, ssid):
        '''
        sets the wlan ssid. 
        @param channel(CmwChannels): string represents needed channel 
        @param ssid (str): the wnated name of the AP 
        @raise ConfigException: in case that the configure failed. 
        @return: No return value
        '''
        Validation.validate_elements_in_list("Channel", channel, CmwChannels.supported_channels)
        self.print_to_log("Configuring WLAN CH{} SSID to {}".format(channel, ssid))
        self.connection.send("CONF:WLAN:SIGN{}:CONN:SSID {}".format(channel, ssid))
        Validation.check_identical_value("SSID at signaling ch{}".format(channel), self.connection.send_receive("CONF:WLAN:SIGN{}:CONN:SSID?".format(channel)), ssid, str)
        
    def get_client_ipv4_address(self, channel):
        return self._get_client_ip_address(channel, CmwWLANIPTypes.IPV4)
    
    def get_client_ipv6_address(self, channel):
        return self._get_client_ip_address(channel, CmwWLANIPTypes.IPV6)

    def _get_client_ip_address(self, channel, ip_type):
        '''
        gets the IPV4 address of the associated client 
        @param channel(CmwChannels): string represents needed channel 
        @return: the IPV4 address
        '''
        Validation.validate_elements_in_list("Channel", channel, CmwChannels.supported_channels)
        Validation.validate_elements_in_list("Ip Type", ip_type, CmwWLANIPTypes.supported_ip_types)
        self.print_to_log("Checking if the client is associated to signaling channel {}...".format(channel))
        if self.is_client_associated(channel):
            self.print_to_log("Getting the client {} address, that associated to signaling channel{}".format(channel, ip_type))
            value = self.connection.send_receive("SENS:WLAN:SIGN{}:UES:UEAD:{}?".format(channel, ip_type))
            ip_addr = str(value).replace('"', "")
            return ip_addr
        else:
            self.print_to_log("The Client isnt associated to the WLAN AP!")
            raise Exception("The Client isnt associated!")

    def get_client_mac_address(self, channel):
        '''
        gets the MAC address of the associated client 
        @param channel(CmwChannels): string represents needed channel 
        @return: the MAC address
        '''
        Validation.validate_elements_in_list("Channel", channel, CmwChannels.supported_channels)
        self.print_to_log("Checking if the client is associated to signaling channel {}...".format(channel))
        if self.is_client_associated(channel):
            self.print_to_log("Getting the client MAC address, that associated to signaling channel{}".format(channel))
            value = self.connection.send_receive("SENS:WLAN:SIGN{}:UEC:MAC:ADDR?".format(channel))
            mac = str(value).replace('"', "")
            return mac
        else:
            self.print_to_log("The Client isnt associated to the WLAN AP!")
            raise Exception("The Client isnt associated!")

    def get_event_log_messages(self, channel):
        '''
        gets the WLAN signaling channel event log 
        @param channel(CmwChannels): string represents needed channel 
        @return(list): Log messgaes
        '''
        Validation.validate_elements_in_list("Channel", channel, CmwChannels.supported_channels)
        self.print_to_log("Getting the event log from signaling channel{}".format(channel))
        log = str(self.connection.send_receive("SENS:WLAN:SIGN{}:ELOG:ALL?".format(channel)).rstrip())
        full_log = log.split(',')
        for row in full_log:
            if row == ("EMPT") or  ('""'):
                full_log.remove(row)
        return full_log

    def set_broadcast_channel(self, channel, wlan_broadcast_channel):
        '''
        sets the wifi channel and spiecific signaling channel 
        @param channel(CmwChannels): string represents needed channel 
        @param wlan_broadcast_channel(CmwWLANChannels): int represents needed channel 
        @return: No return value
        '''
        Validation.validate_elements_in_list("Channel", channel, CmwChannels.supported_channels)
        Validation.validate_limits_min_max(wlan_broadcast_channel, CmwWLANChannels.WLAN_BROADCAST_CHANNEL_MIN, CmwWLANChannels.WLAN_BROADCAST_CHANNEL_MAX, int)
        self.print_to_log("Configuring WLAN signaling channel {} broadcast wifi channel to {}".format(channel, wlan_broadcast_channel))
        self.connection.send("CONF:WLAN:SIGN{}:RFS:CHAN {}".format(channel, wlan_broadcast_channel))
        Validation.check_identical_value("WLAN broadcast channel at signaling ch{}".format(channel), self.connection.send_receive("CONF:WLAN:SIGN{}:RFS:CHAN?".format(channel)), wlan_broadcast_channel, str)
                
    def set_stadnard(self, channel, wlan_standard):
        '''
        sets the wlan wifi standard (like 802.11a etc).
        @param channel(CmwChannels): string represents needed channel 
        @param wlan_standard(CmwWLANStandards): float represents the wanted wifi standard. 
        @return: No return value
        '''
        Validation.validate_elements_in_list("Channel", channel, CmwChannels.supported_channels)
        Validation.validate_elements_in_list("WLAN Standard", wlan_standard, CmwWLANStandards.supported_wlan_standards)
        self.print_to_log("configuring the WLAN Standard at signaling channel {} to {}".format(channel, wlan_standard))
        self.connection.send("CONF:WLAN:SIGN{}:CONN:STAN {}".format(channel, wlan_standard))
        Validation.check_identical_value("WLAN Standard at signaling ch{}".format(channel), self.connection.send_receive("CONF:WLAN:SIGN{}:CONN:STAN?".format(channel)), wlan_standard, str)
        
    def set_AP_power(self, channel, power):
        '''
        configures the AP Power.
        @param channel(CmwChannels): string represents needed channel 
        @param power(int or float): the power value  
        @raise ConfigException: in case that the configure failed.  
        @return: No return value
        '''
        Validation.validate_elements_in_list("Channel", channel, CmwChannels.supported_channels)
        Validation.validate_limits_min_max(power, CmwWLANAPPower.AP_POWER_MIN, CmwWLANAPPower.AP_POWER_MAX, float)
        self.print_to_log("Setting the AP Power channel {} to {}".format(channel, power))
        self.connection.send("CONF:WLAN:SIGN{}:RFS:BOP {}".format(channel, power))
        Validation.check_identical_value("AP Power  at signaling ch{}".format(channel), float(self.connection.send_receive("CONF:WLAN:SIGN{}:RFS:BOP?".format(channel))), float(power), float)
    
    def set_frequency(self, channel, freq):
        '''
        configures the AP frequency.
        @param channel(CmwChannels): string represents needed channel 
        @param freq(float): the freq value at Hz  
        @raise ConfigException: in case that the configure failed.  
        @return: No return value
        '''
        Validation.validate_elements_in_list("Channel", channel, CmwChannels.supported_channels)
        self.connection.send("CONF:WLAN:SIGN{}:RFS:FREQ {}".format(channel, freq))
        self.print_to_log("Setting the AP frequency channel {} to {}".format(channel, freq))
        Validation.check_identical_value("Frequency at signaling ch{}".format(channel), self.connection.send_receive("CONF:WLAN:SIGN{}:RFS:FREQ?".format(channel)), freq, float)
    
    def is_client_associated(self, channel, domain = CmwRMCdomains.PS_DOMAIN, timeout = 20):
        '''
        checks if the client is associated.
        @param channel(CmwChannels): string represents needed channel 
        @param domain(CmwRMCdomains): the type of domain   
        @param timeout(int): timeout in seconds
        @return: if associated - true of false (boolean)
        '''
        Validation.validate_elements_in_list("Channel", channel, CmwChannels.supported_channels)        
        Validation.validate_elements_in_list("Domain", domain, CmwRMCdomains.supported_rmc_domains)
        self.print_to_log("Checking if client is associated at signaling channel {} - {} domain".format(channel, domain))
        try:
            self._wait_for_state(CmwSpecialWLANMessages.CLIENT_ASSOCIATED, "FETC:WLAN:SIGN{}:{}W:STAT?".format(channel, domain), "Client is Associated!!", "Client isnt Associated at signaling channel {}, {} domain".format(channel, domain), 0.1, timeout)
            is_associated = True
        except: 
            self.print_to_log("Client isnt Associated at signaling channel {}, {} domain".format(channel, domain))
            is_associated = False
            
        return is_associated
    
    def _validate_client_associated(self, channel, domain = CmwRMCdomains.PS_DOMAIN, timeout = 20):
        '''
        validate that the client is associated.
        @param channel(CmwChannels): string represents needed channel 
        @param domain(CmwRMCdomains): the type of domain   
        @param timeout(int): timeout in seconds
        '''
        Validation.validate_elements_in_list("Channel", channel, CmwChannels.supported_channels)        
        Validation.validate_elements_in_list("Domain", domain, CmwRMCdomains.supported_rmc_domains)
        self.print_to_log("Checking if client is associated at signaling channel {} - {} domain".format(channel, domain))
        self._wait_for_state(CmwSpecialWLANMessages.CLIENT_ASSOCIATED, "FETC:WLAN:SIGN{}:{}W:STAT?".format(channel, domain), "Client is Associated!!", "Client isnt Associated at signaling channel {}, {} domain".format(channel, domain), 0.1, timeout)
        
    def disconnect(self, channel):
        '''
        disconnect the client from the AP
        @param channel(CmwChannels): string represents needed channel 
        @return: No return value
        '''
        Validation.validate_elements_in_list("Channel", channel, CmwChannels.supported_channels)        
        self.print_to_log("Disconnecting at signaling channel{}".format(channel))
        self.connection.send("CALL:WLAN:SIGN{}:ACT:DISC".format(channel))
        if not self.is_client_associated(channel):
            self.print_to_log("The Client is disconnected from the WLAN AP")
        else: 
            self.print_to_log("Client is still associated at signaling channel {}..".format(channel))
            raise Exception(self._format_msg("Client is still associated at signaling channel {}..".format(channel)))
    
    def set_operation_mode(self, channel, operation_mode):
        '''
        sets the wlan operation mode. 
        @param channel(CmwChannels): string represents needed channel 
        @param operation_mode(CmwWLANOperationMode): string represents wanted op mode. 
        @raise ConfigException: in case that the configure failed.
        @return: No return value
        '''
        Validation.validate_elements_in_list("Channel", channel, CmwChannels.supported_channels)        
        Validation.validate_elements_in_list("Operation Mode", operation_mode, CmwWLANOperationMode.supported_wlan_operation_modes)
        self.print_to_log("Setting the operation mode at signaling channel{} to {}".format(channel, operation_mode))
        self.connection.send("CONF:WLAN:SIGN{}:CONN:OMOD {}".format(channel, operation_mode))
        Validation.check_identical_value("Operation mode at signaling ch{}".format(channel), self.connection.send_receive("CONF:WLAN:SIGN{}:CONN:OMOD?".format(channel)), operation_mode, str)

    def get_client_max_power(self, channel, timeout = 20):
        '''
        gets the associated max power of the client.
        @param channel(CmwChannels): string represents needed channel 
        @param timeout(int): timeout in seconds
        @raise ConfigException: in case that the client isnt associated. 
        @return: is associated - the UE max power
        '''        
        Validation.validate_elements_in_list("Channel", channel, CmwChannels.supported_channels)        
        if self.is_client_associated(channel):
            self.print_to_log("Getting client Power at signaling channel {}..".format(channel))
            power = float(self.connection.send_receive("SENS:WLAN:SIGN{}:UES:RXBP?".format(channel)).rstrip())
            self.print_to_log("The Client Power is {}dbm".format(str(power)))
            return power
        else: 
            self.print_to_log("The Client isnt Associated to the WLAN AP!")
            raise Exception("The Client isnt Associated to the WLAN AP!")

    def ext_set_approximate_rx_burst_power(self, channel, power):
        '''
        sets the approximate RX Burst power at a spiecific signaling channel by fixing the PEP power
        @param channel(CmwChannels): string represents needed channel 
        @param power(float): float represents the wanted power. 
        @return: No return value
        '''
        Validation.validate_limits_min_max(power, CmwPowerRange.MIN_POWER, CmwPowerRange.MAX_POWER, float)
        Validation.validate_elements_in_list("Channel", channel, CmwChannels.supported_channels)
        self.print_to_log("Setting the BS Power channel {} to {}".format(channel, power))
        self._set_epep_power(channel, power)
        self.print_to_log("Getting the aproximate RX Burst Power from signaling channel {} ".format(channel))
        app_rx_burst_power = self._get_approximate_rx_burst_power(channel)
        self.print_to_log("Fixing the aproximate RX Burst Power to {} at signaling channel {}.".format(power, channel))
        self._set_epep_power(channel, float(power) + abs(float(app_rx_burst_power - power)))
        Validation.check_identical_value("WLAN approximate rx burst channel at signaling ch{}".format(channel), float(self.connection.send_receive("SENS:WLAN:SIGN{}:UES:ARXB?".format(channel)).rstrip()), power, float)
    
    def _get_approximate_rx_burst_power(self, channel):
        Validation.validate_elements_in_list("Channel", channel, CmwChannels.supported_channels)
        self.print_to_log("Getting the approximate rx burst power at channel {}".format(channel))
        return float(self.connection.send_receive("SENS:WLAN:SIGN{}:UES:ARXB?".format(channel)).rstrip())
        
    def _set_epep_power(self, channel, power):
        Validation.validate_limits_min_max(power, CmwPowerRange.MIN_POWER, CmwPowerRange.MAX_POWER, float)
        Validation.validate_elements_in_list("Channel", channel, CmwChannels.supported_channels)
        self.print_to_log("Setting the EPEP Power channel {} to {}".format(channel, power))
        self.connection.send("CONF:WLAN:SIGN{}:RFS:EPEP {}".format(channel, power))
    
    def _initiate_test(self, channel, start_power, stop_power, deviation, transport_blocks_amount, PER_threshold):
        ap_power = start_power
        per_measured = 0
        self.print_to_log("Start PER procedure in signaling channel {}..".format(channel))
        self.print_to_log("\n The start AP power is : {}dbm\n The Stop power is : {}dbm\n The deviation is : {}DB\n "
                          "The amount of transported packets is : {}\n The PER threshold is : {}%\n"
                          .format(start_power, stop_power, deviation, transport_blocks_amount, PER_threshold))
        self._configure_packets_amount(channel, transport_blocks_amount)
        return ap_power, per_measured
    
    def _configure_packets_amount(self, channel, transport_blocks_amount):
        Validation.validate_elements_in_list("Channel", channel, CmwChannels.supported_channels)
        self.print_to_log("Configure packets to {} in signaling channel {}..".format(transport_blocks_amount, channel))
        self.connection.send("CONF:WLAN:SIGN{}:PER:PACK {}".format(channel, transport_blocks_amount))
        ans = self.connection.send_receive("CONF:WLAN:SIGN{}:PER:PACK?".format(channel))
        Validation.check_identical_value("Packets at signaling ch{}".format(channel), ans, transport_blocks_amount, int)
        
    def _get_per(self, channel):
        per_list = self.connection.send_receive("FETC:WLAN:SIGN{}:PER?".format(channel))
        self._abort_per(channel)
        values = per_list.split(',')
        per_measured = eval(values[1])
        return per_measured
    
    def _abort_per(self, channel):
        Validation.validate_elements_in_list("Channel", channel, CmwChannels.supported_channels)
        self.print_to_log("Aborting PER in signaling channel {}".format(channel))
        self.connection.send("ABORT:WLAN:SIGN{}:PER".format(channel))
    
    def _transport_packets(self, channel, timeout = 300):
        self._start_per(channel)
        
        start = time.time()
        while (time.time() - start < timeout):
            if self._is_per_finished(channel):
                self.print_to_log("PER finished..")
                break
            else: 
                self.print_to_log("PER isnt ready, collecting measurements")
                time.sleep(2)
        else:
            self.print_to_log("Timeout reached, and per isnt finished!")
            raise Exception("Timeout reached, and per isnt finished!")
    
    def _start_per(self, channel):
        Validation.validate_elements_in_list("Channel", channel, CmwChannels.supported_channels)
        self.print_to_log("Starting transport packets in signaling channel {}".format(channel))
        self.connection.send("INIT:WLAN:SIGN{}:PER".format(channel))
    
    def _is_per_finished(self, channel):
        Validation.validate_elements_in_list("Channel", channel, CmwChannels.supported_channels)        
        self.print_to_log("Checking PER status in signaling channel{}".format(channel))
        ans = self.connection.send_receive("FETC:WLAN:SIGN{}:PER:STAT:ALL?".format(channel)).rstrip()
        if ans == CmwSpecialWLANMessages.PER_FINISHED:
            self.print_to_log("PER finished..")
            return True
        elif ans == CmwSpecialWLANMessages.PER_NOT_FINISHED:
            self.print_to_log("PER not finished..")
            return False 
        else:
            self.print_to_log("{} is not a valid answer for PER status".format(ans))
            raise Exception("{} is not a valid answer for PER status".format(ans))
        
    def ext_get_sesetivity_threshold(self, channel, start_power, stop_power, deviation = 0.5, transport_blocks_amount = 500, PER_threshold = 8.0, transport_timeout = 300):
        '''
        gets the sensetivity of the client. 
        @param channel(CmwChannels): string represents needed channel
        @param start_power(float): the start power 
        @param stop_power(float): the stop power 
        @param deviation(float): the deviation. 
        @param timeout(int): timeout in seconds
        @param PER_threshold(float): the PER threshold
        @raise ConfigException: in case that the configure failed.
        @return: the sensetivity threshold value.
        '''
        Validation.validate_elements_in_list("Channel", channel, CmwChannels.supported_channels)        
        ap_power, per_measured = self._initiate_test(channel, start_power, stop_power, deviation, transport_blocks_amount, PER_threshold)
        self._validate_client_associated(channel)
        while (ap_power >= stop_power):
            self.set_AP_power(channel, ap_power)
            time.sleep(1)
            if not self.is_client_associated(channel):
                self.print_to_log("Client isnt Associated - the client disconnected after updating the AP power to {}".format(ap_power))
                return ap_power + deviation
            self._transport_packets(channel, transport_timeout)
            per_measured = self._get_per(channel)
            if per_measured >= PER_threshold:
                self.print_to_log("The Sensetivity threshold is {}, per value is {}".format(ap_power, per_measured))
                return ap_power + deviation
            else:
                self.print_to_log("The BS power is {}, PER measured is {}, still smaller than PER threshold ({}%)".format(ap_power, per_measured, PER_threshold))
                ap_power = ap_power - deviation
        else: 
            self.print_to_log("BS Power is {} and the stop power is {}, and the PER that have been measured is still smaller than {}.".format(ap_power, stop_power, PER_threshold))
            raise Exception("BS Power is {} and the stop power is {}, and the PER that have been measured is still smaller than {}.".format(ap_power, stop_power, PER_threshold))                    

    def ext_config_wlan_scenario(self, output_connector = CmwRFPaths.RF1_COM, rx_converter = CmwRFPaths.RX1_CONVERTER, tx_converter = CmwRFPaths.TX1_CONVERTER, wifi_standard = CmwWLANStandards.W80211AC, ext_attenuation=0, ap_power = -60, approximate_burst_power = -17.0, freq_channel = 1):
        '''
        ext config for wlan - configes the RF path, the the RF converter, the wifi standard, ext attenuation, app burst power, AP power, and freq channel. 
        @param output_connector = represents the physical output connector - CmwRFPaths.RF<1..4>_COM 
        @param rx_converter = represents the physical output rx converter - if you choose RF1COM or RF3COM - rx connector is 1/3, and if you choose RF2COM or RF4COM - rx connector is 2/4
        @param tx_converter = represents the physical output tx converter - if you choose RF1COM or RF3COM - tx connector is 1/3, and if you choose RF2COM or RF4COM - tx connector is 2/4 
        @param wifi_standard = wifi legacy standard - you need to choose yout standard from the supported standards that are in consts.CmwWLANStandards 
        @param ext_attenuation - float that represents the cable/wireless attenuation. 
        @param ap_power - float that represents the Access point power level. 
        @param approximate_burst_power - float that represents the approximate_burst_power in the cmw configuration. 
        @param freq_channel - the freq channel represents the frequency that we will trnasmit - channel 1 = 2.412Ghz, channel 64 = 5.320 Ghz
        '''
        self.config_standard_cell_scenario(CmwChannels.CMW_CH1, output_connector, rx_converter, output_connector, tx_converter)
        self.set_stadnard(CmwChannels.CMW_CH1, wifi_standard)
        self.set_ext_attenuation(CmwChannels.CMW_CH1, ext_attenuation, CmwAttDirections.INPUT)
        self.set_ext_attenuation(CmwChannels.CMW_CH1, ext_attenuation, CmwAttDirections.OUTPUT)
        self.set_AP_power(CmwChannels.CMW_CH1, ap_power)
        self.ext_set_approximate_rx_burst_power(CmwChannels.CMW_CH1, approximate_burst_power)
        self.set_broadcast_channel(CmwChannels.CMW_CH1, freq_channel)
