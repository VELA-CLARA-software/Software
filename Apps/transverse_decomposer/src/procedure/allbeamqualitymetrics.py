# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 11:27:26 2021

@author: fdz57121
"""

from src.procedure.bqfunctionsminuszernike import rmsqualityfactor, msessim
from src.procedure.zernikefunctions import fitting


def beamquality(image, centre, max_radius):
    # centre is in form [cx,cy]
    aRMS, rRMS, qfactor = rmsqualityfactor(image, centre, max_radius)

    mseuni, msetrun, ssimuni, ssimtrun = msessim(image, centre, max_radius)

    coeff, symm, assym = fitting(image, centre, max_radius,
                                 100)  # second parameter is number of zernikes fit

    return (aRMS, rRMS, qfactor, mseuni, msetrun, ssimuni, ssimtrun, coeff, assym, symm)

