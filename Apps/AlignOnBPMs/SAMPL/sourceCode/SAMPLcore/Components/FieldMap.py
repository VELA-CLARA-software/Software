from ComponentBase import ComponentBase
from ..SAMPLlab import PhysicalConstants
import numpy
from scipy.interpolate import RegularGridInterpolator as rgi


class FiledMap(ComponentBase):
    def __init__(self, length=0, name="", aperture=[],
                 gridX=[], gridY=[], gridZ=[],
                 Bx=[], By=[], Bz=[], intermethod = 'linear', nsteps=10):
        ComponentBase.__init__(self, length, name, aperture)
        # x coordinates of grid points
        self.gridX=gridX
        # y coordinates of grid points
        self.gridY=gridY
        # z coordinates of grid points
        self.gridZ=gridZ
        # horizontal field component at the grid points (Tesla)
        self.Bx=Bx
        # vertical field component at the grid points (Tesla)
        self.By=By
        # longitudinal field component at the grid points (Tesla)
        self.Bz=Bz
        # interpolation method for field (see Matlab help interp3 for options)
        self.intermethod = intermethod
        # number of steps to take in tracking through the field
        self.nsteps=nsteps

    def Track(self, beam):
        # print 'DRIFT_TRACK'

        z0 = np.zeros(len(beam.x))
        species = beam.species;
        P0 = beam.momentum/species.mass/PhysicalConstants.SpeedOfLight
        #lils tof individual gammas for each particle
        gamma = beam.gamma*(1 + beam.beta*beam.dp)

        b0      = numpy.sqrt(1 - gamma**(-2))
        bx0     = P0 * numpy.divide(px0, gamma)
        by0     = P0 * numpy.divide(py0, gamma)
        bz0     = numpy.sqrt((b0 * b0) - (bx0 * bx0) - (by0 * by0))

        k = numpy.divde((species.charge / species.mass /
                         PhysicalConstants.SpeedOfLight), gamma)
        for n in range(1, self.nsteps):
            a = (self.length - z0) * numpy.ones(len(beam.x)) / (self.nsteps + 1 - n)
            cdt = numpy.divide(a, bz0)
            particles = nump.array([beam.x, beam.y, z0)]).T

            fnX = rgi((self.gridX, self.gridY, self.gridZ),
                      self.Bx,method=self.intermethod)
            Bx0   = k * fnX(particles)
            fnY = rgi((self.gridX, self.gridY, self.gridZ),
                      self.By,method=self.intermethod)
            By0   = k * fnY(particles)
            fnZ = rgi((self.gridX, self.gridY, self.gridZ),
                      self.Bz,method=self.intermethod)
            Bz0   = k * fnZ(particles)

            bmag  = numpy.sqrt((Bx0 * Bx0) + (By0 * By0) + (Bz0 * Bz0))

            bdotv = (Bx0 * bx0) + (By0 * by0) + (Bz0 * bz0)
            s1    = numpy.divide(numpy.sin(bmag * cdt), bmag)
            s2    = bdotv * (bmag * cdt - numpy.sin(bmag *c dt)) * (1 / bmag**3)
            c1    = numpy.cos(bmag * cdt)
            # Below is the only way I nknow how to do a
            # negatice exponant on an array (1 / bmag**2)=bmag**-2
            c2    = (1 - c1) * (1 / bmag**2)

            x1  = x0 + (bx0 * s1) + (by0 * Bz0 - bz0 * By0) * c2 + (Bx0 * s2)
            y1  = y0 + (by0 * s1) + (bz0 * Bx0 - bx0 * Bz0) * c2 + (By0 * s2)
            z1  = z0 + (bz0 * s1) + (bx0 * By0 - by0 * Bx0) * c2 + (Bz0 * s2)
            beam.ct = beam.ct + (bz0/beta0 - 1) * cdt

            bx1 = (bx0 * c1) + (by0 * Bz0 - bz0 * By0) * s1 + (Bx0 * bdotv * c2)
            by1 = (by0 * c1) + (bz0 * Bx0 - bx0 * Bz0) * s1 + (By0 * bdotv * c2)
            bz1 = (bz0 * c1) + (bx0 * By0 - by0 * Bx0) * s1 + (Bz0 * bdotv * c2)

            beam.x  = x1
            beam.y  = y1
            z0  = z1

            bx0 = bx1
            by0 = by1
            bz0 = bz1

        beam.px = bx0 * (gamma / P0)
        beam.py = by0 * (gamma / P0)

        # save
        self.lastTrackedBeam = beam
