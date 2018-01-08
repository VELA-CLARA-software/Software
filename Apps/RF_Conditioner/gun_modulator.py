from monitor import monitor
import VELA_CLARA_RF_Modulator_Control

# This class runs in a separate Qthread
# so after instantiation you must call start on it (!)
# At the moment its a very small simple class,
# we may increase what it can do (i.e. reset the mod)
# at a later date

class gun_modulator(monitor):
    init = VELA_CLARA_RF_Modulator_Control.init()
    init.setQuiet()

    def __init__(self,param,gui_dict,gui_dict_key):
        monitor.__init__(self)
        self.param = param
        self.gui_dict = [gui_dict]
        self.gui_dict_key = gui_dict_key
        self.gun = self.init.physical_GUN_MOD_Controller()
        self.mod = [self.gun.getGunObjConstRef()]
        self.gui_dict[0][self.gui_dict_key] = self.mod[0].state
        print 'gun_modulator'
        print 'gun_modulator'
        print 'gun_modulator'
        print 'gun_modulator'
        print 'gun_modulator'
        print 'gun_modulator'
        print 'gun_modulator'
        print 'gun_modulator'

