import sys, os, numpy
#from PyQt4.QtCore import *
from PyQt4.QtGui import *
from check_conditioning import *

os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
os.environ["EPICS_CA_SERVER_PORT"]="6000"

dataarray = range(0,1016)

epics.caput('VM-CLA-GUN-LRF-CTRL-01:ad1:ch1:power_remote',  numpy.random.rand(1016))

class check_rf_rev_power(check_conditioning_buffer):

    def __init__(self, *args, **kwargs):
        super(check_rf_rev_power, self).__init__(*args, **kwargs)
        self.timer.timeout.connect(self.check_LLRF_rev_power_is_low)

    def check_LLRF_rev_power_is_low(self):
        epics.caput('VM-CLA-GUN-LRF-CTRL-01:ad1:ch1:power_remote', numpy.random.rand(1016))
        self.getLatestValue()
        if self.max  > self.alarm*self.maxmean:
            self.setAlarm(str(self.max)+'>'+str(self.alarm*self.maxmean))
        else:
            self.clearAlarm()
        self.updateMean()

def main():
    app = QApplication(sys.argv)
    vac = check_rf_rev_power(pv='VM-CLA-GUN-LRF-CTRL-01:ad1:ch1:power_remote', alarm_value=2.0)
    sys.exit(app.exec_())

if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
