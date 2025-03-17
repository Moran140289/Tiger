from ATE.cmw.modules.wlan import WLAN
from utils.connections.visaCommunication import VisaCommunication


class CMW500(object):
    
    def __init__(self, port_name):
        self.port_name = port_name
        self.connection = VisaCommunication(port_name)
        self.wlan = WLAN(self.connection, port_name)
        
    def preset(self):
        self.print_to_log(self._format_msg("Reset all.."))
        self.connection.send("SYST:PRES:ALL")
        self.print_to_log(self._format_msg("Reset Finished!"))
        
    def close(self):
        self.connection.close()
        self.print_to_log(self._format_msg("Closed"))

    def print_to_log(self, msg):
        print(self._format_msg(msg))

    def _format_msg(self, msg):
        return 'R&S CMW500({}) : {}'.format(self.port_name, msg)


if __name__ == "__main__":  
    cmw = CMW500('GPIB::18::INSTR')
    cmw.wlan.ext_config_wlan_scenario()

