# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 15:13:20 2020

@author: fdz57121
"""


from skimage.metrics import structural_similarity as ssim
import numpy as np
#from opticspy import zernike

from PIL import Image



"""This function isnt actually used anywhere but is useful"""
def centroid(data):

    peak = np.amax(data)
    mask = data>0.1*peak

    h,w = np.shape(data)   
    x = np.arange(0,w)
    y = np.arange(0,h)

    X,Y = np.meshgrid(x,y)


    cx = np.sum(X*mask)/np.sum(mask)
    cy = np.sum(Y*mask)/np.sum(mask)
    
    

    return cx,cy


#FERMI Penco (2013), angular rms and radial rms
#Angular rms had more of a correlation with beam quality than radial in paper
#Measures how uniform the intensity in sections are: radial looks at ring section, angular looks at pie sections
#The ring sections are the same width. The number of sections in both can be changed within the rms functions by changing numsteps at the start of the last function.


"""These first two functions are just defining the sections each rms function cuts out of the image """
def sector_mask(shape,centre,radius,angle_range):#Shape is dimensions of two image array,..., angle_range i guess is defined by how many segments you choose and this number is calculated elsewhere in the program
    x,y = np.ogrid[:shape[0],:shape[1]]
    #radius is of the whole thing
    cx,cy = centre
    tmin,tmax = np.deg2rad(angle_range)#[minangle, maxangle]
# ensure stop angle > start angle
    if tmax < tmin:
        tmax += 2*np.pi
# convert cartesian --> polar coordinates
    circmask = np.ones(shape)
    C = (x-cx) * (x-cx) + (y-cy) * (y-cy) >= ((radius) * (radius))
    circmask[C] = 0
    #print(circmask[0])
    theta = np.arctan2(x-cx,y-cy) - tmin
    #print(theta)
# wrap angles between 0 and 2*pi
    theta %= (2*np.pi)
    #print(theta)

# angular mask
    anglemask = theta < (tmax-tmin)
    return circmask*anglemask

def segment_mask(shape,centre,r1,r2):
	x,y = np.ogrid[:shape[0],:shape[1]]
	cx,cy = centre
	return (np.sqrt((x - cx)**2 + (y - cy)**2) > r1) * (np.sqrt((x - cx)**2 + (y - cy)**2) <= r2)

"""Next two functions find radial and angular rms"""
def radialRMS(imageA,centre,max_radius, num_steps):

    
    cx = centre[0]
    cy = centre[1]

        
    radialaver = []
    
    radii = np.arange(1,num_steps)*(max_radius/num_steps)
    last=0
    
    for i in radii:
        thisSegment = np.nonzero(segment_mask(imageA.shape, (cx,cy), last,i))
        newim = segment_mask(imageA.shape, (cx,cy), last,i)*imageA
        #plt.imshow(newim)
        #plt.show()
    
        #print(np.amax(imageA[thisSegment]))
        #print(np.amin(imageA[thisSegment]))
        radialaver.append(imageA[thisSegment].mean())
    

        #print last, i 
        last=i
    newim = segment_mask(imageA.shape, (cy,cx), 0,last)*imageA
    #plt.imshow(newim[800:1300,900:1400])
    #plt.show()

    radialrmsaver=np.std(radialaver)/np.mean(radialaver)
    #print(radialaver)
    
    return(radialrmsaver)

def angularRMS(imageA,centre,max_radius, num_steps):
    

    angularaver=[]
    last = 0
    a = 0
    for i in np.linspace(360/num_steps,360,num_steps):

        #i steps through the the angles
        thisSector = np.nonzero(sector_mask(np.int64(imageA.shape), (centre[0],centre[1]), max_radius, (i,i+360/num_steps)) )
        #Gives the coordinates of the sector
        
        newimsec = sector_mask(np.int64(imageA.shape), (centre[0],centre[1]), max_radius, (i,i+360/num_steps)) *imageA
        #print(newimsec[0])
        #plt.imshow(imageA - newimsec)
        #plt.colorbar()
        #plt.show()

        angularaver.append(imageA[thisSector].mean())
        #Cuts out positions that are within sector, sums and appends
        a += sector_mask(np.int64(imageA.shape), (centre[1],centre[0]), max_radius, (i,i+360/num_steps))
        #plt.plot(imageA[thisSector])
        #print(np.amin(imageA[thisSector]))
        last = i
        #plt.show()
    angularrmsaver=np.std(angularaver)/np.mean(angularaver)
    #print(angularaver)
    return(angularrmsaver)

#We can actually combine the angular rms and radial functions and gives a quality factor that tells us how uniform the beam is
    
""" Function below generates the angualr and radial rms. Also calculates quality factor from the previous two"""

def rmsqualityfactor(image, centre, max_radius):
    numsteps = 20
    
    angularrms = angularRMS(image, centre, max_radius, numsteps)
    
    radialrms = radialRMS(image, centre, max_radius, numsteps)
    
    qualityfactor = (((1 - angularrms)**2 + (1- radialrms)**2)/2)**0.5
    return(angularrms, radialrms, qualityfactor)

def circle(radius, size):
    """
