import sys,os
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Stage')
os.environ['PATH']=os.environ['PATH']+';\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\stage\\root_v5.34.34\\bin\\'
#import VELA_CLARA_Camera_DAQ_Control as daq
import os
from epics import caget, caput
#os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
#os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255"
#import enum_ext

#import members_as_pyobjects_test
import VELA_CLARA_Camera_DAQ_Control as daq
import VELA_CLARA_Camera_IA_Control as ia
import VELA_CLARA_PILaser_Control as pil
import VELA_CLARA_Shutter_Control as shut
import numpy as np
import data


class model():
    # initDAQ = daq.init()
    initIA = ia.init()
    initpil = pil.init()
    # initDAQ.setVerbose()
    initIA.setVerbose()
    initpil.setVerbose()
    pil = initpil.physical_PILaser_Controller()

    cam_ia = initIA.physical_CLARA_Camera_IA_Controller()

    data = data.data()

    initShut = shut.init()
    shutter = initShut.physical_PIL_Shutter_Controller()

    def __init__(self):
        # self.comment = 'Hello World!!    and the Llamas in the Universe :)'
        # self.cap = daq.CAPTURE_STATE
        # self.wr = daq.WRITE_STATE
        # self.camerasDAQ = self.initDAQ.physical_CLARA_Camera_DAQ_Controller()
        # self.camerasIA = self.initIA.physical_CLARA_Camera_IA_Controller()
        # self.selectedCameraDAQ = [self.camerasDAQ.getSelectedDAQRef()]
        # self.selectedCameraIA = [self.camerasIA.getSelectedIARef()]
        print("model Initialized")

        self.vc_data = [model.pil.getVCDataObjConstRef()]
        self.vc_IA = [model.cam_ia.getCamIAObjConstRef('VC')]
        self.shutter = [model.shutter.getShutterObjConstRef('SHUT01')]

    def resetRunningValues(self):
        model.pil.clearRunningValues()


    def update_values(self):
        model.data.values[data.x_val] = self.vc_data[0].x
        model.data.values[data.y_val] = self.vc_data[0].y
        model.data.values[data.sx_val] = self.vc_data[0].sig_x
        model.data.values[data.sy_val] = self.vc_data[0].sig_y
        #model.data.values[i_val] = self.vc_data[0].x
        model.data.values[data.cov_val] = self.vc_data[0].sig_xy
        model.data.values[data.x_mean] = self.vc_data[0].x_mean
        model.data.values[data.y_mean] = self.vc_data[0].y_mean
        model.data.values[data.sx_mean] = self.vc_data[0].sig_x_mean
        model.data.values[data.sy_mean] = self.vc_data[0].sig_y_mean
        #model.data.values[i_mean] = self.vc_data[0].
        model.data.values[data.cov_mean] = self.vc_data[0].sig_xy_mean
        model.data.values[data.x_sd] = self.vc_data[0].x_sd
        model.data.values[data.y_sd] = self.vc_data[0].y_sd
        model.data.values[data.sx_sd] = self.vc_data[0].sig_x_sd
        model.data.values[data.sy_sd] = self.vc_data[0].sig_y_sd
        #model.data.values[i_sd] = self.vc_data[0].
        model.data.values[data.cov_sd] = self.vc_data[0].sig_xy_sd

        model.data.values[data.image]  = self.get_fast_image()

        model.data.values[data.mask_x_rbv] = self.vc_IA[0].IA.maskX
        model.data.values[data.mask_y_rbv] = self.vc_IA[0].IA.maskY
        model.data.values[data.mask_x_rad_rbv] = self.vc_IA[0].IA.maskXRad
        model.data.values[data.mask_y_rad_rbv] = self.vc_IA[0].IA.maskYRad

        if self.shutter[0].state == shut.SHUTTER_STATE.OPEN:
            model.data.values[data.shutter_open] = True
        else:
            model.data.values[data.shutter_open] = False

    def get_fast_image(self):
        data = model.pil.getFastImage()
        npData = np.array(data).reshape((1080, 1280))
        return np.flip(np.transpose(npData), 1)

    def toggle_shutter(self):
        if self.shutter[0].state == shut.SHUTTER_STATE.CLOSED:
            model.shutter.open('SHUT01')
        elif self.shutter[0].state == shut.SHUTTER_STATE.OPEN:
            model.shutter.close('SHUT01')

    def setStepSize(self, stepSize):
        print(stepSize)
        self.camerasIA.setStepSize(stepSize)

    def setMask(self, x, y, xRad, yRad):
        print 'python setMask called'
        self.camerasIA.setMask(x, y, xRad, yRad)

    def useBkgrnd(self, use):
        print(use)
        self.camerasIA.useBackground(use)

    def useNPoint(self, use):
        print(use)
        self.camerasIA.useNPoint(use)

    def setBkgrnd(self, step):
        print("Setting a new background...")
        self.camerasIA.setBackground()

    def analyse(self):
        if self.vc_IA[0].IA.analysisState == 0:
            mdoel.cam_ia.startAnalysis()
            model.data.values[data.is_analysing] = True
        elif self.vc_IA[0].IA.analysisState == 1:
            mdoel.cam_ia.stopAnalysis()
            model.data.values[data.is_analysing] = False


    def acquire(self):
        if self.camerasDAQ.isNotAcquiring('VC'):
            self.camerasDAQ.startAcquiring()
            model.data.values[data.is_acquiring] = True
        elif self.camerasDAQ.isAcquiring('VC'):
            self.camerasDAQ.stopAcquiring()
            model.data.values[data.is_acquiring] = False

    def collectAndSave(self, numberOfImages):
        if self.camerasDAQ.isAcquiring(self.selectedCameraDAQ[0].name):
            self.camerasDAQ.collectAndSave(numberOfImages)
            # self.camerasDAQ.collectAndSaveJPG()
        elif self.selectedCameraDAQ[0].DAQ.captureState == self.cap.CAPTURING:
            self.camerasDAQ.killCollectAndSave()
        # self.camerasDAQ.killCollectAndSaveJPG()

    def feedback(self, use):
        if use is True:
            height = 2160  # self.selectedCameraIA.IA.imageHeight
            width = 2560  # self.selectedCameraIA.IA.imageWidth
            x = self.vc_IA[0].IA.xPix
            y = self.vc_IA[0].IA.yPix
            sX = self.vc_IA[0].IA.xSigmaPix
            sY = self.vc_IA[0].IA.ySigmaPix
            if x - 5 * sX > 0 and x + 5 * sX < width and y - 5 * sY > 0 and y + 5 * sY < height:
                # print(x-sX)
                # print(y-sY)
                self.setMask(int(x), int(y), int(5 * sX), int(5 * sY))



            #
    # def setStepSize(self, stepSize):
    #     print(stepSize)
    #     self.camerasIA.setStepSize(stepSize)
    #
    # def setMask(self, x,y, xRad, yRad):
    #     print 'python setMask called'
    #     self.camerasIA.setMask(x,y,xRad,yRad)
    #
    # def useBkgrnd(self, use):
    #     print(use)
    #     self.camerasIA.useBackground(use)
    #
    # def useNPoint(self, use):
    #     print(use)
    #     self.camerasIA.useNPoint(use)
    #
    # def setBkgrnd(self, step):
    #     print("Setting a new background...")
    #     self.camerasIA.setBackground()
    #
    # def analyse(self):
    #     if self.selectedCameraIA[0].IA.analysisState== 0:
    #         self.camerasIA.startAnalysis()
    #     elif self.selectedCameraIA[0].IA.analysisState == 1:
    #         self.camerasIA.stopAnalysis()
    #
    # def acquire(self):
    #     if self.camerasDAQ.isNotAcquiring(self.selectedCameraDAQ[0].name):
    #         self.camerasDAQ.startAcquiring()
    #     elif self.camerasDAQ.isAcquiring(self.selectedCameraDAQ[0].name):
    #         self.camerasDAQ.stopAcquiring()
    #
    # def collectAndSave(self, numberOfImages):
    #     if self.camerasDAQ.isAcquiring(self.selectedCameraDAQ[0].name):
    #         self.camerasDAQ.collectAndSave(numberOfImages)
    #         #self.camerasDAQ.collectAndSaveJPG()
    #     elif self.selectedCameraDAQ[0].DAQ.captureState == self.cap.CAPTURING:
    #         self.camerasDAQ.killCollectAndSave()
    #        # self.camerasDAQ.killCollectAndSaveJPG()
    #
    # def feedback(self,use):
    #     if use is True:
    #         height = 2160#self.selectedCameraIA.IA.imageHeight
    #         width = 2560#self.selectedCameraIA.IA.imageWidth
    #         x = self.selectedCameraIA[0].IA.xPix
    #         y = self.selectedCameraIA[0].IA.yPix
    #         sX = self.selectedCameraIA[0].IA.xSigmaPix
    #         sY = self.selectedCameraIA[0].IA.ySigmaPix
    #         if x-5*sX > 0 and x+5*sX < width and y-5*sY > 0 and y+5*sY < height:
    #             #print(x-sX)
    #             #print(y-sY)
    #             self.setMask(int(x),int(y),int(5*sX),int(5*sY))
    # def __init__(self):
    #     self.comment = 'Hello World!!    and the Llamas in the Universe :)'
    #     self.cap = daq.CAPTURE_STATE
    #     self.wr = daq.WRITE_STATE
    #     self.initDAQ = daq.init()
    #     self.initIA = ia.init()
    #     self.initDAQ.setVerbose()
    #     self.initIA.setVerbose()
    #     self.camerasDAQ = self.initDAQ.physical_CLARA_Camera_DAQ_Controller()
    #     self.camerasIA = self.initIA.physical_CLARA_Camera_IA_Controller()
    #     self.selectedCameraDAQ = [self.camerasDAQ.getSelectedDAQRef()]
    #     self.selectedCameraIA = [self.camerasIA.getSelectedIARef()]
    #     print("model Initialized")
    #
    # def setStepSize(self, stepSize):
    #     print(stepSize)
    #     self.camerasIA.setStepSize(stepSize)
    #
    # def setMask(self, x,y, xRad, yRad):
    #     print 'python setMask called'
    #     self.camerasIA.setMask(x,y,xRad,yRad)
    #
    # def useBkgrnd(self, use):
    #     print(use)
    #     self.camerasIA.useBackground(use)
    #
    # def useNPoint(self, use):
    #     print(use)
    #     self.camerasIA.useNPoint(use)
    #
    # def setBkgrnd(self, step):
    #     print("Setting a new background...")
    #     self.camerasIA.setBackground()
    #
    # def analyse(self):
    #     if self.selectedCameraIA[0].IA.analysisState== 0:
    #         self.camerasIA.startAnalysis()
    #     elif self.selectedCameraIA[0].IA.analysisState == 1:
    #         self.camerasIA.stopAnalysis()
    #
    # def acquire(self):
    #     if self.camerasDAQ.isNotAcquiring(self.selectedCameraDAQ[0].name):
    #         self.camerasDAQ.startAcquiring()
    #     elif self.camerasDAQ.isAcquiring(self.selectedCameraDAQ[0].name):
    #         self.camerasDAQ.stopAcquiring()
    #
    # def collectAndSave(self, numberOfImages):
    #     if self.camerasDAQ.isAcquiring(self.selectedCameraDAQ[0].name):
    #         self.camerasDAQ.collectAndSave(numberOfImages)
    #         #self.camerasDAQ.collectAndSaveJPG()
    #     elif self.selectedCameraDAQ[0].DAQ.captureState == self.cap.CAPTURING:
    #         self.camerasDAQ.killCollectAndSave()
    #        # self.camerasDAQ.killCollectAndSaveJPG()
    #
    # def feedback(self,use):
    #     if use is True:
    #         height = 2160#self.selectedCameraIA.IA.imageHeight
    #         width = 2560#self.selectedCameraIA.IA.imageWidth
    #         x = self.selectedCameraIA[0].IA.xPix
    #         y = self.selectedCameraIA[0].IA.yPix
    #         sX = self.selectedCameraIA[0].IA.xSigmaPix
    #         sY = self.selectedCameraIA[0].IA.ySigmaPix
    #         if x-5*sX > 0 and x+5*sX < width and y-5*sY > 0 and y+5*sY < height:
    #             #print(x-sX)
    #             #print(y-sY)
    #             self.setMask(int(x),int(y),int(5*sX),int(5*sY))
