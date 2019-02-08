#!/usr/bin/python

from __future__ import division
import sys
import numpy as np
import scipy.spatial
from numpy import linalg
from random import random

class EllipsoidTool:
    """Some stuff for playing with ellipsoids"""
    def __init__(self): pass

    def getMinVolEllipse(self, P=None, tolerance=0.01):
        """ Find the minimum volume ellipsoid which holds all the points

        Based on work by Nima Moshtagh
        http://www.mathworks.com/matlabcentral/fileexchange/9542
        and also by looking at:
        http://cctbx.sourceforge.net/current/python/scitbx.math.minimum_covering_ellipsoid.html
        Which is based on the first reference anyway!

        Here, P is a numpy array of N dimensional points like this:
        P = [[x,y,z,...], <-- one point per line
             [x,y,z,...],
             [x,y,z,...]]

        Returns:
        (center, radii, rotation)

        """

        hull = scipy.spatial.ConvexHull(P).vertices
        P = np.array(P)[hull]


        (N, d) = np.shape(P)
        d = float(d)

        # Q will be our working array
        Q = np.vstack([np.copy(P.T), np.ones(N)])
        QT = Q.T

        # initializations
        err = 1.0 + tolerance
        u = (1.0 / N) * np.ones(N)

        # Khachiyan Algorithm
        while err > tolerance:
            V = np.dot(Q, np.dot(np.diag(u), QT))
            M = np.diag(np.dot(QT , np.dot(linalg.inv(V), Q)))    # M the diagonal vector of an NxN matrix
            j = np.argmax(M)
            maximum = M[j]
            step_size = (maximum - d - 1.0) / ((d + 1.0) * (maximum - 1.0))
            new_u = (1.0 - step_size) * u
            new_u[j] += step_size
            err = np.linalg.norm(new_u - u)
            u = new_u

        # center of the ellipse
        center = np.dot(P.T, u)

        # the A matrix for the ellipse
        A = linalg.inv(
                       np.dot(P.T, np.dot(np.diag(u), P)) -
                       np.array([[a * b for b in center] for a in center])
                       ) / d

        # Get the values we'd like to return
        U, s, rotation = linalg.svd(A)
        radii = 1.0/np.sqrt(s)

        return (center, radii, rotation, P)

    def getEllipsoidVolume(self, radii):
        """Calculate the volume of the blob"""
        return 4./3.*np.pi*radii[0]*radii[1]*radii[2]

    def plotEllipsoid(self, center, radii, rotation, ax=None, plotAxes=False, cageColor='b', cageAlpha=0.2):
        """Plot an ellipsoid"""
        make_ax = ax == None
        if make_ax:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

        u = np.linspace(0.0, 2.0 * np.pi, 100)
        v = np.linspace(0.0, np.pi, 100)

        # cartesian coordinates that correspond to the spherical angles:
        x = radii[0] * np.outer(np.cos(u), np.sin(v))
        y = radii[1] * np.outer(np.sin(u), np.sin(v))
        z = radii[2] * np.outer(np.ones_like(u), np.cos(v))
        # rotate accordingly
        for i in range(len(x)):
            for j in range(len(x)):
                [x[i,j],y[i,j],z[i,j]] = np.dot([x[i,j],y[i,j],z[i,j]], rotation) + center

        if plotAxes:
            # make some purdy axes
            axes = np.array([[radii[0],0.0,0.0],
                             [0.0,radii[1],0.0],
                             [0.0,0.0,radii[2]]])
            # rotate accordingly
            for i in range(len(axes)):
                axes[i] = np.dot(axes[i], rotation)


            # plot axes
            for p in axes:
                X3 = np.linspace(-p[0], p[0], 100) + center[0]
                Y3 = np.linspace(-p[1], p[1], 100) + center[1]
                Z3 = np.linspace(-p[2], p[2], 100) + center[2]
                ax.plot(X3, Y3, Z3, color=cageColor)

        # plot ellipsoid
        ax.plot_wireframe(x, y, z,  rstride=4, cstride=4, color=cageColor, alpha=cageAlpha)

        if make_ax:
            plt.show()
            plt.close(fig)
            del fig

def ellipse(center, radii, rotation, color='b'):
    a,b = radii
    theta = np.arange(0, 2*3.14159+1/20., 1/20.)
    ab = [[a*np.cos(t), b*np.sin(t)] for t in theta]
    vvab = np.dot(ab, rotation)
    ell = center + vvab
    return Polygon(ell, True, alpha=0.4, color=color)

def remove_Hull(P, desired_len):
    desired_len = int(np.floor(desired_len))
    Q = list(P)
    while len(Q) > desired_len:
        hull = sorted(scipy.spatial.ConvexHull(Q).vertices[:len(Q)-desired_len], reverse=True)
        for s in hull:
            del Q[s]
    return Q

def gaussian_fraction(s, n):
    return n*(1 - np.exp(-1*(s**2)/2))

if __name__ == "__main__":
    # make 100 random points
    from generateGaussianBeamDistribution import *
    from matplotlib.patches import Circle, Wedge, Polygon
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    import timeit
    from functools import partial
    ET = EllipsoidTool()

    beam = generateGaussianBeamDistribution(n=1e3, twiss=[-5.,1.,0,1])
    print( '6D Volume = ', scipy.spatial.ConvexHull(beam).volume)
    P = np.transpose([beam[:,0], beam[:,1]])

    part = partial(scipy.spatial.ConvexHull, P)
    print (timeit.timeit(part, number=10))

    Q = P#np.array(remove_Hull(P, gaussian_fraction(1, len(P))))
    (center, radii, rotation, hullP) = ET.getMinVolEllipse(Q, .001)

    cov = np.cov(np.transpose(P))
    rmsemit = np.sqrt(np.linalg.det(cov))
    w, v = np.linalg.eig(cov)

    # print ('emittance = ', radii[0] * radii[1])
    # print ('rms emittance = ', rmsemit)
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.add_artist(ellipse(center, radii, rotation, color='b'))
    ax.add_artist(ellipse([0,0], np.sqrt(w), np.transpose(v), color='r'))

    # e.set_clip_box(ax.bbox)

    # plot points
    P = np.array(P)
    ax.scatter(P[::int(np.ceil(len(P)/10000)),0], P[::int(np.ceil(len(P)/10000)),1], color='g', s=1)
    ax.scatter(hullP[:,0], hullP[:,1], color='r', s=10)
    hull = scipy.spatial.ConvexHull(P)
    print( 'hull = ', hull)
    for simplex in hull.simplices:
        print( simplex)
        ax.plot(P[simplex, 0], P[simplex, 1], 'k-')
    plt.show()
    plt.close(fig)
    del fig
