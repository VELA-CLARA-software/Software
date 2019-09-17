import scipy.io as sio
import numpy as np
import cv2
import math
import matplotlib.pyplot as plt

# define some parameters
magnfcnx=10
magnfcny=10
psresn=201

# load beam images
beamimages = sio.loadmat('BeamImages.mat')
images=beamimages['imagearray']
images=images[0]

# load beta at observation point for each image
beta=sio.loadmat('BetaObs.mat')
betaobs=beta['Beta_x_y_at_observation_point']
betaxobs=betaobs[:,0]
betayobs=betaobs[:,1]

# initalise image array

imagearray=np.empty((len(images),psresn,psresn))

plt.figure()
r = 0.5
nmax=len(images)
num_rows = math.floor(r*math.sqrt(nmax/r))
num_cols = math.ceil(nmax/num_rows)
# iterate through images
for image, i in zip(images, range(len(images))):
    image=np.rot90(image)
    # scale each image
    imresized=cv2.resize(image,None,fx =magnfcnx/math.sqrt((betaxobs[i])),fy = magnfcny/(math.sqrt(betayobs[i])),interpolation = cv2.INTER_CUBIC)

    # initialise imscaled
    imscaled = np.zeros_like(image)


    def imagecentre(image):
        centre = (np.floor(np.asarray(np.shape(image)) + 1) / 2).astype(int)
        return centre[0],centre[1]

    # original and scaled image centres, correct to 1 pixel
    x1, y1 = imagecentre(imresized)
    x2, y2 = imagecentre(imscaled)

    # get smallest of each dimension
    smallestx = min(x1,x2)-1
    smallesty = min(y1,y2)-1

    # define an image frame, defined by the smaller of each dimension of resized and scaled image
    imscaled[(x2-smallestx):(x2+smallestx),(y2-smallesty):(y2+smallesty)] = imresized[(x1-smallestx):(x1+smallestx),(y1-smallesty):(y1+smallesty)]

    # resize again to fit pixel resolution
    imrescaled=cv2.resize(imscaled,(psresn,psresn),interpolation = cv2.INTER_CUBIC)

    # normalise by total intensity
    imnormed=imrescaled/np.sum(imrescaled)

    # store in image array
    imagearray[i]=imnormed

    plt.subplot(num_rows, num_cols,i+1)
    plt.imshow(imnormed)
plt.show()

