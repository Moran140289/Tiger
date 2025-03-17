
class CmwStates():
    ON = "ON"
    OFF = "OFF"
    
    supported_states = [ON, OFF]


class CmwSpecialWLANMessages():
    CLIENT_ASSOCIATED = "ASS"
    PER_FINISHED = "RDY,ADJ,INV"
    PER_NOT_FINISHED = "RUN,ADJ,ACT"
    PER_SETUP_ERROR = "OFF,INV,INV"


class CmwChannels():
    CMW_CH1 = "1"
    CMW_CH2 = "2"
    CMW_CH3 = "3"
    CMW_CH4 = "4"
    
    supported_channels = [CMW_CH1, CMW_CH2, CMW_CH3, CMW_CH4] #delete and add signaling channels


class CmwRMCdomains():
    CS_DOMAIN = "CS"
    PS_DOMAIN = "PS"

    supported_rmc_domains = [CS_DOMAIN, PS_DOMAIN]


class CmwRFPaths():
    RF1_COM = "RF1C"
    RF2_COM = "RF2C"
    RF3_COM = "RF3C"
    RF4_COM = "RF4C"
    
    RF1_OUT = "RF1O"
    RF3_OUT = "RF3O"
    
    RX1_CONVERTER = "RX1"
    RX2_CONVERTER = "RX2"
    RX3_CONVERTER = "RX3"
    RX4_CONVERTER = "RX4"
    
    TX1_CONVERTER = "TX1"
    TX2_CONVERTER = "TX2"
    TX3_CONVERTER = "TX3"
    TX4_CONVERTER = "TX4"
    
    
    supported_rf_paths = [RF1_COM, RF2_COM, RF3_COM, RF4_COM, RF1_OUT, RF3_OUT, RX1_CONVERTER, RX2_CONVERTER, RX3_CONVERTER, RX4_CONVERTER, TX1_CONVERTER, TX2_CONVERTER, TX3_CONVERTER, TX4_CONVERTER]


class CmwAttDirections():
    OUTPUT = "OUTP"
    INPUT = "INP"

    supported_att_directions = [OUTPUT, INPUT]


class CmwAttValues():
    MIN_ATT = 0
    MAX_ATT = 100
    supported_att_values = range(MIN_ATT,MAX_ATT)


class CmwPowerRange():
    MIN_POWER = -120
    MAX_POWER = 40
    supported_power_range = range(MIN_POWER,MAX_POWER)

class CmwWLANChannels():
    WLAN_BROADCAST_CHANNEL_MIN = 1
    WLAN_BROADCAST_CHANNEL_MAX = 196
    
    supported_wlan_channels = range(1,197)

class CmwWLANOperationMode():
    ACCESS_POINT = "AP"
    STATION = "STAT"

    supported_wlan_operation_modes = [ACCESS_POINT, STATION]

class CmwWLANAPPower():
    AP_POWER_MIN = -100.0
    AP_POWER_MAX = +30.0

class CmwWLANStandards():
    W80211A = "ASTD" #802.11a
    W80211B = "BSTD" #802.11b
    W80211G = "GSTD" #802.11g
    W80211GO = "GOST" #802.11g - ofdm
    W80211NGF = "NGFS" #802.11n(GF)
    W80211AN = "ANST" #802.11a
    W80211GN = "GNST" #802.11g/n
    W80211GON = "GONS" #802.11g(OFDM)/n
    W80211AC = "ACST" #802.11ac
    
    supported_wlan_standards = [W80211A, W80211B, W80211G, W80211GO, W80211NGF, W80211AN, W80211GN, W80211GON, W80211AC]

class CmwWLANSecurityModes():
    DISABLED = "DIS" 
    WPA_PERSONAL = "WPER"
    WPA_ENTERPRISE = "WENT"
    WPA2_PERSONAL = "W2P"
    WPA2_ENTERPRISE = "W2EN"
    
    supported_wlan_security_modes = [DISABLED, WPA_PERSONAL, WPA_ENTERPRISE, WPA2_PERSONAL, WPA2_ENTERPRISE]
    
class CmwWLANIPTypes():
    IPV6 = "IPV6"
    IPV4 = "IPV4"
    
    supported_ip_types = [IPV6, IPV4]
