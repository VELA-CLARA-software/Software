from PIL import Image
import h5py
import numpy as np
import sys
import time
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\stage')
import VELA_CLARA_Camera_IA_Control as ia


class Model():
    def __init__(self):
        self.imageData = None
        self.imageHeight = 0
        self.imageWidth = 0
        self.imageAnalysis = ia.init()
        # self.imageAnalysis.setVerbose()
        self.cameras = self.imageAnalysis.offline_CLARA_Camera_IA_Controller()
        self.offlineAnalysis = self.cameras.getOfflineIARef()
        print("Model Initialized")

    def getImage(self, fullName):
        # Get image type by read last part of the image name
        # IF and image is in RGB/RGBA Format
        imageType = fullName.split('.')[-1]
        image = []
        try:
            if imageType == 'png':
                print("Importing PNG...")
                image = Image.open(fullName)
                self.imageData = np.array(image)
                if self.imageData.ndim == 3:# RBG/RGBA condition
                    self.imageData = self.imageData[:, :, 1]
                self.imageData = np.flip(np.transpose(np.array(self.imageData)), 1)
                self.imageHeight = self.imageData.shape[1]
                self.imageWidth = self.imageData.shape[0]
            elif imageType == 'jpg':
                print("Importing JPG...")
                image = Image.open(fullName)
                self.imageData = np.array(image)
                if self.imageData.ndim == 3:# RBG/RGBA condition
                    self.imageData = self.imageData[:, :, 1]
                print(self.imageData.shape)
                self.imageData = np.flip(np.transpose(np.array(self.imageData)), 1)
                self.imageHeight = self.imageData.shape[1]
                self.imageWidth = self.imageData.shape[0]
            elif imageType == 'raw':
                print("Importing RAW...")
                f = open(fullName, "r")
                # specific for us (16 bit, little endian, file type)
                image = np.fromfile(f, dtype=np.uint16)
                image = image.reshape((1040, 1392))
                image = np.flip(np.transpose(np.array(image)), 1)
                self.imageData = image
                self.imageHeight = self.imageData.shape[1]
                self.imageWidth = self.imageData.shape[0]
            elif imageType == 'bin':
                print("Importing binary file...")
                f = open(fullName, "r")
                # specific for us (16 bit, little endian, file type)
                image = np.fromfile(f, dtype=np.uint16)
                # original CLARA camera height and width
                image = image.reshape((2160, 2560))
                image = np.flip(np.transpose(np.array(image)), 1)
                self.imageData = image
                self.imageHeight = self.imageData.shape[1]
                self.imageWidth = self.imageData.shape[0]
            elif imageType == 'h5':
                print("Importing HDF5...")
                f = h5py.File(fullName, 'r')
                # Won't need this when we know what our standard data key is.
                print("Keys: %s" % f.keys())
                a_group_key = list(f.keys())[1]
                # Get the data
                image = list(f[a_group_key])
                self.imageData =  np.array(image)
                self.imageData = np.flip(np.transpose(np.array(self.imageData)), 1)
                self.imageHeight = self.imageData.shape[1]
                self.imageWidth = self.imageData.shape[0]
            elif imageType == 'tif':
                print("Importing tiff...")
                image = Image.open(fullName)
                self.imageData = np.array(image)
                self.imageData = np.flip(np.transpose(np.array(self.imageData)), 1)
                self.imageHeight = self.imageData.shape[1]
                self.imageWidth = self.imageData.shape[0]
            else:
                print('Unrecognised file type!')
        except IOError:
            print "Unable to load image"

