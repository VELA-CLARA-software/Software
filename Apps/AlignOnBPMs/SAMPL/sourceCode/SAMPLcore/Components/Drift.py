# SAMM to Python Conversion
# DJS August 2017
# TP October 2017
# Version 0.2
#
from ..SAMPLlab import PhysicalConstants
from ComponentBase import ComponentBase
import numpy


class Drift(ComponentBase):

    def __init__(self, length=0, name="", aperture=[]):
        ComponentBase.__init__(self, length, name, aperture)
        self.dummy = 0

    def Track(self, beam):
        # print 'DRIFT_TRACK'
        # Applies the transfer map for a drift to the particles in beam
        # I think the below is NOT as accurate as it might be...
        # this should be updated after some discussions with Wolski
        # The 1 is an approximation for high energy particles...
        d1 = numpy.sqrt(1 - beam.px * beam.px
                        - beam.py * beam.py
                        + 2 * beam.dp / beam.beta
                        + beam.dp * beam.dp)

        # TP: I have kept the 'old' method because I want to compare
        # against SAMM. When We think SAMPL is robust enought we should start
        # making changes

        # abve confirmed!
        # d1 = numpy.sqrt(((beam.gamma*beam.gamma -1)/
        #                   beam.gamma*beam.gamma*beam.beta*beam.beta)
        #                - beam.px * beam.px \
        #                - beam.py * beam.py \
        #                + 2 * beam.dp / beam.beta \
        #                + beam.dp * beam.dp)
        beam.x = beam.x + (self.length * beam.px) / d1
        beam.y = beam.y + self.length * beam.py / d1
        beam.ct = beam.ct + (self.length * (1 - (1 + beam.beta * beam.dp) / d1)
                             / beam.beta)

        # save
        self.lastTrackedBeam = beam

    # Space chargdrift for drift
    def TrackSpaceCharge(self, beam):

        d1 = numpy.sqrt(1 - beam.px * beam.px
                        - beam.py * beam.py
                        + 2 * beam.dp / beam.beta
                        + beam.dp * beam.dp)

        beam.x = beam.x + (self.length * beam.px) / d1 / 2
        beam.y = beam.y + self.length * beam.py / d1 / 2
        beam.ct = beam.ct + (self.length * (1 - (1 + beam.beta * beam.dp) / d1)
                             / beam.beta / 2)

        # Apply space charge kick
        # print beam.bunchcharge
        bunchcharge = beam.bunchcharge
        nparticles = len(beam.x)

        rx = numpy.zeros((nparticles, nparticles))
        ry = numpy.zeros((nparticles, nparticles))
        rz = numpy.zeros((nparticles, nparticles))

        for m in range(nparticles):
            for n in range(m):
                rx[m][n] = beam.x[m] - beam.x[n]
                ry[m][n] = beam.y[m] - beam.y[n]
                rz[m][n] = (beam.ct[m] - beam.ct[n]) * beam.gamma

        #print rx
        rx = rx - rx.T
        ry = ry - ry.T
        rz = rz - rz.T
        # print rx
        invr3 = numpy.power((rx**2 + ry**2 + rz**2), 1.5)
        #print invr3
        for m in range(nparticles):
            invr3[m][m] = 0

        dt = self.length / PhysicalConstants.SpeedOfLight / beam.gamma
        p0 = beam.momentum

        q = bunchcharge / nparticles
        #print q
        q2 = (PhysicalConstants.PositronCharge * q /
              4 / numpy.pi / PhysicalConstants.VacuumPermittivity)

        dpx = q2 * numpy.sum(rx * invr3, axis=1) * dt / p0
        dpy = q2 * numpy.sum(ry * invr3, axis=1) * dt / p0
        #
        # print dpx
        # Note - longitudinal kick not yet implemented!
        # dpz = sum(rz.*invr3,2)*dt;

        beam.px = beam.px + dpx.T
        beam.py = beam.py + dpy.T

        # Apply the second half of the drift
        d1 = numpy.sqrt(1 - beam.px * beam.px
                        - beam.py * beam.py
                        + 2 * beam.dp / beam.beta
                        + beam.dp * beam.dp)

        beam.x = beam.x + (self.length * beam.px) / d1 / 2
        beam.y = beam.y + self.length * beam.py / d1 / 2
        beam.ct = beam.ct + (self.length * (1 - (1 + beam.beta * beam.dp) / d1)
                             / beam.beta / 2)

        # save
        self.lastTrackedBeam = beam
