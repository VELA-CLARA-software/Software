import os
import sys
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\..\\..\\')

from SAMPL.sourceCode.SAMPLcore.Particles import Electron
from SAMPL.sourceCode.SAMPLcore.SAMPLlab import Beamline
from SAMPL.sourceCode.SAMPLcore.SAMPLlab import Beam
from SAMPL.sourceCode.SAMPLcore.SAMPLlab import PhysicalUnits
import SAMPL.sourceCode.SAMPLcore.Components.SolenoidAndRFClass as s
import numpy as np

beam1 = Beam.Beam(species=Electron.Electron, energy=4.5 * PhysicalUnits.MeV)
M1 = np.zeros((2, 4, 4))
M1[:] = np.identity(4)
#print M1
ptcle1 = [0.001, 0, 0, 0, 0, 0]
ptcle2 = [0, 0, 0.001, 0, 0, 0]
ptcle3 = [0, 0, 0, 0, 0, 0]
beam1.particles = np.array([ptcle1, ptcle2, ptcle3])
gun = 'Gun-10'
a = s.SolenoidAndRF(name='Linac1', peakField=20.0, phase=300, solCurrent1=0.0,
                    solCurrent2=0.0, rfMap="", solMap="")
a.Track(beam1)
print a.lastTrackedBeam.particles
