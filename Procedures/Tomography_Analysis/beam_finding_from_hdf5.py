import h5py
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.io import loadmat
from scipy import exp




working_directory='\\\\fed.cclrc.ac.uk\\org\\NLab\\ASTeC\\Projects\\VELA\\Work\\2019\\03\\04' \
                  '\\10pC degaussing, sol -125.0'



image_file_info_path = os.path.join(working_directory, 'ImageFileInformation.mat')

image_file_information = loadmat( image_file_info_path  )



# The image files have this key
image_files = 'Image_and_background_filenames_at_observation_point'
# and we can get the data and background
print image_file_information[image_files][0,0][0]
print image_file_information[image_files][0,1][0]

beam_fn = os.path.join(working_directory, str(image_file_information[image_files][0,0][0]) )
back_fn = os.path.join(working_directory, str(image_file_information[image_files][0,1][0]) )


print beam_fn
print back_fn


beam_image = h5py.File(beam_fn ,'r+')
back_image = h5py.File(back_fn ,'r+')

# all images have this string in their 'group' (key)
image_tag = 'Capture'


beam_keys = [x for x in beam_image.keys() if image_tag in x ]
back_keys = [x for x in back_image.keys() if image_tag in x ]

# get background data
# THIS IS A REAL GOTCHA, HDF5 AND MATLAB ARE SPECIFYING THE TYPE OF THE DATA WE ARE READING IN AS
# UNSIGNED INTEGER, YOU MUST CHANGE THE TYPE TO INT, OR WHEN WE DO SUBTRACTION LATER THINGS GO
# WRONG  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
back_data = np.array(back_image[back_keys[0]][()],dtype=np.float32)
if len(back_keys) > 1:
    for index in range(1,len(back_keys)):
        back_data += np.array(back_image[back_keys[index]][()])
    back_data /= len(back_keys)


beam_images = []


for index in beam_keys:
    # subtract background image

    data = np.array(beam_image[index][()],dtype=np.float32)

    temp = np.array( np.subtract(data, back_data) )

    # print("back = ",back_data[0])
    # print("data = ",data[0])
    # print("temp = ",temp[0])

    # slice first 50 columns out, as this is where the time stamp is imprinted in the image
    beam_images.append( temp[...,49:] )

# gaussian fit to projections



sum_cols = []
sum_rows = []

for image in beam_images[0:1]:
    print( image[0])


    # print image.shape
    sum_cols = image.sum(axis=0).tolist()
    sum_rows = image.sum(axis=1).tolist()
    print(sum_cols)
    print(sum_rows)



def get_first_second_moments(data):
    """
    This function gets the first and second moments (about the mean) for a 1D list
    :param data:
    :return:
    """
    data_indices = np.arange(len(data))
    normalisation = np.sum(data)  # sum of data
    moment_1 = np.dot(data_indices, data) / normalisation
    moment_2 = np.sqrt(np.dot((data_indices - moment_1) ** 2, data) / normalisation)
    return [moment_1, moment_2]

def normal_dist(x, B, A, mean, sigma):
    '''
    A normal distribution
    :param x: point to calculate value
    :param B: Background (DC offset)
    :param A: Amplitude
    :param mean:
    :param sigma:
    :return: value at x
    '''
    return B + A * exp(-(x-mean)**2/(2*sigma**2))


def fit_normal(data):
    '''
    WHEN FITTING REMEMBER TO CHECK THE TYPE OF THE DATA, LIKELY IT SHOULD BE FLOATS!
    :param data: data to fit
    :return:
    '''
    x = np.array(range(len(data)), dtype=np.float32)
    y = np.array(data, dtype=np.float32)
    mean, sigma = get_first_second_moments(y)
    B = 0
    A = max(y)
    paramater_guess = [B, A, mean, sigma]
    popt,pcov = curve_fit(f=normal_dist, xdata=x, ydata=y, p0 = paramater_guess)
    return popt


def plot_normal_fit(data, popt):
    x = np.array(range(len(data)), dtype=np.float32)
    y = np.array(data, dtype=np.float32)
    plt.plot(x,y,'b+:',label='data')
    plt.plot(x,normal_dist(x,*popt),'ro:',label='fit')
    plt.legend()
    plt.title('Fig. 3 - Fit for Time Constant')
    plt.xlabel('Time (s)')
    plt.ylabel('Voltage (V)')
    plt.show()


fit = fit_normal(sum_cols)
plot_normal_fit(sum_cols,fit)

print len(beam_images)




print np.sum(beam_images) / len(beam_images)

# print back_data
#
#
# print beam_keys
# print back_keys
#
# # this gets the numerical array ( try swopping [()] for .value fro )
# print('beam data ')
# print beam_image[ beam_keys[0] ][()]
# print('back data ')
#
# print back_image[ back_keys[0] ][()]

image_file_data = []


# for key, value in image_file_information.iteritems():
#     print key
#     if key == image_files:
#
#         for item in value:
#             print item





# image_files= []
# for file in os.listdir(working_directory):
#     if file.endswith(".hdf5"):
#         image_files.append(file)
#
# f1 = h5py.File( os.path.join(working_directory, image_files[0]),'r+')


