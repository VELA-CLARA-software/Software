#!python2
# -*- coding: utf-8 -*-
"""
Use the RF/solenoid tracking code to calculate a linear relation
between momentum, solenoid current, and Larmor angle
@author: bjs54
"""
import numpy as np
import rf_sol_tracking

name = 'Linac1'
g = rf_sol_tracking.RFSolTracker(name)
setSolCurrent = g.setSolenoidCurrent
if name == 'Gun-10':
    pk_field = np.arange(100., 40., -1.)
    sol_i = np.arange(50., 450., 10.)
elif name == 'Linac1':
    g.setBuckingCoilCurrent(0)
    g.setSolenoidCurrent(0)
    g.setRFPhase(241)
    pk_field = np.arange(35., 3., -1.)
    sol_i = np.arange(0., 210., 10.)
    setSolCurrent = g.setBuckingCoilCurrent # for solenoid 1, otherwise use setSolenoidCurrent (i.e. comment this out)

crest_phase = np.zeros_like(pk_field)
max_p = np.zeros_like(pk_field)
larmor_angle = np.zeros((len(pk_field), len(sol_i)))

for i, pkf in enumerate(pk_field):
    g.setRFPeakField(pkf)
    crest_phase[i] = g.crestCavity()
    max_p[i] = g.getFinalMomentum()
    for j, soli in enumerate(sol_i):
        setSolCurrent(soli)
        # set the correct BC current for zero cathode field
        if name == 'Gun-10':
            g.setCathodeField(0.0)
        larmor_angle[i, j] = g.getFinalLarmorAngle()
    # print(larmor_angle[i, :])

X, Y = np.meshgrid(max_p, sol_i, copy=False)
X = X.flatten()
Y = Y.flatten()

# Terms of coefficients
# X is momentum, and Y is solenoid current
# A = np.array([X**0, X, Y, X*Y, X**2]).T
A = np.array([Y, X*Y, X**2*Y, X**3*Y, X**4*Y]).T
B = larmor_angle.T.flatten()
coeff, resid, rank, s = np.linalg.lstsq(A, B)
print(coeff, resid)

np.savetxt('A.csv', A, delimiter=',')
np.savetxt('B.csv', B, delimiter=',')
