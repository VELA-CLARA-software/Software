from epics import caget,caput
import os,sys
import time
import numpy as np
import datetime

sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\Release')
sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\OnlineModel')

import VELA_CLARA_Camera_DAQ_Control as daq 
import VELA_CLARA_Magnet_Control as mag
import VELA_CLARA_General_Monitor as mon
import VELA_CLARA_LLRF_Control as rf

print 'starting physical camera controllers'
Init = daq.init()
Init.setVerbose()
minit = mag.init()
minit.setVerbose()
monini = mon.init()
rfinit = rf.init()
cameras = Init.physical_CLARA_Camera_DAQ_Controller()
cameras.setCamera('S01-CAM-01')
therf = rfinit.physical_CLARA_LRRG_LLRF_Controller()
scamera = cameras.getSelectedDAQRef()
magnets = minit.physical_CLARA_PH1_Magnet_Controller()
klyspwr = monini.connectPV('CLA-GUN-LRF-CTRL-01:A:RPA1MW')


vsol = magnets.getRI('LRG-SOL')
vbsol = magnets.getRI('LRG-BSOL')
vcorv1 = magnets.getRI('S01-VCOR1')
vcorh1 = magnets.getRI('S01-HCOR1')

tpulse = therf.getPulseLength()
cameras.startAcquiring()
print 'camera acquiring', cameras.isAcquiring('S01-CAM-01')
cameras.collectAndSave(1)
time.sleep(1)
cameras.stopAcquiring()
ix = "test1"
iy = "test2"


time.sleep(2)

vklypwr = monini.getValue(klyspwr)
now = datetime.datetime.now()

nowiso = now.isoformat('-').replace(":", "-").split('.', 1)[0]

#write_str = datetime.datetime.now().isoformat('-').replace(":", "-").split('.', 1)[0] + ' ' + str + '\n'
#nowiso = datetime.now().isoformat('-').replace(":", "-").split('.', 1)[0] + ' ' + str + '\n'
#nowiso = "now"

#os.system('copy \\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\2017\\CurrentCamera\\S01-CAM-01_001.bin \\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\2018\\01\\fjtest\\S01CAM1_'+str(ix)+'_'+str(iy)+'.bin')

os.system('copy \\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\2017\\CurrentCamera\\S01-CAM-01_001.bin \\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\2018\\01\\fjtest\\'+str(nowiso)+'_'+str(scamera.name)+'_SOL'+str(int(vsol))+'_KLYS'+str(round(vklypwr,2))+'MW_'+'S01VCR1_'+str(round(vcorv1,2))+'_S01HCR1_'+str(round(vcorh1,2))+'_'+str(round(tpulse,2))+'us'+'.bin')


print 'copying to test directory ', nowiso, vklypwr, vbsol, vcorv1

cameras.startAcquiring()

#magnets.GetNames()
