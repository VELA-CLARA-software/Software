
import sys,os
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12" #BE SPECIFIC.... YOUR I.P. FOR YOUR VM
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
os.environ["EPICS_CA_SERVER_PORT"]="6000"
sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\Release')
sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\OnlineModel')

import VELA_CLARA_LLRFControl as llrf

llrfInit1 = llrf.init()
llrfInit1.setVerbose()
llrfInit = llrf.init()
llrfInit.setVerbose()
#L = llrfInit.virtual_L01_LLRF_Controller()
v = llrfInit1.virtual_VELA_LRRG_LLRF_Controller()

#L.setAmp(20)
v.setAmp(70)


print(v.getAmp())
#print(L.getAmp())
