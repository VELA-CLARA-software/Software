# SAM to Python Conversion
# DJS August 2017
# Version 0.1
#
from ComponentBase import ComponentBase
# from ..SAMMlab import Beam
from ..SAMPLlab import MasterOscillator
from ..SAMPLlab import PhysicalConstants
import numpy

class RFCavity(ComponentBase):
    def __init__(self, voltage=0, harmonic=1, phase=numpy.pi, length=0,
                 name="", aperture=[]):
        ComponentBase.__init__(self, length, name, aperture)
        # in volts
        self.voltage = voltage
        # frequency (in units of master oscillator frequency)
        self.harmonic = harmonic
        # relative to master oscillator, in radians
        self.phase = phase
        # 1x2 array of elliptical aperture half-axes, in metres
        self.aperture = aperture

    def setFrequency(self, f):
        MasterOscillator.SetFrequency(f / self.harmonic)

    def getFrequency(self):
        return self.harmonic * MasterOscillator.GetFrequency()

    def Track(self, beam):
        # Applies the dynamical map for an RF cavity to the particles
        # in beam1.  The reference momentum is unchanged.
        mofreq = MasterOscillator.GetFrequency()
        ds = self.length
        f = self.harmonic * mofreq
        # First apply a drift through ds/2
        d1 = numpy.sqrt(1 - beam.px**2 - beam.py**2 +
                        2 * beam.dp / beam.beta + beam.dp**2)
        x1 = beam.x + ds * beam.px / d1 / 2
        y1 = beam.y + ds * beam.py / d1 / 2
        ct1 = beam.ct + ds * (1 - (1 + beam.dp * beam.beta) / d1) / beam.beta / 2
        # Next, apply an rf 'kick'
        p = numpy.floor(beam.globaltime * mofreq)
        beam.globaltime = beam.globaltime - (p / mofreq)
        t = (beam.globaltime -
             ct1 / (beam.beta * PhysicalConstants.SpeedOfLight))
        ft = (f * t) - numpy.floor(f * t)
        vnorm = self.voltage / beam.rigidity / PhysicalConstants.SpeedOfLight
        beam.dp = beam.dp + (vnorm * math.sin((2 * math.pi * ft) + self.phase))
        # Finally, apply a second drift through ds/2
        d1 = numpy.sqrt(1 - beam.px**2 - beam.py**2 +
                        2 * beam.dp / beam.beta + beam.dp**2)
        beam.x = x1 + (ds * beam.x) / d1 / 2
        beam.y = y1 + (ds * beam.y) / d1 / 2
        beam.ct = ct1 + (ds * (1 - (1 + beam.beta * beam.dp) / d1) /
                         beam.beta / 2)
        # save
        self.lastTrackedBeam = beam
