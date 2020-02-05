import numpy as np
import h5py
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import lsqr as lsqr
from scipy.io import loadmat

'''
This is a working copy of the matlab script, to do the tomography analysis 
It uses CLARATomography.m and covers teh code from after the image's have been prepared / scaled 
etc. 
It DOES NOT YET create the final phase space plots  
First we build the "Tomography Matrix" based on pre-computed phase advances
for each quad setting 

The we build the "tomography matrix" which part of the projection tells where the beam in pixel in 
phase space
"ends up"  

Then we use it with the bream projection data to find a phase space distribution that 
re-creates "as good a a match" to the projections as we can.  


!!!!!!!!WARNING!!!!!!!! 
Throughout this code there is the possibility of getting the array indexes wrong. In 
the original Matlab code the first elements have index 1, in python the first elements are index 0 
As is common with these types of calculation it can be very easy to be off by a single pixel
What is presented here exactly reproduces the Matlab output 

'''

'''
First we define some constants, and input data,
I expect that these numbers will be defined / calculated earlier in the procedure 
'''

'''
phase advances (between observation  and recon point?for each quad setting,
These are calculated earlier in the procedure
'''
phase_advances = [[0.336646899467633, 0.228677801765683], [0.187706900011030, 0.246774303860592],
                  [0.557301245734776, 0.218226902788538], [0.646249817696088, 0.212050203302031],
                  [0.847182618687409, 0.251044121023979], [0.110780647521904, 0.468106739372366],
                  [2.62569135318545, 0.194023921811343], [2.83364380029125, 0.188854333509495],
                  [1.19793501134747, 0.360159286931395], [2.35792837214027, 0.707884839231188],
                  [2.40860466658718, 0.565425984158209], [0.128075565772166, 0.508255210347035],
                  [0.142547024324626, 0.498223437389374], [0.138603132035716, 0.444475122604461],
                  [0.167608435974038, 0.540792110187697], [0.162285462530223, 0.489530259542603],
                  [0.141324894117748, 0.600002949342541], [0.155153927292574, 0.437232958404853],
                  [2.47011962261521, 0.466152684147431], [0.167988731208729, 0.411351048916142],
                  [0.163124570409165, 0.544156188746966], [0.176059572366250, 0.583855269238915],
                  [1.35152798395836, 0.343960230499161], [0.227803144165605, 1.03170836139496],
                  [1.99805399675554, 0.446186152909307], [0.254602909063604, 1.96683072792882],
                  [0.240376121070856, 0.720248742970963], [2.05741721523473, 0.423956512784906],
                  [1.90285150619246, 0.380575735308209], [2.11593101331609, 0.401566209842100],
                  [0.483931193105037, 0.835315141319805], [1.44808596780524, 0.395283820308017],
                  [2.86285656512334, 1.61993600234020], [1.80958014192688, 3.16447504868879],
                  [2.11112675621833, 3.22156906985141], [3.17202280936962, 0.514232105089073],
                  [2.85305455690855, 0.890605054554737], [2.10827467056920, 3.22377151541008]]
'''
Cherry pick our datasets.

Here we are manually choosing which quad settings (by index) to include in the tomogrpahy 
calculation,

How do we choose? witchcraft - i've copied this from the original matlab script, Incoporating 
this step into our analysis will not be trivial   
'''
xdata_matlab = [1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
                27, 28, 29, 30, 32, 33, 34, 35, 36, 37, 38]
xdata_indexes = [x - 1 for x in xdata_matlab]
nx = len(xdata_indexes)

ydata_matlab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                24, 25, 26, 27, 28, 29, 30, 31, 32, 34, 35, 36, 37]
ydata_indexes = [x - 1 for x in ydata_matlab]
ny = len(ydata_indexes)

print('Number of x datasets = ', nx)
print('Number of y datasets = ', ny)

'''
constants for processed image resolution 
the processed image resolution, or number of pixels in x and y for the processed images 
This is the offset to the centre of the beam. The processed images are all centered on the
electron beam ...
'''
psresn = 201
ctroffset = 101

