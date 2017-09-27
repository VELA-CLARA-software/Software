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
        mainWindow.resize(1310, 1010)
        mainWindow.setObjectName(_fromUtf8('Matlab Image Viewer'))
        self.mainWidget = QtGui.QWidget(mainWindow)
        self.mainWidget.resize(1300, 1000)
        self.mainWidget.setObjectName(_fromUtf8('mainWidget'))
        self.mainBox = QtGui.QHBoxLayout(self.mainWidget)

        # loading files and config, etc.
        self.configVBox = QtGui.QVBoxLayout()
        self.plotVBox = QtGui.QVBoxLayout()
        self.analysisPlotVBox = QtGui.QVBoxLayout()
        self.plotsVBox = QtGui.QVBoxLayout()
        self.sigmaPlotsVBox = QtGui.QVBoxLayout()
        self.setDirOrFileLayout = QtGui.QHBoxLayout()
        self.setDirOrFile = QtGui.QGroupBox()
        self.setDirOrFile.setAlignment(QtCore.Qt.AlignCenter)
        self.setDirOrFile.setGeometry(QtCore.QRect(360, 140, 193, 211))
        self.setDirectory = QtGui.QRadioButton()
        self.setDirectory.setObjectName(_fromUtf8('setDirectory'))
        self.setDirectory.setMinimumSize(QtCore.QSize(100,20))
        self.setFile = QtGui.QRadioButton()
        self.setFile.setObjectName(_fromUtf8('setFile'))
        self.setFile.setMinimumSize(QtCore.QSize(100, 20))
        self.setDirOrFileLayout.addWidget(self.setDirectory)
        self.setDirOrFileLayout.addWidget(self.setFile)
        self.setDirOrFile.setLayout(self.setDirOrFileLayout)
        self.getDirectoryLayout = QtGui.QHBoxLayout()
        self.setLayout(self.getDirectoryLayout)
        self.getDirectoryLineEdit = QtGui.QLineEdit(self)
        self.getDirectoryLayout.addWidget(self.getDirectoryLineEdit)
        self.getDirectoryButton = QtGui.QPushButton('...', self)
        self.getDirectoryLayout.addWidget(self.getDirectoryButton)
        # self.loadFilesButton = QtGui.QPushButton('Load files', self)
        # self.loadFilesButton.setObjectName(_fromUtf8('loadFilesButton'))
        # self.loadFilesButton.setMaximumSize(QtCore.QSize(100, 40))
        self.fileTypeHBox = QtGui.QHBoxLayout()
        self.fileTypeGroupBox = QtGui.QGroupBox()
        self.fileTypeGroupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.fileTypeGroupBox.setMinimumSize(QtCore.QSize(300, 80))
        self.fileTypeGroupBox.setMaximumSize(QtCore.QSize(300, 80))
        self.emitMeas = QtGui.QRadioButton()
        self.emitMeas.setObjectName(_fromUtf8('emitMeas'))
        self.emitMeas.setMinimumSize(QtCore.QSize(100, 20))
        self.emitMeas.setMaximumSize(QtCore.QSize(100, 20))
        self.energySpreadMeas = QtGui.QRadioButton()
        self.energySpreadMeas.setObjectName(_fromUtf8('energySpreadMeas'))
        self.energySpreadMeas.setMinimumSize(QtCore.QSize(100, 20))
        self.energySpreadMeas.setMaximumSize(QtCore.QSize(100, 20))
        self.fileTypeHBox.addWidget(self.emitMeas)
        self.fileTypeHBox.addWidget(self.energySpreadMeas)
        self.fileTypeGroupBox.setLayout(self.fileTypeHBox)
        self.fileTypeGroupBox.setTitle(_fromUtf8('File type?? (*.dat for emit, or *.mat for e-spread)'))
        self.readFilesButton = QtGui.QPushButton('Read files', self)
        self.readFilesButton.setObjectName(_fromUtf8('readFilesButton'))
        self.readFilesButton.setMaximumSize(QtCore.QSize(100, 40))
        self.convertFilesButton = QtGui.QPushButton('Convert to ASCII?', self)
        self.convertFilesButton.setObjectName(_fromUtf8('convertFilesButton'))
        self.convertFilesButton.setMaximumSize(QtCore.QSize(100, 40))
        self.allFilesLabel = QtGui.QLabel()
        self.allFilesLabel.setObjectName(_fromUtf8('allFilesLabel'))
        self.allFilesComboBox = QtGui.QComboBox()
        self.allFilesComboBox.setObjectName(_fromUtf8('allFilesComboBox'))
        self.loadFileButton = QtGui.QPushButton('Load file', self)
        self.loadFileButton.setObjectName(_fromUtf8('loadFileButton'))
        self.loadFileButton.setMaximumSize(QtCore.QSize(100, 40))
        self.keysLabel = QtGui.QLabel()
        self.keysLabel.setObjectName(_fromUtf8('keysLabel'))
        self.keysComboBox = QtGui.QComboBox()
        self.keysComboBox.setObjectName(_fromUtf8('keysComboBox'))
        self.subKeysLabel = QtGui.QLabel()
        self.subKeysLabel.setObjectName(_fromUtf8('subKeysLabel'))
        self.subKeysComboBox = QtGui.QComboBox()
        self.subKeysComboBox.setObjectName(_fromUtf8('subKeysComboBox'))
        self.subSubKeysLabel = QtGui.QLabel()
        self.subSubKeysLabel.setObjectName(_fromUtf8('subSubKeysLabel'))
        self.subSubKeysComboBox = QtGui.QComboBox()
        self.subSubKeysComboBox.setObjectName(_fromUtf8('subSubKeysComboBox'))
        self.viewKeysText = QtGui.QPlainTextEdit()
        self.viewKeysText.setObjectName(_fromUtf8('viewKeysText'))

        self.sigmaXPlotVBox = QtGui.QVBoxLayout()
        self.sigmaXPlotWidget = self.addSigmaXPlotPanel()
        self.clearSigmaPlotsButton = QtGui.QPushButton('Clear sigma plots', self)
        self.sigmaXPlotVBox.addLayout(self.sigmaxlayoutVertical)
        self.sigmaXPlotVBox.addWidget(self.clearSigmaPlotsButton)
        self.sigmaXPlotVBox.addStretch()
        self.sigmaYPlotVBox = QtGui.QVBoxLayout()
        self.sigmaYPlotWidget = self.addSigmaYPlotPanel()
        self.sigmaYPlotVBox.addLayout(self.sigmaylayoutVertical)
        self.sigmaYPlotVBox.addStretch()
        self.sigmaPlotsVBox.addLayout(self.sigmaXPlotVBox)
        self.sigmaPlotsVBox.addLayout(self.sigmaYPlotVBox)

        self.configVBox.addWidget(self.setDirOrFile)
        self.configVBox.addLayout(self.getDirectoryLayout)
        self.configVBox.addWidget(self.readFilesButton)
        self.configVBox.addWidget(self.convertFilesButton)
        self.configVBox.addWidget(self.allFilesLabel)
        self.configVBox.addWidget(self.allFilesComboBox)
        self.configVBox.addWidget(self.fileTypeGroupBox)
        self.configVBox.addWidget(self.loadFileButton)
        self.configVBox.addWidget(self.keysLabel)
        self.configVBox.addWidget(self.keysComboBox)
        self.configVBox.addWidget(self.subKeysLabel)
        self.configVBox.addWidget(self.subKeysComboBox)
        self.configVBox.addWidget(self.subSubKeysLabel)
        self.configVBox.addWidget(self.subSubKeysComboBox)
        self.configVBox.addWidget(self.viewKeysText)
        self.configVBox.addStretch()

        # make all plots
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
        self.plotsVBox.addLayout(self.plotVBox)

        # analysis plots
        self.makeAnalysisPlotButton = QtGui.QPushButton('Analyse data', self)
        self.analysisPlotWidget = self.addAnalysisPlotPanel()
        self.analysisPlotVBox.addWidget(self.makeAnalysisPlotButton)
        # self.makeSigmaPlotButton = QtGui.QPushButton('Make sigma plots', self)
        # self.analysisPlotVBox.addWidget(self.makeSigmaPlotButton)
        # # self.clearSigmaPlotsButton = QtGui.QPushButton('Clear sigma plots', self)
        self.analysisPlotVBox.addLayout(self.analysislayoutVertical)
        self.analysisPlotVBox.addStretch()
        self.averagingHBox = QtGui.QHBoxLayout()
        self.averagingGroupBox = QtGui.QGroupBox()
        self.averagingGroupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.averagingGroupBox.setMinimumSize(QtCore.QSize(300, 80))
        self.averagingGroupBox.setMaximumSize(QtCore.QSize(300, 80))
        self.noAvg = QtGui.QRadioButton()
        self.noAvg.setObjectName(_fromUtf8('noAvg'))
        self.noAvg.setMinimumSize(QtCore.QSize(100, 20))
        self.noAvg.setMaximumSize(QtCore.QSize(100, 20))
        self.averaging = QtGui.QRadioButton()
        self.averaging.setObjectName(_fromUtf8('setFile'))
        self.averaging.setMinimumSize(QtCore.QSize(100, 20))
        self.averaging.setMaximumSize(QtCore.QSize(100, 20))
        self.intervalVBox = QtGui.QVBoxLayout()
        self.intervalLabel = QtGui.QLabel()
        self.intervalLabel.setObjectName(_fromUtf8('intervalLabel'))
        self.intervalText = QtGui.QPlainTextEdit()
        self.intervalText.setObjectName(_fromUtf8('intervalText'))
        self.intervalText.setMaximumSize(QtCore.QSize(40, 40))
        self.intervalVBox.addWidget(self.intervalLabel)
        self.intervalVBox.addWidget(self.intervalText)
        self.averagingHBox.addWidget(self.noAvg)
        self.averagingHBox.addWidget(self.averaging)
        self.averagingGroupBox.setLayout(self.averagingHBox)
        self.averagingHBox.addLayout(self.intervalVBox)
        self.plotsVBox.addWidget(self.averagingGroupBox)
        # self.plotsVBox.addWidget(self.makeSigmaPlotButton)
        self.plotsVBox.addLayout(self.averagingHBox)
        self.plotsVBox.addLayout(self.analysisPlotVBox)

        # add all layouts and make main panel
        self.mainBox.addLayout(self.configVBox)
        self.mainBox.addLayout(self.plotsVBox)
        self.mainBox.addLayout(self.sigmaPlotsVBox)
        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(_translate('mainWindow', 'Matlab File Viewer', None))
        self.setDirectory.setText(_translate('mainWindow', 'Set Directory', None))
        self.setFile.setText(_translate('mainWindow', 'Set File', None))
        self.readFilesButton.setText(_translate('mainWindow', 'Read .mat files', None))
        self.allFilesLabel.setText(_translate('mainWindow', 'Files in folder', None))
        self.emitMeas.setText(_translate('mainWindow', 'Emittance', None))
        self.energySpreadMeas.setText(_translate('mainWindow', 'Energy spread', None))
        self.loadFileButton.setText(_translate('mainWindow', 'Load .mat file', None))
        self.keysLabel.setText(_translate('mainWindow', 'Keys in file', None))
        self.subKeysLabel.setText(_translate('mainWindow', 'Subkeys in file[key]', None))
        self.subSubKeysLabel.setText(_translate('mainWindow', 'Subkeys in subfile[key]', None))
        self.intervalLabel.setText(_translate('mainWindow', 'Set interval', None))
        self.noAvg.setText(_translate('mainWindow', 'No averaging', None))
        self.averaging.setText(_translate('mainWindow', 'Averaging', None))
        return

    def addPlotPanel(self):
        self.figure = plt.figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.axis = self.figure.add_subplot(111)
        self.layoutVertical = QtGui.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.canvas)
        self.layoutVertical.addWidget(self.toolbar)
        self.canvas.setParent(self.mainWidget)
        self.canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.canvas.setFocus()
        return self.figure

    def addAnalysisPlotPanel(self):
        self.analysisfigure = plt.figure()
        self.analysiscanvas = FigureCanvasQTAgg(self.analysisfigure)
        self.analysistoolbar = NavigationToolbar(self.analysiscanvas, self)
        self.analysisaxis = self.analysisfigure.add_subplot(111)
        self.analysislayoutVertical = QtGui.QVBoxLayout(self)
        self.analysislayoutVertical.addWidget(self.analysiscanvas)
        self.analysislayoutVertical.addWidget(self.analysistoolbar)
        self.analysiscanvas.setParent(self.mainWidget)
        self.analysiscanvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.analysiscanvas.setFocus()
        return self.analysisfigure

    def addSigmaXPlotPanel(self):
        self.sigmaxfigure = plt.figure()
        self.sigmaxcanvas = FigureCanvasQTAgg(self.sigmaxfigure)
        self.sigmaxaxis = self.sigmaxfigure.add_subplot(111)
        self.sigmaxlayoutVertical = QtGui.QVBoxLayout(self)
        self.sigmaxlayoutVertical.addWidget(self.sigmaxcanvas)
        self.sigmaxcanvas.setParent(self.mainWidget)
        self.sigmaxcanvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.sigmaxcanvas.setFocus()
        return self.sigmaxfigure

    def addSigmaYPlotPanel(self):
        self.sigmayfigure = plt.figure()
        self.sigmaycanvas = FigureCanvasQTAgg(self.sigmayfigure)
        self.sigmayaxis = self.sigmayfigure.add_subplot(111)
        self.sigmaylayoutVertical = QtGui.QVBoxLayout(self)
        self.sigmaylayoutVertical.addWidget(self.sigmaycanvas)
        self.sigmaycanvas.setParent(self.mainWidget)
        self.sigmaycanvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.sigmaycanvas.setFocus()
        return self.sigmayfigure

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
        self.plotdata = numpy.transpose(numpy.transpose(self.newdata)[self.shotnum])
        self.ax.imshow(self.plotdata)
        self.ax.set_aspect('equal')
        #self.cax = self.plotfigure.add_axes([0.12, 0.1, 0.78, 0.8])
        #self.cax.get_xaxis().set_visible(False)
        #self.cax.get_yaxis().set_visible(False)
        #self.cax.patch.set_alpha(0)
        #self.cax.set_frame_on(False)
        print self.shotnum
        return self.plotfigure, self.plotdata

    def drawAnalysisPlot(self, datafile, datastruct, imagedata, arrayshape, shotnum, plotfigure, newarray):
        self.datafile = datafile
        self.datastruct = datastruct
        self.imagedata = imagedata
        self.arrayshape = arrayshape
        self.shotnum = shotnum
        self.newarray = newarray
        self.data = self.datafile[self.datastruct][self.imagedata]
        self.newdata = numpy.reshape(self.data, self.arrayshape)
        self.croppedplotfigure = plotfigure
        self.croppedplotfigure.canvas.flush_events()
        self.ax = self.croppedplotfigure.add_subplot(111)
        self.ax.set_title('shot number ' + str(self.shotnum))
        self.xCropMax = max(self.newarray[:2])
        self.xCropMin = min(self.newarray[:2])
        self.yCropMax = max(self.newarray[2:])
        self.yCropMin = min(self.newarray[2:])
        self.croppeddata = numpy.transpose(numpy.transpose(self.newdata)[self.shotnum][self.xCropMin:self.xCropMax])[self.yCropMin:self.yCropMax]
        self.ax.imshow(self.croppeddata)
        self.ax.set_aspect('equal')
        #self.cax = self.croppedplotfigure.add_axes([0.12, 0.1, 0.78, 0.8])
        #self.cax.get_xaxis().set_visible(False)
        #self.cax.get_yaxis().set_visible(False)
        #self.cax.patch.set_alpha(0)
        #self.cax.set_frame_on(False)
        return self.croppedplotfigure, self.croppeddata

    # self.imageSizeLabel = QtGui.QLabel()
    # self.imageSizeLabel.setObjectName(_fromUtf8('imageSizeLabel'))
    # self.imageDataHBox = QtGui.QHBoxLayout()
    # self.imageSizeY = QtGui.QPlainTextEdit()
    # self.imageSizeY.setObjectName(_fromUtf8('imageSizeY'))
    # self.imageSizeX = QtGui.QPlainTextEdit()
    # self.imageSizeX.setObjectName(_fromUtf8('imageSizeX'))
    # self.imageSizeSpacer = QtGui.QLabel()
    # self.imageSizeSpacer.setObjectName(_fromUtf8('imageSizeSpacer'))
    # self.imageNumShotsSpacer = QtGui.QLabel()
    # self.imageNumShotsSpacer.setObjectName(_fromUtf8('imageNumShotsSpacer'))
    # self.imageNumShots = QtGui.QPlainTextEdit()
    # self.imageNumShots.setObjectName(_fromUtf8('imageNumShots'))
    # self.imageNumShotsLabel = QtGui.QLabel()
    # self.imageNumShotsLabel.setObjectName(_fromUtf8('imageNumShotsLabel'))
    # self.imageSizeY.setMaximumSize(QtCore.QSize(50, 30))
    # self.imageSizeX.setMaximumSize(QtCore.QSize(50, 30))
    # self.imageNumShots.setMaximumSize(QtCore.QSize(50, 30))
    # self.imageDataHBox.addWidget(self.imageSizeY)
    # self.imageDataHBox.addWidget(self.imageSizeSpacer)
    # self.imageDataHBox.addWidget(self.imageSizeX)
    # self.imageDataHBox.addWidget(self.imageNumShots)
    # self.imageDataHBox.addWidget(self.imageNumShotsLabel)