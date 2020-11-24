import sys
sys.path.append("../../../")
from machine import Machine
clara = Machine('Physical', None, None, controllers=['bpms'])
# print clara.getMeanBPMPosition('S01-BPM01')
# print clara.getBPMBuffer('S01-BPM01', 10, plane='Y')
clara.bpms.setBufferSize(10)
print clara.bpms.getQ('BA1-BPM01')
