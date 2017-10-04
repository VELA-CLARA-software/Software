#!python2
# -*- coding: utf-8 -*-
# encoding=utf8

import numpy as np
from fractions import Fraction
import pyqtgraph as pg
import scipy.interpolate
from PyQt4 import QtCore

path = r'\\fed.cclrc.ac.uk\Org\NLab\ASTeC-TDL\Projects\tdl-1168 CLARA\CLARA-ASTeC Folder\Accelerator Physics\ASTRA\Injector\fieldmaps' + '\\'
entrance_data = np.loadtxt(path + 'L1entrancecell.dat', converters={0:Fraction})
single_cell_data = np.loadtxt(path + 'L1singlecell.dat', converters={0:Fraction})
exit_data = np.loadtxt(path + 'L1exitcell.dat', converters={0:Fraction})
grad_phase_data = np.loadtxt(path + 'RI_linac_grad_phase_error.txt')
rel_grads = grad_phase_data[:, 0] / np.max(grad_phase_data[:, 0])  # convert from percentage to fraction
phase_adv = np.cumsum(np.radians(grad_phase_data[:, 1]))
n_cells = len(grad_phase_data)

sol_data = np.loadtxt(path + 'SwissFEL_linac_sols.dat')

data_z_length = entrance_data[-1, 0] - entrance_data[0, 0]

ent_interp = scipy.interpolate.interp1d(entrance_data[:, 0], entrance_data[:, 1], fill_value=0, bounds_error=False)
sgl_interp = scipy.interpolate.interp1d(single_cell_data[:, 0], single_cell_data[:, 1], fill_value=0, bounds_error=False)
exit_interp = scipy.interpolate.interp1d(exit_data[:, 0], exit_data[:, 1], fill_value=0, bounds_error=False)
sol_interp = scipy.interpolate.interp1d(sol_data[:, 0], sol_data[:, 1], fill_value=0, bounds_error=False)
win = pg.GraphicsWindow(title="Linac 1")

# p2 = win.addPlot()
# p2.plot(entrance_data, pen=(255,0,0), name="Entrance cell")
# p2.plot(single_cell_data, pen=(0,255,0), name="Main cells")
# p2.plot(exit_data, pen=(0,0,255), name="Exit cell")

n_sols = 2
cell_length = 0.033327  # from "Injector Simulations" document
dz = 0.001
z_length = n_cells * cell_length + data_z_length  # include a bit extra at the ends
z_map = np.arange(-z_length / 2, z_length / 2, dz)
E_map = np.zeros((n_cells, len(z_map)))
E_map_ideal = np.zeros((n_cells, len(z_map)))
B_map = np.zeros((n_sols, len(z_map)))

n_offset = (n_cells - 1) / 2

z_offset = np.array([1, -1]) * cell_length * (n_cells - 1) / 4
for i in range(n_sols):
    B_map[i] = (-1) ** i * sol_interp(z_map + z_offset[i])

p3 = win.addPlot()
p3.addLegend()
curve_ideal = p3.plot(z_map, np.sum(E_map_ideal, 0), pen=0.4, name='Cavity (ideal)')
curve = p3.plot(z_map, np.sum(E_map, 0), name='Cavity')
p3.plot(z_map, np.sum(B_map, 0), pen='r', name='Solenoid')
p3.enableAutoRange('xy', False)
p3.setYRange(-1, 1)
phase = 0

def update():
    global curve, data, p3, phase, E_map
    # Build up full field map
    for i in range(n_cells):
        interp = ent_interp if i == 0 else exit_interp if i == n_cells - 1 else sgl_interp
        E_map[i] = rel_grads[i] * np.cos(phase_adv[i] + phase) * interp(z_map + (n_offset - i) * cell_length)
        E_map_ideal[i] = np.cos(2 * np.pi * i / 3 + phase) * interp(z_map + (n_offset - i) * cell_length)
    curve.setData(z_map, np.sum(E_map, 0))
    curve_ideal.setData(z_map, np.sum(E_map_ideal, 0))
    if phase == 0:
        p3.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
    p3.setTitle(u'Phase {:.0f}°'.format(np.degrees(phase)))
    phase = (phase + np.pi / 60) % (2 * np.pi)

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

# p4 = win.addPlot()
# p4.plot(sol_data, pen='r', name='Solenoid')

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()
