

class libera_interlocks:
    def __init__(self, llrf_controller):
        self.llrf_controller = llrf_controller

    @property
    def libera_interlocks_ok(self):
        # Check The 'interlock' on the Libera panel
        if self.llrf_controller.interlockActive():
            print('RF LIBERA interlock active')
            return False
        # Check The RF output
        if self.llrf_controller.RFOutput() is False:
            print('LIBERA RF Output is Set to OFF ')
            return False
        # Check the FF lock (check box)
        if self.llrf_controller.isFFNotLocked():
            print('LIBERA FF NOT locked')
            return False

