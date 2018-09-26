import numpy as np

def DispersionMatrix(dispersionList):
    dx, dpx, dy, dpy = map(float, dispersionList)
    return [[1,0,0,0,0,dx],[0,1,0,0,0,dpx],[0,0,1,0,0,dy],[0,0,0,1,0,dpy],[0,0,0,0,1,0],[0,0,0,0,0,1]]

def BetaMatrix(betx, bety):
    return [[np.sqrt(betx),0,0,0,0,0],[0,np.sqrt(1/betx),0,0,0,0],[0,0,np.sqrt(bety),0,0,0],[0,0,0,np.sqrt(1/bety),0,0],[0,0,0,0,1,0],[0,0,0,0,0,1]]

def AlfaMatrix(alfx, alfy):
    return [[1,0,0,0,0,0],[-float(alfx),1,0,0,0,0],[0,0,1,0,0,0],[0,0,-float(alfy),1,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1]]

def CouplingMatrix(couplingList):
    xy, xyp, xpy, xpyp = couplingList
    return [[1,0,xy,xyp,0,0],[0,1,xpy,xpyp,0,0],[0,0,1,0,0,0],[0,0,0,1,0,0],[0,0,0,0,1,0],[0,0,0,0,0,1]]

def eMatrix(emittancelist, n):
    ex, ey, deltap, ct = map(float, emittancelist)
    n = int(n)
    return [np.random.normal(0, np.sqrt(ex), size=n), np.random.normal(0, np.sqrt(ex), size=n), np.random.normal(0, np.sqrt(ey), size=n), \
             np.random.normal(0, np.sqrt(ey), size=n), np.random.normal(0, ct, size=n), np.random.normal(0, deltap, size=n)]

def generateGaussianBeamDistribution(n=1, emittances=[1,1,0,1e-3], twiss=[0,1,0,1], dispersion=[0,0,0,0], coupling=[0,0,0,0]):
    D = DispersionMatrix(dispersion)
    B = BetaMatrix(twiss[1], twiss[3])
    A = AlfaMatrix(twiss[0], twiss[2])
    C = CouplingMatrix(coupling)
    e = eMatrix(emittances, n)
    return np.transpose(np.linalg.multi_dot([D,B,A,C,e]))

if __name__ == "__main__":
    beam = generateGaussianBeamDistribution(n=1e6, twiss=[-3.,10.,0,1])
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # plot points
    ax.scatter(beam[::100,0], beam[::100,1], color='r', s=1)
    plt.show()
    plt.close(fig)
    del fig
