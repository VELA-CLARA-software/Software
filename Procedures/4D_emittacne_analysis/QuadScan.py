#!/usr/bin/python
# -*- coding: utf-8 -*-
#import time
import numpy
import matplotlib.pyplot as plt
#import h5py

import matplotlib.pyplot as plt


#Load directory (Given as "Data 2019-03-04/ImageFileInformation.mat") ##Line not needed as python uses directory code is located in

def FileOpen(filename):         ##Subroutine used to read data from a text file into an array
    if filename[-4:] != ".txt":     
        filename = filename + ".txt"
    
    data = numpy.array([])

    nlines = 0
    
    file = open(filename, "r")  #opens on 'read' mode
    
    for line in file:
        nlines += 1
        data = numpy.append(data,numpy.fromstring(line,dtype=numpy.float,sep=','))
            
    file.close
    
    data = numpy.reshape(data, (nlines, int(data.size/nlines) ))

    return data


def I2K_CLARA_simple(currents, beamMomentum):
    '''
    :param currents:
    :param beamMomentum:
    :return: k_values for each quadrupole
    '''
    # quad calibrations are in the magnet controller
    pfitq = numpy.array(FileOpen('QuadCalibration.txt'))

    # currents are from the experiment
    currents = numpy.array(currents)
    kvals = numpy.zeros(5)
    for n in range(5):
        kvals[n] = 0
        for p in range(4):
            kvals[n] = kvals[n] + pfitq[p][n]*currents[n]**(3-p)
    # k value with momentum - what is this factor of 30???
    kvals = kvals*30/beamMomentum
    return kvals


def TransferMatrixDrift(length):    ##Subroutine TransferMatrixDrift defined
    # should be in SAMPL
    m = numpy.array([[1, length, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 1, length],
         [0, 0, 0, 1]])
    return m


def TransferMatrixQuad(k1,length):      ##Subroutine TransferMatrixQuad defined
    # should be in SAMPL
    m = TransferMatrixDrift(length)
    
    if k1 > 0:
        omega = numpy.sqrt(k1)
        wl = omega*length

        m = numpy.array([[numpy.cos(wl), numpy.sin(wl)/omega, 0, 0],
             [-numpy.sin(wl)*omega, numpy.cos(wl), 0, 0],
             [0, 0, numpy.cosh(wl), numpy.sinh(wl)/omega],
             [0, 0, numpy.sinh(wl) * omega, numpy.cosh(wl)]])

    if k1 < 0:
        omega = numpy.sqrt(-k1)
        wl = omega*length
        
        m = numpy.array([[numpy.cosh(wl),numpy.sinh(wl)/omega, 0, 0],
             [numpy.sinh(wl)*omega, numpy.cosh(wl), 0, 0],
             [0, 0, numpy.cos(wl), numpy.sin(wl)/omega],
             [0, 0, -numpy.sin(wl)*omega, numpy.cos(wl)]])

    return m
        

def TransferMatrixQuadScan(qstrengths):     ##Subroutine TransferMatrixQuadScan defined
    '''
    returns the transfer matrix for the given quad strengths
    :param qstrengths:
    :return:
    '''
    # should be in SAMPL
    # ret
    qfringe = 0.0250
    qlength = 0.1007 + qfringe

    dlen1 = 0.165967 - qfringe/2
    dlen2 = 0.299300 - qfringe
    dlen3 = 0.712450 - qfringe
    dlen4 = 0.181183 - qfringe/2
    #print("qstrengths = ", qstrengths)
    mq3 = TransferMatrixQuad(qstrengths[2],qlength)
    mq4 = TransferMatrixQuad(qstrengths[3],qlength)
    mq5 = TransferMatrixQuad(qstrengths[4],qlength)

    md1 = TransferMatrixDrift(dlen1)
    md2 = TransferMatrixDrift(dlen2)
    md3 = TransferMatrixDrift(dlen3)
    md4 = TransferMatrixDrift(dlen4)

    m = numpy.array(((((((md4.dot(mq5)).dot(md3)).dot(mq4)).dot(md2)).dot(mq3)).dot(md1)))  ##Performs matrix multiplication on all 'md4','mq5','md3','mq4','md2','mq3','md1'

    return m


