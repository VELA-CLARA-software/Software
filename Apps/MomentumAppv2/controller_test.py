import os,sys
from epics import caget,caput

sys.path.append('C:\\Users\\djd63\\Desktop\\Release')
import VELA_CLARA_BPM_Control as bpm
bpmInit = bpm.init()
Cbpms = bpmInit.physical_CLARA_PH1_BPM_Controller()

print os.system('caget CLA-S01-DIA-CAM-01:ANA:X_RBV')
print Cbpms.getXFromPV('S02-BPM01')
