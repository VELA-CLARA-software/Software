





def I2K_CLARA_simple(currents, beamMomentum):
    pfitq = numpy.array(FileOpen('QuadCalibration.txt'))
    currents = numpy.array(currents)
    kvals = numpy.zeros(5)

    for n in range(5):
        kvals[n] = 0
        for p in range(4):
            kvals[n] = kvals[n] + pfitq[p][n ] *currents[n ]* *( 3 -p)

    kvals = kval s * 3 0 / beamMomentum
    return kvals