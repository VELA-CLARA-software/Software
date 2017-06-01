# uncompyle6 version 2.10.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.10 (default, May 23 2015, 09:40:32) [MSC v.1500 32 bit (Intel)]
# Embedded file name: D:\VELA-CLARA_software\Software\matlabImageViewer\view\matlabImageViewUI.py
# Compiled at: 2017-06-01 15:50:28
from PyQt4 import QtCore, QtGui, Qt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import numpy
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:

    def _fromUtf8(s):
        return s


try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)


except AttributeError:

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class matlabImageViewUI(object):

    def setupUi(self, mainWindow):
        mainWindow.resize(1010, 610)
        mainWindow.setObjectName(_fromUtf8('Matlab Image Viewer'))
        self.mainWidget = QtGui.QWidget(mainWindow)
        self.mainWidget.resize(1000, 600)
        self.mainWidget.setObjectName(_fromUtf8('mainWidget'))
        self.mainBox = QtGui.QHBoxLayout(self.mainWidget)
        self.configVBox = QtGui.QVBoxLayout()
        self.plotVBox = QtGui.QVBoxLayout()
        self.setDirectoryLabel = QtGui.QLabel()
        self.setDirectoryLabel.setObjectName(_fromUtf8('setDirectoryLabel'))
        self.getDirectoryLayout = QtGui.QHBoxLayout()
        self.setLayout(self.getDirectoryLayout)
        self.getDirectoryLineEdit = QtGui.QLineEdit(self)
        self.getDirectoryLayout.addWidget(self.getDirectoryLineEdit)
        self.getDirectoryButton = QtGui.QPushButton('...', self)
        self.getDirectoryLayout.addWidget(self.getDirectoryButton)
        self.loadFilesButton = QtGui.QPushButton('Load files', self)
        self.loadFilesButton.setObjectName(_fromUtf8('loadFilesButton'))
        self.loadFilesButton.setMaximumSize(QtCore.QSize(100, 40))
        self.convertFilesButton = QtGui.QPushButton('Convert to ASCII?', self)
        self.convertFilesButton.setObjectName(_fromUtf8('convertFilesButton'))
        self.convertFilesButton.setMaximumSize(QtCore.QSize(100, 40))
        self.allFilesLabel = QtGui.QLabel()
        self.allFilesLabel.setObjectName(_fromUtf8('allFilesLabel'))
        self.allFilesComboBox = QtGui.QComboBox()
        self.allFilesComboBox.setObjectName(_fromUtf8('allFilesComboBox'))
        self.keysLabel = QtGui.QLabel()
        self.keysLabel.setObjectName(_fromUtf8('keysLabel'))
        self.keysComboBox = QtGui.QComboBox()
        self.keysComboBox.setObjectName(_fromUtf8('keysComboBox'))
        self.viewKeysText = QtGui.QPlainTextEdit()
        self.viewKeysText.setObjectName(_fromUtf8('viewKeysText'))
        self.imageSizeLabel = QtGui.QLabel()
        self.imageSizeLabel.setObjectName(_fromUtf8('imageSizeLabel'))
        self.imageDataHBox = QtGui.QHBoxLayout()
        self.imageSizeY = QtGui.QPlainTextEdit()
        self.imageSizeY.setObjectName(_fromUtf8('imageSizeY'))
        self.imageSizeX = QtGui.QPlainTextEdit()
        self.imageSizeX.setObjectName(_fromUtf8('imageSizeX'))
        self.imageSizeSpacer = QtGui.QLabel()
        self.imageSizeSpacer.setObjectName(_fromUtf8('imageSizeSpacer'))
        self.imageNumShotsSpacer = QtGui.QLabel()
        self.imageNumShotsSpacer.setObjectName(_fromUtf8('imageNumShotsSpacer'))
        self.imageNumShots = QtGui.QPlainTextEdit()
        self.imageNumShots.setObjectName(_fromUtf8('imageNumShots'))
        self.imageNumShotsLabel = QtGui.QLabel()
        self.imageNumShotsLabel.setObjectName(_fromUtf8('imageNumShotsLabel'))
        self.imageSizeY.setMaximumSize(QtCore.QSize(50, 30))
        self.imageSizeX.setMaximumSize(QtCore.QSize(50, 30))
        self.imageNumShots.setMaximumSize(QtCore.QSize(50, 30))
        self.imageDataHBox.addWidget(self.imageSizeY)
        self.imageDataHBox.addWidget(self.imageSizeSpacer)
        self.imageDataHBox.addWidget(self.imageSizeX)
        self.imageDataHBox.addWidget(self.imageNumShots)
        self.imageDataHBox.addWidget(self.imageNumShotsLabel)
        self.configVBox.addWidget(self.setDirectoryLabel)
        self.configVBox.addLayout(self.getDirectoryLayout)
        self.configVBox.addWidget(self.loadFilesButton)
        self.configVBox.addWidget(self.convertFilesButton)
        self.configVBox.addWidget(self.allFilesLabel)
        self.configVBox.addWidget(self.allFilesComboBox)
        self.configVBox.addWidget(self.keysLabel)
        self.configVBox.addWidget(self.keysComboBox)
        self.configVBox.addWidget(self.viewKeysText)
        self.configVBox.addStretch()
        self.makePlotsButton = QtGui.QPushButton('Make plots', self)
        self.plotWidget = self.addPlotPanel()
        self.fileSlider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.fileSlider.setObjectName(_fromUtf8('fileSlider'))
        self.fileSlider.tickPosition = QtGui.QSlider.TicksBelow
        self.fileSlider.setMinimum(0)
        self.fileSlider.setMaximum(19)
        self.fileSlider.setTickInterval(1)
        self.fileSlider.setSingleStep(1)
        self.fileSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        self.clearPlotsButton = QtGui.QPushButton('Clear plots', self)
        self.plotVBox.addWidget(self.makePlotsButton)
        self.plotVBox.addLayout(self.layoutVertical)
        self.plotVBox.addWidget(self.fileSlider)
        self.plotVBox.addWidget(self.clearPlotsButton)
        self.plotVBox.addStretch()
        self.mainBox.addLayout(self.configVBox)
        self.mainBox.addLayout(self.plotVBox)
        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(_translate('mainWindow', 'Matlab File Viewer', None))
        self.setDirectoryLabel.setText(_translate('mainWindow', 'Set Directory', None))
        self.loadFilesButton.setText(_translate('mainWindow', 'Load .mat files', None))
        self.allFilesLabel.setText(_translate('mainWindow', 'Files in folder', None))
        self.keysLabel.setText(_translate('mainWindow', 'Keys in file', None))
        return

    def addPlotPanel(self):
        self.figure = plt.figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.axis = self.figure.add_subplot(111)
        self.layoutVertical = QtGui.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.canvas)
        self.canvas.setParent(self.mainWidget)
        self.canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.canvas.setFocus()
        return self.figure

    def makePlots(self, datafile, datastruct, imagedata, arrayshape, shotnum, plotfigure):
        self.datafile = datafile
        self.datastruct = datastruct
        self.imagedata = imagedata
        self.arrayshape = arrayshape
        self.shotnum = shotnum
        self.data = self.datafile[self.datastruct][self.imagedata]
        self.newdata = numpy.reshape(self.data, self.arrayshape)
        self.plotfigure = plotfigure
        self.plotfigure.canvas.flush_events()
        self.ax = self.plotfigure.add_subplot(111)
        self.ax.set_title('shot number ' + str(self.shotnum))
        self.ax.imshow(numpy.transpose(numpy.transpose(self.newdata)[self.shotnum]))
        self.ax.set_aspect('equal')
        self.cax = self.plotfigure.add_axes([0.12, 0.1, 0.78, 0.8])
        self.cax.get_xaxis().set_visible(False)
        self.cax.get_yaxis().set_visible(False)
        self.cax.patch.set_alpha(0)
        self.cax.set_frame_on(False)
        print self.shotnum
        return self.plotfigure