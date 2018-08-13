from numpy import linalg as LA
import ComputeClosedOrbit as CCO
import ComputeTransferMatrix as CTM
import numpy as np


def standardphase(m):

    psix = np.angle(m[0, 1] + 1j * m[0, 0]) - np.pi / 2
    psiy = np.angle(m[2, 3] + 1j * m[2, 2]) - np.pi / 2
    psiz = np.angle(m[4, 5] + 1j * m[4, 4]) - np.pi / 2

    rot = [[np.cos(psix), np.sin(psix), 0, 0, 0, 0],
           [-np.sin(psix), np.cos(psix), 0, 0, 0, 0],
           [0, 0, np.cos(psiy), np.sin(psiy), 0, 0],
           [0, 0, -np.sin(psiy), np.cos(psiy), 0, 0],
           [0, 0, 0, 0, np.cos(psiz), np.sin(psiz)],
           [0, 0, 0, 0, -np.sin(psiz), np.cos(psiz)]]

    mrot = m * rot
    return mrot


def ComputeMatchedTwiss(beamline, beam):

    # [beta tune closedorbit] = FindMatchedTwiss(beamline,rigidity)
    # Find the lattice functions around the ring, the betatron and
    #  synchrotron tunes, and the closed orbit.

    # beta(n,i,j,k) is a four dimensional array containing the lattice functions:
    # - n is an element index specifying the location in the lattice;
    # - i,j are indices of a 6x6 matrix (see below);
    # - k (=1,2,3) is an index specifying a degree of freedom.

    # tune(k) is a list of the three tunes, with k specifying a degree of freedom.

    # closedorbit(6,n) contains the closed orbit at each point around the ring.

    # In an uncoupled lattice:
    # - beta(:,1,1,1) is beta_x around the ring
    # - beta(:,1,2,1) is -alpha_x
    # - beta(:,2,2,1) is gamma_x
    # - beta(:,3,3,2) is beta_y
    # - beta(:,3,4,2) is -alpha_y
    # - beta(:,4,4,2) is gamma_y

    S = [[0, 1, 0, 0, 0, 0],
         [-1, 0, 0, 0, 0, 0],
         [0, 0, 0, 1, 0, 0],
         [0, 0, -1, 0, 0, 0],
         [0, 0, 0, 0, 0, 1],
         [0, 0, 0, 0, -1, 0]]

    T1 = [[0, 1, 0, 0, 0, 0],
          [1, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0]]

    T2 = [[0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0],
          [0, 0, 0, 1, 0, 0],
          [0, 0, 1, 0, 0, 0],
          [0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0]]

    T3 = [[0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 1],
          [0, 0, 0, 0, 1, 0]]

    closedorbit = CCO.ComputeClosedOrbit(beamline, beam)
    m = CTM.ComputeTransferMatrix(beamline,
                                  [0, len(beamline.componentlist) - 1],
                                  beam, closedorbit[:, 1])

    m1 = m[:, :, end]

    if m1[5][4] == 0:
        # add some longitudinal focusing
        lf = np.zeros(6, 6)
        lf[5][4] = 1e-12
        m1 = (np.eye(6) - np.sign(m1[4][5]) * lf) * m1

    # Find the eigensystem of the transfer matrix
    D, V = LA.eig(m1[:, :, end])

    # Sort the eigenvalues and eigenvectors into conjugate pairs
    indx = np.argsort(-np.absolute(np.diag(D)))
    V = V[:, indx[0]]

    # Normalise the eigenvectors
    w = np.diag(np.dot(np.matrix(V).getH(), np.dot(S, V)))
    V = np.dot(V, np.diag(np.divide(1, np.sqrt(w))))

    # Attempt to sort the eigenvectors into horizontal, vertical, and
    # longitudinal
    vsort = np.zeros((3, 3))
    for mi in range(1, 7, 2):
        normv = V[:, mi].T * V[:, mi]
        for ni in range(1, 7, 2):
            Vsub = V[(ni - 1):(ni), mi]
            vsort[ni / 2, mi / 2] = (Vsub.T * Vsub) / normv
    t = np.matrix(vsort)
    ix = t.max(0)
    ix1 = np.zeros(6)
    ix1[0] = 2 * ix[0] - 1
    ix1[1] = 2 * ix[1]
    ix1[2] = 2 * ix[2] - 1
    ix1[3] = 2 * ix[3]
    ix1[4] = 2 * ix[4] - 1
    ix1[5] = 2 * ix[5]
    V = V[:, ix1]

    # Calculate the Twiss parameters at the start of the beamline...
    beta = np.zeros((6, 6, 3, len(beamline.componentlist) + 1))
    beta[:, :, 1, 1] = V * T1 * V.T
    beta[:, :, 2, 1] = V * T2 * V.T
    beta[:, :, 3, 1] = V * T3 * V.T

    # Check to see if the "transverse" beta matrices are in the expected order.
    # If not, swap them round.
    if (beta(3, 3, 1, 1) > beta(1, 1, 1, 1)) and (beta(1, 1, 2, 1) > beta(3, 3, 2, 1)):
        beta1 = beta[:, :, 1, :]
        beta2 = beta[:, :, 0, :]
        beta[:, :, 0, :] = beta1
        beta[:, :, 1, :] = beta2
        V1 = V[:, 2]
        V2 = V[:, 3]
        V3 = V[:, 0]
        V4 = V[:, 1]
        V[:, 0] = V1
        V[:, 1] = V2
        V[:, 2] = V3
        V[:, 3] = V4

    mu = np.zeros(len(beamline.componentlist) + 1, 3)

    nmat = np.sqrt(2) * np.array([np.real(V[:][0]), np.imag(V[:][0]),
                                 np.real(V[:][2]), np.imag(V[:][2]),
                                 np.real(V[:][4]), np.imag(V[:][4])])
    nmat = standardphase(nmat)

    # ...and propagate along the beamline.
    for n in range(1, len(beamline.componentlist) + 1):
        m1 = m[:, :, n]
        beta[:, :, 1, n] = m1 * beta[:, :, 1, 1] * m1.T
        beta[:, :, 2, n] = m1 * beta[:, :, 2, 1] * m1.T
        beta[:, :, 3, n] = m1 * beta[:, :, 3, 1] * m1.T

        nmat1 = standardphase(m1 * nmat)
        R = LA.inv(nmat1) * m1 * nmat
        mu[n, :] = np.arctan2([R[0, 1], R[2, 3], R[4, 5]],
                              [R[0, 0], R[2, 2], R[4, 4]])

    tune = abs(np.unwrap(mu)) / 2 / np.pi

    return beta, tune, closedorbit
