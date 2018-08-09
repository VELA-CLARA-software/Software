import numpy as np


def ComputeTransferMatrix(beamline, startStop, beam, trajectory):
    n = startStop[1] - startStop[0] + 2
    eref = beam.energy * np.ones(n)
    m = np.zeros((n, 6, 6))
    m[0, :, :] = np.eye(6)

    precn = beamline.precision
    print precn
    p = precn * np.eye(6, 6)
    for i in range(6):
        p[:, i] = p[:, i] + trajectory

    beam.particles = p
    #print beam.particles

    for i in range(startStop[0], startStop[1] + 1):
        print i
        print beamline.componentlist[i].name
        beamline.componentlist[i].Track(beam)
        p1 = beam.particles.T
        # print p1
        for j in range(6):
            m[i - startStop[0] + 1, j, :] = (p1[j] - trajectory) / precn

        eref[i - startStop[0] + 1] = beam.energy
    return m, eref