Makes a circular mask in centre of with given radius.
Size is the size of the array the circle is made in.
    """
    # (2) Generate the output array:
    C = np.zeros((size, size))

    radius = radius

    coords = np.arange(0.5, size, 1.0)


    # (3.c) Generate the 2-D coordinates of the pixel's centres:
    x, y = np.meshgrid(coords, coords)


    x -= size / 2.
    y -= size / 2.

    mask = x * x + y * y <= radius * radius
    C[mask] = 1

    # (5) Return:
    return C

"""Twod gauss generating function for making profiles to compare to image"""
def twodgauss(dimensions, max_radius,centre):
    cx,cy  = centre
    spacing = 2/(2*max_radius)
    x,y = np.meshgrid(np.linspace(-spacing*(cy), spacing*(dimensions[1]-cy-1), dimensions[1]), np.linspace(-spacing*(cx), spacing*(dimensions[0]-cx-1), dimensions[0]))
    
    circmask = circle(max_radius, dimensions[0])
    """circmask = np.zeros(dimensions)
    
    #
    C = (x) * (x) + (y) * (y) <= 1 #this is centred on zero zero so should make circle in right place and shape because the zeros in xy and in the right place
    
    circmask[C] = 1#just to cut the gaussian to the right size at the end"""
    sx = 1/(np.sqrt(2*np.log(2)))
    sy = sx
     
        
    g =  np.exp(-((x)**2. / (2. * sx**2.) + (y)**2. / (2. * sy**2.)))
    
    data = g*255/np.amax(g)
    #print(np.amax(data))
    if np.amax(data)>255:
        print('Error!!!')
    if np.amin(data)<0:
        print('error')
    #need to convert into form of images and back again as this conversion blurs things a bit
    image = Image.fromarray(data)
    image = image.convert('L')
    im_array = np.asarray(image)
    area = sum(sum(circmask))
    gauss = im_array*circmask


    return (gauss, circmask)

"""Function combining the two similarity methods mean squared error and structural similarity"""
def msessim(imageA, centre, max_radius):

	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
    dimensions = np.shape(imageA)
    cx,cy  = centre
    spacing = 2/(2*max_radius)
    x,y = np.meshgrid(np.linspace(-spacing*(cy), spacing*(dimensions[1]-cy-1), dimensions[1]), np.linspace(-spacing*(cx), spacing*(dimensions[0]-cx-1), dimensions[0]))
    circmask = np.zeros(dimensions)

    
    #Tries to make total pixel value in area od interst equal
    norm = np.sum(imageA*circmask)
    gauss, circmask = twodgauss(dimensions, max_radius,[cx,cy])
    
    #Tries to make total pixel value in area od interst equal
    normgauss = gauss*(np.sum(imageA*circmask)/np.sum(gauss))
    
    #plt.imshow(imageA)
    #plt.colorbar()
    #plt.show()
    
                
    #plt.imshow(truncgauss)
    #plt.colorbar()
    #plt.show()
    #plt.imshow(imageA)
    #plt.colorbar()
    #plt.show()
    #plt.imshow(truncgauss)
    #plt.colorbar()
    #plt.show()
    
    #Need to crop images otherwise the similarlity will be really close because itll mostly be comparing the background
    
    imagecropped = imageA[int(np.floor(cx-max_radius)):int(np.ceil(cx+max_radius)),int(np.floor(cy-max_radius)):int(np.ceil(cy+max_radius))]
    normgausscropped= normgauss[int(np.floor(cx-max_radius)):int(np.ceil(cx+max_radius)),int(np.floor(cy-max_radius)):int(np.ceil(cy+max_radius))]
    
    #Calculates mean squared error between two images
    errtrun = np.sum((imagecropped.astype("float") - normgausscropped.astype("float"))** 2)

    
    errtrun /= float(dimensions[0]*dimensions[1])
	
	# the lower the error, the more "similar"
    
    uni = circmask.astype(float)*(np.sum(imageA*circmask)/np.sum(circmask.astype(float)))
    
    unicropped= uni[int(np.floor(cx-max_radius)):int(np.ceil(cx+max_radius)),int(np.floor(cy-max_radius)):int(np.ceil(cy+max_radius))]
    
    erruni = np.sum((imagecropped.astype("float") - unicropped.astype("float")) ** 2)
    #plt.imshow(imageA-uniform)
    #plt.title('Difference')
    #plt.colorbar()
    #plt.show()
    erruni /= float(dimensions[0]*dimensions[1])
    
 
    ssimuni = ssim(imagecropped, unicropped)#data range is that for profile 9
    ssimtrun = ssim(imagecropped, normgausscropped)#data range is that for profile 9

    #There are more things you can change in the ssimfunction
    #To match the implementation of Wang et. al. [1], set gaussian_weights to True, sigma to 1.5, and use_sample_covariance to False.
    return(erruni,errtrun, ssimuni,ssimtrun)

