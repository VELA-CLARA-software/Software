from ComponentBase import ComponentBase
from ..SAMPLlab import Utilities
import numpy


class Multipole(ComponentBase):
    def __init__(self, length=0, name="", aperture=[],
                 curvature=0, field=[], angle=0):
        ComponentBase.__init__(self, length, name, aperture)
        self.dummy = 0#
        # reciprocal of radius of curvature of reference trajectory,
        # in 1/metres (for applying weak focusing)
        self.curvature = curvature
        # Nx2 array of N field components [index normal-component+i*skew-component]
        # [n][0]=real component, [n][1] = imaginary componnet
        self.field = field
        # bending angle of reference trajectory, in radians
        self.angle = angle

    def Track(self, beam):
        dpx = -self.angle * (1 + beam.dp - self..curvature * beam.x);
        # Apply a multipole 'kick'
        xi0 = beam.x + beam.y*1j;

        for i in range(len(self.field)):
            n   = self.field[i][0]
            if n >= 0:
                dpx = dpx + (self.field[i][1] * (xi0**n) / beam.rigidity /
                             numpy.math.factorial(n))
            else
                dpx = dpx + (self.field[i][1] * (1 / xi0**abs(n)) /
                             beam.rigidity / numpy.math.factorial(n))
        beam.px = beam.px - real(dpx);
        beam.py = beam.py + imag(dpx);
        beam.ct = beam.ct - self.angle * beam.x;
        # save
        self.lastTrackedBeam = beam

    def GetBField(self, beam):
        # [bx, by, bz] = Multipole.GetBField(beam)
        # Returns the *integrated* magnetic field (in tesla metres) at
        # the locations of the particles in the beam.
        xi = beam.x + beam.y*1j
        b  = 0

        for i in range(len(self.field)):
            n = self.field[i][0]
            if n >= 0:
                b = b + self.field[i][2] * xi**n / numpy.math.factorial(n)
            else:
                b = b + self.field[i][2] * (1 / xi**abs(n)) / numpy.math.factorial(n)

        bx = b.real
        by = b.imag
        bz = [0.0] * len(beam.y)
        return [bx, by, bz]

    def TrackSpin(self, beam):
        #  Multipole.Trackspin(beam)
        # Tracks particle spins through a Multipole.
        [bxL, byL, bzL] = self.GetBField(beam);
        nomlength = 1e-9;
        Utilities.SpinRotation(beam, bxL/nomlength, byL/nomlength, bzL/nomlength, nomlength);
        # Account for the rotation of the local coordinate system
        if self.angle != 0:

            [theta1, phi1] = beam.GetSpins();

            polsnx2 = numpy.sin(theta1) * numpy.cos(phi1)
            polsny2 = numpy.sin(theta1) * numpy.sin(phi1)
            polsnz2 = numpy.cos(theta1)

            thetaprime = numpy.arccos(polsny2)
            phiprime = numpy.arctan2(polsnx2,polsnz2) + self.angle

            polsnx3 = numpy.sin(thetaprime) * numpy.sin(phiprime)
            polsny3 = numpy.cos(thetaprime)
            polsnz3 = numpy.sin(thetaprime) * numpy.cos(phiprime)

            phi2 = numpy.arctan2(polsny3,polsnx3)
            theta2 = numpy.arccos(polsnz3)

            beam.SetSpins(theta2, phi2)
