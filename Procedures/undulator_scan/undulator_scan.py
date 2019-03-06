import numpy as np
import epics
import urllib2
from time import sleep


vcor = epics.PV('CLA-C2V-MAG-VCOR-01:SETI')
min_v, max_v = -5.7, 3.5
step = 0.2
url = 'http://148.79.170.74/data/comm.html?command=:MEASU:MEAS2:VAL?'

i_range = np.arange(min_v, max_v + step, step)
signal_array = np.zeros_like(i_range)
for i, current in enumerate(i_range):
    # print(current)
    vcor.put(current)
    sleep(6.4)

    contents = urllib2.urlopen(url).read()
    lines = contents.split('\n')
    signal = float(lines[0])
    signal_array[i] = signal
    print current, signal

