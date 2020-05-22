import VELA_CLARA_PILaser_Control as pil
import time

pil_init = pil.init()
pil_init.setVerbose()


pil_control = pil_init.physical_PILaser_Controller()

print  'Press key to set position'
raw_input()
	

pil_control.setMaskFeedBackOn_VC()
	
a = pil_control.setVCPos(5.5,6.0)

# monitor  this paramter to know when ity has finished 

set_pos_succes = False

while 1:
	set_pos_state = pil_control.getSetVCPosState()
	if set_pos_state == pil.VC_SET_POS_STATE.SUCCESS:
		set_pos_succes = True
		break
	else:
		print set_pos_state
	time.sleep(1)

print("Set Position Finished",pil_control.getSetVCPosState())