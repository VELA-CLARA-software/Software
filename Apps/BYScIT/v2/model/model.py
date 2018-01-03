from PyQt4 import QtCore
from PIL import Image
import h5py
import numpy as np
import sys
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\stage')
import VELA_CLARA_Camera_IA_Control as ia


class Model(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)
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

    '''def analyseImage(self):
        self.view.pushButton_analyse.setText('Analysing ...')
        image = np.transpose(np.flip(self.imageData, 1))
        image = image.flatten().tolist()
        im = ia.std_vector_double()
        im.extend(image)

        self.offlineAnalysis.loadImage(im, self.imageHeight, self.imageWidth)
        if self.view.checkBox_useBackground.isChecked() is True:
            self.offlineAnalysis.useBackground(True)

            bk = np.transpose(np.flip(self.backgroundData.imageData, 1))
            bk = bk.flatten().tolist()
            b = ia.std_vector_double()
            b.extend(bk)
            self.offlineAnalysis.loadBackgroundImage(b)
        else:
            self.offlineAnalysis.useBackground(False)
        # This is where we will house expert settings
        self.offlineAnalysis.useESMask(True)
        if self.view.checkBox_useCustomMask.isChecked() is True:
            self.offlineAnalysis.setESMask(int(self.customMaskROI.pos()[0]+self.customMaskROI.size()[0]/2),
                                                 int(self.customMaskROI.pos()[1]+self.customMaskROI.size()[0]/2),
                                                 int(self.customMaskROI.size()[0]/2),
                                                 int(self.customMaskROI.size()[1]/2))
        else:
            # make mask span full width of image
            x = int(self.imageWidth / 2)
            y = int(self.imageHeight / 2)
            self.offlineAnalysis.setESMask(x, y, x, y)

        if self.view.checkBox_rollingAverage.isChecked() is True:
            self.offlineAnalysis.useESFilter(True)
            self.offlineAnalysis.setESFilter(int(self.view.lineEdit_rollingAverage.text()))
        else:
            self.offlineAnalysis.useESFilter(False)

        if self.view.checkBox_rSquared.isChecked() is True:
            self.offlineAnalysis.useESRRThreshold(True)
            self.offlineAnalysis.setESRRThreshold(float(self.view.lineEdit_rSquared.text()))
        else:
            self.offlineAnalysis.useESRRThreshold(False)

        if self.view.checkBox_lowestPixValue.isChecked() is True:
            self.offlineAnalysis.useESDirectCut(True)
            self.offlineAnalysis.setESDirectCut(float(self.view.lineEdit_lowestPixelValue.text()))
        else:
            self.offlineAnalysis.useESDirectCut(False)
        self.offlineAnalysis.analyse()
        # Set Results Labels in GUI
        self.view.label_xMLE.setText(str(self.offlineAnalysis.CoIA.xMLE))
        self.view.label_yMLE.setText(str(self.offlineAnalysis.CoIA.yMLE))
        self.view.label_sxMLE.setText(str(self.offlineAnalysis.CoIA.sxMLE))
        self.view.label_syMLE.setText(str(self.offlineAnalysis.CoIA.syMLE))
        self.view.label_cxyMLE.setText(str(self.offlineAnalysis.CoIA.cxyMLE))
        self.view.label_xBVN.setText(str(self.offlineAnalysis.CoIA.xBVN))
        self.view.label_yBVN.setText(str(self.offlineAnalysis.CoIA.yBVN))
        self.view.label_sxBVN.setText(str(self.offlineAnalysis.CoIA.sxBVN))
        self.view.label_syBVN.setText(str(self.offlineAnalysis.CoIA.syBVN))
        self.view.label_cxyBVN.setText(str(self.offlineAnalysis.CoIA.cxyBVN))

        # Set crosshairs
        x = float(self.offlineAnalysis.CoIA.xMLE)
        y = float(self.offlineAnalysis.CoIA.yMLE)
        v1 = (float(self.offlineAnalysis.CoIA.yMLE) -
              float(self.offlineAnalysis.CoIA.syMLE))
        v2 = (float(self.offlineAnalysis.CoIA.yMLE) +
              float(self.offlineAnalysis.CoIA.syMLE))
        h1 = (float(self.offlineAnalysis.CoIA.xMLE) -
              float(self.offlineAnalysis.CoIA.sxMLE))
        h2 = (float(self.offlineAnalysis.CoIA.xMLE) +
              float(self.offlineAnalysis.CoIA.sxMLE))
        #self.vLineMLE.setData(x=[x, x], y=[v1, v2])
        #self.hLineMLE.setData(x=[h1, h2], y=[y, y])

        x = float(self.offlineAnalysis.CoIA.xBVN)
        y = float(self.offlineAnalysis.CoIA.yBVN)
        v1 = (float(self.offlineAnalysis.CoIA.yBVN) -
              float(self.offlineAnalysis.CoIA.syBVN))
        v2 = (float(self.offlineAnalysis.CoIA.yBVN) +
              float(self.offlineAnalysis.CoIA.syBVN))
        h1 = (float(self.offlineAnalysis.CoIA.xBVN) -
              float(self.offlineAnalysis.CoIA.sxBVN))
        h2 = (float(self.offlineAnalysis.CoIA.xBVN) +
              float(self.offlineAnalysis.CoIA.sxBVN))
        #self.vLineBVN.setData(x=[x, x], y=[v1, v2])
        #self.hLineBVN.setData(x=[h1, h2], y=[y, y])
        self.view.pushButton_analyse.setText('Analyse')


	def __del__(self):
		self.wait()

    def run(self):
        self.analyseImage()'''
