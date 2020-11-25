import h5py
from glob import glob
import numpy as np
from imageio import imsave
import argparse

parser = argparse.ArgumentParser(description='Convert h5 files to png.')
parser.add_argument('--bitdepth', default=16, help='Set image bit depth', type=int)
parser.add_argument('--scale', default='y', help='Set rescaling magnitude', type=str)
parser.add_argument('--extension', default='png', help='Set filetype', type=str)
parser.add_argument('indir', metavar='Input_Directory',
                   help='directory containing the input image files')
parser.add_argument('outdir', metavar='Output_Directory',
                   help='directory to contain the output image files')

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def converth5toPNG(bitdepth, indir='.', outdir='./output/'):
    if bitdepth <= 8:
        numpybitdepth = np.uint8
        divisor = 2**(16-bitdepth)
    elif bitdepth > 16:
        numpybitdepth = np.uint32
        divisor = 1
    else:
        numpybitdepth = np.uint16
        divisor = 1
    if not args.scale.lower() == 'y':
        if RepresentsInt(args.scale):
            divisor = int(args.scale)
        else:
            divisor = 1
    # print divisor, bitdepth, numpybitdepth
    filenames = glob(indir+'/*.hdf5')
    for f in filenames:
        print 'Converting file ', f, 'to', args.bitdepth,'bit',args.extension,'...'
        saveImageAsPNG(f.replace('.hdf5','.'+args.extension).replace(indir,outdir), readH5File(f), numpybitdepth, divisor)

def saveImageAsPNG(filename, imageData, bitdepth, divisor):
    imsave(filename, (imageData*divisor).astype(bitdepth))

def readH5File(filename):
    with h5py.File(filename, 'r') as f:
        image = list(f['Capture000001'])
    imageData = np.array(image)
    imageData = np.flip(np.transpose(np.array(imageData)), 1)
    return imageData

args = parser.parse_args()
converth5toPNG(args.bitdepth, args.indir, args.outdir)
