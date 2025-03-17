
import serial
import time


class SerialCommunication(serial.Serial):
    RETRY = 2

    def __init__(self, port_name, baud_rate=19200, timeout=1):

        serial.Serial.__init__(self, port=port_name, baudrate=baud_rate, timeout=timeout)
        self.flushInput()
        self.flushOutput()
        self.send(b'')

    def send(self, message, time_to_wait=0.1):
        message = message if type(message) == bytes else message.encode()
        self.flushInput()
        self.flushOutput()
        self.write(message)
        time.sleep(time_to_wait)  # Sleep was made in order to let the 'send' command get the device

    def send_receive(self, message, time_to_wait=0.1, eol=False):
        retry = 0
        response = None
        while (response == None or response == "") and retry < self.RETRY:
            self.send(message)
            time.sleep(time_to_wait)
            if eol:
                response = self.receive_until_EOL()
                if response == None or response == "":
                    time.sleep(time_to_wait)
                    response = self.receive_until_EOL()
            else:
                response = self.receive()
                if response == None or response == "":
                    time.sleep(time_to_wait)
                    response = self.receive()
            retry += 1

        return response

    def receive(self, block_size=None, timeout=5.0):
        start_time = time.time()
        while (self.inWaiting() < block_size) and (time.time() - start_time < timeout):
            time.sleep(0.1)
        if self.inWaiting() >= block_size:
            data = self.read(block_size)
            data = data.decode("iso-8859-1")
        else:
            self.log_manager.log_info_msg(
                "Serial Connection on port '%s': Failed to read %s characters from serial buffer after %s sec" % (
                self.port_name, block_size, timeout))
            data = None
        return data


