import sys, os
import time


os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
os.environ["EPICS_CA_SERVER_PORT"] = "6000"
sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\stagetim')
sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\OnlineModel')

import onlineModel
import VELA_CLARA_LLRFControl as llrf
import VELA_CLARA_Magnet_Control as mag
		self.pilInit = pil.init()
class TEST:
    def __init__(self):

        self.rfInit = llrf.init()
        self.magInit = mag.init()
        self.gun = self.rfInit.virtual_CLARA_LRRG_LLRF_Controller()
        self.magnets = self.magInit.virtual_VELA_INJ_Magnet_Controller()
        self.ASTRA = onlineModel.ASTRA(V_MAG_Ctrl=self.magnets, V_RF_Ctrl=self.gun)

    def hi(self):
        aa = 'V1'
        if aa == 'C1':
            self.gun.setPhiDEG(10)
            self.gun.setAmpMVM(20)
        elif aa == 'V1':
            self.gun.setPhiDEG(-10)
            self.gun.setAmpMVM(40)
        else:
            print 'NOT STARTING ON A LINE WITH A GUN!'
        ob = self.gun.getLLRFObjConstRef()
        time.sleep(1)
        print self.gun.getAmpMVM()
        print ob.amp_MVM
        #self.ASTRA.go('V1-GUN', 'SP-YAG04', 'temp-start.ini')
