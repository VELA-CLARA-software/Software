import PyQt4.QtCore as QtCore
from PyQt4.QtCore import QTimer
from PyQt4.QtCore import QObject
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import QThread

class mask_setter(QThread):

    KFPow = 'KLYSTRON_FORWARD_POWER'
    CRPow = 'CAVITY_REVERSE_POWER'
    CRPha = 'CAVITY_REVERSE_PHASE'

    def __init__(self, llrf_controller = None, update_time = 50):
        QThread.__init__(self)
        self.llrf_controller = llrf_controller
        self.update_time = update_time
        self.get_timer = QTimer()
        self.get_timer.timeout.connect(self.set_cav_rev_power_mask)
        self.get_timer.start( self.update_time )
        self.llrfObj = [self.llrf_controller.getLLRFObjConstRef()]

    def setNumRollingAverageTraces(self, value ):
        self.llrf_controller.setNumRollingAverageTraces(value)

    # we will need more of these for different traces
    def set_cav_rev_power_mask(self):
        if self.llrfObj[0].trace_data[self.CRPow].rolling_sum_counter > 10: #MAGIC_NUMBER
            # some function to create a mask, make better in future
            # by accessing data in struct instead of passing it
            average = self.llrf_controller.getCavRevPowerAv()
            hi_mask = average + 100
            lo_mask = average - 100
            self.llrf_controller.setHighMask(self.CRPow,hi_mask)
            self.llrf_controller.setLowMask(self.CRPow,lo_mask)





