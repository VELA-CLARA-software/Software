import numpy as np
import math
import scipy.io as sio


def tmdrift(dlength):

    m = np.array([[1,dlength,0,0],[0,1,0,0],[0,0,1,dlength],[0,0,0,1]])

    return m


def tmquad(qstrength,qlength):

    if qstrength>0:
        omega = math.sqrt(qstrength)
        oml=omega*qlength
        m = np.array([[math.cos(oml),math.sin(oml)/omega,0,0],[-math.sin(oml)*omega,math.cos(oml),0,0],
             [0,0,math.cosh(oml),math.sinh(oml)/omega],[0,0,math.sinh(oml)*omega,math.cosh(oml)]])

    elif qstrength<0:
        omega=math.sqrt(-qstrength)
        oml = omega*qlength
        m = np.array([[math.cosh(oml), math.sinh(oml)/omega, 0, 0], [math.sinh(oml)*omega, math.cosh(oml), 0, 0],
             [0, 0, math.cos(oml), math.sin(oml)/omega], [0, 0, -math.sin(oml)*omega, math.cos(oml)]])

    else:
        m = tmdrift(qlength)

    return m


def tmquadscan(qstrengths):

    qfringe = 0.0250
    qlength = 0.1007 + qfringe

    dlen1 = 0.165967 - qfringe/2
    dlen2 = 0.299300 - qfringe
    dlen3 = 0.712450 - qfringe
    dlen4 = 0.181183 - qfringe/2

    mq3 = tmquad(qstrengths[:,2], qlength)
    mq4 = tmquad(qstrengths[:,3], qlength)
    mq5 = tmquad(qstrengths[:,4], qlength)

    md1 = tmdrift(dlen1)
    md2 = tmdrift(dlen2)
    md3 = tmdrift(dlen3)
    md4 = tmdrift(dlen4)


    m = md4 @ mq5 @ md3 @ mq4 @ md2 @ mq3 @ md1

    return m

def currenttokCLARA(quadcurrents,p0_MeVc=30):
    c = 2.99792458e8

    lengths = np.array([128.68478212775, 126.817287248819,127.241994829126, 127.421664936758, 127.162566301558])/1000
    field_integral_coeffs_PosI =np.array([[-2.23133410405682E-10, 4.5196171252132E-08, -3.46208258004659E-06,1.11195870210961E-04,
                                  2.38129337415767E-02, 9.81229429460256E-03],
                                 [- 4.69068497199892E-10, 7.81236692669882E-08, -4.99557108021749E-06,
                                  1.39687166906618E-04,2.32819099224878E-02,9.77695097574923E-03],
                                 [- 4.01132756980213E-10, 7.04774652367448E-08, -4.7303680012511E-06,
                                  1.37571730391246E-04, 2.33327839789932E-02, 9.49568371388574E-03],
                                 [- 3.12868198002574E-10, 5.87771428279647E-08, -4.18748562338666E-06,
                                  1.27524427731924E-04, 2.34218216296292E-02, 9.38588316008555E-03],
                                 [- 3.12232013228657E-10, 5.86576256524889E-08, -4.17897080912429E-06,
                                  1.27265120139323E-04, 2.33741958038237E-02, 9.36679794786415E-03]])

    offsets = np.array(field_integral_coeffs_PosI[:,[-1]])

    field_integral_coeffs_noOffset = field_integral_coeffs_PosI
    field_integral_coeffs_noOffset[:,-1]= 0
    Ineg=np.clip(quadcurrents,a_min=None,a_max=0)
    Ipos=np.clip(quadcurrents,a_min=0,a_max=None)


    fieldvals = offsets.T

    for n in range(5):

        p0overc = p0_MeVc * 1e6 * lengths[n] / c
        fieldvals[:, n] = (fieldvals[:, n] + np.polyval(-field_integral_coeffs_noOffset[n], abs(Ineg[n])) + np.polyval(field_integral_coeffs_noOffset[n], Ipos[n])) / p0overc
    return fieldvals

def calculateoptics(betax,alphax,betay,alphay,quadcurrents,beammomentum):

    alphax=alphax.item()
    betax = betax.item()
    alphay = alphay.item()
    betay = betay.item()

    gammax = (1+alphax**2)/betax
    gammay = (1+alphay**2)/betay

    csScrn2 = np.array([[betax, -alphax, 0, 0],
               [-alphax, gammax, 0, 0],
               [0, 0, betay, -alphay],
               [0, 0, -alphay, gammay]])

    nrmScrn2 = np.array([[1/math.sqrt(betax), 0, 0, 0],
                [alphax/math.sqrt(betax), math.sqrt(betax), 0, 0],
                [0, 0, 1/math.sqrt(betay), 0],
                [0, 0, alphay/math.sqrt(betay), math.sqrt(betay)]])

    optics = np.zeros((len(quadcurrents),14))

    for n in range(len(quadcurrents)):

        # need to also rewrite I2K_CLARA
        quadstrengths = currenttokCLARA(quadcurrents[n], beammomentum)

        # and TransferMatrixQuadScan
        m = tmquadscan(quadstrengths)

        cs3 = m@csScrn2@(m.T)
        # works up to here
        nrmScrn3 = np.array([[1 / math.sqrt(cs3[0,0]), 0, 0, 0],
                    [- cs3[0,1] / math.sqrt(cs3[0,0]), math.sqrt(cs3[0,0]), 0, 0],
                    [0, 0, 1 / math.sqrt(cs3[2,2]), 0],
                    [0, 0, -cs3[2,3] / math.sqrt(cs3[2,2]), math.sqrt(cs3[2,2])]])

        r = np.linalg.solve(nrmScrn2.T,(nrmScrn3@m).T).T

        mux = np.arctan2(r[0,1],r[0,0])

        if mux < 0:
            mux = mux + 2 * math.pi

        muy = np.arctan2(r[2,3], r[2,2])

        if muy < 0:
            muy = muy + 2 * math.pi

        optics[n] = [cs3[0,0], -cs3[0,1], cs3[2,2], -cs3[2,3], mux, muy, m[0,0], m[0,1], m[1,0], m[1,1],
                     m[2,2], m[2,3], m[3,2], m[3,3]]
    return optics


opticsdata = sio.loadmat('opticstestdata.mat')
betax=np.array(opticsdata['betax'])
alphax=np.array(opticsdata['alphax'])
betay=np.array(opticsdata['betay'])
alphay=np.array(opticsdata['alphay'])
quadcurrents=np.array(opticsdata['QuadCurrents'])
beammomentum=np.array(opticsdata['BeamMomentum'])

betaxobs=opticsdata['Beta_x_y_at_observation_point'][:,0]
betayobs=opticsdata['Beta_x_y_at_observation_point'][:,1]
alphaxobs=opticsdata['Alpha_x_y_at_observation_point'][:,0]

alphayobs=opticsdata['Alpha_x_y_at_observation_point'][:,1]
phaseadvancex=opticsdata['PhaseAdvance_x_y'][:,0]
phaseadvancey=opticsdata['PhaseAdvance_x_y'][:,1]
results=calculateoptics(betax,alphax,betay,alphay,quadcurrents,beammomentum)
if np.allclose(betaxobs,results[:,0]) and np.allclose(alphaxobs,results[:,1]) and np.allclose(betayobs,results[:,2]) and np.allclose(alphayobs,results[:,3]) and np.allclose(phaseadvancex,results[:,4]) and np.allclose(phaseadvancey,results[:,5]):
    print('CalculateOptics is correct!')