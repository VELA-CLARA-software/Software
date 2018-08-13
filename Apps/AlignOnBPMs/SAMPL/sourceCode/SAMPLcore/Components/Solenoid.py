# SAM to Python Conversion
# DJS August 2017
# Version 0.1
from ComponentBase import ComponentBase
import numpy

class Solenoid(ComponentBase):
    def __init__(self,field=0,taper=0,length=0, name="", aperture=[]):
        ComponentBase.__init__(self, length, name, aperture)
        # solenoid field in tesla
        self.field = field
        # taper parameter, in / metre
        self.taper = taper

    def Track(self,beam):
        # Solenoid.Track(beam)
        # Applies the dynamical map for a solenoid to the particles
        # in beam1.
        # Note that the path length is approximate.

        # First, apply a drift map through  self.length/2
        # to the longitudinal coordinate
        d1 = numpy.sqrt(1 - beam.px * beam.px - beam.py * beam.py +
                        2 * beam.dp / beam.beta + beam.dp * beam.dp)
        ct1 = beam.ct + (self.length * (1 - (1 + beam.beta * beam.dp) / d1)
                         / beam.beta / 2)
        #% Now apply a solenoid map to the transverse variables
        gds   = self.taper * self.length
        b1    = self.field / (1 + gds)

        helmA = numpy.sqrt(self.field/b1) * np.ones( len(beam.x0) ) # CHECK
        helmB = 2 * beam.rigidity * (1 + beam.dp) / numpy.sqrt(self.field * b1)
        helmF = -1 / helmB
        helmG =  1 / helmA

        w = self.field * self.length / 2 / beam.rigidity / (1 + beam.dp)
        if gds != 0:
            w = w * numpy.log(1 + gds) / gds # ! CHECK log

        cw2 = numpy.cos(w) * numpy.cos(w)
        s2w = numpy.sin(2 * w)
        sw2 = numpy.sin(w) * numpy.sin(w)

        beam.x  = (helmA * cw2 * beam.x + helmB * s2w * beam.px / 2 +
                   helmA * s2w * beam.y / 2 + helmB * sw2 * beam.py)
        beam.px = (helmF * s2w * beam.x / 2 + helmG * cw2 * beam.px +
                   helmF * sw2 * beam.y + helmG * s2w * beam.py / 2)
        beam.y = -(helmA * s2w * beam.x / 2 - helmB * sw2 * beam.px +
                   helmA * cw2 * beam.y + helmB * s2w * beam.py / 2)
        beam.py = -(helmF * sw2 * beam.x - helmG * s2w * beam.px / 2 +
                    helmF * s2w * beam.y / 2 + helmG * cw2 * beam.py)

        #% First, apply a drift map through  self.length/2
        #% to the longitudinal coordinate
        d1 = numpy.sqrt(1 - beam.px * beam.px - beam.py * beam.py +
                        2 * beam.dp / beam.beta + beam.dp * beam.dp)
        beam.ct = ct1 + (self.length * (1 - (1 + beam.beta * beam.dp) / d1)
                         / beam.beta / 2)
        # save
        self.lastTrackedBeam = beam

    def GetBField(self,beam):
        # Solenoid.GetBField(beam)
        # Returns the magnetic field (in tesla) at the locations of
        # the particles in the beam.
        gds = self.taper * self.length
        bx = beam.x * self.field * self.g / (1 + gds) / 2
        by = beam.y * self.field * self.g / (1 + gds) / 2
        bz = self.field * numpy.ones(len(beam.x))

        if gds != 0:
            bz = self.bz * (numpy.log(1 + gds) / gds)

        return [bx, by, bz]

    def TrackSpin(self, beam):
        # Octupole.Trackspin(beam)
        # Tracks particle spins through an Octupole.
        [bx, by, bz] = self.GetBField(beam)
        Utilities.SpinRotation(beam, bx, by, bz, self.length)
