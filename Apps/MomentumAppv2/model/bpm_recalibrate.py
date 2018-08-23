import VELA_CLARA_enums as vce
import VELA_CLARA_BPM_Control as bpm
import VELA_CLARA_Charge_Control as chg
import numpy, time

bpm_init = bpm.init()
chg_init = chg.init()

bpm_ctrl = bpm_init.getBPMController(vce.MACHINE_MODE.PHYSICAL,vce.MACHINE_AREA.CLARA_2_BA1_BA2)
chg_ctrl = chg_init.getChargeController(vce.MACHINE_MODE.PHYSICAL,vce.MACHINE_AREA.CLARA_PH1)

time.sleep(2)

bpm_names = bpm_ctrl.getBPMNames()
wcm_name = "WCM"

wcm_charge = numpy.mean(chg_ctrl.getChargeBuffer(wcm_name))
print "charge from wcm = ", wcm_charge
for i in bpm_names:
	bpm_ctrl.reCalAttenuation(i, wcm_charge)
	print "new SA1 for ", i, " = ", bpm_ctrl.getRA1(i)
	print "new SA2 for ", i, " = ", bpm_ctrl.getRA2(i)

raw_input("hit any key to exit")
