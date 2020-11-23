from data_monitors.monitor import monitor
from PyQt5.QtCore import QTimer
import data.charge_measurement_data_base as dat
import numpy

class llrf_monitor(monitor):
    # whoami
    my_name = 'llrf_monitor'
    set_success = False
    # a history of the values when not in cooldown
    # (beware: during startup, all values are added to this list!)
    _value_history = []
    # the latest signal value

    def __init__(self):
        self.my_name = 'llrf_monitor'
        self.bunch_charge = 0
        # init base-class
        monitor.__init__(self,update_time=1000)

        self.check_llrf_is_monitoring()
        self.timer = QTimer()
        #self.timer.timeout.connect(self.update_rf_values)

        self.set_success = True
        #self.timer.start(self.update_time)

        self.run()
        self.llrf_key_to_pv = {}
        self.llrf_key_to_pv.update({monitor.config.llrf_config['GUN_KLYSTRON_POWER']: dat.kly_fwd_pwr_values})
        self.llrf_key_to_pv.update({monitor.config.llrf_config['GUN_CAVITY_POWER']: dat.gun_fwd_pwr_values})
        self.llrf_key_to_pv.update({monitor.config.llrf_config['GUN_PHASE_SP']: dat.gun_pha_sp_values})
        self.llrf_key_to_pv.update({monitor.config.llrf_config['GUN_PHASE_FF']: dat.gun_pha_ff_values})
        self.llrf_key_to_pv.update(
            {monitor.config.llrf_config['GUN_PHASE_FF_LOCK_STATE']: dat.gun_pha_ff_lock_values})


    def run(self):
        # now we're ready to start the timer, (could be called from a function)
        # item = [self.bunch_charge]
        # if self.sanity_checks(item):
        #     self.timer.start(self.update_time)
        #     monitor.logger.message(self.my_name, ' STARTED running')
        #     self.set_good()
        # else:
        monitor.logger.message(self.my_name, ' STARTED running')

    def update_rf_values(self, hwp):
        monitor.data.values[dat.kly_fwd_pwr_values][hwp] = monitor.llrf_objects[
            monitor.config.llrf_config['GUN_KLYSTRON_POWER']].getBuffer()
        monitor.data.values[dat.gun_fwd_pwr_values][hwp] = monitor.llrf_objects[
            monitor.config.llrf_config['GUN_CAVITY_POWER']].getBuffer()
        monitor.data.values[dat.gun_pha_sp_values][hwp] = monitor.llrf_objects[
            monitor.config.llrf_config['GUN_PHASE_SP']].getBuffer()
        monitor.data.values[dat.gun_pha_ff_values][hwp] = monitor.llrf_objects[
            monitor.config.llrf_config['GUN_PHASE_FF']].getBuffer()
        monitor.data.values[dat.gun_pha_ff_lock_values][hwp] = monitor.llrf_objects[monitor.config.llrf_config[
            'GUN_PHASE_FF_LOCK_STATE']].getValue()
        monitor.data.values[dat.off_crest_phase_dict][hwp] = monitor.data.values[dat.off_crest_phase]
        monitor.data.values[dat.kly_fwd_pwr_mean][hwp] = numpy.mean(monitor.data.values[dat.kly_fwd_pwr_values][hwp])
        monitor.data.values[dat.gun_fwd_pwr_mean][hwp] = numpy.mean(monitor.data.values[dat.gun_fwd_pwr_values][hwp])
        monitor.data.values[dat.gun_pha_sp_mean][hwp] = numpy.mean(monitor.data.values[dat.gun_pha_sp_values][hwp])
        monitor.data.values[dat.gun_pha_ff_mean][hwp] = numpy.mean(monitor.data.values[dat.gun_pha_ff_values][hwp])
        monitor.data.values[dat.kly_fwd_pwr_stderr][hwp] = numpy.std(
            monitor.data.values[dat.kly_fwd_pwr_values][hwp]) / numpy.sqrt(
            len(monitor.data.values[dat.kly_fwd_pwr_values][hwp]))
        monitor.data.values[dat.gun_fwd_pwr_stderr][hwp] = numpy.std(
            monitor.data.values[dat.gun_fwd_pwr_values][hwp]) / numpy.sqrt(
            len(monitor.data.values[dat.gun_fwd_pwr_values][hwp]))
        monitor.data.values[dat.gun_pha_sp_stderr][hwp] = numpy.std(
            monitor.data.values[dat.gun_pha_sp_values][hwp]) / numpy.sqrt(
            len(monitor.data.values[dat.gun_pha_sp_values][hwp]))
        monitor.data.values[dat.gun_pha_ff_stderr][hwp] = numpy.std(
            monitor.data.values[dat.gun_pha_ff_values][hwp]) / numpy.sqrt(
            len(monitor.data.values[dat.gun_pha_ff_values][hwp]))


    def check_llrf_is_monitoring(self):
        pass
        # charge_buffer = monitor.charge_control.getChargeBuffer(monitor.config.charge_config['CHARGE_DIAG_TYPE'])
        # if len(charge_buffer) > 1:
        #     if charge_buffer[-1] != charge_buffer[-2]:
        #         monitor.data.values[dat.charge_status] = True
        # else:
        #     monitor.data.values[dat.charge_status] = False
