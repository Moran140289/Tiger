import time
import visa


class VisaCommunication(object):

    def __init__(self, port_name):
        rm = visa.ResourceManager('')
        self.visa_instrument = rm.open_resource(port_name)
        self.port_name = port_name

    def send(self, message, time_to_wait = 0.1):
        '''
        Send the message to the the device.
        @param message: message to send
        @param time_to_wait: time to wait after sending the message 
        '''
        self.visa_instrument.write(message)
        time.sleep(time_to_wait)
    
    def receive(self):
        '''
        Returns a string sent from the device to the computer
        '''
        return self.visa_instrument.read()

    def send_receive(self, message, time_to_wait = 0.1):
        '''
        Sends the string message to the device and returns the answer string from the device.
        @param message: message to send
        @param time_to_wait: time to wait after sending the message, before reading the answer.
        '''
        self.send(message)
        if time_to_wait > 0:
            time.sleep(time_to_wait)
        return self.receive()

    def recieve_until_str(self, str_to_wait, timeout = 0):
        '''
        Get the string sent from the device to the computer till reaching a givven string.
        @param str_to_wait: the "end" string
        @param timeout: not relevant for GPIB connection      
        '''
        return self.visa_instrument.read(termination = str_to_wait)
        
    def close(self):
        self.visa_instrument.close()

