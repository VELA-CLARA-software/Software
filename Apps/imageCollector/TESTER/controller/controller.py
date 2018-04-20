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


class Controller():

    def __init__(self, view, model):
        '''define model and view'''
        monitor = pg.GraphicsView()
        layout = pg.GraphicsLayout(border=(100, 100, 100))
        monitor.setCentralItem(layout)
        self.view = view
        self.model = model
        self.view.acquire_pushButton.clicked.connect(self.model.acquire)
        self.view.cameraName_comboBox.currentIndexChanged.connect(self.changeCamera)
        self.view.save_pushButton.clicked.connect(lambda: self.model.collectAndSave(self.view.numImages_spinBox.value()))
        self.view.liveStream_pushButton.clicked.connect(lambda: webbrowser.open(self.model.selectedCameraDAQ.streamingIPAddress))
        self.view.getImages_pushButton.clicked.connect(self.openImageDir)
        self.view.analyse_pushButton.clicked.connect(self.model.analyse)
        self.view.resetBackground_pushButton.clicked.connect(self.model.setBkgrnd)
        self.cameraNames = self.model.camerasDAQ.getCameraNames()
        self.view.cameraName_comboBox.addItems(self.cameraNames)
        self.view.useBackground_checkBox.stateChanged.connect(self.setUseBkgrnd)

        '''Update GUI'''
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

        #self.ImageBox = layout.addViewBox(lockAspect=True, colspan=2)
        self.Image = pg.ImageItem(np.random.normal(size=(1280, 1080)))
        self.Image.scale(2,2)
        self.ImageBox= layout.addPlot(lockAspect=True)
        self.view.gridLayout.addWidget(monitor, 0, 2, 11, 3)
        STEPS = np.linspace(0, 1, 4)
        CLRS = ['k', 'r', 'y', 'w']
        a = np.array([pg.colorTuple(pg.Color(c)) for c in CLRS])
        clrmp = pg.ColorMap(STEPS, a)
        lut = clrmp.getLookupTable()
        self.Image.setLookupTable(lut)
        self.ImageBox.setRange(xRange=[0,2560],yRange=[0,2160])
        self.ImageBox.addItem(self.Image)
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
        print 'Set camera to ', str(comboBox.currentText())

    def openImageDir(self):
        if self.view.comboBox.currentText() == 'FAKE_VC':
            QtGui.QFileDialog.getOpenFileNames(self.view.centralwidget, 'Images',
                                              '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\Work\\2017\\VirtualCathode')
        else:
            QtGui.QFileDialog.getOpenFileNames(self.view.centralwidget, 'Images',
                                          '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\Work\\2017\\CurrentCamera')

    def setUseBkgrnd(self):
        if self.view.useBackground_checkBox.isChecked() == True:
            self.model.useBkgrnd(True)
        else:
            self.model.useBkgrnd(False)
    def update(self):
        #print(self.model.selectedCameraIA.IA.x)
        name = self.model.selectedCameraDAQ.name
        if self.model.camerasDAQ.isAcquiring(name):
            self.view.acquire_pushButton.setText('Stop Acquiring')
            self.view.acquire_pushButton.setStyleSheet("background-color: green")
            self.view.save_pushButton.setEnabled(True)
            # Set crosshairs
            x = caget('CLA-VCA-DIA-CAM-01:ANA:X_RBV')
            y = caget('CLA-VCA-DIA-CAM-01:ANA:Y_RBV')
            v1 = (caget('CLA-VCA-DIA-CAM-01:ANA:Y_RBV') -
                  caget('CLA-VCA-DIA-CAM-01:ANA:SigmaY_RBV'))
            v2 = (caget('CLA-VCA-DIA-CAM-01:ANA:Y_RBV') +
                  caget('CLA-VCA-DIA-CAM-01:ANA:SigmaY_RBV'))
            h1 = (caget('CLA-VCA-DIA-CAM-01:ANA:X_RBV') -
                  caget('CLA-VCA-DIA-CAM-01:ANA:SigmaX_RBV'))
            h2 = (caget('CLA-VCA-DIA-CAM-01:ANA:X_RBV') +
                  caget('CLA-VCA-DIA-CAM-01:ANA:SigmaX_RBV'))
            self.vLineMLE.setData(x=[x, x], y=[v1, v2])
            self.hLineMLE.setData(x=[h1, h2], y=[y, y])

            data = caget(self.model.selectedCameraDAQ.pvRoot + 'CAM2:ArrayData')
            #print type(data[0])
            npData = np.array(data).reshape((1080, 1280))
            self.Image.setImage(np.flip(np.transpose(npData), 1))
            #self.Image.setImage(np.flip(np.transpose(frame[:, :, 0]), 1))
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
