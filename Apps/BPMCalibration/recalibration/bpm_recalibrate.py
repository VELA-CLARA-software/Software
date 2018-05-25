import VELA_CLARA_BPM_Control as vbpmc
import VELA_CLARA_Charge_Control as vccc
import numpy
import sys

bpminit = vbpmc.init()
bpmcontrol = bpminit.physical_CLARA_PH1_BPM_Controller()
chargeinit = vccc.init()
chargecontrol = chargeinit.physical_CLARA_PH1_Charge_Controller()

bpmnames = bpmcontrol.getBPMNames()
charge = numpy.mean(chargecontrol.getChargeBuffer("WCM"))

for i in bpmnames:
	bpmcontrol.reCalAttenuation(i,charge)

print "recalibrated BPMs!"
raw_input("hit any key to exit")