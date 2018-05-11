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

    def __init__(self, view, model):
        '''define model and view'''
        monitor = pg.GraphicsView()
        layout = pg.GraphicsLayout(border=(100, 100, 100))
        monitor.setCentralItem(layout)
        self.view = view
        self.model = model
        self.runFeedback = False
        self.counter=0
        self.view.acquire_pushButton.clicked.connect(self.model.acquire)
        self.view.cameraName_comboBox.currentIndexChanged.connect(self.changeCamera)
        self.view.save_pushButton.clicked.connect(lambda: self.model.collectAndSave(self.view.numImages_spinBox.value()))
        self.view.liveStream_pushButton.clicked.connect(lambda: webbrowser.open(self.model.selectedCameraDAQ.streamingIPAddress))
        self.view.setMask_pushButton.clicked.connect(lambda: self.model.setMask(self.view.maskX_spinBox.value(),
                                                                                self.view.maskY_spinBox.value(),
                                                                                self.view.maskXRadius_spinBox.value(),
                                                                                self.view.maskYRadius_spinBox.value()))
        self.view.getImages_pushButton.clicked.connect(self.openImageDir)
        self.view.analyse_pushButton.clicked.connect(self.model.analyse)
        self.view.resetBackground_pushButton.clicked.connect(self.model.setBkgrnd)
        self.cameraNames = self.model.camerasDAQ.getCameraNames()
        self.view.cameraName_comboBox.addItems(self.cameraNames)
        self.view.useBackground_checkBox.stateChanged.connect(self.setUseBkgrnd)
        self.view.checkBox.stateChanged.connect(lambda: self.toggleFeedBack(self.view.checkBox.isChecked()))

        self.view.maskX_spinBox.valueChanged.connect(self.changeEllipse)
        self.view.maskY_spinBox.valueChanged.connect(self.changeEllipse)
        self.view.maskXRadius_spinBox.valueChanged.connect(self.changeEllipse)
        self.view.maskYRadius_spinBox.valueChanged.connect(self.changeEllipse)
        
        self.view.stepSize_spinBox.valueChanged.connect(lambda: self.model.setStepSize(self.view.stepSize_spinBox.value()))

        '''Update GUI'''
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

        #self.ImageBox = layout.addViewBox(lockAspect=True, colspan=2)
        self.Image = pg.ImageItem(np.random.normal(size=(1280, 1080)))
        self.Image.scale(2,2)
        self.ImageBox= layout.addPlot(lockAspect=True)
        self.view.gridLayout.addWidget(monitor, 0, 2, 23, 3)
        STEPS = np.linspace(0, 1, 4)
        CLRS = ['k', 'r', 'y', 'w']
        a = np.array([pg.colorTuple(pg.Color(c)) for c in CLRS])
        clrmp = pg.ColorMap(STEPS, a)
        lut = clrmp.getLookupTable()
        self.Image.setLookupTable(lut)
        self.ImageBox.setRange(xRange=[0,2560],yRange=[0,2160])
        self.ImageBox.addItem(self.Image)
        self.roi = pg.EllipseROI([0, 0], [500, 500], movable=False)
        self.ImageBox.addItem(self.roi)
        self.vLineMLE = self.ImageBox.plot(x=[1000,1000],y=[900,1100],pen='g')
        self.hLineMLE = self.ImageBox.plot(x=[900,1100],y=[1000,1000],pen='g')
        #self.ImageBox.removeItem(self.vLineMLE)
        #self.ImageBox.removeItem(self.hLineMLE)
        # self.ImageView.autoLevels()

    def changeCamera(self):
        comboBox = self.view.cameraName_comboBox
        self.model.camerasDAQ.setCamera(str(comboBox.currentText()))
        self.model.camerasIA.setCamera(str(comboBox.currentText()))
        self.view.numImages_spinBox.setMaximum(self.model.selectedCameraDAQ.DAQ.maxShots)
        if self.model.selectedCameraIA.IA.useBkgrnd is True:
            self.view.useBackground_checkBox.setChecked(True)
        else:
            self.view.useBackground_checkBox.setChecked(False)
        if self.model.selectedCameraIA.IA.useNPoint is True:
            self.view.useNPoint_checkBox.setChecked(True)
        else:
            self.view.useNPoint_checkBox.setChecked(False)

        self.view.maskX_spinBox.setValue(self.model.selectedCameraIA.IA.maskX)
        self.view.maskY_spinBox.setValue(self.model.selectedCameraIA.IA.maskY)
        self.view.maskXRadius_spinBox.setValue(self.model.selectedCameraIA.IA.maskXRad)
        self.view.maskYRadius_spinBox.setValue(self.model.selectedCameraIA.IA.maskYRad)
        self.changeEllipse()

        print 'Set camera to ', str(comboBox.currentText())


    def openImageDir(self):
        QtGui.QFileDialog.getOpenFileNames(self.view.centralwidget, 'Images',
                                          '\\\\claraserv3\\CameraImages\\')

    def setUseBkgrnd(self):
        if self.view.useBackground_checkBox.isChecked() == True:
            self.model.useBkgrnd(True)
        else:
            self.model.useBkgrnd(False)

    def changeEllipse(self):
        x = self.view.maskX_spinBox.value()-self.view.maskXRadius_spinBox.value()
        y = self.view.maskY_spinBox.value()-self.view.maskYRadius_spinBox.value()
        xRad = 2*self.view.maskXRadius_spinBox.value()
        yRad = 2*self.view.maskYRadius_spinBox.value()
        point = QtCore.QPoint(x,y)
        self.roi.setPos(point)
        pointRad = QtCore.QPoint(xRad,yRad)
        self.roi.setSize(pointRad)

    def toggleFeedBack(self,use):
        print(use)
        self.runFeedback = use

    def update(self):
        #print(self.model.selectedCameraIA.IA.x)
        name = self.model.selectedCameraDAQ.name
        if self.model.camerasDAQ.isAcquiring(name):
            self.view.acquire_pushButton.setText('Stop Acquiring')
            self.view.acquire_pushButton.setStyleSheet("background-color: green")
            self.view.save_pushButton.setEnabled(True)
            # Set crosshairs
            x = self.model.selectedCameraIA.IA.xPix
            y = self.model.selectedCameraIA.IA.yPix
            sigX = self.model.selectedCameraIA.IA.xSigmaPix
            sigY = self.model.selectedCameraIA.IA.ySigmaPix
            v1 = (y - sigY)
            v2 = (y + sigY)
            h1 = (x - sigX)
            h2 = (x + sigX)
            self.vLineMLE.setData(x=[x, x], y=[v1, v2])
            self.hLineMLE.setData(x=[h1, h2], y=[y, y])

            #labels
            self.view.apI_label.setText(str(round(self.model.selectedCameraIA.IA.averagePixelIntensity,3)))
            self.view.xMM_label.setText(str(round(self.model.selectedCameraIA.IA.x,3)))
            self.view.yMM_label.setText(str(round(self.model.selectedCameraIA.IA.y,3)))
            self.view.sxMM_label.setText(str(round(self.model.selectedCameraIA.IA.sigmaX,3)))
            self.view.syMM_label.setText(str(round(self.model.selectedCameraIA.IA.sigmaY,3)))
            self.view.covXY_label.setText(str(round(self.model.selectedCameraIA.IA.covXY,3)))
            
            data = caget(self.model.selectedCameraDAQ.pvRoot + 'CAM2:ArrayData')
            if name == "VC":
                npData = np.array(data).reshape((1080, 1280))
            else:
                npData = np.array(data).reshape((1280, 1080))
            self.Image.setImage(np.flip(np.transpose(npData), 1))
            self.Image.setLevels([self.view.spinBox_minLevel.value(),
                                  self.view.spinBox_maxLevel.value()], update=True)
        else:
            self.view.acquire_pushButton.setText('Start Acquiring')
            self.view.acquire_pushButton.setStyleSheet("background-color: red")
            self.view.save_pushButton.setEnabled(False)

        if self.model.selectedCameraDAQ.DAQ.captureState == self.model.cap.CAPTURING:
            self.view.save_pushButton.setText('Kill')
        elif self.model.selectedCameraDAQ.DAQ.writeState == self.model.wr.WRITING:
            self.view.save_pushButton.setText('Writing to Disk..')
        else:
            self.view.save_pushButton.setText('Collect and Save')

        if self.model.selectedCameraIA.IA.analysisState == True:
            self.view.analyse_pushButton.setText('Analysing...')
        else:
            self.view.analyse_pushButton.setText('Analyse')
            
        #This should be activated by a button
        self.counter += 1
        if self.counter == 10:
            self.counter = 0
            self.model.feedback(self.runFeedback)
            if self.runFeedback is True:
                self.view.maskX_spinBox.setValue(self.model.selectedCameraIA.IA.maskX)
                self.view.maskY_spinBox.setValue(self.model.selectedCameraIA.IA.maskY)
                self.view.maskXRadius_spinBox.setValue(self.model.selectedCameraIA.IA.maskXRad)
                self.view.maskYRadius_spinBox.setValue(self.model.selectedCameraIA.IA.maskYRad)
