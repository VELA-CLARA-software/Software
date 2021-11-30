from data_monitors.monitor import monitor
from PyQt5.QtCore import QTimer
import data.charge_measurement_data_base as dat
import numpy

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
        monitor.__init__(self, update_time=1000)

        self.timer = QTimer()
        self.check_charge_is_monitoring()
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

    def get_charge_buffer(self):
        return monitor.charge_factory.getQBuffer(monitor.config.charge_config['WCM_NAME'])

    def check_charge_is_monitoring(self):
        charge_buffer = monitor.charge_factory.getQBuffer(monitor.config.charge_config['WCM_NAME'])
        if len(charge_buffer) > 1:
            if charge_buffer[-1] != charge_buffer[-2]:
                monitor.data.values[dat.charge_status] = True
        else:
            monitor.data.values[dat.charge_status] = False

    def set_buffer_size(self, value):
        monitor.charge_factory.setBufferSize(value)

    def update_charge_values(self, hwp, hwpprev=None):
        monitor.data.values[dat.charge_values][hwp] = monitor.charge_factory.getQBuffer(
            monitor.config.charge_config['WCM_NAME'])
        monitor.data.values[dat.bunch_charge][hwp] = numpy.mean(monitor.data.values[dat.charge_values][hwp])
        self.chargemean = numpy.mean(list(monitor.data.values[dat.charge_values][hwp]))
        if self.chargemean > monitor.config.charge_config['MIN_CHARGE_ACCEPTED']:
            if monitor.data.values[dat.first_measurement]:
                monitor.data.values[dat.charge_mean][hwp] = numpy.mean(list(monitor.data.values[dat.charge_values][hwp]))
                monitor.data.values[dat.charge_stderr][hwp] = numpy.std(
                    list(monitor.data.values[dat.charge_values][hwp])) / numpy.sqrt(
                    len(list(monitor.data.values[dat.charge_values][hwp])))
                return True
            else:
                if self.chargemean > max(list(monitor.data.values[dat.charge_mean].values())):
                    monitor.data.values[dat.charge_mean][hwp] = numpy.mean(
                        list(monitor.data.values[dat.charge_values][hwp]))
                    monitor.data.values[dat.charge_stderr][hwp] = numpy.std(
                        list(monitor.data.values[dat.charge_values][hwp])) / numpy.sqrt(
                        len(list(monitor.data.values[dat.charge_values][hwp])))
                    return True
                else:
                    return False
        else:
            return False


