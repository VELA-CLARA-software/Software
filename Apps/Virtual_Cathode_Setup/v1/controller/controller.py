from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import Qt
import webbrowser
#import os
import pyqtgraph as pg
#import cv2
from epics import caget
#from epics import caput
import numpy as np
from decimal import *



class Controller():
<<<<<<< HEAD
    view = None
    model = None

    def __init__(self, view, model):
        '''define model and view'''
        Controller.view = view
        Controller.model = model
        self.connect_widgets()
        Controller.view.show()
        print 'Running'

    def handle_collectAndSave_pushButton(self):
        print 'handle_collectAndSave_pushButton'

    def handle_liveStream_pushButton(self):
        print 'handle_liveStream_pushButton'

    def handle_setPosition_pushButton(self):
        print 'handle_setPosition_pushButton'

    def handle_setMask_pushButton(self):
        print 'handle_setMask_pushButton'

    def handle_setIntensity_pushButton(self):
        print 'handle_setIntensity_pushButton'

    def handle_load_pushButton(self):
        print 'handle_load_pushButton'

    def handle_save_pushButton(self):
        print 'handle_save_pushButton'

    def handle_resetMeanSD_pushButton(self):
        print 'handle_resetMeanSD_pushButton'

    def handle_analyse_pushButton(self):
        print 'handle_analyse_pushButton'

    def handle_resetBackground_pushButton(self):
        print 'handle_resetBackground_pushButton'

    def handle_useBackground_checkBox(self):
        print 'handle_useBackground_checkBox'

    def handle_useNPoint_checkBox(self):
        print 'handle_useNPoint_checkBox'

    def handle_acquire_pushButton(self):
        print 'handle_acquire_pushButton'

    def handle_numImages_spinBox(self):
        print 'handle_numImages_spinBox'

    def handle_stepSize_spinBox(self):
        print 'handle_stepSize_spinBox'

    def handle_maskX_spinBox(self):
        print 'handle_maskX_spinBox'

    def handle_maskY_spinBox(self):
        print 'handle_maskY_spinBox'

    def handle_maskXRadius_spinBox(self):
        print 'handle_maskXRadius_spinBox'

    def handle_maskYRadius_spinBox(self):
        print 'handle_maskYRadius_spinBox'

    def handle_feed_back_check(self):
        print 'handle_feed_back_check'

    def handle_spinBox_minLevel(self):
        print 'handle_spinBox_minLevel'

    def handle_spinBox_maxLevel(self):
        print 'handle_spinBox_maxLevel'

    def connect_widgets(self):
        Controller.view.collectAndSave_pushButton.clicked.connect(self.handle_collectAndSave_pushButton)
        Controller.view.liveStream_pushButton.clicked.connect(self.handle_liveStream_pushButton)
        Controller.view.setPosition_pushButton.clicked.connect(self.handle_setPosition_pushButton)
        Controller.view.setInt_pushButton.clicked.connect(
                self.handle_setIntensity_pushButton)
        Controller.view.setMask_pushButton_2.clicked.connect(self.handle_setMask_pushButton)
        Controller.view.setMask_pushButton.clicked.connect(self.handle_setMask_pushButton)
        Controller.view.load_pushButton.clicked.connect(self.handle_load_pushButton)
        Controller.view.save_pushButton.clicked.connect(self.handle_save_pushButton)
        Controller.view.save_pushButton_2.clicked.connect(self.handle_save_pushButton)
        Controller.view.resetMeanSD_pushButton.clicked.connect(self.handle_resetMeanSD_pushButton)
        Controller.view.analyse_pushButton.clicked.connect(self.handle_analyse_pushButton)
        Controller.view.resetBackground_pushButton.clicked.connect(self.handle_resetBackground_pushButton)
        Controller.view.useBackground_checkBox.released.connect(self.handle_useBackground_checkBox)
        Controller.view.feed_back_check.released.connect(self.handle_feed_back_check)
        Controller.view.useNPoint_checkBox.released.connect(self.handle_useNPoint_checkBox)
        Controller.view.acquire_pushButton.clicked.connect(self.handle_acquire_pushButton)
        Controller.view.numImages_spinBox.valueChanged.connect(self.handle_numImages_spinBox)
        Controller.view.stepSize_spinBox.valueChanged.connect(self.handle_stepSize_spinBox)
        Controller.view.maskX_spinBox.valueChanged.connect(self.handle_maskX_spinBox)
        Controller.view.maskY_spinBox.valueChanged.connect(self.handle_maskY_spinBox)
        Controller.view.maskXRadius_spinBox.valueChanged.connect(self.handle_maskXRadius_spinBox)
        Controller.view.maskYRadius_spinBox.valueChanged.connect(self.handle_maskYRadius_spinBox)
        Controller.view.spinBox_minLevel.valueChanged.connect(self.handle_spinBox_minLevel)
        Controller.view.spinBox_maxLevel.valueChanged.connect(self.handle_spinBox_maxLevel)

    # stepSize_spinBox
    # maskX_spinBox
    # maskY_spinBox
    # maskXRadius_spinBox
    # maskYRadius_spinBox

    # acquire_pushButton
    # numImages_spinBox

    # resetMeanSD_pushButton
    # analyse_pushButton
    # resetBackground_pushButton
    # useBackground_checkBox
    # useNPoint_checkBox

    # last_filename
    # liveStream_pushButton
    # spinBox_maxLevel
    # spinBox_minLevel
    # maskX_spinBox_5
    # maskX_spinBox_4
    # int_read_2
    # int_spinBox_2
    # setPosition_pushButton
    # setInt_pushButton
    # setMask_pushButton_2
    # load_pushButton
    # save_pushButton_2
    # sum_val
    # sum_mean
    # sum_sd
    # x_val
    # x_mean
    # x_sd
    # y_val
    # y_mean
    # y_sd
    # sx_val
    # sx_mean
    # sx_sd
    # sy_val
    # sy_mean
    # sy_sd
    # cov_val
    # cov_mean
    # cov_sd
    # resetMeanSD_pushButton
    # analyse_pushButton
    # resetBackground_pushButton
    # useBackground_checkBox
    # useNPoint_checkBox
    # stepSize_spinBox
    # mask_x_read
    # maskX_spinBox
    # mask_y_read
    # maskY_spinBox
    # mas_y_rad
    # maskXRadius_spinBox
    # mask_y_rad
    # maskYRadius_spinBox
    # feed_back_check
    # setMask_pushButton
    # acquire_pushButton
    # numImages_spinBox
    # save_pushButton
    # getImages_pushButton
    # menubar
    # statusbar
    # liveStream_pushButton
    # spinBox_minLevel
    # spinBox_maxLevel
    # analyse_pushButton
    # resetBackground_pushButton
    # useBackground_checkBox
    # useNPoint_checkBox
    # stepSize_spinBox
    # maskX_spinBox
    # maskY_spinBox
    # maskXRadius_spinBox
    # maskYRadius_spinBox
