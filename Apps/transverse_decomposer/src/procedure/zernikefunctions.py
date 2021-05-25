# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 09:26:48 2020

@author: fdz57121
"""


import numpy as numpy
import matplotlib.pyplot as plt

#This is easier to understand with the wiki page handy and looking at the definitions section: 
#https://en.wikipedia.org/wiki/Zernike_polynomials

def zernike_nm(n, m, N):
    """
     Creates the Zernike polynomial with radial index, n, and azimuthal index, m.

     Args:
        n (int): The radial order of the zernike mode
        m (int): The azimuthal order of the zernike mode
        N (int): The diameter of the zernike more in pixels
     Returns:
        ndarray: The Zernike mode
     """
     
    """This just applies the right cos/sin bit to the Rmn part"""

    coords = numpy.linspace(-1,1,N)
    X, Y = numpy.meshgrid(coords, coords)
    R = numpy.sqrt(X**2 + Y**2)
    theta = numpy.arctan2(Y, X)

    if m==0:
        Z = zernikeRadialFunc(n, 0, R)
    else:
        if m > 0: # j is even
            Z = zernikeRadialFunc(n, m, R) * numpy.cos(m*theta)
        else:   #i is odd
            m = abs(m)
            Z = zernikeRadialFunc(n, m, R) * numpy.sin(m * theta)

    # clip
    Z = Z*numpy.less_equal(R, 1.0)
    
    return Z



def circle(radius, size):
    """
Makes a circular mask in centre of with given radius.
Size is the size of the array the circle is made in.
    """
    # (2) Generate the output array:
    C = numpy.zeros((size, size))



    coords = numpy.arange(0.5, size, 1.0)


    # (3.c) Generate the 2-D coordinates of the pixel's centres:
    x, y = numpy.meshgrid(coords, coords)


    x -= size / 2.
    y -= size / 2.

    mask = x * x + y * y <= radius * radius
    C[mask] = 1

    # (5) Return:
    return C

def zernikeRadialFunc(n, m, r):
    """
    Fucntion to calculate the Zernike radial function

    Parameters:
        n (int): Zernike radial order
        m (int): Zernike azimuthal order
        r (ndarray): 2-d array of radii from the centre the array

    Returns:
        ndarray: The Zernike radial function
    """
    """this calculates the Rnm part using the sum function in the wiki definitions"""

    R = numpy.zeros(r.shape)
    for i in range(0, int((n - m) / 2) + 1):

        R += numpy.array(r**(n - 2 * i) * (((-1)**(i)) *
                         numpy.math.factorial(n - i)) /
                         (numpy.math.factorial(i) *
                          numpy.math.factorial(0.5 * (n + m) - i) *
                          numpy.math.factorial(0.5 * (n - m) - i)),
                         dtype='float')
        #print(n,m,i)
        #print('num', 0.5 * (n - m) - i)
    return R


def ref (j, N):
    
    """
    Find the [n,m] list giving the radial order n and azimuthal order
    of the Zernike polynomial of Noll index j.

    Parameters:
        j (int): The Noll index for Zernike polynomials

    Returns:
        list: n, m values
    """
    n = int((-1.+numpy.sqrt(8*(j-1)+1))/2.)
    p = (j-(n*(n+1))/2.)
    k = n%2
    m = int((p+k)/2.)*2 - k

    if m!=0:
        if j%2==0:
            s=1
        else:
            s=-1
        m *= s
    if m == 0:

        normalization2 = ((n+1)/numpy.pi)**0.5
    else:
        normalization2 = ((2)*(n+1)/numpy.pi)**0.5
     

    #print(N)
   
    
    z = zernike_nm(n,m,N)*normalization2

    return(z)


def fitting(imageuncut,centre,max_radius, numzernikemodes, powers = 'yes'):

    """"the zernike fitting is only applied to data within the circle specified using centre and radius
    so everything else is cut out"""
    
    #image = imageuncut[int(centre[0]-max_radius):int(centre[0]+max_radius+1),int(centre[1] -max_radius):int(centre[1]+max_radius+1)]
    image = imageuncut
    l = len(image)
    c = circle(max_radius,l)
    #image = image*c

    #plt.imshow(image)
    #plt.show()
    
    #just makes an empty list for the zernike amplitudes to populate
    a = numpy.zeros(numzernikemodes+1)
    

    circsymm = []
    noncirc = []
    
    #goes through each mode to find the contribution 
    #the noll index which i am using starts at 1 so hence i + 1 everywhere, yes probably could have written this better
    for i in range(numzernikemodes):
        
        #calculates n and m so the position of the circ symmetric ones can be found
        n = int((-1.+numpy.sqrt(8*(i+1-1)+1))/2.)#plus 1 because index needs to start at 1 not zero
        p = (i+1-(n*(n+1))/2.)
        k = n%2
        m = int((p+k)/2.)*2 - k
        #print(n,m)
        
        if m == 0:
            circsymm.append(i+1)#finds the position of all the circsymm fucntions in list of coeffs
        else:
            noncirc.append(i+1)
        
        #generates the zernike reference mode and finds the contributions from it in the image
        #They are orthogonal so you can find the contribution by an average
            
        refer = ref(i+1,l)
        c = sum(sum(refer*refer))
        a[i+1] = sum(sum(refer*image))/c
        
        if powers == 'yes':
            symm = numpy.sum(abs(a[circsymm[1::]])/sum(abs(a[2:])))
            asymm = numpy.sum(abs(a[noncirc])/sum(abs(a[2:])))

    if powers == 'yes':
        return(a, symm,asymm)
    else:
        return(a)

def reconstruction(a, N):
    recon = numpy.zeros([N,N])
    for i in range(len(a)):
        #skips zero because 0 doesnt exist in noll index
        if a[i] != 0:

            im = ref(i,N)
            recon += im*a[i]
            #generates the zernike polynomial multipies by the contributions and adds to the image
    return(recon)

"""Again just testing a random Vc image"""
"""
from scipy import ndimage
from skimage.io import imread
import numpy as np

image = imread('VIRTUAL_CATHODE_2019-11-26_16-48-15_5images_000.tiff')

#Just finding an approximate centre of the image to give to the functions

c = ndimage.measurements.center_of_mass(image>np.amax(image)*0.2)


#Powers = yes just makes it give you the symmetry and asymmetry powers
#this is easier to do within the function that with the list of amplitudes after that
#this is because the zernike modes are generated and labeled with two indexes n and m
#and when m = 0 its circularly symmetric so as it is going through the indexes you can get it
#to catch all the amplitudes with m = 0 with iswhat the if m = 0 bits are doing.

#100 is the radius of the beam, 250 is number of zernike modes

zernikemodes, asymmpower, symmpower = fitting(image,c, 100,250, powers = 'yes')

#N in the reconstruction function is just the size of the recreated image 
#line 214 and 215 is the plt.imshow of what its trying to reconstruct in the fitting function

reconfromzernikes = reconstruction(zernikemodes, 200)
plt.imshow(reconfromzernikes)
plt.show()

#Can see even with 200 zernikes doesnt reconstruct it super well.

#Often people plot the contributions from each as bar graph
plt.bar(np.arange(0, len(zernikemodes),1),zernikemodes)
plt.show()


r = reconstruction([0,1,0,0,1,00,0.5,0,0.5,0,0,0,0,0.2], 500)

from PIL import Image
r /= np.max(r) / 255
image = Image.fromarray(r)
image = image.convert('L')
image.save('test.bmp')"""