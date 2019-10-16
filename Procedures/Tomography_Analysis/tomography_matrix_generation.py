import numpy as np
import h5py
from scipy.sparse import csr_matrix
'''
This is the first attempt at following the matlab script, to be improved when it is working ... 
'''


#
# Build the Tomography Matrix ,
# we're going to try adn reproduce this code from the matlab script

# phase advances (between obs and recon point?for each quad setting,
# These are calcaulted in an ealrier part of the procedure
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

# These are which data (by index) we are going to use for analysis I presume they are chosen by 
# hand ... ?
indxx = [1, 2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 27, 28,
         29, 30, 32, 33, 34, 35, 36, 37, 38]
indxx_py  =[x - 1 for x in indxx]
nx = len(indxx)
indxy = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25,
         26, 27, 28, 29, 30, 31, 32, 34, 35, 36, 37]
indxy_py  =[x - 1 for x in indxy]
ny = len(indxx)

# the processed image resolution? number of pixels in the formatted data?
psresn = 201
# This is the offset to thr centre of the beam? the processed images are all centered on the
# electron beam ...
ctroffset = 101





# load in image array, this is an array of rescaled images for each quad setting,
imagearraypath = ".//Image Scaling//matlab_imagearray.h5"
image_array_file = h5py.File(imagearraypath, 'r+')
image_array = image_array_file["/data" ]
#print(image_array[0].sum(axis=0))




# np.zeros((2, 1))
# array([[ 0.],
#        [ 0.]])
# IN MATLAB!!
# zeros([2 3]) returns a 2-by-3 matrix.

# fill empty vectors for this (needs a better name)
dfindxx = np.zeros(( 2,nx*pow(psresn,2)),dtype=int)
dfindxy = np.zeros(( 2,ny*pow(psresn,2)),dtype=int)


print('dfindxx shape =  ', dfindxx.shape )
print('dfindxy shape =  ', dfindxy.shape )


# fill empty vectors for projections
# SET THE CORRECT TYPE HERE!!!
xprojection = np.zeros((nx * psresn), dtype=float)
yprojection = np.zeros((ny * psresn), dtype=float)

#xprojection[0:201] = np.array(image_array[0].sum(axis=0))
#print(xprojection[0:201])

# get 'Tomography mMatrix'
'''
loop over each x and px pixel
I think what we are doing is: seeing if a pixel at the observation point, "maps" to a pixel in 
the reconstruction point. (clearly all the pixels do, maybe i should say "is in the field of 
view of the recon point?") There is probably a much more accurate wording for this  
'''
#I think this is just a counter to let you know which pixel in the recon part
dfcntrx = 1
for index in range(0, nx): # !!!!!!!!! the matlab code starts at 1
    #print("index = ", index)
    dataset = indxx_py[index ]

    #print(" phase_advances = ", phase_advances[dataset][0])
    #print(" phase_advances = ", phase_advances[dataset][0])

    cosmux = np.cos( phase_advances[dataset][0])
    sinmux = np.sin( phase_advances[dataset][0])
    #print(" cosmux,sinmux = ", cosmux,sinmux)

    # copying matlab code so loop indexes start at 1 ...
    for x in range(1,psresn+1):
        for px in range(1,psresn+1):
            xindx0 = int(round(cosmux*(x - ctroffset) - sinmux*(px - ctroffset) + ctroffset))
            #print('xindx0 = ', xindx0)
            if 0 < xindx0:
                if xindx0 <= psresn:
                    pxindx0 = int(round(sinmux*(x-ctroffset) + cosmux*(px - ctroffset) + ctroffset))
                    #print('pxindx0 = ', pxindx0)
                    if 0 < pxindx0:
                        if pxindx0 <= psresn:

                            # different to matlba code as here 'index' starts at 0
                            dfindxx[:,dfcntrx-1] = [(index)*psresn + x, (xindx0 - 1) *
                             psresn+pxindx0]

                            # print("[(index)*psresn + x, (xindx0 - 1) * psresn+pxindx0] = ",
                            #       [(index)*psresn + x, (xindx0 - 1) * psresn+pxindx0])
                            # print("dfindxx[dfcntrx] = ", dfindxx[dfcntrx])

                            dfcntrx += 1

                            # if dfcntrx % 10000 == 0:
                            #     print(xindx0,pxindx0)


    # x projection is sum of columns
    xprojection[index*psresn : (index +1) * psresn ] = image_array[dataset].sum(axis=0)

    #print('dfcntrx = ', dfcntrx)
    #print(xprojection[index*psresn] , "  ", (image_array[dataset].sum(axis=0))[0] )
    #print("index = ", [index*psresn , (index +1) * psresn  ] )
    #print("lens  = ", len(xprojection[index*psresn : (index +1) * psresn ]))


from scipy.io import loadmat
import os

# where are the raw image files we want to analyse?

#final count for dfcntrx
print('Final dfcntrx = ', dfcntrx)
print("xprojection[1-1] = ",xprojection[1-1])
print("xprojection[1000-1] = ",xprojection[1000-1])
print("xprojection[-1] = ",xprojection[-1])

