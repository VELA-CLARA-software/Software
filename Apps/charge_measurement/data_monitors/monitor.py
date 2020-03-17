from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QObject
import numbers
from base.base import base

class monitor(QObject,base):
    # name
    my_name = 'monitor'

    set_success = True
    def __init__(self,update_time=100):
        QObject.__init__(self)
        base.__init__(self)
        self.update_time = update_time
        self.timer = QTimer()
