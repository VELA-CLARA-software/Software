import sys,os
import time
#os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12" #BE SPECIFIC.... YOUR I.P. FOR YOUR VM
#os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
os.environ["EPICS_CA_SERVER_PORT"]="6000"
#sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\model')
#sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\controller')
#sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\view')
#from PyQt4 import QtGui, QtCore
#import model_VELA as model
#import model.model_CLARA_SAMPL as model
#import controller.controller
#import view.view
from epics import caget, caput

sys.path.append('C:\\Users\\djd63\\Desktop\\VA workshop\\OnlineModel-master\\OnlineModel-master\\onlineModel-v1')
#sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\stagetim')
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release')
os.environ["PATH"] = os.environ["PATH"]+";\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\root_v5.34.34\\bin\\"
#import VELA_CLARA_BPM_Control as bpm

#print 'VM-EBT-INJ-MAG-QUAD-01:SETI =', str(caget('VM-EBT-INJ-MAG-QUAD-01:SETI'))
#print caget('VM-CLA-S02-MAG-QUAD-01:SETI',10.0)
parameter = 'CLA-S01-MAG-HCOR-01:SETI'
print caget(parameter)
parameter = 'CLA-S01-MAG-VCOR-01:SETI'
print caget(parameter)
parameter = 'CLA-S01-MAG-HCOR-02:SETI'
print caget(parameter)
parameter = 'CLA-S01-MAG-VCOR-02:SETI'
print caget(parameter)
# parameter = 'VM-CLA-S01-MAG-HCOR-01:SETI'
# print caget(parameter)
# parameter = 'VM-CLA-S01-MAG-VCOR-01:SETI'
# print caget(parameter)
# parameter = 'VM-CLA-S01-MAG-HCOR-02:SETI'
# print caget(parameter)
# parameter = 'VM-CLA-S01-MAG-VCOR-02:SETI'
# print caget(parameter)


#caput(parameter,0.0)
#print caget(parameter)

# print caget(parameter)
# val = 1
# while True:
#     val = -1*val
#     caput(parameter,val)
#     print caget(parameter)
#     time.sleep(10)


#caput('VM-CLA-S01-MAG-QUAD-01:SETI',10.0)
#print 'VM-CLA-C2V-DIA-CAM-01:ANA:X_RBV =', str(caget('VM-CLA-C2V-DIA-CAM-01:ANA:X_RBV'))
#print 'VM-CLA-C2V-DIA-CAM-01:ANA:SigmaX_RBV =', str(caget('VM-CLA-C2V-DIA-CAM-01:ANA:SigmaX_RBV'))
#print 'VM-CLA-C2V-DIA-CAM-01:ANA:SigmaXPix_RBV =', str(caget('VM-CLA-C2V-DIA-CAM-01:ANA:SigmaXPix_RBV'))
#print 'VM-CLA-C2V-DIA-BPM-01:X =', str(caget('VM-CLA-C2V-DIA-BPM-01:X'))
#print 'VM-CLA-S02-DIA-CAM-01:SigmaY =', str(caget('VM-CLA-C2V-DIA-BPM-01:X'))


#class Model():
#    def __init__(self):
#        self.bpmInit = bpm.init()
#        self.Cbpms = self.bpmInit.virtual_CLARA_PH1_BPM_Controller()
#        print 'BPM readout =', str(self.Cbpms.getXFromPV('BPM01'))
#a=Model()
#print a.Cbpms.getXFromPV('BPM01')

#bpmInit = bpm.init()
#Cbpms = bpmInit.virtual_CLARA_PH1_BPM_Controller()
#time.sleep(1)
#print 'BPM readout =', str(Cbpms.getXFromPV('C2V-BPM01'))
#print 'BPM readout =', str(Cbpms.getX('C2V-BPM01'))
#caget(camera+':X_RBV')
