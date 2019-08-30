import h5py
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.io import loadmat
from scipy import exp


# function defintiions here ...
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


def plot_normal_fit(data1, popt1, data2, popt2):
    fig = plt.figure(figsize=(17, 8))
    ax = fig.add_subplot(121)
    ay = fig.add_subplot(122)
    x1 = np.array(range(len(data1)), dtype=np.float32)
    y1 = np.array(data1, dtype=np.float32)

    x2 = np.array(range(len(data2)), dtype=np.float32)
    y2 = np.array(data2, dtype=np.float32)

    ax.plot(x1,y1,'b+:',label='data')
    ax.plot(x1,normal_dist(x1,*popt1),'ro:',label='fit')
    ay.plot(x2,y2,'b+:',label='data')
    ay.plot(x2,normal_dist(x2,*popt2),'ro:',label='fit')
    ax.legend()
    plt.xlabel('X (PIXEL)')
    plt.ylabel('y (PIXEL)')
    plt.show()


def get_image_data_to_fit(beam_fn, back_fn):
    '''
    takes two input files and produces the "average" image from those files
    :param beam_fn: full path to beam image file
    :param back_fn:  fukll path to background image file
    :return: the average beam image MINUS the average background image
    '''

    print("Beam Image file = ", beam_fn)
    print("Background file = ", back_fn)

    beam_image = h5py.File(beam_fn, 'r+')
    back_image = h5py.File(back_fn, 'r+')

    # all images in the hdf5 file have this string in their 'group' (key)
    image_tag = 'Capture'
    # get all keys that have image_tag in them
    beam_keys = [x for x in beam_image.keys() if image_tag in x ]
    back_keys = [x for x in back_image.keys() if image_tag in x ]
    # now we can find an average of all the beam / background images
    # get the first beam image
    print "getting beam images"
    beam_0 = np.array(back_image[back_keys[0]][()],dtype=np.float32)
    for image in beam_keys[1:]:
        temp = np.array(beam_image[image][()],dtype=np.float32)
        beam_0 = np.add(temp, beam_0)
        print beam_0[0]
    print("len(beam_keys)",len(beam_keys))
    beam_0 = np.true_divide(beam_0, len(beam_keys))
    print beam_0[0]

    print "getting back images"
    back_0 = np.array(back_image[back_keys[0]][()],dtype=np.float32)
    for image in back_keys[1:]:
        temp = np.array(back_image[image][()],dtype=np.float32)
        back_0 = np.add(temp, back_0)
        print back_0[0]
    back_0 = np.true_divide(back_0 , len(back_keys))
    print back_0[0]

    beam_image = np.subtract(beam_0,back_0)
    # slice first 50 columns out, as this is where the time stamp is imprinted in the image
    return beam_image  [..., 49:]



# Some inputs

# where are the raw image files we want to analyse?
working_directory='\\\\fed.cclrc.ac.uk\\org\\NLab\\ASTeC\\Projects\\VELA\\Work\\2019\\03\\04' \
                  '\\10pC degaussing, sol -125.0'

# ImageFileInformation contains a list fo which beam image goes with which background image
image_file_info_path = os.path.join(working_directory, 'ImageFileInformation.mat')


# get the image file information (beam images and background)
image_file_information = loadmat(image_file_info_path)
# The image files have this key
image_files = 'Image_and_background_filenames_at_observation_point'

# there can be multiple beam images and multiple background images
# we sum all teh images, find an average, then subtract the background from the beam


# filenames for the data to read
beam_fn = os.path.join(working_directory, str(image_file_information[image_files][0,0][0]) )
back_fn = os.path.join(working_directory, str(image_file_information[image_files][0,1][0]) )


image_to_fit = get_image_data_to_fit( beam_fn, back_fn)
print image_to_fit[0]

# Now we fit a normal distribution to the projections of the image_to_fit
# we call the projections sum_rows and sum_cols to make our axes obvious

sum_cols = image_to_fit.sum(axis=0).tolist()
sum_rows = image_to_fit.sum(axis=1).tolist()


fit_cols = fit_normal(sum_cols)
fit_rows = fit_normal(sum_rows)

plot_normal_fit(sum_cols,fit_cols, sum_rows,fit_rows)


# now we can crop the data about the centre of each gaussian

final_image_size = 1200 # pixels


raw_input()
