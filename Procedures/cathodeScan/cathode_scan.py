# Scan the laser position over a 2D grid, using the position on the virtual cathode.
# At each point, record the BPM position at two RF phases.
# The aim is to find the minimum deflection, which should correspond to the centre of the cavity.

import numpy as np
from vcmove_proto1 import lasmover
import epics
import time
import os
import errno

# Range of values over which to move the laser
xlo = 5.25
xhi = 7.25
ylo = 3.70
yhi = 5.70
nx = 5
ny = 5

xrange = np.linspace(xlo,xhi,nx)
yrange = np.linspace(ylo,yhi,ny)

approx_calib = 1000  # steps per mm of cathode movement
x_delta = (xrange[1] - xrange[0]) * -approx_calib
y_delta = (yrange[1] - yrange[0]) * approx_calib

mylasmove = lasmover()
accurate_move = True

phase_pv = 'CLA-GUN-LRF-CTRL-01:vm:dsp:sp_ph:phase'
bpm_x = 'CLA-S01-DIA-BPM-01:X'
bpm_y = 'CLA-S01-DIA-BPM-01:Y'
max_ph = -145
min_ph = -180

folder = r'\\fed.cclrc.ac.uk\Org\NLab\ASTeC\Projects\VELA\Work' + time.strftime(r'\%Y\%m\%d')
try:
    os.makedirs(folder)
except OSError as e:  # catch
    if e.errno != errno.EEXIST:
        raise
filename = folder + '\\' + time.strftime('%H%M') + ' bpm movement vs laser posn.csv'
csv_file = open(filename, 'a')  # append

for x in xrange:
    accurate_move = True
    for y in yrange:
        if accurate_move:
            mylasmove.setposition(x, y, delta=5, prec=0.1)
            # accurate_move = False  # just do it for the first one
        else:
            # just move the laser by an approximate amount
            mylasmove.move_vert(y_delta)

        epics.caput(phase_pv, min_ph)
        time.sleep(2)
        min_x = epics.caget(bpm_x)[0]  # TODO: take 10 averages; use general monitor thingy
        min_y = epics.caget(bpm_y)[0]
        epics.caput(phase_pv, max_ph)
        time.sleep(2)
        max_x = epics.caget(bpm_x)[0]
        max_y = epics.caget(bpm_y)[0]

        timestamp = time.strftime('%d/%m/%y %H:%M:%S')
        out_array = [x, y, mylasmove.lasx, mylasmove.lasy, min_ph, min_x, min_y, max_ph, max_x, max_y]
        line = timestamp + ',' + ','.join(['{:.3f}'.format(pt) for pt in out_array]) + '\n'
        print line
        csv_file.writelines(line)
        time.sleep(1)
