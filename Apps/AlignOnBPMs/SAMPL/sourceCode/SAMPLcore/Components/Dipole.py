# SAM to Python Conversion
# DJS August 2017
# Version 0.1
#
from ..SAMPLlab import PhysicalConstants
from ComponentBase import ComponentBase
import numpy


class Dipole(ComponentBase):
    def __init__(self,field=0,gradient=0,hgap=0,e1=0,fint1=0,fint2=0,
                 e2=0,length=0, name="", aperture=[],theta=0,curvature=0):
        ComponentBase.__init__(self, length, name, aperture)
        # dipole field strength, in tesla
        self.field = field
        # quadrupole gradient, in tesla/metre
        self.gradient = gradient
        # gap height (for fringe field map), in metres
        self.hgap = hgap
        # entrance pole face rotation, in radians
        self.e1 = e1
        # entrance fringe field integral
        self.fint1 = fint1
        # exit pole face rotation, in radians
        self.e2 = e2
        # exit fringe field integral
        self.fint2 = fint2
        #  bending angle in radians
        if theta != 0:
            self.theta = theta
        if curvature != 0:
            self.__curvature = curvature

    # get the radius of curvature
    @property
    def curvature(self):
        return self.__curvature

    @curvature.setter
    def curvature(self, curvature):
        self.__curvature = curvature

    @property
    def theta(self):
        return self.length * self.__curvature

    @theta.setter
    def theta(self, theta):
        self.__curvature = theta / self.length

    def Track(self, beam):
        # print 'DIP_TRACK'
        k0 = self.field / beam.rigidity
        d1 = numpy.sqrt(1 + 2 * beam.dp / beam.beta + beam.dp * beam.dp)
        # First, apply a map for the entrance fringe field
        sine1 = numpy.sin(self.e1)
        phi = (2 * self.fint1 * self.hgap * k0 * (1 + sine1 * sine1)
               / numpy.cos(self.e1))
        r10 = k0 * numpy.tan(self.e1)
        r32 = -k0 * numpy.tan(self.e1 - phi)

        beam.px = beam.px + r10 * beam.x
        beam.py = beam.py + r32 * beam.y

        # Then, apply a map for the body of the dipole
        k1 = self.gradient / beam.rigidity
        a1 = self.curvature - k0 / d1

        wx = numpy.sqrt((self.__curvature * k0 + k1) / d1)
        xc = numpy.cos(wx * self.length)
        xs = numpy.sin(wx * self.length) / wx
        xs2 = numpy.sin(2 * wx * self.length) / wx
        wy = numpy.sqrt(k1 / d1)
        yc = numpy.cosh(wy * self.length)


        if(wy.any() != 0):
            ys = numpy.sinh(wy * self.length) / wy
            ys2 = numpy.sinh(2 * wy * self.length) / wy
        else:
            ys = self.length
            ys2 = 2 * self.length

        x2 = (beam.x * xc) + (beam.px * xs / d1) + (a1 * (1 - xc) / wx / wx)
        px2 = (-d1 * wx * wx * beam.x * xs) + (beam.px * xc) + (a1 * xs * d1)
        y2 = (beam.y * yc) + (beam.py * ys / d1)
        py2 = (d1 * wy * wy * beam.y * ys) + (beam.py * yc)

        d0 = 1 / beam.beta + beam.dp

        c0 = ((1 / beam.beta - d0 / d1) * self.length
              - d0 * a1 * (self.curvature * (self.length - xs)
              + a1 * (2 * self.length - xs2) / 8) / wx / wx / d1)

        c1 = -d0 * (self.curvature * xs -
                    a1 * (2 * self.length - xs2) / 4) / d1
        c2 = -d0 * (self.curvature * (1 - xc) / wx / wx +
                    a1 * xs * xs / 2) / d1 / d1

        c11 = -d0 * wx * wx * (2 * self.length - xs2) / d1 / 8
        c12 = d0 * wx * wx * xs * xs / d1 / d1 / 2
        c22 = -d0 * (2 * self.length + xs2) / d1 / d1 / d1 / 8

        c33 = -d0 * wy * wy * (2 * self.length - ys2) / d1 / 8
        c34 = -d0 * wy * wy * ys * ys / d1 / d1 / 2
        c44 = -d0 * (2 * self.length + ys2) / d1 / d1 / d1 / 8

        beam.ct = (beam.ct + c0 + c1 * beam.x + c2 * beam.px +
                   c11 * beam.x * beam.x + c12 * beam.x * beam.px +
                   c22 * beam.px * beam.px + c33 * beam.y * beam.y +
                   c34 * beam.y * beam.py + c44 * beam.py * beam.py)

        # Finally, apply a map for the exit fringe field
        sine2 = numpy.sin(self.e2)
        phi = (2 * self.fint2 * self.hgap * k0 * (1 + sine2 * sine2)
               / numpy.cos(self.e2))
        r10 = k0 * numpy.tan(self.e2)
        r32 = -k0 * numpy.tan(self.e2 - phi)

        beam.px = px2 + r10 * x2
        beam.py = py2 + r32 * y2
        beam.x = x2
        beam.y = y2

        # save
        self.lastTrackedBeam = beam

    def TrackSpaceCharge(self, beam):
        k0 = self.field / beam.rigidity
        d1 = numpy.sqrt(1 + 2 * beam.dp / beam.beta + beam.dp * beam.dp)
        # First, apply a map for the entrance fringe field
        sine1 = numpy.sin(self.e1)
        phi = (2 * self.fint1 * self.hgap * k0 * (1 + sine1 * sine1)
               / numpy.cos(self.e1))
        r10 = k0 * numpy.tan(self.e1)
        r32 = -k0 * numpy.tan(self.e1 - phi)

        beam.px = beam.px + r10 * beam.x
        beam.py = beam.py + r32 * beam.y

        # Then, apply a map for fist HALF of the body of the dipole
        k1 = self.gradient / beam.rigidity
        a1 = self.curvature - k0 / d1

        wx = numpy.sqrt((self.curvature * k0 + k1) / d1)
        xc = numpy.cos(wx * self.length/2)
        xs = numpy.sin(wx * self.length/2) / wx
        xs2 = numpy.sin(2 * wx * self.length/2) / wx
        wy = numpy.sqrt(k1 / d1)
        yc = numpy.cosh(wy * self.length/2)

        if(wy.any() != 0):
            ys = numpy.sinh(wy * self.length/2) / wy
            ys2 = numpy.sinh(2 * wy * self.length/2) / wy
        else:
            ys = self.length/2
            ys2 = 2 * self.length/2

        x2 = (beam.x * xc) + (beam.px * xs / d1) + (a1 * (1 - xc) / wx / wx)
        px2 = (-d1 * wx * wx * beam.x * xs) + (beam.px * xc) + (a1 * xs * d1)
        y2 = (beam.y * yc) + (beam.py * ys / d1)
        py2 = (d1 * wy * wy * beam.y * ys) + (beam.py * yc)

        d0 = 1 / beam.beta + beam.dp

        c0 = ((1 / beam.beta - d0 / d1) * self.length/2
              - d0 * a1 * (self.curvature * (self.length/2 - xs)
              + a1 * (2 * self.length/2 - xs2) / 8) / wx / wx / d1)

        c1 = -d0 * (self.curvature * xs -
                    a1 * (2 * self.length/2 - xs2) / 4) / d1
        c2 = -d0 * (self.curvature * (1 - xc) / wx / wx +
                    a1 * xs * xs / 2) / d1 / d1

        c11 = -d0 * wx * wx * (2 * self.length/2 - xs2) / d1 / 8
        c12 = d0 * wx * wx * xs * xs / d1 / d1 / 2
        c22 = -d0 * (2 * self.length/2 + xs2) / d1 / d1 / d1 / 8

        c33 = -d0 * wy * wy * (2 * self.length/2 - ys2) / d1 / 8
        c34 = -d0 * wy * wy * ys * ys / d1 / d1 / 2
        c44 = -d0 * (2 * self.length/2 + ys2) / d1 / d1 / d1 / 8

        beam.ct = (beam.ct + c0 + c1 * beam.x + c2 * beam.px +
                   c11 * beam.x * beam.x + c12 * beam.x * beam.px +
                   c22 * beam.px * beam.px + c33 * beam.y * beam.y +
                   c34 * beam.y * beam.py + c44 * beam.py * beam.py)

        # SPACE CHARGE KICK
        # Apply space charge kick
        #print beam.bunchcharge
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
        #print dpx
        # Note - longitudinal kick not yet implemented!
        # dpz = sum(rz.*invr3,2)*dt;

        beam.px = beam.px + dpx.T
        beam.py = beam.py + dpy.T

        # Then, apply a map for second HALF of the body of the dipole
        k1 = self.gradient / beam.rigidity
        a1 = self.curvature - k0 / d1

        wx = numpy.sqrt((self.curvature * k0 + k1) / d1)
        xc = numpy.cos(wx * self.length/2)
        xs = numpy.sin(wx * self.length/2) / wx
        xs2 = numpy.sin(2 * wx * self.length/2) / wx
        wy = numpy.sqrt(k1 / d1)
        yc = numpy.cosh(wy * self.length/2)

        if(wy.any() != 0):
            ys = numpy.sinh(wy * self.length/2) / wy
            ys2 = numpy.sinh(2 * wy * self.length/2) / wy
        else:
            ys = self.length/2
            ys2 = 2 * self.length/2

        x2 = (beam.x * xc) + (beam.px * xs / d1) + (a1 * (1 - xc) / wx / wx)
        px2 = (-d1 * wx * wx * beam.x * xs) + (beam.px * xc) + (a1 * xs * d1)
        y2 = (beam.y * yc) + (beam.py * ys / d1)
        py2 = (d1 * wy * wy * beam.y * ys) + (beam.py * yc)

        d0 = 1 / beam.beta + beam.dp

        c0 = ((1 / beam.beta - d0 / d1) * self.length/2
              - d0 * a1 * (self.curvature * (self.length/2 - xs)
              + a1 * (2 * self.length/2 - xs2) / 8) / wx / wx / d1)

        c1 = -d0 * (self.curvature * xs -
                    a1 * (2 * self.length/2 - xs2) / 4) / d1
        c2 = -d0 * (self.curvature * (1 - xc) / wx / wx +
                    a1 * xs * xs / 2) / d1 / d1

        c11 = -d0 * wx * wx * (2 * self.length/2 - xs2) / d1 / 8
        c12 = d0 * wx * wx * xs * xs / d1 / d1 / 2
        c22 = -d0 * (2 * self.length/2 + xs2) / d1 / d1 / d1 / 8

        c33 = -d0 * wy * wy * (2 * self.length/2 - ys2) / d1 / 8
        c34 = -d0 * wy * wy * ys * ys / d1 / d1 / 2
        c44 = -d0 * (2 * self.length/2 + ys2) / d1 / d1 / d1 / 8

        beam.ct = (beam.ct + c0 + c1 * beam.x + c2 * beam.px +
                   c11 * beam.x * beam.x + c12 * beam.x * beam.px +
                   c22 * beam.px * beam.px + c33 * beam.y * beam.y +
                   c34 * beam.y * beam.py + c44 * beam.py * beam.py)
        # Finally, apply a map for the exit fringe field
        sine2 = numpy.sin(self.e2)
        phi = (2 * self.fint2 * self.hgap * k0 * (1 + sine2 * sine2)
               / numpy.cos(self.e2))
        r10 = k0 * numpy.tan(self.e2)
        r32 = -k0 * numpy.tan(self.e2 - phi)

        beam.px = px2 + r10 * x2
        beam.py = py2 + r32 * y2
        beam.x = x2
        beam.y = y2

        # save
        self.lastTrackedBeam = beam