=======

    def __init__(self, view, model):
        '''define model and view'''



>>>>>>> 61a9e380278271c5f352948c5d3699d21e6b48d6












#    def connectMainView(self):
        # collectAndSave_pushButton
        # liveStream_pushButton
        # spinBox_maxLevel
        # spinBox_minLevel
        # maskX_spinBox_5
        # maskX_spinBox_4
        # int_read_2
        # int_spinBox_2
        # setPosition_pushButton
        # setInt_pushButton
        # setMask_pushButton_2
        # load_pushButton
        # save_pushButton_2
        # sum_val
        # sum_mean
        # sum_sd
        # x_val
        # x_mean
        # x_sd
        # y_val
        # y_mean
        # y_sd
        # sx_val
        # sx_mean
        # sx_sd
        # sy_val
        # sy_mean
        # sy_sd
        # cov_val
        # cov_mean
        # cov_sd
        # resetMeanSD_pushButton
        # analyse_pushButton
        # resetBackground_pushButton
        # useBackground_checkBox
        # useNPoint_checkBox
        # stepSize_spinBox
        # mask_x_read
        # maskX_spinBox
        # mask_y_read
        # maskY_spinBox
        # mas_y_rad
        # maskXRadius_spinBox
        # mask_y_rad
        # maskYRadius_spinBox
        # feed_back_check
        # setMask_pushButton
        # acquire_pushButton
        # numImages_spinBox
        # save_pushButton
        # getImages_pushButton
        # menubar
        # statusbar
        # liveStream_pushButton
        # spinBox_minLevel
        # spinBox_maxLevel
        # analyse_pushButton
        # resetBackground_pushButton
        # useBackground_checkBox
        # useNPoint_checkBox
        # stepSize_spinBox
        # maskX_spinBox
        # maskY_spinBox
        # maskXRadius_spinBox
        # maskYRadius_spinBox










    #
    #
    #
    #     monitor = pg.GraphicsView()
    #     layout = pg.GraphicsLayout(border=(100, 100, 100))
    #     monitor.setCentralItem(layout)
    #     self.view = view
    #     self.model = model
    #     self.runFeedback = False
    #     self.counter=0
    #     self.counter=0
    #     self.view.acquire_pushButton.clicked.connect(self.model.acquire)
    #     self.view.cameraName_comboBox.currentIndexChanged.connect(self.changeCamera)
    #     self.view.save_pushButton.clicked.connect(lambda: self.model.collectAndSave(self.view.numImages_spinBox.value()))
    #     self.view.liveStream_pushButton.clicked.connect(lambda: webbrowser.open(self.model.selectedCameraDAQ[0].streamingIPAddress))
    #     self.view.setMask_pushButton.clicked.connect(lambda: self.model.setMask(self.view.maskX_spinBox.value(),
    #                                                                             self.view.maskY_spinBox.value(),
    #                                                                             self.view.maskXRadius_spinBox.value(),
    #                                                                             self.view.maskYRadius_spinBox.value()))
    #     self.view.getImages_pushButton.clicked.connect(self.openImageDir)
    #     self.view.analyse_pushButton.clicked.connect(self.model.analyse)
    #     self.view.resetBackground_pushButton.clicked.connect(self.model.setBkgrnd)
    #     self.cameraNames = self.model.camerasDAQ.getCameraNames()
    #     self.view.cameraName_comboBox.addItems(self.cameraNames)
    #     self.view.useBackground_checkBox.stateChanged.connect(self.setUseBkgrnd)
    #     self.view.checkBox.stateChanged.connect(lambda: self.toggleFeedBack(self.view.checkBox.isChecked()))
    #
    #     self.view.maskX_spinBox.valueChanged.connect(self.changeEllipse)
    #     self.view.maskY_spinBox.valueChanged.connect(self.changeEllipse)
    #     self.view.maskXRadius_spinBox.valueChanged.connect(self.changeEllipse)
    #     self.view.maskYRadius_spinBox.valueChanged.connect(self.changeEllipse)
    #
    #     self.view.stepSize_spinBox.valueChanged.connect(lambda: self.model.setStepSize(self.view.stepSize_spinBox.value()))
    #
    #     '''Update GUI'''
    #     print 'starting GUI update'
    #     self.timer = QtCore.QTimer()
    #     self.timer.timeout.connect(self.update)
    #     self.timer.start(100)
    #
    #     #self.ImageBox = layout.addViewBox(lockAspect=True, colspan=2)
    #     self.Image = pg.ImageItem(np.random.normal(size=(1280, 1080)))
    #     self.Image.scale(2,2)
    #     self.ImageBox= layout.addPlot(lockAspect=True)
    #     self.view.gridLayout.addWidget(monitor, 0, 2, 23, 3)
    #     STEPS = np.linspace(0, 1, 4)
    #     CLRS = ['k', 'r', 'y', 'w']
    #     a = np.array([pg.colorTuple(pg.Color(c)) for c in CLRS])
    #     clrmp = pg.ColorMap(STEPS, a)
    #     lut = clrmp.getLookupTable()
    #     self.Image.setLookupTable(lut)
    #     self.ImageBox.setRange(xRange=[0,2560],yRange=[0,2160])
    #     self.ImageBox.addItem(self.Image)
    #     self.roi = pg.EllipseROI([0, 0], [500, 500], movable=False)
    #     self.ImageBox.addItem(self.roi)
    #     self.vLineMLE = self.ImageBox.plot(x=[1000,1000],y=[900,1100],pen='g')
    #     self.hLineMLE = self.ImageBox.plot(x=[900,1100],y=[1000,1000],pen='g')
    #     #self.ImageBox.removeItem(self.vLineMLE)
    #     #self.ImageBox.removeItem(self.hLineMLE)
    #     # self.ImageView.autoLevels()
    #
    # def changeCamera(self):
    #     print 'changeCamera called'
    #     comboBox = self.view.cameraName_comboBox
    #     self.model.camerasDAQ.setCamera(str(comboBox.currentText()))
    #     self.model.camerasIA.setCamera(str(comboBox.currentText()))
    #
    #
    #     self.view.numImages_spinBox.setMaximum(self.model.selectedCameraDAQ[0].DAQ.maxShots)
    #     if self.model.selectedCameraIA[0].IA.useBkgrnd is True:
    #         self.view.useBackground_checkBox.setChecked(True)
    #     else:
    #         self.view.useBackground_checkBox.setChecked(False)
    #     if self.model.selectedCameraIA[0].IA.useNPoint is True:
    #         self.view.useNPoint_checkBox.setChecked(True)
    #     else:
    #         self.view.useNPoint_checkBox.setChecked(False)
    #
    #     print ('maskX = ', self.model.selectedCameraIA[0].IA.maskX)
    #     print ('maskY = ', self.model.selectedCameraIA[0].IA.maskY)
    #     print ('maskXRad = ', self.model.selectedCameraIA[0].IA.maskXRad)
    #     print ('maskYRad = ', self.model.selectedCameraIA[0].IA.maskYRad)
    #
    #
    #     self.view.maskX_spinBox.setValue(self.model.selectedCameraIA[0].IA.maskX)
    #     self.view.maskY_spinBox.setValue(self.model.selectedCameraIA[0].IA.maskY)
    #     self.view.maskXRadius_spinBox.setValue(self.model.selectedCameraIA[0].IA.maskXRad)
    #     self.view.maskYRadius_spinBox.setValue(self.model.selectedCameraIA[0].IA.maskYRad)
    #     self.changeEllipse()
    #
    #     print 'Set camera to ', str(comboBox.currentText())
    #
    #
    # def openImageDir(self):
    #     QtGui.QFileDialog.getOpenFileNames(self.view.centralwidget, 'Images',
    #                                       '\\\\claraserv3\\CameraImages\\')
    #
    # def setUseBkgrnd(self):
    #     if self.view.useBackground_checkBox.isChecked() == True:
    #         self.model.useBkgrnd(True)
    #     else:
    #         self.model.useBkgrnd(False)
    #
    # def changeEllipse(self):
    #     x = self.view.maskX_spinBox.value()-self.view.maskXRadius_spinBox.value()
    #     y = self.view.maskY_spinBox.value()-self.view.maskYRadius_spinBox.value()
    #     xRad = 2*self.view.maskXRadius_spinBox.value()
    #     yRad = 2*self.view.maskYRadius_spinBox.value()
    #     point = QtCore.QPoint(x,y)
    #     self.roi.setPos(point)
    #     pointRad = QtCore.QPoint(xRad,yRad)
    #     self.roi.setSize(pointRad)
    #
    # def toggleFeedBack(self,use):
    #     print(use)
    #     self.runFeedback = use
    #
    # def update(self):
    #     #print(self.model.selectedCameraIA[0].IA.x)
    #     name = self.model.selectedCameraDAQ[0].name
    #     if self.model.camerasDAQ.isAcquiring(name):
    #         self.view.acquire_pushButton.setText('Stop Acquiring')
    #         self.view.acquire_pushButton.setStyleSheet("background-color: green")
    #         self.view.save_pushButton.setEnabled(True)
    #         # Set crosshairs
    #         x = self.model.selectedCameraIA[0].IA.xPix
    #         y = self.model.selectedCameraIA[0].IA.yPix
    #         sigX = self.model.selectedCameraIA[0].IA.xSigmaPix
    #         sigY = self.model.selectedCameraIA[0].IA.ySigmaPix
    #         v1 = (y - sigY)
    #         v2 = (y + sigY)
    #         h1 = (x - sigX)
    #         h2 = (x + sigX)
    #         self.vLineMLE.setData(x=[x, x], y=[v1, v2])
    #         self.hLineMLE.setData(x=[h1, h2], y=[y, y])
    #         #labels
    #         self.view.apI_label.setText(str(round(self.model.selectedCameraIA[0].IA.averagePixelIntensity,3)))
    #         self.view.xMM_label.setText(str(round(self.model.selectedCameraIA[0].IA.x,3)))
    #         self.view.yMM_label.setText(str(round(self.model.selectedCameraIA[0].IA.y,3)))
    #         self.view.sxMM_label.setText(str(round(self.model.selectedCameraIA[0].IA.sigmaX,3)))
    #         self.view.syMM_label.setText(str(round(self.model.selectedCameraIA[0].IA.sigmaY,3)))
    #         self.view.covXY_label.setText(str(round(self.model.selectedCameraIA[0].IA.covXY,3)))
    #         data = caget(self.model.selectedCameraDAQ[0].pvRoot + 'CAM2:ArrayData')
    #         if data is not None:
    #             if len(data) == 1080*1280:
    #                 if name == "VC":
    #                     npData = np.array(data).reshape((1080, 1280))
    #                 else:
    #                     npData = np.array(data).reshape((1280, 1080))
    #                 self.Image.setImage(np.flip(np.transpose(npData), 1))
    #                 self.Image.setLevels([self.view.spinBox_minLevel.value(),
    #                                       self.view.spinBox_maxLevel.value()], update=True)
    #     else:
    #         self.view.acquire_pushButton.setText('Start Acquiring')
    #         self.view.acquire_pushButton.setStyleSheet("background-color: red")
    #         self.view.save_pushButton.setEnabled(False)
    #
    #     if self.model.selectedCameraDAQ[0].DAQ.captureState == self.model.cap.CAPTURING:
    #         self.view.save_pushButton.setText('Kill')
    #     elif self.model.selectedCameraDAQ[0].DAQ.writeState == self.model.wr.WRITING:
    #         self.view.save_pushButton.setText('Writing to Disk..')
    #     else:
    #         self.view.save_pushButton.setText('Collect and Save')
    #
    #     if self.model.selectedCameraIA[0].IA.analysisState == True:
    #         self.view.analyse_pushButton.setText('Analysing...')
    #     else:
    #         self.view.analyse_pushButton.setText('Analyse')
    #
    #     #This should be activated by a button
    #     self.counter += 1
    #     if self.counter == 10:
    #         self.counter = 0
    #         self.model.feedback(self.runFeedback)
    #         if self.runFeedback is True:
    #             self.view.maskX_spinBox.setValue(self.model.selectedCameraIA[0].IA.maskX)
    #             self.view.maskY_spinBox.setValue(self.model.selectedCameraIA[0].IA.maskY)
    #             self.view.maskXRadius_spinBox.setValue(self.model.selectedCameraIA[0].IA.maskXRad)
    #             self.view.maskYRadius_spinBox.setValue(self.model.selectedCameraIA[0].IA.maskYRad)
