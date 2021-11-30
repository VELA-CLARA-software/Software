import numpy as np
import time
import re
import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt
import glob
#import sys

#file1 = sys.argv[1]
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
    laserE = data_array[:,4].reshape((int(npoints_1D), int(npoints_1D)))
    VCintens = data_array[:,5].reshape((int(npoints_1D), int(npoints_1D)))

    for y, line in enumerate(vcy):
        if y % 2 != 0:
            #print y
            vcy[y,:] = np.flipud(vcy[y,:])
            charge[y,:] = np.flipud(charge[y,:])
            laserE[y,:] = np.flipud(laserE[y,:])
            VCintens[y,:] = np.flipud(VCintens[y,:])
            #print vcy[y,:]
    return vcx, vcy, charge, laserE, VCintens

def do_plotting(subplot, vcx, vcy, charge, cmin, cmax, title, cbarlabel, x, y):
    ax = plt.subplot(1, 3, subplot)#,aspect='equal')
    plt.pcolormesh(vcx, vcy, charge, vmin=cmin, vmax=cmax, cmap='YlGnBu')#, shading='gouraud')#, cmap='rainbow')
    #plt.imshow(charge, extent=(np.amin(vcx), np.amax(vcx), np.amin(vcy), np.amax(vcy)), origin="upper")#, aspect = 'auto')
    plt.xlabel('x [mm]', fontsize=16)
    plt.ylabel('y [mm]', fontsize=16)
    ax.tick_params(axis = 'both', which = 'major', labelsize = 14)
    plt.title(title)
    #plt.rcParams['figure.facecolor'] = 'white'
    cbar = plt.colorbar()#im, cax=cax, orientation='horizontal')
    cbar.ax.tick_params(labelsize=14)
    #cbar.set_label(label = 'Charge [pC]',size=16)
    cbar.set_label(label = cbarlabel,size=16)
    plt.scatter(x,y, c='r', marker='*', edgecolors='r', s=500)
    plt.axis('equal')

#fig = plt.figure(figsize=(8,7))
#filelist = ['qscan20181101-160720.txt', 'qscan20181102-092138.txt']
filelist = glob.glob("qscan*txt")

for file1 in filelist:
    print file1
    fig = plt.figure(figsize=(20,5.5))
    try:
        vcx1, vcy1, charge1, laserE1, VCintens1 = readfile(file1)

        max1 = np.max(charge1).round(1)
        max1_x = vcx1[np.where(charge1 == charge1.max())][0].round(2)
        max1_y = vcy1[np.where(charge1 == charge1.max())][0].round(2)
        max2 = np.max(1e6*laserE1).round(1)
        max2_x = vcx1[np.where(laserE1 == laserE1.max())][0].round(2)
        max2_y = vcy1[np.where(laserE1 == laserE1.max())][0].round(2)
        max3 = np.max(VCintens1).round(1)
        max3_x = vcx1[np.where(VCintens1 == VCintens1.max())][0].round(2)
        max3_y = vcy1[np.where(VCintens1 == VCintens1.max())][0].round(2)

        title1 = re.sub('[^0-9-]','',str(file1))+': Charge\nmax = '+str(max1)+' pC @ x = '+str(max1_x)+', y = '+str(max1_y)
        cbarlabel1 = 'Charge [pC]'
        title2 = re.sub('[^0-9-]','',str(file1))+': Laser energy\nmax = '+str(max2)+' uJ @ x = '+str(max2_x)+', y = '+str(max2_y)
        cbarlabel2 = 'Laser energy [uJ]'
        title3 = re.sub('[^0-9-]','',str(file1))+': VC intensity\nmax = '+str(max3)+' @ x = '+str(max3_x)+', y = '+str(max3_y)
        cbarlabel3 = 'VC intensity [a.u]'
        #do_plotting(1, vcx1, vcy1, charge1, 0, np.max(charge1), title1)
        do_plotting(1, vcx1, vcy1, charge1, 0, 200, title1, cbarlabel1, max1_x, max1_y)
        #do_plotting(2, vcx1, vcy1, 1e6*laserE1, np.min(1e6*laserE1), np.max(1e6*laserE1), 'some text', cbarlabel2)
        do_plotting(2, vcx1, vcy1, 1e6*laserE1, 0, 10, title2, cbarlabel2, max2_x, max2_y)
        do_plotting(3, vcx1, vcy1, VCintens1, np.min(VCintens1), np.max(VCintens1), title3, cbarlabel3, max3_x, max3_y)
        plt.tight_layout()

        #plt.show()
        plt.savefig(re.sub('[^0-9-]','',str(file1))+'.png')
    except Exception:
        pass
