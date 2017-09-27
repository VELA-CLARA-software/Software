
import sys,os
import time
from epics import caget,caput
import threads
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
os.environ["EPICS_CA_SERVER_PORT"]="6000"

sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\stagetim\\')


import VELA_CLARA_LLRFControl as llrf

llrfInit = llrf.init()

gun = llrfInit.virtual_VELA_LRRG_LLRF_Controller()

print gun.getPhi()
print 'caget = '+ str(caget('VM-EBT-GUN:Phi:WR'))
t = threads.GenericThread(gun.setPhi,10)
t.start()
while gun.getPhi()!=10:
	print t.isRunning()
	print gun.getPhi()
	time.sleep(1)
print gun.getPhi()
print 'caget = '+ str(caget('VM-EBT-GUN:Phi:WR'))
