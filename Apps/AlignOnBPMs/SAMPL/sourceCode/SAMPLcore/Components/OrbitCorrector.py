# SAM to Python Conversion
# DJS August 2017
# Version 0.1
from ..SAMPLlab import Utilities
from ComponentBase import ComponentBase
import numpy


class OrbitCorrector(ComponentBase):
    def __init__(self, field=[0, 0], length=0, name="", aperture=[]):
        ComponentBase.__init__(self, length, name, aperture)
        # horizontal and vertical magnetic field, in tesla
        self.field = field
        # quadrupole gradient, in tesla/metre

    def Track(self, beam):
        # print 'KICK_TRACK'
        # OrbitCorrector.Track(beam)
        # Applies the transfer map for an orbit corrector
        # to the particles in in beam.

        k0 = numpy.divide(self.field, beam.rigidity)
        d1 = numpy.sqrt(1 + 2 * beam.dp / beam.beta + beam.dp * beam.dp)

        beam.x = beam.x + (self.length * beam.px / d1 -
                           self.length * self.length * k0[1] / d1 / 2)
        beam.px = beam.px - self.length * k0[1]

        beam.y = beam.y + (self.length * beam.py / d1 +
                           self.length * self.length * k0[0] / d1 / 2)
        beam.py = beam.py + self.length * k0[0]

        f1 = self.length * (1 / beam.beta + beam.dp) / d1 / d1 / d1 / 2

        c0 = beam.ct + (self.length / beam.beta -
                        self.length * (1 / beam.beta + beam.dp) / d1 -
                        self.length * self.length * f1 * (k0[0] * k0[0] +
                                                          k0[1] * k0[1]) / 3)

        beam.ct = c0 + (self.length * f1 * (k0[1] * beam.px - k0[0] * beam.py) -
                        f1 * (beam.px * beam.px + beam.py * beam.py))
        # save
        self.lastTrackedBeam = beam

    def GetBField(self, beam):
        # [bx, by, bz] = OrbitCorrector.GetBField(beam)
        # Returns the magnetic field (in tesla) at the locations of
        # the particles in the beam.
        bx = self.field[0]
        by = self.field[1]
        bz = [0.0] * len(beam.y)
        return [bx, by, by]

    def TrackSpin(self, beam):
            # OrbitCorrector.Trackspin(beam1)
            # Tracks particle spins through an OrbitCorrector.
            [bx, by, bz] = self.GetBField(beam)
            Utilities.SpinRotation(beam,bx,by,bz,self.length)
