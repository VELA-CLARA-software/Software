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
        self.view.liveStream_pushButton.clicked.connect(lambda: webbrowser.open(self.model.selectedCamera.streamingIPAddress))
        self.view.getImages_pushButton.clicked.connect(self.openImageDir)
        self.cameraNames = self.model.cameras.getCameraNames()
        self.view.cameraName_comboBox.addItems(self.cameraNames)

        '''Update GUI'''
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

        self.ImageBox = layout.addViewBox(lockAspect=True, colspan=2)
        self.Image = pg.ImageItem(np.random.normal(size=(1280, 1080)))

        self.ImageBox.addItem(self.Image)
        self.view.gridLayout.addWidget(monitor, 0, 2, 11, 3)
        STEPS = np.linspace(0, 1, 4)
        CLRS = ['k', 'r', 'y', 'w']
        a = np.array([pg.colorTuple(pg.Color(c)) for c in CLRS])
        clrmp = pg.ColorMap(STEPS, a)
        lut = clrmp.getLookupTable()
        self.Image.setLookupTable(lut)
        # self.ImageView.autoLevels()

    def changeCamera(self):
        comboBox = self.view.cameraName_comboBox
        self.model.cameras.setCamera(str(comboBox.currentText()))
        self.view.numImages_spinBox.setMaximum(self.model.selectedCamera.DAQ.maxShots)
        print 'Set camera to ', str(comboBox.currentText())

    def openImageDir(self):
        if comboBox.currentText() == 'VC':
            QtGui.QFileDialog.getOpenFileNames(self.view.centralwidget, 'Images',
                                              '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\Work\\2017\\VirtualCathode')
        else:
            QtGui.QFileDialog.getOpenFileNames(self.view.centralwidget, 'Images',
                                          '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\Work\\2017\\CurrentCamera')

    def update(self):
        name = self.model.selectedCamera.name
        if self.model.cameras.isAcquiring(name):
            self.view.acquire_pushButton.setText('Stop Acquiring')
            self.view.acquire_pushButton.setStyleSheet("background-color: green")
            self.view.save_pushButton.setEnabled(True)
            #cap = cv2.VideoCapture(self.model.selectedCamera.streamingIPAddress)
            #_, frame = cap.read()
            #frame = np.divide(frame, 0.01)
            data = caget(self.model.selectedCamera.pvRoot + 'CAM2:ArrayData')
            print type(data[0])
            npData = np.array(data).reshape((1080, 1280))
            self.Image.setImage(np.flip(np.transpose(npData), 1))
            #self.Image.setImage(np.flip(np.transpose(frame[:, :, 0]), 1))
            self.Image.setLevels([self.view.spinBox_minLevel.value(),
                                  self.view.spinBox_maxLevel.value()], update=True)
        else:
            self.view.acquire_pushButton.setText('Start Acquiring')
            self.view.acquire_pushButton.setStyleSheet("background-color: red")
            self.view.save_pushButton.setEnabled(False)

        if self.model.selectedCamera.DAQ.captureState == self.model.cap.CAPTURING:
            self.view.save_pushButton.setText('Kill')
        elif self.model.selectedCamera.DAQ.writeState == self.model.wr.WRITING:
            self.view.save_pushButton.setText('Writing to Disk..')
        else:
            self.view.save_pushButton.setText('Collect and Save')
