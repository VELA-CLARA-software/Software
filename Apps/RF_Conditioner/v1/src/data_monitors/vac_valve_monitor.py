from state_monitor import state_monitor
from VELA_CLARA_LLRF_Control import LLRF_TYPE
from VELA_CLARA_Vac_Valve_Control import VALVE_STATE
import src.data.rf_condition_data_base as dat
# At the moment its a very small simple class,
# we may increase what it can do (i.e. reset the protection)
# at a later date
#
class vac_valve_monitor(state_monitor):
    # whoami
    my_name = 'vac_valve_monitor'
    old_value = None
    def __init__(self):
        state_monitor.__init__(self, update_time=state_monitor.config.vac_valve_config['VAC_VALVE_CHECK_TIME'])# MAGIC


        self.local_valve_control = state_monitor.valve_control

        self.valve_name = state_monitor.config.vac_valve_config['VAC_VALVE']

        self.valve_obj = [self.local_valve_control.getVacValveObjConstRef( self.valve_name )]# MAGIC
        self.keep_valve_open = state_monitor.config.vac_valve_config['KEEP_VALVE_OPEN']# MAGIC
        #self.local_valve_control.openVacValve(self.valve_name)
        self.start()
        self.set_success = True

    def check(self):
        #print 'checkng valve state'
        state_monitor.data.values[dat.vac_valve_status] =  self.valve_obj[0].vacValveState
        if vac_valve_monitor.old_value !=  self.valve_obj[0].vacValveState:
            if self.valve_obj[0].vacValveState == VALVE_STATE.VALVE_OPEN:
                self.alarm('valve open')
            elif self.valve_obj[0].vacValveState == VALVE_STATE.VALVE_CLOSED:
                self.alarm('valve closed')
            vac_valve_monitor.old_value = self.valve_obj[0].vacValveState

        if self.keep_valve_open:
            if self.valve_obj[0].vacValveState == VALVE_STATE.VALVE_CLOSED:
                self.local_valve_control.openVacValve(self.valve_name)





