import os,sys
sys.path.append('C:\\Users\\djd63\\Desktop\\Release')
import VELA_CLARA_BPM_Control as vbpmc
import time
import numpy as np

bpminit = vbpmc.init()
bpmctrl = bpminit.getBPMController(vbpmc.MACHINE_MODE.PHYSICAL,vbpmc.MACHINE_AREA.CLARA_2_BA1_BA2)

time.sleep(2)

bpm_name = 'S01-BPM01'

# method 1 for getting status
statusbufferfromfunc = bpmctrl.getStatusBuffer(bpm_name)
# method 2 for getting status
bpmdataobj = bpmctrl.getBPMDataObject(bpm_name)
statusbufferfromobj = bpmdataobj.statusBuffer

for i, j in zip(statusbufferfromfunc, statusbufferfromobj):
	print "from func = ", i, " from data object = ", j

# method 1 for getting charge
chargebufferfromfunc = bpmctrl.getBPMQBuffer(bpm_name)
print 'test', chargebufferfromfunc
print np.mean(chargebufferfromfunc)
# method 2 for getting charge
chargebufferfromobj = bpmdataobj.qBuffer

for i, j in zip(chargebufferfromfunc, chargebufferfromobj):
	print "from func = ", i, " from data object = ", j

raw_input("hit any key to exit")
