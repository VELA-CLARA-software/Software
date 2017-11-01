from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import Qt
import webbrowser
import os

class Controller():

    def __init__(self, view, model):
        '''define model and view'''
        self.view = view
        self.model = model
        self.view.acquire_pushButton.clicked.connect(self.model.acquire)
        self.view.cameraName_comboBox.currentIndexChanged.connect(self.changeCamera)
        self.view.save_pushButton.clicked.connect(lambda: self.model.collectAndSave(self.view.numImages_spinBox.value()))
        self.view.liveStream_pushButton.clicked.connect(lambda: webbrowser.open(self.model.selectedCamera.streamingIPAddress))
        self.view.getImages_pushButton.clicked.connect(self.openImageDir)
        self.cameraNames = self.model.cameras.getCameraNames()
        self.view.cameraName_comboBox.addItems(self.cameraNames)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(0)

    def changeCamera(self):
        comboBox = self.view.cameraName_comboBox
        self.model.cameras.setCamera(str(comboBox.currentText()))
        self.view.numImages_spinBox.setMaximum(self.model.selectedCamera.DAQ.maxShots) 
        print 'Set camera to ', str(comboBox.currentText())

    def openImageDir(self):
        QtGui.QFileDialog.getOpenFileName(self.view.centralwidget, 'Images',
                                          '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\Work\\2017\\CurrentCamera')
 #

    def update(self):
        name = self.model.selectedCamera.name
        if self.model.cameras.isAcquiring(name):
            self.view.acquire_pushButton.setText('Stop Acquiring')
            self.view.save_pushButton.setEnabled(True)
        else:
            self.view.acquire_pushButton.setText('Start Acquiring')
            self.view.save_pushButton.setEnabled(False)

        if self.model.selectedCamera.DAQ.captureState == self.model.cap.CAPTURING:
            self.view.save_pushButton.setText('Kill')
        elif self.model.selectedCamera.DAQ.writeState == self.model.wr.WRITING:
            self.view.save_pushButton.setText('Writing to Disk..')
        else:
            self.view.save_pushButton.setText('Collect and Save')
