import sys, time, os
sys.path.append('../../')
from Software.Widgets.generic.pv import *

update = 0
while True:
    print 'Update # = ', update
    for i in range(1,9):
        # print 'i = ', i
        pv = PVObject('CLA-L01-LRF-CTRL-01:ad1:ch'+str(i)+':power_remote.SCAN')
        setattr(pv, 'writeAccess', True)
        pv.value = 9
        pv = PVObject('CLA-L01-LRF-CTRL-01:ad1:ch'+str(i)+':amp_phase.SCAN')
        setattr(pv, 'writeAccess', True)
        pv.value = 9

        pv = PVObject('CLA-GUN-LRF-CTRL-01:ad1:ch'+str(i)+':power_remote.SCAN')
        setattr(pv, 'writeAccess', True)
        pv.value = 9
        pv = PVObject('CLA-GUN-LRF-CTRL-01:ad1:ch'+str(i)+':amp_phase.SCAN')
        setattr(pv, 'writeAccess', True)
        pv.value = 9

        pv = PVObject('CLA-GUN-LRF-CTRL-01:ad1:ch'+str(i)+':amp_phase_s.SCAN')
        setattr(pv, 'writeAccess', True)
        pv.value = 9

        pv = PVObject('CLA-L01-LRF-CTRL-01:ad1:ch'+str(i)+':amp_phase_s.SCAN')
        setattr(pv, 'writeAccess', True)
        pv.value = 9
    update += 1
    time.sleep(10)
