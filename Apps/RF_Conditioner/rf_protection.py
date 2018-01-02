from monitor import monitor
import VELA_CLARA_RF_Protection_Control

# This class runs in a separate Qthread
# so after instantiation you must call start on it (!)
# At the moment its a very small simple class,
# we may increase what it can do (i.e. reset the protection)
# at a later date

class rf_protection(monitor):
    init = VELA_CLARA_RF_Protection_Control.init()
    init.setQuiet()

    def __init__(self,controller_type,gui_dict,gui_dict_key):
        monitor.__init__(self)
        self.gui_dict = [gui_dict]
        self.gui_dict_key = gui_dict_key
        self.init_controller(controller_type)


    def init_controller(self,controller_type):
        if controller_type == 'L01': # MAGIC_STRING future proofing
            a = None
        else:
            self.prot_control = self.init.physical_Gun_Protection_Controller()
            self.prot_object = [self.prot_control.getRFProtObjConstRef(controller_type)]
            self.gui_dict[0][self.gui_dict_key] = self.prot_object[0].status

