from numpy import linalg as LA
import numpy as np


def MakeMatchedBunch(orbit, beta, emittances, nparticles):
    S = np.array(([0, 1, 0, 0, 0, 0],
                  [-1, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, 0, 0],
                  [0, 0, -1, 0, 0, 0],
                  [0, 0, 0, 0, 0, 1],
                  [0, 0, 0, 0, -1, 0]))

    # Construct the correlation (sigma) matrix for
    # the given beta functions and emittances
    #print beta[:][:][0]
    sigma = (beta[0, :, :] * emittances[0] +
             beta[1, :, :] * emittances[1] +
             beta[2, :, :] * emittances[2])
    # Find the eigensystem of sigma*S

    D, V = LA.eig(np.dot(sigma, S))
    # Sort the eigenvalues and eigenvectors into conjugate pairs
    indx = np.argsort(-np.absolute(np.diag(D)))
    D = -np.sort(-np.absolute(D))
    V = V[:, indx[0]]
    # Normalise the eigenvectors
    w = np.diag(np.dot(np.matrix(V).getH(),np.dot(S, V)))
    V = np.dot(V, np.diag(np.divide(1, np.sqrt(w))))

    nmat = np.sqrt(2) * np.array([np.real(V[:][0]), np.imag(V[:][0]),
                                 np.real(V[:][2]), np.imag(V[:][2]),
                                 np.real(V[:][4]), np.imag(V[:][4])])
    nmat = nmat.T
    xn = np.dot(np.diag(np.sqrt(D)), np.random.randn(6, nparticles))
    
    #print np.dot(orbit, np.ones((1,nparticles)))
    particles = (np.dot(orbit, np.ones((1,nparticles))) + np.dot(nmat, xn)).T

    return particles
