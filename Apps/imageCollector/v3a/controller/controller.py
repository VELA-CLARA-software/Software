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

IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1280
IMAGE_DIMS = (IMAGE_WIDTH, IMAGE_HEIGHT)

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
        # self.histogram = pg.PlotWidget()
        # self.view.gridLayout.addWidget(self.histogram, 21, 0, 1, 1)
        self.view.acquire_pushButton.clicked.connect(self.model.acquire)
        self.view.cameraName_comboBox.currentRowChanged.connect(self.changeCamera)
        self.view.save_pushButton.clicked.connect(lambda: self.model.collectAndSave(self.view.numImages_spinBox.value()))
        self.view.liveStream_pushButton.clicked.connect(lambda: webbrowser.open(self.model.selectedCameraDAQ[0].streamingIPAddress))
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
        print 'starting GUI update'
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

        #self.ImageBox = layout.addViewBox(lockAspect=True, colspan=2)
        self.Image = pg.ImageItem(np.random.normal(size=(IMAGE_HEIGHT, IMAGE_WIDTH)))
        self.Image.scale(2,2)
        self.ImageBox = layout.addPlot()
        self.view.gridLayout.addWidget(monitor, 1, 2, 20, 3)  # row, col, rowspan, colspan
        # build colour map: black-red-yellow-white
        STEPS = np.linspace(0, 1, 4)
        CLRS = ['k', 'r', 'y', 'w']
        a = np.array([pg.colorTuple(pg.Color(c)) for c in CLRS])
        clrmp = pg.ColorMap(STEPS, a)
        # lut = clrmp.getLookupTable()
        # self.Image.setLookupTable(lut)
        self.ImageBox.setRange(xRange=[0,IMAGE_HEIGHT*2],yRange=[0,IMAGE_WIDTH*2])
        self.ImageBox.addItem(self.Image)
        self.roi = pg.EllipseROI([0, 0], [500, 500], movable=False)
        self.ImageBox.addItem(self.roi)
        self.ImageBox.setAspectLocked(True)
        self.vLineMLE = self.ImageBox.plot(x=[1000,1000],y=[900,1100],pen='g')
        self.hLineMLE = self.ImageBox.plot(x=[900,1100],y=[1000,1000],pen='g')
        histogram = pg.HistogramLUTItem(self.Image)
        grad = histogram.gradient
        # Show the colour map on the histogram, and make the outermost ticks draggable
        grad.setColorMap(clrmp)
        grad.getTick(0).sigMoving.connect(self.tickMoving)
        grad.getTick(1).movable = False
        grad.getTick(2).movable = False
        grad.getTick(3).sigMoving.connect(self.tickMoving)
        layout.addItem(histogram)
        
        #self.ImageBox.removeItem(self.vLineMLE)
        #self.ImageBox.removeItem(self.hLineMLE)
        # self.ImageView.autoLevels()

    def tickMoving(self, tick):
        """We're moving one of the outermost histogram tick marks - adjust the other two to the correct position."""
        ref = tick.view  # weakref to the view
        grad = ref()
        min_val, max_val = grad.tickValue(0), grad.tickValue(3)  # they are returned in order
        for i in (1, 2):
            val = i * (max_val - min_val) / 3 + min_val
            grad.setTickValue(i, val)
        
    def changeCamera(self):
        print 'changeCamera called'
        comboBox = self.view.cameraName_comboBox
        camera_name = str(comboBox.currentItem().text())
        self.view.title_label.setText('<h1>{}</h1>'.format(camera_name))
        print 'Setting camera to', camera_name
        self.model.camerasDAQ.setCamera(camera_name)
        self.model.camerasIA.setCamera(camera_name)


        self.view.numImages_spinBox.setMaximum(self.model.selectedCameraDAQ[0].DAQ.maxShots)
        if self.model.selectedCameraIA[0].IA.useBkgrnd is True:
            self.view.useBackground_checkBox.setChecked(True)
        else:
            self.view.useBackground_checkBox.setChecked(False)
        if self.model.selectedCameraIA[0].IA.useNPoint is True:
            self.view.useNPoint_checkBox.setChecked(True)
        else:
            self.view.useNPoint_checkBox.setChecked(False)

        print ('maskX = ', self.model.selectedCameraIA[0].IA.maskX)
        print ('maskY = ', self.model.selectedCameraIA[0].IA.maskY)
        print ('maskXRad = ', self.model.selectedCameraIA[0].IA.maskXRad)
        print ('maskYRad = ', self.model.selectedCameraIA[0].IA.maskYRad)


        self.view.maskX_spinBox.setValue(self.model.selectedCameraIA[0].IA.maskX)
        self.view.maskY_spinBox.setValue(self.model.selectedCameraIA[0].IA.maskY)
        self.view.maskXRadius_spinBox.setValue(self.model.selectedCameraIA[0].IA.maskXRad)
        self.view.maskYRadius_spinBox.setValue(self.model.selectedCameraIA[0].IA.maskYRad)
        self.changeEllipse()

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
        #print(self.model.selectedCameraIA[0].IA.x)
        name = self.model.selectedCameraDAQ[0].name
        if self.model.camerasDAQ.isAcquiring(name):
            self.view.acquire_pushButton.setText('Stop Acquiring')
            self.view.acquire_pushButton.setStyleSheet("background-color: green")
            self.view.save_pushButton.setEnabled(True)
            # Set crosshairs
            x = self.model.selectedCameraIA[0].IA.xPix
            y = self.model.selectedCameraIA[0].IA.yPix
            sigX = self.model.selectedCameraIA[0].IA.xSigmaPix
            sigY = self.model.selectedCameraIA[0].IA.ySigmaPix
            v1 = (y - sigY)
            v2 = (y + sigY)
            h1 = (x - sigX)
            h2 = (x + sigX)
            self.vLineMLE.setData(x=[x, x], y=[v1, v2])
            self.hLineMLE.setData(x=[h1, h2], y=[y, y])
            #labels
            self.view.apI_label.setText(str(round(self.model.selectedCameraIA[0].IA.averagePixelIntensity,3)))
            self.view.xMM_label.setText(str(round(self.model.selectedCameraIA[0].IA.x,3)))
            self.view.yMM_label.setText(str(round(self.model.selectedCameraIA[0].IA.y,3)))
            self.view.sxMM_label.setText(str(round(self.model.selectedCameraIA[0].IA.sigmaX,3)))
            self.view.syMM_label.setText(str(round(self.model.selectedCameraIA[0].IA.sigmaY,3)))
            self.view.covXY_label.setText(str(round(self.model.selectedCameraIA[0].IA.covXY,3)))
            data = caget(self.model.selectedCameraDAQ[0].pvRoot + 'CAM2:ArrayData')
            if data is not None and len(data) == IMAGE_HEIGHT * IMAGE_WIDTH:
                dims = (IMAGE_WIDTH, IMAGE_HEIGHT) if name == 'VC' else (IMAGE_HEIGHT, IMAGE_WIDTH)
                npData = np.array(data).reshape(dims)
                self.Image.setImage(np.flip(np.transpose(npData), 1))
                # self.Image.setLevels([self.view.spinBox_minLevel.value(),
                                      # self.view.spinBox_maxLevel.value()], update=True)
        else:
            self.view.acquire_pushButton.setText('Start Acquiring')
            self.view.acquire_pushButton.setStyleSheet("background-color: red")
            self.view.save_pushButton.setEnabled(False)

        if self.model.selectedCameraDAQ[0].DAQ.captureState == self.model.cap.CAPTURING:
            self.view.save_pushButton.setText('Kill')
        elif self.model.selectedCameraDAQ[0].DAQ.writeState == self.model.wr.WRITING:
            self.view.save_pushButton.setText('Writing to Disk..')
        else:
            self.view.save_pushButton.setText('Collect and Save')

        if self.model.selectedCameraIA[0].IA.analysisState == True:
            self.view.analyse_pushButton.setText('Analysing...')
        else:
            self.view.analyse_pushButton.setText('Analyse')
            
        #This should be activated by a button
        self.counter += 1
        if self.counter == 10:
            self.counter = 0
            self.model.feedback(self.runFeedback)
            if self.runFeedback is True:
                self.view.maskX_spinBox.setValue(self.model.selectedCameraIA[0].IA.maskX)
                self.view.maskY_spinBox.setValue(self.model.selectedCameraIA[0].IA.maskY)
                self.view.maskXRadius_spinBox.setValue(self.model.selectedCameraIA[0].IA.maskXRad)
                self.view.maskYRadius_spinBox.setValue(self.model.selectedCameraIA[0].IA.maskYRad)