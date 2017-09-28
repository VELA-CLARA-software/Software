from VELA_CLARA_LLRF_Control import MACHINE_AREA
from VELA_CLARA_LLRF_Control import MACHINE_MODE
import VELA_CLARA_BPM_Control as bpm

s=bpm.init()
p=s.getBPMController(MACHINE_MODE.VIRTUAL,MACHINE_AREA.VELA_INJ)


raw_input()