from PyQt4.QtCore import QTimer
from PyQt4.QtCore import QThread
from PyQt4.QtCore import pyqtSignal
# The 'monitor' is a base class designed to be used for monitoring
# parameters in a a separate Qthread.
# It has a timer that can be used to check the status
# of something - so after instantiation you must call start on it (!)
# you should overload cooldown_function in the child class

class monitor(QThread):
    # is the monitor in cooldown or not?
    _in_cooldown = False
    def __init__(self, update_time = 100, cooldown_time = 5000, timed_cooldown = False, level_cooldown = True):
        QThread.__init__(self)
        self.update_time = update_time
        self.cool_down_time = cooldown_time
        self.timer = QTimer()
        # for timed_cooldown we have a timer
        self.cooldown_timer = QTimer()
        self.cooldown_timer.setSingleShot(True)
        self.cooldown_timer.timeout.connect(self.cooldown_function)
        # wec have 2 cooldown modes
        if timed_cooldown:
            self.set_timed_cooldown()
        if level_cooldown:
            self.set_level_cooldown()

    # a timed cooldown will set not ibnn_cooldown = false a set time after an event
    def set_timed_cooldown(self):
        self.timed_cooldown = True
        self.level_cooldown = False

    # a timed cooldown will set not ibnn_cooldown = false a set time after an event
    def set_level_cooldown(self):
        self.timed_cooldown = False
        self.level_cooldown = True

    # you should probably overload this in child class
    def cooldown_function(self):
        print 'monitor function called, cool down ended'
        self.incool_down = False

    def set_cooldown_mode(self,mode):
        if mode == 'LEVEL':
            self.set_level_cooldown()
        elif mode == 'TIMED':
            self.set_timed_cooldown()
        else:
            self.set_level_cooldown()
