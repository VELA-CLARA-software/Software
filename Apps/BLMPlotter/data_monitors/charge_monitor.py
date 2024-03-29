from monitor import monitor
from PyQt4.QtCore import QTimer
import data.blm_plotter_data_base as dat
import numpy
import time

class charge_monitor(monitor):
    # whoami
    my_name = 'charge_monitor'
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

        self.check_charge_is_monitoring()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_bunch_charge)

        self.set_success = True
        self.timer.start(self.update_time)

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

    def check_charge_is_monitoring(self):
        charge_buffer = monitor.charge_control.getChargeBuffer(monitor.config.charge_config['CHARGE_NAME'])
        if len(charge_buffer) > 1:
            if charge_buffer[-1] != charge_buffer[-2]:
                monitor.data.values[dat.charge_status] = True
        else:
            monitor.data.values[dat.charge_status] = False

    def check_buffer(self):
        if monitor.charge_control.isChargeBufferFull(monitor.config.charge_config['CHARGE_NAME']):
            return True
        else:
            return False

    def update_bunch_charge(self):
        monitor.data.values[dat.charge_values] = []
        monitor.data.values[dat.charge_values] = monitor.charge_control.getChargeBuffer(monitor.config.charge_config['CHARGE_NAME'])
        monitor.data.values[dat.bunch_charge] = numpy.mean(monitor.data.values[dat.charge_values])
