from ComponentBase import ComponentBase
from ..SAMPLlab import Utilities
import numpy


class Sextupole(ComponentBase):
    def __init__(self, length=0, name="", aperture=[], gradient=0):
        ComponentBase.__init__(self, length, name, aperture)
        self.dummy = 0
        # gradient in tesla/metre^2
        self.gradient = gradient

    def Track(self, beam):
        # normalised gradient
        k2 = self.gradient / beam.rigidity
        # First apply a drift through ds/2
        d1 = numpy.sqrt(1 - beam.px * beam.px - beam.py * beam.py +
                        2 * beam.dp / beam.beta + beam.dp * beam.dp)
        beam.x = beam.x + (self.length * beam.px) / d1 / 2
        beam.y = beam.y + (self.length * beam.py) / d1 / 2
        beam.ct = beam.ct + (self.length * (1 - (1 + beam.beta * beam.dp) / d1)
                             / beam.beta / 2)
        # Next, apply a Sextupole 'kick'
        beam.px = beam.px - ((beam.x * beam.x * beam.x -
                              3 * beam.x * beam.y * beam.y)
                             * k2 * self.length)
        beam.py = beam.py + (beam.x * beam.y * k2 * self.length)
        # Finally, apply a second drift through ds/2
        d1 = numpy.sqrt(1 - beam.px * beam.px - beam.py * beam.py +
                        2 * beam.dp / beam.beta + beam.dp * beam.dp)
        beam.x = beam.x + (self.length * beam.px) / d1 / 2
        beam.y = beam.y + (self.length * beam.py) / d1 / 2
        beam.ct = beam.ct + (self.length * (1 - (1 + beam.beta * beam.dp) / d1)
                             / beam.beta / 2)
        # save
        self.lastTrackedBeam = beam

    def GetBField(self, beam):
        # [bx, by, bz] = Octupole.GetBField(beam)
        # Returns the magnetic field (in tesla) at the locations of
        # the particles in the beam.
        bx = self.gradient * (beam.x * beam.x - beam.y * beam.y) / 2
        by = self.gradient * beam.x * beam.y
        bz = [0.0] * len(beam.y)
        return [bx, by, bz]

    def TrackSpin(self, beam):
        #  Octupole.Trackspin(beam)
        # Tracks particle spins through an Octupole.
        [bx, by, bz] = self.GetBField(beam)
        Utilities.SpinRotation(beam, bx, by, bz, self.length)
