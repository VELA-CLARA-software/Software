from monitor import monitor
from VELA_CLARA_enums import STATE
from PyQt4.QtCore import QTimer
import data.bpm_attenuation_calibrate_data_base as dat
import numpy
import time

class scope_monitor(monitor):
    # whoami
    my_name = 'scope_monitor'
    set_success = False
    # a history of the values when not in cooldown
    # (beware: during startup, all values are added to this list!)
    _value_history = []
    # the latest signal value

    def __init__(self):
        self.my_name = 'scope_monitor'
        self.bunch_charge = 0
        # init base-class
        monitor.__init__(self,update_time=1000)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_bunch_charge)

        self.set_success = True
        self.timer.start(self.update_time)

        self.check_scope_is_monitoring()
        self.run()

    def run(self):
        # now we're ready to start the timer, (could be called from a function)
        # item = [self.bunch_charge]
        # if self.sanity_checks(item):
        #     self.timer.start(self.update_time)
        #     monitor.logger.message(self.my_name, ' STARTED running')
        #     self.set_good()
        # else:
        monitor.logger.message(self.my_name, ' NOT STARTED running')

    def check_scope_is_monitoring(self):
        num_data_buffer = monitor.scope_control.getScopeNumBuffer(monitor.config.scope_config['SCOPE_NAME'][0], monitor.config.scope_config['SCOPE_CHANNEL'])
        if len(num_data_buffer) > 1:
            if num_data_buffer[-1] != num_data_buffer[-2]:
                monitor.data.values[dat.scope_status] = True
        else:
            monitor.data.values[dat.scope_status] = False

    def update_bunch_charge(self):
        monitor.data.values[dat.scope_values] = []
        monitor.data.values[dat.scope_values] = monitor.scope_control.getScopeNumBuffer(monitor.config.scope_config['SCOPE_NAME'][0], monitor.config.scope_config['SCOPE_CHANNEL'])
        monitor.data.values[dat.bunch_charge] = numpy.mean(monitor.data.values[dat.scope_values])
