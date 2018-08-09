# SAM to Python Conversion
# DJS August 2017
# Version 0.1
#
import numpy
from ComponentBase import ComponentBase


class BeamPositionMonitor(ComponentBase):
    def __init__(self, length=0, name="", aperture=[]):
        ComponentBase.__init__(self, length, name, aperture)
        self.dummy = 0
        self.x = None
        self.y = None

    def Track(self, beam):
        # currently no buffer pointers like in SAMM
        # Track drift through bpm
        d1 = numpy.sqrt(1 - beam.px * beam.px
                        - beam.py * beam.py
                        + 2 * beam.dp / beam.beta
                        + beam.dp * beam.dp)
        beam.x = beam.x + (self.length * beam.px) / d1
        beam.y = beam.y + (self.length * beam.py) / d1
        beam.ct = (beam.ct +
                   self.length * (1 - (1 + beam.beta * beam.dp) / d1)
                   / beam.beta)
        # Next, Calc Y and Y at the end of the BPM
        self.x = numpy.mean(beam.x)
        self.y = numpy.mean(beam.y)
        # save
        self.lastTrackedBeam = beam
