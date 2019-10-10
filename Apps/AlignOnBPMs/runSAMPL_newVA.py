import os
import sys
from epics import caget
import time

#VE setup
#os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
#os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
#os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
#os.environ["EPICS_CA_SERVER_PORT"] = "6000"
# New VA
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.246"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
os.environ["EPICS_CA_SERVER_PORT"] = "6003"

# OM setup
#sys.path.append('C:\\Users\\wln24624\\Documents\\SOFTWARE\\OnlineModel')
#sys.path.append('C:/Users/djd63/Desktop/VA workshop/OnlineModel-master')
#sys.path.append('C:\\Users\\djd63\\Desktop\\VA workshop\\OnlineModel-master\\OnlineModel-master')
import SAMPL.v2_developing.sampl as sampl

#Controllers
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release')
os.environ["PATH"] = os.environ["PATH"]+";\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\root_v5.34.34\\bin\\"
import VELA_CLARA_Magnet_Control as mag
import VELA_CLARA_LLRF_Control as llrf
import VELA_CLARA_Camera_IA_Control as camIA
#Setup controllers
magInit = mag.init()
llrfInit = llrf.init()
camInit = camIA.init()

#llrfInit.setVerbose()

Cmagnets = magInit.virtual_CLARA_PH1_Magnet_Controller()
gun400 = llrfInit.virtual_VELA_HRRG_LLRF_Controller()
LINAC01 = llrfInit.virtual_L01_LLRF_Controller()
cameras = camInit.virtual_CLARA_Camera_IA_Controller()

#Setup Virtual Accelerators
Cmagnets.switchONpsu('DIP01')
cameras.setCamera('C2V-CAM-01')
selectedCamera = cameras.getSelectedIARef()
Cmagnets.setSI('DIP01',-91.6)
gun400.setAmpMVM(70)
gun400.setPhiDEG(-16)
LINAC01.setAmpMVM(21)
LINAC01.setPhiDEG(-9)

SAMPL = sampl.Setup(V_MAG_Ctrl=None,
                    C_S01_MAG_Ctrl=Cmagnets,
                    C_S02_MAG_Ctrl=Cmagnets,
                    C2V_MAG_Ctrl=Cmagnets,
                    LRRG_RF_Ctrl=None,
                    HRRG_RF_Ctrl=gun400,
                    L01_RF_Ctrl=LINAC01,
                    messages=True)

SAMPL.startElement = 'CLA-HRG1-GUN-CAV'
SAMPL.stopElement = 'CLA-C2V-DIA-SCR-01-W'
SAMPL.initDistribFile = '4k-250pC.ini'

time.sleep(1)

while True:

    print("")
    print('New Run:')
    I = float(raw_input("Re-enter a current: "))
    Cmagnets.setSI('DIP01', I)

    SAMPL.run()
    print('Beam\'s X position an C2V Camera (m):')
    print(selectedCamera.IA.x)
