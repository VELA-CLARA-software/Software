import sys
import os
import time
import numpy as np
import epics
import urllib2
sys.path.append("../../../")
import Software.Utils.dict_to_h5 as h5dict

data = {}
data['corrector'] = 'CLA-C2V-MAG-VCOR-01'
data['Undulator_Current'] = 120
vcor = epics.PV(data['corrector']+':SETI')
start_current = vcor.get()
min_v, max_v = -5.0, 5.0
step = 0.2
url = 'http://148.79.170.74/data/comm.html?command=:MEASU:MEAS1:VAL?'

i_range = np.arange(min_v, max_v + step, step)
signal_array = []
for i, current in enumerate(i_range):
    # print(current)
    vcor.put(current)
    # sleep(6.4)
    time.sleep(6.4)

    contents = urllib2.urlopen(url).read()
    lines = contents.split('\n')
    signal = float(lines[0])
    signal_array.append([current,signal])
    print current, signal

vcor.put(start_current)
data['data'] = signal_array
timestr = time.strftime("%H%M%S")
dir = '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\'+time.strftime("%Y\\%m\\%d")+'\\'
try:
    os.makedirs(dir)
except OSError:
    if not os.path.isdir(dir):
        dir = './'
filename = dir+timestr+'_UndulatorScans_'+str(data['Undulator_Current'])+'A_'+data['corrector']+'.h5'
h5dict.save_dict_to_hdf5(data, filename)
