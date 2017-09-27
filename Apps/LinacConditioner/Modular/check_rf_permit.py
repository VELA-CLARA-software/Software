import sys
# from PyQt4.QtCore import *
from PyQt4.QtGui import *
from check_conditioning import *

class check_rf_permit(check_conditioning):

    def __init__(self, pv='CLA-L01-RF-PROTE-01:Cmi', *args, **kwargs):
        super(check_rf_permit, self).__init__(pv=pv, *args, **kwargs)
        self.timer.timeout.connect(self.check_RF_permit_is_good)

    def check_RF_permit_is_good(self):
        self.getLatestValue()
        print 'self.latest_values = ', self.latest_values
        if not self.latest_values == self.alarm:
            self.setAlarm()
        else:
            self.clearAlarm()

def main():
    app = QApplication(sys.argv)
    vac = check_rf_permit()
    sys.exit(app.exec_())

if __name__ == '__main__':
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
