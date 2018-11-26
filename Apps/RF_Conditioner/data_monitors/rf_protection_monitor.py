from state_monitor import state_monitor
import data.rf_condition_data_base as dat
# At the moment its a very small simple class,
# we may increase what it can do (i.e. reset the protection)
# at a later date
#
class rf_protection_monitor(state_monitor):
    # whoami
    my_name = 'rf_protection_monitor'
    old_value = None
    def __init__(self):
        state_monitor.__init__(self, update_time=state_monitor.config.rfprot_config['RF_PROT_CHECK_TIME'])
        if state_monitor.prot_control:
            self.prot_object = [state_monitor.prot_control.getRFProtObjConstRef(self.llrf_type_string())]
            self.start()
            self.set_success = True
        else:
            self.set_success = False


    def check(self):
        #print('Checking rf protection state')
        if self.set_success:
            state_monitor.data.values[dat.rfprot_state] = self.prot_object[0].status
