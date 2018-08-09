import os
import sys
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\..\\')
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\..\\..\\')
import createBeam as cb
from SAMPL.sourceCode.SAMPLcore.Particles import Electron
from SAMPL.sourceCode.SAMPLcore.SAMPLlab import Beamline
from SAMPL.sourceCode.SAMPLcore.SAMPLlab import Beam
from SAMPL.sourceCode.SAMPLcore.SAMPLlab import PhysicalUnits
import SAMPL.sourceCode.SAMPLcore.Components.Drift as D
import SAMPL.sourceCode.SAMPLcore.Physics.MakeMatchedBunch as MMB
import numpy as np


import matplotlib.pyplot as plt




beam = Beam.Beam(species=Electron.Electron, energy=12.0 * PhysicalUnits.MeV)

centroid0 = np.zeros((6,1))
beta0 = np.zeros((3, 6, 6))


beta0[0,0:2,0:2] = np.eye(2)
beta0[1,2:4,2:4] = np.eye(2)
beta0[2,4:6,4:6] = np.eye(2)

epsilonx = 5e-6 / beam.gamma  # horizontal emittance in metres
epsilony = 5e-6 / beam.gamma  # vertical emittance in metres
epsilonz = 1e-6 / beam.gamma  # longitudinal emittance in metres

nparticles = 2000 # number of particles
beam.bunchcharge = 80e-12
beam.particles = MMB.MakeMatchedBunch(centroid0, beta0,
                                      [epsilonx, epsilony, epsilonz],
                                      nparticles)
beam.ct = 2e-3*(np.random.rand(nparticles) - 0.5)
beam.dp = np.zeros(nparticles)
#plt.scatter(beam.x, beam.px, s=10, c='r' , alpha=0.5)



a = D.Drift(name='', length=0.1)
n = 16
sX = np.zeros(n)


for i in range(n):

    a.TrackSpaceCharge(beam)
    sX[i] = np.std(a.lastTrackedBeam.x)

#print beam.particles


#plt.scatter(beam.x, beam.px, s=10, c='b', alpha=0.5)

#plt.show()

plt.plot(sX)

plt.show()