def CalculateOptics(betax, alphax, betay, alphay, QuadCurrents, BeamMomentum):      ##Subroutine CalculateOptics defined (same function as in matlab)
    #print("betax = ", betax)                   ##All prints below are used to check values
    #print("alphax = ", alphax)
    #print("betay = ", betay)
    #print("alphay = ", alphay)
    #print("QuadCurrents = ", QuadCurrents)
    #print("BeamMomentum = ", BeamMomentum)
    '''

    :param betax:
    :param alphax:
    :param betay:
    :param alphay:
    :param QuadCurrents:
    :param BeamMomentum:
    :return:
    '''

    gammax = (1 + alphax**2) / betax
    gammay = (1 + alphay**2) / betay

    csScrn2 = [[betax, -alphax, 0, 0],
               [-alphax, gammax, 0, 0],
               [0, 0, betay, -alphay],
               [0, 0, -alphay, gammay]]
    #print("csScrn2 = ", csScrn2)       ##Checking statement

    sqrtbx = numpy.sqrt(betax)
    sqrtby = numpy.sqrt(betay)

    nrmScrn2 = numpy.array([[1/sqrtbx, 0, 0, 0],
                 [alphax/sqrtbx, sqrtbx, 0, 0],
                 [0, 0, 1/sqrtby, 0],
                 [0, 0, alphay/sqrtby, sqrtby]])
    #print("nrmScrn2 = ", nrmScrn2)         ##Checking statement

    optics = numpy.zeros((len(QuadCurrents),14))
    #print("Optics = ", optics)         ##Checking statement

    for n in range(1,len(QuadCurrents)+1):
        quadStrengths = I2K_CLARA_simple(QuadCurrents[n-1],BeamMomentum)  #Calls I2K_CLARA_simple subroutine and assigns returned value to variable 'quadStrengths'
        #print("quadStrengths = ", quadStrengths)       ##Checking statement
        m = numpy.array(TransferMatrixQuadScan(quadStrengths))
        #print("m = ", m)       ##Checking statement

        cs3 = (m.dot(csScrn2)).dot(m.transpose())
        #print("cs3 = ", cs3)       ##Checking statement

        sqrtbx = numpy.sqrt(cs3[0][0])
        sqrtby = numpy.sqrt(cs3[2][2])
        
        nrmScrn3 = numpy.array([[1/sqrtbx, 0, 0, 0],
                    [-cs3[0][1]/sqrtbx, sqrtbx, 0, 0],
                    [0, 0, 1/sqrtby, 0],
                    [0, 0, -cs3[2][3]/sqrtby, sqrtby]])
        #print("nrmScrn3 = ", nrmScrn3)         ##Checking statement


        r = (nrmScrn3.dot(m)).dot(numpy.linalg.inv(nrmScrn2))
        #print("r = ", r)       ##Checking statement

        
        optics[n-1]= [cs3[0][0], -cs3[0][1], cs3[2][2], -cs3[2][3],
                    numpy.arctan2(r[0][1],r[0][0]), numpy.arctan2(r[2][3],r[2][2]),
                    m[0][0], m[0][1], m[1][0], m[1][1],
                    m[2][2], m[2][3], m[3][2], m[3][3]]

    return optics


#Beginning of idxx & indxy "setdiff" segment
indxx = []
indxy = []
indxxCmpTo = [3, 4, 5, 26, 31]
indxyCmpTo = [33]

for i in range(1, 39):
    if i not in indxxCmpTo:
        indxx.append(i-1)
    if i not in indxyCmpTo:
        indxy.append(i-1)

# print("indxx = ", indxx)
# print("indxy = ", indxy)
#End of idxx & indxy "setdiff" segment

BeamMomentum = 29.5 #30.0 MeV nominal
BeamGamma = BeamMomentum / 0.511