'''
load in processed image array, this is an array of rescaled images for each quad setting,
Ths is calculated earlier in the procedure, here we are importing the Matlab results
'''
imagearraypath = ".//Image Scaling//matlab_imagearray.h5"
image_array_file = h5py.File(imagearraypath, 'r+')
image_array = image_array_file["/data"]

'''
Create empty arrays for results

dfindxx, dfindxy are the "Tomography Matrices"

xprojection, yprojection are the beam image projections 

!!!!WARNING!!!! SET THE CORRECT TYPE HERE

'''

dfindxx = np.zeros((2, nx * pow(psresn, 2)), dtype=int)
dfindxy = np.zeros((2, ny * pow(psresn, 2)), dtype=int)
print('dfindxx shape =  ', dfindxx.shape)
print('dfindxy shape =  ', dfindxy.shape)

xprojection = np.zeros((nx * psresn), dtype=float)
yprojection = np.zeros((ny * psresn), dtype=float)
print('xprojections length = ', len(xprojection))
print('yprojections length = ', len(yprojection))

'''
Calculate the Tomography Matrix for X-phase space  
loop over each x and px pixel
I think what we are doing is: seeing if a pixel at the observation point, "maps" to a pixel in 
the reconstruction point. (clearly all the pixels do, maybe i should say "is in the field of 
view of the recon point?") There is probably a much more accurate wording for this  

These loops can be turned in to a function, and probably calculated for all quad settings, 
then you manually choose which dataset to leave out later ...  
'''
print('Calculating (x, px) plane Tomography Matrix')
count = 1  # a counter to let you know which pixel in the recon part
for index in range(0, nx):  # !!!!!!!!! the matlab code starts at 1
    # print("index = ", index)
    dataset = xdata_indexes[index]
    cosmux = np.cos(phase_advances[dataset][0])
    sinmux = np.sin(phase_advances[dataset][0])
    # print(" phase_advances = ", phase_advances[dataset][0])
    # print(" cosmux,sinmux = ", cosmux,sinmux)
    for x in range(1, psresn + 1):  # copying Matlab code so loop indexes start at 1 ...
        for px in range(1, psresn + 1):
            xindx0 = int(round(cosmux * (x - ctroffset) - sinmux * (px - ctroffset) + ctroffset))
            if 0 < xindx0 and xindx0 <= psresn:
                pxindx0 = int(
                    round(sinmux * (x - ctroffset) + cosmux * (px - ctroffset) + ctroffset))
                if 0 < pxindx0 and pxindx0 <= psresn:
                    # Slight difference to Matlab as 'index' should start at 0 in Python
                    dfindxx[:, count - 1] = [(index) * psresn + x, (xindx0 - 1) * psresn + pxindx0]
                    # print("[(index)*psresn + x, (xindx0 - 1) * psresn+pxindx0] = ",
                    #       [(index)*psresn + x, (xindx0 - 1) * psresn+pxindx0])
                    # print("dfindxx[dfcntrx] = ", dfindxx[dfcntrx])
                    count += 1  # increment counter  # if dfcntrx % 10000 == 0:  #     print(  #
                    # xindx0,pxindx0)
    # x projection is sum of columns
    xprojection[index * psresn: (index + 1) * psresn] = image_array[dataset].sum(axis=0)
x_count_final = count

print('Calculating (y, py) plane Tomography Matrix')
count = 1  # a counter to let you know which pixel in the recon part
for index in range(0, ny):  # !!!!!!!!! the matlab code starts at 1
    # print("index = ", index)
    dataset = ydata_indexes[index]
    cosmuy = np.cos(phase_advances[dataset][1])
    sinmuy = np.sin(phase_advances[dataset][1])
    # print(" phase_advances = ", phase_advances[dataset][0])
    # print(" cosmuy,sinmuy = ", cosmuy,sinmuy)
    for y in range(1, psresn + 1):  # copying Matlab code so loop indexes start at 1 ...
        for py in range(1, psresn + 1):
            yindx0 = int(round(cosmuy * (y - ctroffset) - sinmuy * (py - ctroffset) + ctroffset))
            if 0 < yindx0 and yindx0 <= psresn:
                pyindx0 = int(
                    round(sinmuy * (y - ctroffset) + cosmuy * (py - ctroffset) + ctroffset))
                if 0 < pyindx0 and pyindx0 <= psresn:
                    # Slight difference to Matlab as 'index' should start at 0 in Python
                    dfindxy[:, count - 1] = [(index) * psresn + y, (yindx0 - 1) * psresn + pyindx0]
                    count += 1  # increment counter
    # x projection is sum of columns
    yprojection[index * psresn: (index + 1) * psresn] = image_array[dataset].sum(axis=1)
