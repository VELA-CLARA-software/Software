#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
//              This file is part of VELA-CLARA-Software.                             //
//------------------------------------------------------------------------------------//
//    VELA-CLARA-Software is free software: you can redistribute it and/or modify     //
//    it under the terms of the GNU General Public License as published by            //
//    the Free Software Foundation, either version 3 of the License, or               //
//    (at your option) any later version.                                             //
//    VELA-CLARA-Controllers is distributed in the hope that it will be useful,       //
//    but WITHOUT ANY WARRANTY; without even the implied warranty of                  //
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                   //
//    GNU General Public License for more details.                                    //
//                                                                                    //
//    You should have received a copy of the GNU General Public License               //
//    along with VELA-CLARA-Software.  If not, see <http://www.gnu.org/licenses/>.    //
//
//  Author:      DJS
//  Last edit:   19-07-2019
//  FileName:    online_analysis.py
//  Description: walk through of the online analaysis procedure
                 History (notes in .\docs:
                 2014/2105 Duncan Scott developed main procedure  2 notes:
                    Calculating Beam Sizes From Screen Images on VELA
                    Covariance Matrices of VELA Beam Distributions
                 2015/2016 Duncan Scott & Matt Toplis develop procedures, consider errors,
                 1 note and Mathematica notebook
                    Method of Estimating Beam Size from VELA Screen Images.doc
                    Method of Estimating Beam Size from VELA Screen Images.nb
                 2016-2018 Tim Price writes c++ version of procedure, plus works with James
                 Wilson on providing 'online analysis through control system.' For c++ see fitter
                 class in TP CamerIA module in github
"""
from __future__ import division # force python division t use floats !!!
import h5py
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.patches import Rectangle


#

image_path = os.path.join(os.getcwd(),"images")
beam_image_1 ="beam.hdf5"
back_image_1 ="back.hdf5"


def get_first_hdf5_image(path, filename):
    """
    gets the FIRST image from the passed file, we have to hardocde in the 'Capture000001'
    :param full_path: a path to the image file
    :return: a numpy array of the image
    """
    full_path = os.path.join(path,filename)
    print("Importing frist image in ",full_path)
    f = h5py.File(full_path, 'r')
    # Get the data ! hardcoded this key
    image = list(f['Capture000001'])
    f.close()
    return np.array(image)

""" 
    LOAD IMAGES, 
    We assume this returns a 2D array, where rows are vertical and columns are horizontal
    WE ASSUME the horizontal / vertical direction are correct
    WE ASSUME that the (0,0) pixel will be displayed in the top left hand corner of the image
    WE ASSUME that row numbers increase as you go down from the top row of the image   
"""
beam_image = get_first_hdf5_image(image_path,beam_image_1)
back_image = get_first_hdf5_image(image_path,back_image_1)
#
"""
    The mask is an ellipse, defined by it's centre position and its radius in x/y
    In this implementation the mask IS NOT rotated with respect to the horizontal direction
"""
mask_horizontal_center = 1000
mask_vertical_center   = 900
mask_horizontal_radius  = 400
mask_vertical_radius    = 750
"""
    This means the ellipse exactly fits within a rectangular bounding box that has these start 
    and end pixel values 
    NB this is accurate to within ~1 pixel either side depending on how you count
"""
mask_boundingbox_horizontal_start =  mask_horizontal_center - mask_horizontal_radius
mask_boundingbox_horizontal_end =   mask_horizontal_center + mask_horizontal_radius
mask_boundingbox_vertical_start =  mask_vertical_center - mask_vertical_radius
mask_boundingbox_vertical_end =  mask_vertical_center + mask_vertical_radius
mask_boundingbox_width = 2 * mask_horizontal_radius
mask_boundingbox_height= 2 * mask_vertical_radius
"""
    We can now make a copy of the data that is within the bounding box 
    REMEMBER Slicing does rows then columns ...
"""
beam_image_cut = beam_image[mask_boundingbox_vertical_start:mask_boundingbox_vertical_end,
               mask_boundingbox_horizontal_start:mask_boundingbox_horizontal_end]
beam_image_cut_plot = beam_image_cut
back_image_cut = back_image[mask_boundingbox_vertical_start:mask_boundingbox_vertical_end,
               mask_boundingbox_horizontal_start:mask_boundingbox_horizontal_end]


"""
    WE KNOW everything outside the ellipse, should have a pixel value of zero
    This can be done by creating a mask of 0s and 1s, 
    if a pixel is inside the ellipse it is a 1, else it is outiside the ellipse and is a 0 
"""
def is_coordinate_inside_ellipse(x,y,xrad,yrad,xcentre,ycentre):
    """
    :param x: horizontal index of pixel
    :param y: vertical index of pixel
    :param xrad: ellipse horizontal radius
    :param yrad: ellipse vertical radius
    :param xcentre: ellipse horizontal centre
    :param ycentre: ellipse vertical centre
    :return: True if (x,y) is inside ellipse, else False
    """
    if x-xcentre > xrad:
        return False
    if y-ycentre > yrad:
        return False
    if ((x-xcentre)/xrad)**2 + ((y-ycentre)/yrad)**2 > 1:
        return False
    return True
def set_one_for_inside_ellipse(image,xrad,yrad,xcentre,ycentre):
    """
    set pixels inside the ellipse to be 1
    :param image: 2d array of data, all zeroes
    :param xrad: ellipse horizontal radius
    :param yrad: ellipse vertical radius
    :param xcentre: ellipse horizontal centre
    :param ycentre: ellipse vertical centre
    :return: array with inside ellipse pixels set to 1
    """
    for y in range(0, len(image)): # loop over vertical
        for x in range(0, len(image[0])): # loop over horizontal
            if is_coordinate_inside_ellipse(x,y,xrad,yrad, xcentre, ycentre):
                image[y,x] = 1.
    return image

mask_1 = set_one_for_inside_ellipse(np.zeros((len(beam_image_cut), len(beam_image_cut[0]))),
                                   mask_horizontal_radius, mask_vertical_radius,
                                   mask_horizontal_radius, mask_vertical_radius)

"""
    We can now multiply our image by the mask
"""
beam_image_cut_2 = beam_image_cut * mask_1
beam_image_cut_2_plot = beam_image_cut * mask_1 # make a copy to plot
"""
    NOW lets get the projections (i.e. the row and column sums )
    In the plots you can see how setting the pixel values outside the ellipse to zero has 
    introduced an artifact into the projections.  
    We can account for this artifact with "NPOINT scaling"  
"""
horizontal_projection_1 = beam_image_cut_2.sum(axis=0)
vertical_projection_1 = beam_image_cut_2.sum(axis=1)


"""
    NPOINT SCALING (of the MASK)
    "This method assumes that the first and last ten points in both the x and y directions fro
    the image are "background" and contain no beam or dark current signals."
    NPOINT scaling is going to scale the MASK by a constant to minimise the effect of the
    elliptical mask (i.e instead of 1 for inside the ellipse it's going to be L,
    where L is an "optimised" value)


    root-mean-square difference between mask_1 and the data, (of the first and last 10 points for
    each projections)
"""
"First take the first and last ten points in x and y from the projection of the DATA "
"and last ten points in x and y from the projection of the MASK "
NPOINTS = 10  # HOW MANY points ???
dxE = horizontal_projection_1[-NPOINTS:]
dyS = vertical_projection_1[:NPOINTS]
dxS = horizontal_projection_1[:NPOINTS]
dyE = vertical_projection_1[-NPOINTS:]
mxS = mask_1.sum(axis=0)[:NPOINTS]
mxE = mask_1.sum(axis=0)[-NPOINTS:]
myS = mask_1.sum(axis=1)[:NPOINTS]
myE = mask_1.sum(axis=1)[-NPOINTS:]

"""
    we are linearly scaling the mask, so we only need to find two points and find where the 
    straight line they sit on crosses y = 0 (the x axis is the scaling factor) 
    these are the data from the image and the mask  # POINTS MUST BE IN THE SAME ORDER!!
"""
imagepoints = np.concatenate((dxS, dxE, dyS, dyE))
maskpoints = np.concatenate((mxS, mxE, myS, myE))
"""
    to make the math easier we can choose smart value ...
    make point 1 for the straight line for a scaling factor of 0
    point 2 can be anywhere, say x = 1, to make the math easier
"""
point_1 = [0, np.mean( -1 * imagepoints)]
point_2= [1, np.mean( [a_i - b_i for a_i, b_i in zip(maskpoints, imagepoints)])]
"""
    now we can use the equation of a straight line to find where it crosses y=0
    This is very simple because we have chosen points that make it simple
    just re-arrange the equation fro a straight line  
    y = m x + c, where m is gradient and c is intercept, x = c / m
"""
npoint_scaling = -1 * point_1[1] / (point_2[1] - point_1[1])
"""
    now we have the "optimum" scaLing factor for the mask, we should use that instead
"""

beam_image_cut_3 = beam_image_cut_2 - npoint_scaling * mask_1

horizontal_projection_2 = beam_image_cut_3.sum(axis=0)
vertical_projection_2 = beam_image_cut_3.sum(axis=1)

"""
    Now Lets' calculate the moments of the projections
     
    the 1st moment can be thought of as the "balance" point, or centre of mass,
    the 2nd moment is the square root of the variance of the distribution
"""
def get_first_second_moments(data):
    """
    This funciton get sth efirts and second moments (about the mean) fro a 1D list
    :param data:
    :return:
    """
    data_indices = np.arange(len(data))
    normalisation = np.sum(data) # sum of data
    moment_1 = np.dot(data_indices, data) / normalisation
    moment_2 = np.sqrt( np.dot( (data_indices - moment_1)**2, data ) / normalisation )
    return [moment_1,moment_2]

horizontal_moments = get_first_second_moments(horizontal_projection_2)
vertical_moments = get_first_second_moments(vertical_projection_2)


# Plot overlays to show ellipse and bounding box
# ELLIPSE
# https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.patches.Ellipse.html?highlight=ellipse
# iot seems we need to make a new ellipse/rectangle each time we want to inlcude one
full_image_mask_ellipse_art = Ellipse((mask_horizontal_center, mask_vertical_center),
                          width= mask_horizontal_radius * 2 ,
                          height=mask_vertical_radius * 2 ,
                          edgecolor='white',facecolor='none',linewidth=1)

cut_image_mask_ellipse_art = Ellipse((mask_horizontal_radius, mask_vertical_radius),
                          width= mask_horizontal_radius * 2 ,
                          height=mask_vertical_radius * 2 ,
                          edgecolor='white',facecolor='none',linewidth=1)
cut_image_mask_ellipse_art_2 = Ellipse((mask_horizontal_radius, mask_vertical_radius),
                          width= mask_horizontal_radius * 2 ,
                          height=mask_vertical_radius * 2 ,
                          edgecolor='white',facecolor='none',linewidth=1)
# of course rectangle are defined differently,
# https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.patches.Rectangle.html
mask_boundingbox_art = Rectangle((mask_boundingbox_horizontal_start, mask_boundingbox_vertical_start),
                          width= mask_horizontal_radius * 2,
                          height=mask_vertical_radius * 2,
                          edgecolor='red',facecolor='none',linewidth=1)

"""PLOTTING"""


"""
    WE will show the position and width from the moments as a cross hair of length = second_moments
    https://stackoverflow.com/questions/12864294/adding-an-arbitrary-line-to-a-matplotlib-plot-in-ipython-notebook
"""

# for the cropped image
hpos = horizontal_moments[0]
hwidth = horizontal_moments[1]/2.0
vpos = vertical_moments[0]
vwidth = vertical_moments[1]/2.0

x_cross_hair = [[hpos-hwidth, hpos+hwidth],  [vpos ,vpos ]]
y_cross_hair = [[hpos, hpos],  [vpos -vwidth ,vpos + vwidth ]]


# for the FULL image the centre position changes, not the width
hpos_f = horizontal_moments[0] + ( mask_horizontal_center - mask_horizontal_radius)
vpos_f = vertical_moments[0] + ( mask_vertical_center - mask_vertical_radius)

x_cross_hair_f = [[hpos_f-hwidth, hpos_f+hwidth],  [vpos_f ,vpos_f ]]
y_cross_hair_f = [[hpos_f, hpos_f],  [vpos_f -vwidth ,vpos_f + vwidth ]]


fig = plt.figure(figsize=(17, 8))

ax = fig.add_subplot(151)
ax.set_title('beam_image')
ax.add_patch(full_image_mask_ellipse_art)
ax.add_patch(mask_boundingbox_art)
plt.imshow(beam_image, vmax = 1000)
plt.plot(x_cross_hair_f[0],x_cross_hair_f[1],'k-',lw=2)
plt.plot(y_cross_hair_f[0],y_cross_hair_f[1],'k-',lw=2)
ax.set_aspect('equal')
cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
cax.get_xaxis().set_visible(False)
cax.get_yaxis().set_visible(False)
cax.patch.set_alpha(0)
cax.set_frame_on(False)


ax2 = fig.add_subplot(152)
ax2.set_title('beam_image_cut_2')
plt.imshow(beam_image_cut_2, vmax = 1000)
plt.plot(x_cross_hair[0],x_cross_hair[1],'k-',lw=2)
plt.plot(y_cross_hair[0],y_cross_hair[1],'k-',lw=2)
ax2.add_patch(cut_image_mask_ellipse_art)
ax2.set_aspect('equal')
cax2 = fig.add_axes([0.12, 0.1, 0.78, 0.8])
cax2.get_xaxis().set_visible(False)
cax2.get_yaxis().set_visible(False)
cax2.patch.set_alpha(0)
cax2.set_frame_on(False)


ax3 = fig.add_subplot(153)
ax3.set_title('First Projections')
ax3.plot(horizontal_projection_1)
ax3.plot(vertical_projection_1)


ax4 = fig.add_subplot(154)
ax4.set_title('beam_image_cut_3')
plt.imshow(beam_image_cut_3, vmax = 1000)
ax4.add_patch(cut_image_mask_ellipse_art_2)
ax4.set_aspect('equal')
cax4 = fig.add_axes([0.12, 0.1, 0.78, 0.8])
cax4.get_xaxis().set_visible(False)
cax4.get_yaxis().set_visible(False)
cax4.patch.set_alpha(0)
cax4.set_frame_on(False)

ax5 = fig.add_subplot(155)
ax5.set_title('NPOINT Scaled  Projections')
ax5.plot(horizontal_projection_2)
ax5.plot(vertical_projection_2)



#
# ax = fig.add_subplot(253)
# ax.set_title('mask_1')
# plt.imshow(mask_1, vmax = 1)
#
# ax = fig.add_subplot(254)
# ax.set_title('image_to_analyze_2')
# plt.imshow(image_to_analyze_2_plot, vmax = 1000)
# cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
# cax.get_xaxis().set_visible(False)
# cax.get_yaxis().set_visible(False)
# cax.patch.set_alpha(0)
# cax.set_frame_on(False)



plt.show()


raw_input()