betax = 6.2734
alphax = -1.3246
betay = 1.4150
alphay = -1.8897

#def GetH5Image(fname, fnameb, rangeX, calibration):    ##Defines function used to read and process hdf5 files (at the moment is in development in separate code: 'hdf5 test.py'
#    info = h5py.File(fname, 'r')
#
#    infob = h5py.File(fnameb, 'r')

QuadCurrents = FileOpen("QuadCurrents")     ##opens specialised QuadCurrents text file (exported from matlab) by calling FileOpen subroutine, stores data in variable 'QuadCurrents'
imagesigma = FileOpen("imagesigma")         ##opens specialised imagesigma text file (exported from matlab) by calling FileOpen subroutine, stores data in variable 'imagesigma'
#sigmaerror = FileOpen("sigmaerror")         ##opens specialised sigmaerror text file (exported from matlab) by calling FileOpen subroutine, stores data in variable 'sigmaerror'

optics = CalculateOptics(betax, alphax, betay, alphay, QuadCurrents, BeamMomentum) ##assigns optics matrix/array to returned value of subroutine 'calculateOptics'

#psresn = 201 #Resolution (px) of phase space reconstruction
#imgrange = 1200 #Range for cropping raw camera image around beam image
calibration = 0.0181 #Screen 3 calibration factor in millimeters/pixel
#magnfcn = [10,15]

#print('Loading the images... ')
#time.sleep(0.01)

##Below are lines from matlab which are unnecessary in python
#nmax = len(Image_and_background_filenames_at_observation_point) #Variable Image_and... given in directory
#imagearray = cell(1,nmax)
#tic #Begins stopwatch
#load('BeamImages.mat')

#print("Optics = ", optics)         ##Checking statement
#print("len(indxx) = ", len(indxx))         ##Checking statement

####x
dxmatrx = numpy.zeros((len(indxx),3))
for i in range(len(indxx)):
    dxmatrx[i][0] = optics[indxx[i]][6]**2
    dxmatrx[i][1] = 2 * optics[indxx[i]][6] * optics[indxx[i]][7]
    dxmatrx[i][2] = optics[indxx[i]][7]**2

dxinv = numpy.linalg.pinv(dxmatrx)

psx2 = numpy.zeros(3)
for i in range(len(indxx)):
    psx2[0] = psx2[0] + dxinv[0][i] * imagesigma[indxx[i]][0]**2 * calibration**2
    psx2[1] = psx2[1] + dxinv[1][i] * imagesigma[indxx[i]][0]**2 * calibration**2
    psx2[2] = psx2[2] + dxinv[2][i] * imagesigma[indxx[i]][0]**2 * calibration**2
    
psx2m = [[psx2[0], -psx2[1]],
         [-psx2[1], psx2[2]]]

epsx = numpy.sqrt(numpy.linalg.det(psx2m))     ##determinant
betx = psx2[0] / epsx
alfx =-psx2[1] / epsx

#print('epsx = ', epsx)

gepsx = BeamGamma * epsx
####end of x

####y
dymatrx = numpy.zeros((len(indxy),3))
for i in range(len(indxy)):
    dymatrx[i][0] = optics[indxy[i]][10]**2
    dymatrx[i][1] = 2 * optics[indxy[i]][10] * optics[indxy[i]][11]
    dymatrx[i][2] = optics[indxy[i]][11]**2

dyinv = numpy.linalg.pinv(dymatrx)

psy2 = numpy.zeros(3)
for i in range(len(indxy)):
    psy2[0] = psy2[0] + dyinv[0][i] * imagesigma[indxy[i]][1]**2 * calibration**2
    psy2[1] = psy2[1] + dyinv[1][i] * imagesigma[indxy[i]][1]**2 * calibration**2
    psy2[2] = psy2[2] + dyinv[2][i] * imagesigma[indxy[i]][1]**2 * calibration**2
    
psy2m = [[psy2[0], -psy2[1]],
         [-psy2[1], psy2[2]]]

