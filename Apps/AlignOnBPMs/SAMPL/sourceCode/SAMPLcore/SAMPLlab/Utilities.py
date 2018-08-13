
import PhysicalConstants
import numpy


def SpinRotation(beam, Bx, By, Bz, ds):

    [theta0, phi0] = beam.GetSpins()
    # initial x component of the polarisation
    polsnx0 = numpy.sin(theta0) * numpy.cos(phi0)
    # initial y component of the polarisation
    polsny0 = numpy.sin(theta0) * numpy.sin(phi0)
    # initial z component of the polarisation
    polsnz0 = numpy.cos(theta0)

    species = beam.species
    # beta*gamma for a particle with the reference momentum
    betagammaRef = (beam.momentum /
                    species.mass /
                    PhysicalConstants.SpeedOfLight)
    # relativistic gamma at the reference momentum
    gammaRef = numpy.sqrt(betagammaRef * betagammaRef + 1)
    # relativistic beta at the reference momentum
    betaRef = numpy.sqrt(1 - 1 / gammaRef / gammaRef)

    # relativistic gamma for each particle
    gamma = (beam.dp * betaRef + 1) * gammaRef
    # relativistic beta for each particle
    beta = numpy.sqrt(1 - numpy.divie(numpy.divide(1, gamma), gamma))
    # total normalised momentum
    ptot = beta * gamma / betagammaRef
    # CHECK!!!
    # normalised longitudinal momentum
    pz = numpy.real(numpy.sqrt(ptot * ptot -
                               beam.px * beam.px -
                               beam.py * beam.py))
    # This has to be a real number!  Something needs to be fixed...
    pdotb = numpy.divide(numpy.divide((beam.px * Bx + beam.py * By + pz * Bz),
                                      ptot),
                         ptot)

    bParx = pdotb * beam.px
    bPary = pdotb * beam.py
    bParz = pdotb * pz

    bPerpx = Bx - bParx
    bPerpy = By - bPary
    bPerpz = Bz - bParz

    emdg = numpy.divide(species.charge / species.mass, gamma)
    G = (species.g - 2) / 2
    omegax = -emdg * ((1 + G * gamma) * bPerpx + (1 + G) * bParx)
    omegay = -emdg * ((1 + G * gamma) * bPerpy + (1 + G) * bPary)
    omegaz = -emdg * ((1 + G * gamma) * bPerpz + (1 + G) * bParz)

    omega = numpy.sqrt(omegax * omegax + omegay * omegay + omegaz * omegaz)

    pdotomega = polsnx0 * omegax + polsny0 * omegay + polsnz0 * omegaz

    coswt = numpy.cos(omega * ds / PhysicalConstants.SpeedOfLight)
    sinwt = numpy.sin(omega * ds / PhysicalConstants.SpeedOfLight)
    if omega == 0:
        omega = float('Inf')

    polsnx1 = (polsnx0 * coswt +
               omegax * pdotomega * numpy.divide(numpy.divide((1 - coswt),
                                                              omega),
                                                 omega) +
               (polsnz0 * omegay - polsny0 * omegaz) * numpy.divide(sinwt,
                                                                    omega))

    polsny1 = (polsny0 * coswt +
               omegay * pdotomega * numpy.divide(numpy.divide((1 - coswt),
                                                              omega),
                                                 omega) +
               (polsnx0 * omegaz - polsnz0 * omegax) * numpy.divide(sinwt,
                                                                    omega))

    polsnz1 = (polsnz0 * coswt +
               omegaz * pdotomega * numpy.divide(numpy.divide((1 - coswt),
                                                              omega),
                                                 omega) +
               (polsny0 * omegax - polsnx0 * omegay) * numpy.divide(sinwt,
                                                                    omega))

    phi1 = numpy.arctan2(polsny1, polsnx1)
    theta1 = numpy.arccos(polsnz1)

    beam.SetSpins(theta1, phi1)
