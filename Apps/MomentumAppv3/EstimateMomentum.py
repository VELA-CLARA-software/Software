import sys
sys.path.append("../../../")
import Software.Procedures.linacTiming as linacTiming
import VELA_CLARA_LLRF_Control as llrf

llrfInit = llrf.init()

gun = llrfInit.physical_CLARA_LRRG_LLRF_Controller()
linac1 = llrfInit.physical_L01_LLRF_Controller()

#print linac1.getPhiSP()
#print linac1.getAmpMVM()
print gun.getAmpSP()
#print gun.getCavFwdPowerData()
#print gun.ProbePower()
print gun.RFOutput()

#print linac1.getAmpSP()
#print linac1.getCavFwdPower()

Linac01Timing = linacTiming.Linac01Timing()

print Linac01Timing.isLinacOn()
#if self.Linac01Timing.isLinacOn:
