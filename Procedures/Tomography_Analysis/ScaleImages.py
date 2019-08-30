import scipy.io as sio
import numpy as np
import cv2
import math

# define some parameters
magnfcnx=10
magnfcny=10
psresn=201

# load beam images
beamimages = sio.loadmat('BeamImages.mat')
images=beamimages['imagearray']
images=images[0]

# load beta at observation point for each image
imagefileinformation=sio.loadmat('ImageFileInformation.mat')
betaobs=imagefileinformation['Beta_x_y_at_observation_point']
betaxobs=betaobs[:,0]
betayobs=betaobs[:,1]

# initalise image array
imagearray=np.empty((len(images),psresn,psresn))

# iterate through images
for image, i in zip(images, range(len(images))):

    # scale each image
    imresized=cv2.resize(image,None,fx =magnfcnx/np.sqrt(betaxobs[i]),fy = magnfcny/np.sqrt(betayobs[i]),interpolation = cv2.INTER_LINEAR)

    # initialise imscaled
    imscaled = np.zeros_like(image)

    # original and scaled image centres, correct to 1 pixel
    x1 = math.floor((np.shape(imresized)[0]+1)/2)
    y1 = math.floor((np.shape(imresized)[1]+1)/2)
    x2 = math.floor((np.shape(imscaled)[0]+1)/2)
    y2 = math.floor((np.shape(imscaled)[1]+1)/2)

    # get smallest of each dimension
    smallestx = min(x1,x2)-1
    smallesty = min(y1,y2)-1

    # define an image frame, defined by the smaller of each dimension of resized and scaled image
    imscaled[(x2-smallestx):(x2+smallestx),(y2-smallesty):(y2+smallesty)] = imresized[(x1-smallestx):(x1+smallestx),(y1-smallesty):(y1+smallesty)]

    # resize again to fit pixel resolution
    imrescaled=cv2.resize(imscaled,(psresn,psresn),interpolation = cv2.INTER_LINEAR)

    # normalise by total intensity
    imnormed=imrescaled/np.sum(imrescaled)

    # store in image array
    imagearray[i]=imnormed