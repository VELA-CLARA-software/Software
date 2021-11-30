import h5py
from glob import glob
import numpy as np
from imageio import imsave
import argparse

parser = argparse.ArgumentParser(description='Convert h5 files to png.')
# parser.add_argument('--bitdepth', default=16, help='Set image bit depth', type=int)
# parser.add_argument('--scale', default='y', help='Set rescaling magnitude', type=str)
parser.add_argument('--extension', default='tiff', help='Set filetype', type=str)
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

def converth5toTIFF(indir='.', outdir='./output/'):
    # if bitdepth <= 8:
    #     numpybitdepth = np.uint8
    #     divisor = 2**(16-bitdepth)
    # elif bitdepth > 16:
    #     numpybitdepth = np.uint32
    #     divisor = 1
    # else:
    #     numpybitdepth = np.uint16
    #     divisor = 1
    # if not args.scale.lower() == 'y':
    #     if RepresentsInt(args.scale):
    #         divisor = int(args.scale)
    #     else:
    #         divisor = 1
    # print divisor, bitdepth, numpybitdepth
    filenames = glob(indir+'/*.hdf5')
    for f in filenames:
        print ('Converting file ', f, 'to', args.extension,'...')
        h5images = readH5File(f)
        for i, hf in enumerate(h5images):
            name = f.replace('.hdf5','.'+args.extension).replace(indir,outdir) if len(h5images) == 1 else f.replace('.hdf5','_'+str(i).zfill(3)+'.'+args.extension).replace(indir,outdir)
            saveImageAsTIFF(name, hf)

def saveImageAsTIFF(filename, imageData):
    imsave(filename, imageData)

def readallcaptures(filename):
    images = []
    i = 1
    with h5py.File(filename, 'r') as f:
        while True:
            try:
                image = list(f['Capture'+str(i).zfill(6)])
                images = images + [image]
                i+=1
            except Exception as e:
                return images

def readH5File(filename):
    images = readallcaptures(filename)
    print('INFO: Found ',len(images),' capture files')
    imageData = [np.flip(np.transpose(np.array(image)), 1) for image in images]
    return imageData

args = parser.parse_args()
converth5toTIFF(args.indir, args.outdir)
