import sys
#from PyQt4.QtCore import *
from PyQt4.QtGui import *
from check_conditioning import *

class check_vacuum(check_conditioning_buffer):

    def __init__(self, *args, **kwargs):
        super(check_vacuum, self).__init__(*args, **kwargs)
        self.timer.timeout.connect(self.check_VAC_change_is_small)

    def check_VAC_change_is_small(self):
        self.getLatestValue()
        print 'self.latest_values = ', self.latest_values
        self.delta_VAC = self.latest_values - self.mean
        if self.delta_VAC > self.alarm:
            self.setAlarm()
        else:
            self.clearAlarm()
            self.updateMean()

def main():
    app = QApplication(sys.argv)
    vac = check_vacuum(pv='CLA-S01-VAC-IMG-01:PRES')
    sys.exit(app.exec_())

if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
