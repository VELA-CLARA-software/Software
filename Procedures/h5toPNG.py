import h5py
from glob import glob
import numpy as np
from scipy.misc import imsave

import argparse

parser = argparse.ArgumentParser(description='Convert h5 files to png.')
parser.add_argument('indir', metavar='Input_Directory',
                   help='directory containing the input image files')
parser.add_argument('outdir', metavar='Output_Directory',
                   help='directory containing the output image files')

def converth5toPNG(indir='.', outdir='./output/'):
    filenames = glob(indir+'/*.hdf5')
    for f in filenames:
        print 'Converting file ', f, ' to PNG...'
        saveImageAsPNG(f.replace('.hdf5','.png').replace(indir,outdir), readH5File(f))

def saveImageAsPNG(filename, imageData):
    imsave(filename, imageData)

def readH5File(filename):
    with h5py.File(filename, 'r') as f:
        image = list(f['Capture000001'])
    imageData = np.array(image)
    imageData = np.flip(np.transpose(np.array(imageData)), 1)
    return imageData

args = parser.parse_args()
converth5toPNG(args.indir, args.outdir)
