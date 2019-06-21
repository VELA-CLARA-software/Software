from PyQt4.QtCore import QTimer
from PyQt4.QtCore import QObject

from VELA_CLARA_LLRF_Control import LLRF_TYPE
# The 'monitor' is a base class designed to be used for monitoring
# parameters in a a separate Qthread.
# It has a timer that can be used to check the status
# of something - so after instantiation you must call start on it (!)
# you should overload cooldown_function in the child class
import numbers
#from VELA_CLARA_enums import STATE
from src.base.base import base


class monitor(QObject,base):
    # name
    my_name = 'monitor'
    # is the monitor in cooldown or not?
    _in_cooldown = False
    # flag to denote whether sanity checks etc have worked
    set_success = True
    def __init__(self,
                 update_time=100,
                 cooldown_time=5000,
                 timed_cooldown=False,
                 level_cooldown=True,
                 no_cooldown=False
            ):
        QObject.__init__(self)
        base.__init__(self)
        self.timed_cooldown = None
        self.level_cooldown = None
        self.no_cooldown = None
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
        if no_cooldown:
            self.set_no_cooldown()


    # a timed cooldown will set not ibnn_cooldown = false a set time after an event
    def set_timed_cooldown(self):
        self.timed_cooldown = True
        self.level_cooldown = False
        self.no_cooldown = False

    # a timed cooldown will set not ibnn_cooldown = false a set time after an event
    def set_level_cooldown(self):
        self.timed_cooldown = False
        self.level_cooldown = True
        self.no_cooldown = False

    def set_no_cooldown(self):
        self.timed_cooldown = False
        self.level_cooldown = True
        self.no_cooldown = False

    # you should probably overload this in child class
    def cooldown_function(self):
        base.logger.message(self.my_name + 'monitor function called, cool down ended')
        self.incool_down = False

    def set_cooldown_mode(self,mode):
        if mode == 'LEVEL':#MAGIC_STRING
            self.set_level_cooldown()
        elif mode == 'TIMED':#MAGIC_STRING
            self.set_timed_cooldown()
        elif mode == 'LEVEL_NO_SPIKE':#MAGIC_STRING
            self.set_no_cooldown()
        else:
            self.set_level_cooldown()

    def sanity_checks(self, items):
        i = 0
        for item in items:
            if not isinstance(item, numbers.Real):
                base.logger.message(self.my_name,' item ', i, ' failed sanity check',True)
                i+=1
                self.set_success = False
        return self.set_success

    def llrf_type_string(self):
        if monitor.llrf_type == LLRF_TYPE.CLARA_HRRG:
            return 'CLARA_HRRG'
        elif monitor.llrf_type == LLRF_TYPE.CLARA_LRRG:
            return 'CLARA_LRRG'
        elif monitor.llrf_type == LLRF_TYPE.VELA_HRRG:
            return 'VELA_HRRG'
        elif monitor.llrf_type == LLRF_TYPE.VELA_LRRG:
            return 'VELA_LRRG'
        elif monitor.llrf_type == LLRF_TYPE.L01:
            return 'L01'
        elif monitor.llrf_type == LLRF_TYPE.UNKNOWN_TYPE:
            base.logger.message(self.my_name + ' llrf_type_string ERROR llrf_type UNKNOWN',True)
            return False
        else:
            return False