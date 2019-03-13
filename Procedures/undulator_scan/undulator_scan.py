#!python2
# -*- coding: utf-8 -*-
# encoding=utf8

# Scan a corrector (or any EPICS PV) and read a measurement from a networked scope
# Ben Shepherd, James Jones
# 6 March 2019
# Originally written to optimise the MCT signal output from the SCU installed on CLARA

import sys
import os
import time
import numpy as np
import epics
import urllib2
sys.path.append("../../../")
import Software.Utils.dict_to_h5 as h5dict


work_folder = r'\\fed.cclrc.ac.uk\Org\NLab\ASTeC\Projects\VELA\Work'
data = {}
data['corrector'] = 'CLA-C2V-MAG-HCOR-01'
data['Undulator_Current'] = 120
scan_pv = epics.PV(data['corrector'] + ':SETI')
start_value = scan_pv.get()
min_val, max_val = -1.2, 3.7
step = 0.2
scope_url = 'http://148.79.170.74/data/comm.html?command=:MEASU:MEAS1:VAL?'  # asks for the value of measurement 1
wait_time = 6.4  # if scope averaging is enabled, need to wait before asking for a measurement

intro_text = 'Scanning {pv_name} from {min_val:.3f} {units} to {max_val:.3f} {units} in steps of {step:.3f} {units}' \
             ' with a delay of {wait_time} s at each step. Original value was {start_value:.3f} {units}.'
print(intro_text.format(pv_name=data['corrector'], units=scan_pv.units, **locals()))

scan_range = np.arange(min_val, max_val + step, step)
signal_array = []
for i, current in enumerate(scan_range):
    # print(current)
    scan_pv.put(current)
    time.sleep(wait_time)

    contents = urllib2.urlopen(scope_url).read()  # for example scope response, see scope_response.htm
    # first line is semicolon-delimited list of measurement results - we can discard the other lines
    lines = contents.split('\n')
    signal = float(lines[0])
    signal_array.append([current, signal])
    print current, signal

print('Scan complete. Restoring {pv_name} to {start_value:.3f} {units}.'.format(pv_name=data['corrector'], units=scan_pv.units, **locals()))
scan_pv.put(start_value)  # restore the original value
data['data'] = signal_array  # store 2d array in HDF5 file - each row is (current, signal) pair
timestr = time.strftime("%H%M%S")
folder = work_folder + '\\' + time.strftime(r"%Y\%m\%d") + '\\'
try:
    os.makedirs(folder)
except OSError:
    if not os.path.isdir(folder):
        folder = './'

filename = folder + timestr + '_UndulatorScans_' + str(data['Undulator_Current']) + 'A_' + data['corrector'] + '.h5'
print(' Saving data to {}.'.format(filename))
h5dict.save_dict_to_hdf5(data, filename)
