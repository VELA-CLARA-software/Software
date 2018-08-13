from ComponentBase import ComponentBase
import MasterOscillator
from ..SAMPLlab import PhysicalConstants
from ..SAMPLlab import PhysicalUnits
import numpy
import math


class RFAcceleratingStructure(ComponentBase):
    def __init__(self, voltage=0, harmonic=1, phase=numpy.pi, length=0,
                 name="", aperture=[], ncell=0, structureType='TravellingWave'):
        ComponentBase.__init__(self, length, name, aperture)
        # in volts
        self.voltage = voltage
        # frequency (in units of master oscillator frequency)
        self.harmonic = harmonic
        # relative to master oscillator, in radians
        self.phase = phase
        # 1x2 array of elliptical aperture half-axes, in metres
        self.aperture = aperture
        # Number of cells
        self.ncell = ncell
        # Structure type, 'TravellingWave' or 'StandingWave'
        self.structureType = structureType
        # 1 = synchronise with global clock
        self.globalclock = 1

    def setFrequency(self, f):
        MasterOscillator.SetFrequency(f / self.harmonic)

    def getFrequency(self):
        return self.harmonic * MasterOscillator.GetFrequency()

    def Track(self, beam):
        print self.name
        print ('Energy before acceleration: '+str(beam.energy/PhysicalUnits.MeV)+'MeV')
        # RFAcceleratingStructure.Track(beam)
        # Applies the dynamical map for a linac structure to the particles
        # in beam.  The reference energy is changed by qV*cos(phase).
        mofreq = MasterOscillator.frequency
        nc = self.ncell
        f = self.harmonic * mofreq
        L = self.length / nc
        cosphi = numpy.cos(self.phase)

        beam.globaltime = (beam.globaltime -
                           math.floor(beam.globaltime * mofreq) / mofreq)

        gt = beam.globaltime * self.globalclock

        dE = beam.species.charge * self.voltage * cosphi / nc
        #print(dE/PhysicalUnits.eV)
        E0 = beam.energy
        E1 = E0 + dE

        if abs(dE / E0) > 1e-6:
            if self.structureType == 'TravellingWave':
                logE = numpy.log(1 + dE / E0)
                r11 = 1 - logE / 2
                r12 = L * logE * E0 / dE
                r21 = -dE * logE / 4 / L / E1
                r22 = E0 * (2 + logE) / 2 / E1
            elif self.structureType == 'StandingWave':
                L1 = PhysicalConstants.SpeedOfLight / 2 / f
                if abs(L / L1 - 1) > 1e-2:
                    print('RFAcceleratingStructure:BadLength  ',
                          'RFAcceleratingStructure.length should be c/2f.')
                a = numpy.log(E1 / E0) / numpy.sqrt(8) / cosphi
                Eprime = (E1 - E0) / L

                r11 = numpy.cos(a) - numpy.sqrt(2) * cosphi * numpy.sin(a)
                r12 = numpy.sqrt(8) * cosphi * numpy.sin(a) * E0 / Eprime
                r21 = -((cosphi / numpy.sqrt(2) + 1 / numpy.sqrt(8) / cosphi)
                        * numpy.sin(a) * Eprime / E1)
                r22 = (numpy.cos(a) +
                       numpy.sqrt(2) * cosphi * numpy.sin(a)) * E0 / E1
            else:
                print self.structureType
                print('RFAcceleratingStructure:UnrecognisedType  ' +
                      'RFAcceleratingStructure.structureType should' +
                      ' be StandingWave or TravellingWave.')
        else:
            r11 = 1
            r12 = L * (1 - dE / 2 / E0)
            r21 = 0
            r22 = 1 - dE / E0

        for n in range(1, nc + 1):
            # First, apply a drift map through L/2
            # to the longitudinal coordinate
            d1 = numpy.sqrt(1 - beam.px * beam.px - beam.py * beam.py +
                            2 * beam.dp / beam.beta + beam.dp * beam.dp)
            beam.ct = (beam.ct +
                       L * (1 - (1 + beam.beta * beam.dp) / d1) / beam.beta / 2)

            # Now apply the RF structure map to the transverse variables
            # and the momentum deviation
            x1 = r11 * beam.x + r12 * beam.px
            beam.px = r21 * beam.x + r22 * beam.px
            beam.x = x1

            y1 = r11 * beam.y + r12 * beam.py
            beam.py = r21 * beam.y + r22 * beam.py
            beam.y = y1

            P0 = beam.momentum
            Edc = (beam.dp + 1 / beam.beta) * P0

            beam.energy = beam.energy + dE
            P0 = beam.momentum

            t = gt - beam.ct / PhysicalConstants.SpeedOfLight
            Edc = Edc + (beam.species.charge * self.voltage *
                         numpy.cos(2 * numpy.pi * f * t + self.phase) /
                         nc / PhysicalConstants.SpeedOfLight)

            beam.dp = Edc / P0 - 1 / beam.beta

            # Finally, apply a drift map through L/2
            # to the longitudinal coordinate
            d1 = numpy.sqrt(1 - beam.px * beam.px - beam.py * beam.py +
                            2 * beam.dp / beam.beta + beam.dp * beam.dp)
            beam.ct = beam.ct + (L * (1 - (1 + beam.beta * beam.dp) / d1)
                                 / beam.beta / 2)

        # save
        print ('Final energy after acceleration: '+str(beam.energy/PhysicalUnits.MeV)+'MeV')
        self.lastTrackedBeam = beam
