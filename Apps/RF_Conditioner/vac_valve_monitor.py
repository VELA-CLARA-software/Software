# base-class
import monitor
from numpy import mean
from PyQt4.QtCore import pyqtSignal
import VELA_CLARA_Vac_Valve_Control as valve_control
from VELA_CLARA_enums import MACHINE_AREA
from VELA_CLARA_enums import MACHINE_MODE


class vac_valve_monitor(monitor.monitor):
    # whoami
    my_name = 'vac_valve_monitor'
    def __init__(self,
                 area,
                 valve,
                 state_dict,
                 state_dict_key,
                 gui_dict,
                 gui_dict_key,
                 update_time
                 ):
        # init base-class
        # super(monitor, self).__init__()
        monitor.monitor.__init__(self)
        self.area = area
        self.valve = valve
        self.state_dict = [state_dict]
        self.gui_dict   = [gui_dict]
        self.state_dict_key = state_dict_key
        self.gui_dict_key   = gui_dict_key
        self.init()

    def init(self):
        try:
            self.area
        except NameError:
            print(self.my_name," ERROR AREA NOT DEFINED!")
        else:
            self.init_controller()

    def init_controller(self):
        self.valve_init = valve_control.init()
        self.valve_init.setQuiet()
        self.valve_controller = self.valve_init.getVacValveController(MACHINE_MODE.PHYSICAL,self.area)

        self.valve_obj = [ self.valve_controller.getVacValveObjConstRef( self.valve) ]

        self.gui_dict[0][self.gui_dict_key] = self.valve_obj[0].vacValveState
        #self.timer.timeout.connect(self.check_valve)
        #self.timer.start(self.update_time)

    def check_valve(self):
        if self.valve_controller.isOpen(self.valve):
            self.state_dict[0][self.state_dict_key] = monitor.state.GOOD
            self.gui_dict[0][self.gui_dict_key] = monitor.state.GOOD
        else:
            self.state_dict[0][self.state_dict_key] = monitor.state.BAD
            self.gui_dict[0][self.gui_dict_key] = monitor.state.BAD