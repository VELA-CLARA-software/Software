import numpy as np
import time
import re
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt
import sys

file1 = sys.argv[1]
file2 = sys.argv[2]
#file1 = 'qscan20181101-160720.txt'
#file2 = 'qscan20181102-092138.txt'

############ Read in the data and put it in the correct form ###################
def readfile(file):
    with open(file) as qscan_file:
        content = qscan_file.readlines()
    # number of individuals
    npoints = len(content)
    #print npoints
    npoints_1D = np.sqrt(npoints)
    #print npoints_1D

    # split first line to get length for initialising data_array
    #content_split_0=content[0].split()
    data_array = np.zeros((len(content), 6))#len(content_split_0)))

    # convert strings etc. from content variable to floats in data_array
    for i, line in enumerate(content):
        content_split = line.split()
        for j, x in enumerate(np.arange(2, 13, 2)):
            #print j, x
            data_array[i, j] = float(content_split[x])
        #for j, element in enumerate(content_split):
        #    data_array[i, j] = element#float(re.sub('[^0-9\.]','',element))

    #print len(data_array)
    vcx = data_array[:,1].reshape((int(npoints_1D), int(npoints_1D)))
    vcy = data_array[:,2].reshape((int(npoints_1D), int(npoints_1D)))
    charge = data_array[:,3].reshape((int(npoints_1D), int(npoints_1D)))

    for y, line in enumerate(vcy):
        if y % 2 != 0:
            #print y
            vcy[y,:] = np.flipud(vcy[y,:])
            charge[y,:] = np.flipud(charge[y,:])
            #print vcy[y,:]
    return vcx, vcy, charge

def do_plotting(subplot, vcx, vcy, charge, cmin, cmax, title, cbarlabel):
    ax = plt.subplot(1, 3, subplot)#,aspect='equal')
    plt.pcolormesh(vcx, vcy, charge, vmin=cmin, vmax=cmax, cmap='YlGnBu')#, shading='gouraud')#, cmap='rainbow')
    #plt.imshow(charge, extent=(np.amin(vcx), np.amax(vcx), np.amin(vcy), np.amax(vcy)), origin="upper")#, aspect = 'auto')
    plt.xlabel('x [mm]', fontsize=14)
    plt.ylabel('y [mm]', fontsize=14)
    ax.tick_params(axis = 'both', which = 'major', labelsize = 14)
    plt.title(title)
    #plt.rcParams['figure.facecolor'] = 'white'
    cbar = plt.colorbar(label = cbarlabel)#im, cax=cax, orientation='horizontal')
    cbar.ax.tick_params(labelsize=14)
    cbar.set_label(label = cbarlabel, size=16)
    plt.axis('equal')


fig = plt.figure(figsize=(15,5))

vcx1, vcy1, charge1 = readfile(file1)
vcx2, vcy2, charge2 = readfile(file2)

max1 = np.max(charge1).round(1)
max2 = np.max(charge2).round(1)
maxc = np.max([max1, max2])

max1_x = vcx1[np.where(charge1 == charge1.max())][0].round(2)
max1_y = vcy1[np.where(charge1 == charge1.max())][0].round(2)
title1 = re.sub('[^0-9-]','',str(file1))+', max = '+str(max1)+' pC\n@ x = '+str(max1_x)+', y = '+str(max1_y)
cbarlabel1 = 'Charge [pC]'
do_plotting(1, vcx1, vcy1, charge1, 0, maxc, title1, cbarlabel1)

max2_x = vcx2[np.where(charge2 == charge2.max())][0].round(2)
max2_y = vcy2[np.where(charge2 == charge2.max())][0].round(2)
title2 = re.sub('[^0-9-]','',str(file2))+', max = '+str(max2)+' pC\n@ x = '+str(max2_x)+', y = '+str(max2_y)
cbarlabel1 = 'Charge [pC]'
do_plotting(2, vcx2, vcy2, charge2, 0, maxc, title2, cbarlabel1)

charge_diff = charge2 / charge1
cbarlabel3 = 'Ratio'
do_plotting(3, vcx2, vcy2, charge_diff, np.min(charge_diff), np.max(charge_diff), 'Difference', cbarlabel3)
#do_plotting(3, vcx2, vcy2, charge_diff, -np.max(charge1)/2, np.max(charge1)/2)

plt.tight_layout()

plt.show()
fig = plt.figure()
fig.set_figheight(32)
fig.set_figwidth(9)