#% Finally, construct the (sparse) matrix relating the projected
#% distribution at YAG02 to the phase space distribution at YAG01

print('dfindxx[0:10] ',dfindxx[0:10]  )


print("test format")
print("dfindxx.shape = ", dfindxx.shape)
dfindxx2 = dfindxx[:,0:dfcntrx-1] -1 # go from nmatlab 1 is first element to python 0 is first
# element
print("dfindxx2.shape = ", dfindxx2.shape)


#findxx_mat_path = os.path.join(working_directory, 'dfindxx.mat')
dfindxx_mat_data = loadmat('.//TomographyMatrix_djs//dfindxx.mat')
dfindxx_mat = dfindxx_mat_data['dfindxx']
print("dfindxx_mat.shape = ", dfindxx_mat.shape)

print(dfindxx_mat[0])
print(dfindxx_mat[1])
print(dfindxx2[0])
print(dfindxx2[1])
print(dfindxx2 == dfindxx_mat )


print("Create final sparse matrix")
print("dfindxx2[0,:].shape = ",dfindxx2[0,:].shape)
print("dfindxx2[1,:].shape = ",dfindxx2[1,:].shape)
print(nx*psresn,psresn*psresn)

# sparse matrix part
# https://stackoverflow.com/questions/40890960/numpy-scipy-equivalent-of-matlabs-sparse-function
# there are sparse ROW and sparse COLUMN matrices that are faster for operations on rows or columns
# lets try a "compressed sparse row => csr"
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html#scipy.sparse.csr_matrix


# i am not creating the sparse matrix correctly ....
print("max(dfindxx2[0,:]) ", max(dfindxx2[0, :])  )
print("max(dfindxx2[1,:]) ", max(dfindxx2[1, :])  )


dfullx = csr_matrix( (np.ones(dfcntrx-1), (dfindxx2[0,:], dfindxx2[1,:])), shape=(nx*psresn,
                                                                              psresn*psresn))
#dfully = sparse( dfindxy(1,:),dfindxy(2,:), ones(1,dfcntry-1), ny*psresn,psresn^2);


from scipy.sparse.linalg import lsqr as lsqr
rhovectorx, istop, itn, normr = lsqr( A=dfullx, b = xprojection, atol=0.000001, iter_lim =400)[:4]


print("rhovectorx     ", rhovectorx  )
print("istop ", istop  )
print("itn   ", itn )
print("normr ", normr )



# Matlab answer
mat_datax = loadmat('.//TomographyMatrix_djs//TomographyMatrixX.mat')
rhovectorx_mat = mat_datax['rhovectorx']
xprojection_mat = mat_datax['xprojection']
dfullx_mat = mat_datax['dfullx']

print("xprojection     = ", xprojection)
print("xprojection_mat = ", xprojection_mat )

print("xprojection = ", xprojection == xprojection_mat.flatten() )
print("xprojection = ", np.subtract(xprojection, xprojection_mat.flatten()) )
print("rhovectorx = ", rhovectorx_mat == rhovectorx )
#print("dfullx = ", dfullx_mat != dfullx )


mat_datay = loadmat('.//TomographyMatrix_djs//TomographyMatrixY.mat')
rhovectory_mat = mat_datay['rhovectory']
yprojection_mat = mat_datay['yprojection']
dfully_mat = mat_datay['dfully']


rhox = rhovectorx.reshape((psresn,psresn))
rhoy = rhovectory_mat.reshape((psresn, psresn))




print("PLOTTING ")

# reproduce the plots
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(17, 8))
ax = fig.add_subplot(2,2,1)
ax.plot(xprojection,'-k')
ax.plot(dfullx*rhovectorx,'--r')


p2 = fig.add_subplot(2,2,2)
p2.plot(xprojection - dfullx*rhovectorx,'-r')

p2.set_xlabel('Data point')
p2.set_ylabel('x residual')

plt.show()

input()




"""
for n = 1:nx

    indx   = indxx(n);

    % Set the phase advance

    cosmux = cos(PhaseAdvance_x_y(indx,1));
    sinmux = sin(PhaseAdvance_x_y(indx,1));

    % Find the indices of the non-zero values of the matrix relating the
    % projected distribution at YAG02 to the phase space distribution at YAG01

    for xindx1 = 1:psresn
        for pxindx1 = 1:psresn
            xindx0  = round(cosmux*(xindx1 - ctroffset) - sinmux*(pxindx1 - ctroffset) + ctroffset);
            if xindx0>0 && xindx0<=psresn
                pxindx0 = round(sinmux*(xindx1 - ctroffset) + cosmux*(pxindx1 - ctroffset) + ctroffset);
                if pxindx0>0 && pxindx0<=psresn

                    dfindxx(:,dfcntrx) = [(n-1)*psresn + xindx1; (xindx0-1)*psresn + pxindx0];
                    dfcntrx = dfcntrx + 1;

                end
            end
        end
    end

    % Construct the vector of image pixels
    % why not normalised?
%     nrm = sum(sum(imagearray[indx]));

    xprojection(((n-1)*psresn+1):n*psresn) = sum(imagearray[indx],2); %/nrm;

end
"""