epsy = numpy.sqrt(numpy.linalg.det(psy2m))
bety = psy2[0] / epsy
alfy =-psy2[1] / epsy

gepsy = BeamGamma * epsy
####end of y

#sigreconx = numpy.sqrt(dxmatrx.dot(psx2))
#sigrecony = numpy.sqrt(dymatrx.dot(psy2))

#imgfilename = dirname + '/' + Image_and_background_filenames_at_reconstruction_point[0][0] #Processing text file needed here
#bgdfilename = dirname + '/' + Image_and_background_filenames_at_reconstruction_point[0][1] #Processing text file needed here

#calibnrp = 0.0122 #Calibration in millimetres/pixel of screen at reconstruction point

####This section not needed for the specific graphs outputted
##imagerp, sigxrp, sigyrp = GetH5Image(imgfilename, bgdfilename, 600, calibnrp)
##sigxrp = sigxrp * calibnrp
##sigyrp = sigyrp * calibnrp
##
##sigxrecon = (epsx*betx)**(1/2)
##sigyrecon = (epsy*bety)**(1/2)
##
##print('Horizontal beam size at reconstruction point: \n')
##print('  Observed = ' + sigxrp + 'mm')
##print('  Fitted = ' + sigxrecon + 'mm')
##print('  Error = ' + 100 * ((sigxrecon-sigxrp)/sigxrp) + '%')
##
##print('Vertical beam size at reconstruction point: \n')
##print('  Observed = ' + sigyrp + 'mm')
##print('  Fitted = ' + sigyrecon + 'mm')
##print('  Error = ' + 100 * ((sigyrecon-sigyrp)/sigyrp) + '%')

#print("Calibration = ", calibration)    ##Checking statement
#print("imagesigma = ", imagesigma)  ##Checking statement
#print("normx = ", normx)        ##Checking statement


#for i in range(0,len(indxx)):
    #print("indxx[i] = ", indxx[i])
    #print("calibration*imagesigma[indxx[i]][0]/normx[i] = ", calibration*imagesigma[indxx[i]][0]/normx[0][i])


plt.figure(2)
plt.subplot(2,1,1)
#plt.title(r'$\gamma \epsilon_x=${0:5.3f}um, $\beta_x=${1:5.3f}m, $\alpha_x=${2:5.3f}'.format(gepsx,betx,alfx))
plt.title('title 1')
plt.xlabel('Scan Point Index')
#plt.ylabel(r'$\sigma_x / √\beta_x$ (mm/√m)')
plt.ylabel('y label')
plt.ylim(0, 0.8)


XplotYs = numpy.zeros(len(indxx))    ##Array holding y values for graph of x
for i in range(len(indxx)):
    XplotYs[i] = calibration*imagesigma[indxx[i]][0]/numpy.sqrt(optics[indxx[i]][0])

plt.plot(indxx, XplotYs, '--ko', fillstyle='none')
plt.plot([0,38], numpy.sqrt([epsx, epsx]), '-b')

plt.subplot(2,1,2)
#plt.title(r'$\gamma \epsilon_y=${0:5.3f}um, $\beta_y=${1:5.3f}m, $\alpha_y=${2:5.3f}'.format(gepsy,bety,alfy))
plt.title('tiotel 2 ')
plt.xlabel('Scan Point Index')
#plt.ylabel(r'$\sigma_y / √\beta_y$ (mm/√m)')
plt.ylabel('ylabel')
plt.ylim(0, 0.41)

YplotYs = numpy.zeros(len(indxy))    ##Array holding y values for graph of y
for i in range(len(indxy)):
    YplotYs[i] = calibration*imagesigma[indxy[i]][1]/numpy.sqrt(optics[indxy[i]][2])

plt.plot(indxy, YplotYs, '--ko', fillstyle='none')
plt.plot([0,38], numpy.sqrt([epsy, epsy]), '-b')
plt.subplots_adjust(hspace=0.7)

print'asdasdfdsd'


plt.show()      ##Shows the figures












      
