from monitor import monitor
from PyQt4.QtCore import pyqtSignal
from VELA_CLARA_RF_Modulator_Control import GUN_MOD_STATE
#import VELA_CLARA_RF_Modulator_Control as mod
# This class runs in a separate Qthread
# so after instantiation you must call start on it (!)
# Assuming connecting the interface works

class gun_modulator(monitor):

    gunModStateSignal = pyqtSignal(bool)

    def __init__(self, gun_mod_controller, update_time = 100):
        monitor.__init__(self)
        self.gun_mod_controller = gun_mod_controller
        self.modulator = [ self.gun_mod_controller.getGunObjConstRef() ]
        self.update_time = update_time
        self.get_timer = QTimer()
        self.get_timer.timeout.connect(self.is_gun_modulator_in_Trig)
        self.get_timer.start( self.update_time )
        self.currentState = self.modulator[0].state

    def is_gun_modulator_in_Trig(self):
        new_state = self.modulator[0].state
        if self.currentState != new_state:
            if self.modulator[0].state == GUN_MOD_STATE.Trig:
                self.gunModInTrigSignal.emit(False)
            else:
                self.gunModInTrigSignal.emit(True)
            self.currentState = new_state