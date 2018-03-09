# At the moment its a very small simple class,
# we may increase what it can do (i.e. reset the mod)
# at a later date
from state_monitor import state_monitor
import data.rf_condition_data_base as dat
from VELA_CLARA_RF_Modulator_Control import GUN_MOD_STATE

# At the moment its a very small simple class,
# we may increase what it can do (i.e. reset the protection)
# at a later date
#
class modulator_monitor(state_monitor):
    # whoami
    my_name = 'modulator_monitor'
    def __init__(self):
        state_monitor.__init__(self, update_time=state_monitor.config.mod_config['MOD_CHECK_TIME'])
        self.mod = [state_monitor.mod_control.getGunObjConstRef()]
        self.start()
        self.set_success = True

    def check(self):
        #print('Checking mod state ' + str(self.mod[0].state))
        state_monitor.data.values[dat.modulator_state] =  self.mod[0].state



