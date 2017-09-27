import epics, sys, signal
# import numpy as np
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class updaetRFPV(QObject):

    def __init__(self, parent=None):
        super(updaetRFPV, self).__init__(parent)

        self.timepv = epics.PV('CLA-GUN-LRF-CTRL-01:app:time_vector')
        self.llrfpv = epics.PV('CLA-GUN-LRF-CTRL-01:ad1:ch4:power_remote.POWER')
        self.scopepv = epics.PV('EBT-INJ-SCOPE-01:P4')

        self.RF_time_to_sample = 1.125

        self.timer = QTimer()
        self.timer.timeout.connect(self.updatePV)
        self.timer.start(1000/10)

    def updatePV(self):
        time = self.timepv.get()
        timearraypos = min(range(len(time)), key=lambda i: abs(time[i]-self.RF_time_to_sample))
        val = self.llrfpv.get()
        self.scopepv.put(val[timearraypos])

def sigint_handler(*args):
    """Handler for the SIGINT signal."""
    QCoreApplication.quit()

def main():
    signal.signal(signal.SIGINT, sigint_handler)
    app = QCoreApplication(sys.argv)
    rfupdate = updaetRFPV()
    # gc.gc.updateLatestValues()
    #gc.gc.getRepRate()
    # gc.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()
