import numpy as np
from numpy import linalg as LA
from ..SAMPLlab.PhysicalConstants import PhysicalConstants
from ..Components.MasterOscillator import MasterOscillator


def ComputeClosedOrbit(beamline, beam):
    m = np.zeros((6, 6))
    xco = np.zeros(6)

    lf = np.zeros((6, 6))
    lf[5, 4] = 1e-12

    itern = 1
    resdl = 1
    precn = beamline.precision

    while (itern < 10) and (resdl > 10 * precn * precn):

        p = precn * np.eye(6, 7)
        for n in range(8):
            p[:, n] = p[:, n] + xco

        beam.particles = p
        beam.globaltime = 0
        beam = beamline.Track([0, len(beamline.componentlist) - 1], beam)

        p1 = beam.particles
        for n in range(7):
            m[:, n] = (p1[:, n] - p1[:, 6]) / precn

        if m[6, 4] == 0:
            # add some longitudinal focusing
            m = (np.eye(6) - np.sign(m[4, 5]) * lf) * m

        dt = beam.globaltime * MasterOscillator.GetFrequency()
        p1[4, 6] = p1[4, 6] - ((dt - round(dt)) * beam.beta *
                               PhysicalConstants.SpeedOfLight /
                               MasterOscillator.GetFrequency())

        d = p1[:, 7] - xco
        dco = LA.inv(np.eye(6) - m) * d
        resdl = dco.T * dco
        xco = xco + dco

        itern = itern + 1

    beam.particles = xco
    beam.globaltime = 0

    closedorbit = np.zeros((6, len(beamline.componentlist) + 1))
    closedorbit[:, 1] = xco
    for n in range(len(beamline.componentlist)):
        beam = beamline.componentlist[n].Track(beam)
        closedorbit[:, n + 1] = beam.particles

    return closedorbit, m