y_count_final = count

print('Building sparse matrices and solving')
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html#scipy.sparse.csr_matrix
dfindxx2 = dfindxx[:, 0:x_count_final - 1] - 1  # go from nmatlab 1 is first element to python 0
dfullx = csr_matrix((np.ones(x_count_final - 1), (dfindxx2[0, :], dfindxx2[1, :])),
                    shape=(nx * psresn, psresn * psresn))
dfindxy2 = dfindxy[:, 0:y_count_final - 1] - 1  # go from nmatlab 1 is first element to python 0
dfully = csr_matrix((np.ones(y_count_final - 1), (dfindxy2[0, :], dfindxy2[1, :])),
                    shape=(ny * psresn, psresn * psresn))

rhovectorx, istopx, itnx, normrx = lsqr(A=dfullx, b=xprojection, atol=0.000001, iter_lim=400)[:4]
rhovectory, istopy, itny, normry = lsqr(A=dfully, b=yprojection, atol=0.000001, iter_lim=400)[:4]

print("Complete")
print("")

'''
Check some of the calculated numbers against matlab 
'''
# Load Matlab answers
mat_datax = loadmat('.//TomographyMatrix_djs//TomographyMatrixX.mat')
rhovectorx_mat = mat_datax['rhovectorx']
xprojection_mat = mat_datax['xprojection']
dfullx_mat = mat_datax['dfullx']

mat_datay = loadmat('.//TomographyMatrix_djs//TomographyMatrixY.mat')
rhovectory_mat = mat_datay['rhovectory']
yprojection_mat = mat_datay['yprojection']
dfully_mat = mat_datay['dfully']

print("Comparison With MATLAB results ")
print("")
print("X PROJECTION")
print("xprojection     = ", xprojection)
print("xprojection_mat = ", xprojection_mat.flatten())
print("EQUAL ? = ", xprojection == xprojection_mat.flatten())
print("rhovectorx     = ", rhovectorx)
print("rhovectorx_mat = ", rhovectorx_mat.flatten())
print("EQUAL ? = ", rhovectorx_mat == rhovectorx)
print("")
print("Y PROJECTION")
print("yprojection     = ", yprojection)
print("yprojection_mat = ", yprojection_mat.flatten())
print("EQUAL ? = ", yprojection == yprojection_mat.flatten())
print("rhovectory     = ", rhovectory)
print("rhovectory_mat = ", rhovectory_mat.flatten())
print("EQUAL ? = ", rhovectory_mat == rhovectory)

''' 
    reproduce the plots  of projections and fitted projections / residuals
'''
print("PLOTTING ")

import matplotlib.pyplot as plt

fig = plt.figure(figsize=(15, 5))
x1 = fig.add_subplot(2, 2, 1)
x1.plot(xprojection, '-k')
x1.plot(dfullx * rhovectorx, '--r')
x2 = fig.add_subplot(2, 2, 2)
x2.plot(xprojection - dfullx * rhovectorx, '-r')
x2.set_xlabel('Data point')
x2.set_ylabel('x residual')

y1 = fig.add_subplot(2, 2, 3)
y1.plot(yprojection, '-k')
y1.plot(dfully * rhovectory, '--r')
y2 = fig.add_subplot(2, 2, 4)
y2.plot(yprojection - dfully * rhovectory, '-r')
y2.set_xlabel('Data point')
y2.set_ylabel('x residual')

plt.show()

print("TODO: create an actual plot of the calculated phase spaces ")

input()
input()
input()
