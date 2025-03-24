

class TigerBaseTest():
    '''
    This Class should contain all the shared funcs and procedures for all tests.
    '''

    def print_to_log(self, msg):
        print(self._format_msg(msg))
        self.logger.info(msg)

