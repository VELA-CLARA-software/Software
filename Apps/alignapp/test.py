import sys,os
import time
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"

import VELA_CLARA_BPM_Control as vbpmc

s=vbpmc.init()
p=s.virtual_VELA_INJ_BPM_Controller()
numShots = 1
p.setY('BPM01',1.3)
p.setX('BPM01',1.4)
print "setting BPM01 y = ", 1.3
print "setting BPM01 x = ", 1.4
time.sleep(0.1)
tr1=p.getYFromPV('BPM01')
tr2=p.getXFromPV('BPM01')
print "y = ", tr1
print "x = ", tr2
time.sleep(1)
p.setY('BPM01',2.3)
p.setX('BPM01',2.3)
print "setting BPM01 y = ", 2.3
print "setting BPM01 x = ", 2.4
time.sleep(0.1)
tr1=p.getYFromPV('BPM01')
tr2=p.getXFromPV('BPM01')
print "y = ", tr1
print "x = ", tr2