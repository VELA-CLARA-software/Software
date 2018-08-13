from ComponentBase import ComponentBase
import numpy as np
import SolenoidAndRF.rf_sol_tracking as RFSolTracking
from ..SAMPLlab import PhysicalUnits
from ..SAMPLlab import PhysicalConstants


class SolenoidAndRF(ComponentBase):
    def __init__(self, length=0, name="", aperture=[], peakField=0.0,
                 phase=0.0, solCurrent1=0.0, solCurrent2=0.0,
                 rfMap="", solMap=""):
        self.peakField = peakField
        self.phase = phase
        self.solCurrent1 = solCurrent1
        self.solCurrent2 = solCurrent2
        self.rfMap = rfMap
        self.solMap = solMap

        ComponentBase.__init__(self, length, name, aperture)
        # super(ComponentBase, self).__init__(length, name, aperture)
        self.dummy = 0

    def Track(self, beam):
        # print 'Paricle before:'
        # print beam.particles

        rfAndSol = RFSolTracking.RFSolTracker(self.name, quiet=True)
        print ('Peak field: ' + str(self.peakField))
        rfAndSol.setRFPeakField(self.peakField)

        rfAndSol.setRFPhase(self.phase)
        rfAndSol.setBuckingCoilCurrent(self.solCurrent1)
        rfAndSol.setSolenoidCurrent(self.solCurrent2)

        matrix = rfAndSol.getOverallMatrix()
        #print matrix
        mom = rfAndSol.getMomentumMap()
        momInitial = mom[:-1]
        momFinal = mom[1:]



        x_xPrime_y_yPrime = np.array([beam.x, beam.px, beam.y, beam.py])
        end = np.array([matrix.dot(x.T) for x in x_xPrime_y_yPrime.T])
        beam.x = end.T[0]
        beam.px = end.T[1]
        beam.y = end.T[2]
        beam.py = end.T[3]
        d1 = np.sqrt(1 - beam.px * beam.px
                        - beam.py * beam.py
                        + 2 * beam.dp / beam.beta
                        + beam.dp * beam.dp)
        beam.ct = beam.ct + self.length * (1 - (1 + beam.beta * beam.dp) / d1) / beam.beta
        print beam.momentum * PhysicalConstants.SpeedOfLight / PhysicalUnits.MeV
        #beam.momentum = (beam.momentum +
        #                 rfAndSol.getFinalMomentum()
        #                 * PhysicalUnits.MeV / PhysicalConstants.SpeedOfLight)
        beam.momentum = (rfAndSol.getFinalMomentum()
                         * PhysicalUnits.MeV / PhysicalConstants.SpeedOfLight)
        print beam.momentum * PhysicalConstants.SpeedOfLight / PhysicalUnits.MeV
        # savePhysicalUnits
        # print 'Paricle After:'
        # print beam.particles
        print('Bunch energy: ' + str(beam.energy / PhysicalUnits.eV) + 'eV')
        self.lastTrackedBeam = beam
