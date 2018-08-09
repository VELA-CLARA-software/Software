
from SAMPLcore.Components import Drift as d
from SAMPLcore.Components import Dipole as D
from SAMPLcore.Components import Quadrupole as Q
from SAMPLcore.Components import Screen as S
from SAMPLcore.Components import OrbitCorrector as C
from SAMPLcore.Components import BeamPositionMonitor as BPM
from SAMPLcore.SAMPLlab import Beamline
from SAMPLcore.SAMPLlab import Beam
from SAMPLcore.Particles import Electron
from SAMPLcore.SAMPLlab import PhysicalUnits
import numpy as np

#[t1, t2] = np.array([[1], [2]])

#beam1 = Beam.Beam(species=Electron.Electron)

#beam1.energy = 1.20 * PhysicalUnits.GeV

# help(comp)
beam1 = Beam.Beam(species=Electron.Electron, energy=4.5 * PhysicalUnits.MeV)
# beam1 = Beam.Beam(species=Positron, energy = 2)

# print('beam1.energy = ', beam1.energy)
# print('beam1.rigidity = ',beam1.rigidity )
# print('beam1.momentum = ',beam1.momentum )

ptcle1 = [0.001, 0, 0, 0, 0, 0]
ptcle2 = [0, 0, 0.001, 0, 0, 0]
ptcle3 = [0, 0, 0, 0, 0, 0]
beam1.particles = np.array([ptcle1, ptcle2, ptcle3])
# Make VELA libroutine
EBT_S01_DRIFT_01 = d.Drift(length=0.4)
EBT_INJ_MAG_HVCOR_01 = C.OrbitCorrector(field=[0, 0], length=0.05)
EBT_S01_DRIFT_02 = d.Drift(length=0.25)
EBT_INJ_DIA_WCM_01 = d.Drift(length=0.0)
EBT_S01_DRIFT_03 = d.Drift(length=0.15)
EBT_INJ_DIA_BPM_01 = BPM.BeamPositionMonitor(length=0.05)
EBT_S01_DRIFT_04 = d.Drift(length=0.05)
EBT_INJ_MAG_HVCOR_02 = C.OrbitCorrector(field=[0, 0], length=0.05)
EBT_S01_DRIFT_05 = d.Drift(length=0.05)
EBT_INJ_DIA_YAG_01 = S.Screen()
EBT_S01_DRIFT_06 = d.Drift(length=0.185)
EBT_INJ_MAG_QUAD_01 = Q.Quadrupole(length=0.1, gradient=0.0)
EBT_S01_DRIFT_07 = d.Drift(length=0.11)
EBT_INJ_MAG_QUAD_02 = Q.Quadrupole(length=0.1, gradient=0.0)
EBT_S01_DRIFT_08 = d.Drift(length=0.11)
EBT_INJ_MAG_QUAD_03 = Q.Quadrupole(length=0.1, gradient=0.0)
EBT_S01_DRIFT_09 = d.Drift(length=0.11)
EBT_INJ_MAG_QUAD_04 = Q.Quadrupole(length=0.1, gradient=0.0)
EBT_S01_DRIFT_10 = d.Drift(length=0.18)
EBT_INJ_DIA_YAG_02 = S.Screen()
EBT_S01_DRIFT_11 = d.Drift(length=0.275)
EBT_INJ_MAG_HVCOR_03 = C.OrbitCorrector(field=[0, 0], length=0.05)
EBT_S01_DRIFT_12 = d.Drift(length=0.05)
EBT_INJ_TDC_01 = d.Drift(length=0.5)
EBT_S01_DRIFT_13 = d.Drift(length=0.033)
EBT_INJ_MAG_HVCOR_04 = C.OrbitCorrector(field=[0, 0], length=0.05)
EBT_S01_DRIFT_14 = d.Drift(length=0.22)
EBT_INJ_DIA_YAG_03 = S.Screen()
EBT_S01_DRIFT_15 = d.Drift(length=0.126)
EBT_INJ_DIA_BPM_02 = BPM.BeamPositionMonitor(length=0.07)
EBT_S01_DRIFT_16 = d.Drift(length=0.318)
CLA_C2V_MAG_DIP_02_DRIFT_01 = d.Drift(length=0.0781)
angle = np.pi/4
Field = beam1.rigidity * angle / 0.4
print angle
print Field
CLA_C2V_MAG_DIP_02 = D.Dipole(length=0.4, field=Field, theta=angle)
CLA_C2V_MAG_DIP_02_DRIFT_02 = d.Drift(length=0.0781)
CLA_SP1_DRIFT_01 = d.Drift(length=0.13)
EBT_INJ_DIA_BPM_03 = BPM.BeamPositionMonitor(length=0.0563)
EBT_INJ_MAG_HVCOR_05 = C.OrbitCorrector(field=[0, 0], length=0.059)
CLA_SP1_DRIFT_02 = d.Drift(length=0.103)
EBT_INJ_MAG_QUAD_05_DRIFT_01 = d.Drift(length=0.0225)
EBT_INJ_MAG_QUAD_05 = Q.Quadrupole(length=0.1, gradient=0.0)
EBT_INJ_MAG_QUAD_05_DRIFT_02 = d.Drift(length=0.0225)
CLA_SP1_DRIFT_03 = d.Drift(length=0.255)
EBT_INJ_MAG_QUAD_06_DRIFT_01 = d.Drift(length=0.0225)
EBT_INJ_MAG_QUAD_06 = Q.Quadrupole(length=0.1, gradient=0.0)
EBT_INJ_MAG_QUAD_06_DRIFT_02 = d.Drift(length=0.0225)
CLA_SP1_DRIFT_04 = d.Drift(length=0.884)
EBT_INJ_DIA_SCR_04_DRIFT_01 = d.Drift(length=0.1)
EBT_INJ_DIA_SCR_04 = S.Screen()
EBT_INJ_DIA_SCR_04_DRIFT_02 = d.Drift(length=0.1)
CLA_SP1_DRIFT_05 = d.Drift(length=0.0)
EBT_INJ_DIA_FCUP_01 = d.Drift(length=0.0)
V1 = Beamline.Beamline(componentlist=[EBT_S01_DRIFT_01,
                                      EBT_INJ_MAG_HVCOR_01,
                                      EBT_S01_DRIFT_02,
                                      EBT_INJ_DIA_WCM_01,
                                      EBT_S01_DRIFT_03,
                                      EBT_INJ_DIA_BPM_01,
                                      EBT_INJ_MAG_HVCOR_02,
                                      EBT_S01_DRIFT_05,
                                      EBT_INJ_DIA_YAG_01,
                                      EBT_S01_DRIFT_06,
                                      EBT_INJ_MAG_QUAD_01,
                                      EBT_S01_DRIFT_07,
                                      EBT_INJ_MAG_QUAD_02,
                                      EBT_S01_DRIFT_08,
                                      EBT_INJ_MAG_QUAD_03,
                                      EBT_S01_DRIFT_09,
                                      EBT_INJ_MAG_QUAD_04,
                                      EBT_S01_DRIFT_10,
                                      EBT_INJ_DIA_YAG_02,
                                      EBT_S01_DRIFT_11,
                                      EBT_INJ_MAG_HVCOR_03,
                                      EBT_S01_DRIFT_12,
                                      EBT_INJ_TDC_01,
                                      EBT_S01_DRIFT_13,
                                      EBT_INJ_MAG_HVCOR_04,
                                      EBT_S01_DRIFT_14,
                                      EBT_INJ_DIA_YAG_03,
                                      EBT_S01_DRIFT_15,
                                      EBT_INJ_DIA_BPM_02,
                                      EBT_S01_DRIFT_16,
                                      CLA_C2V_MAG_DIP_02_DRIFT_01,
                                      CLA_C2V_MAG_DIP_02,
                                      CLA_C2V_MAG_DIP_02_DRIFT_02,
                                      CLA_SP1_DRIFT_01,
                                      EBT_INJ_DIA_BPM_03,
                                      EBT_INJ_MAG_HVCOR_05,
                                      CLA_SP1_DRIFT_02,
                                      EBT_INJ_MAG_QUAD_05_DRIFT_01,
                                      EBT_INJ_MAG_QUAD_05,
                                      EBT_INJ_MAG_QUAD_05_DRIFT_02,
                                      CLA_SP1_DRIFT_03,
                                      EBT_INJ_MAG_QUAD_06_DRIFT_01,
                                      EBT_INJ_MAG_QUAD_06,
                                      EBT_INJ_MAG_QUAD_06_DRIFT_02,
                                      CLA_SP1_DRIFT_04,
                                      EBT_INJ_DIA_SCR_04_DRIFT_01,
                                      EBT_INJ_DIA_SCR_04])

print 'hi'

a=46
print V1.componentlist[a].length
print V1.componentlist[a]
#print V1.componentlist[a].theta
V1.componentlist[a].length
beam2 = V1.TrackMatlab([0, a], beam1)
print "beam2 particle1 = ", beam2.particles[0]
print "beam2 particle2 = ", beam2.particles[1]
print "beam2 particle3 = ", beam2.particles[2]
#print EBT_S01_DRIFT_12.lastTrackedBeam.particles[0]
