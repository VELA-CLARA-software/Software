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


class emittanceMeasurementViewUI(object):

    def setupUi(self, mainWindow):
        mainWindow.resize(1310, 1010)
        mainWindow.setObjectName(_fromUtf8('Matlab emittance measurement tool'))
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

        self.configVBox.addWidget(self.setDirOrFile)
        self.configVBox.addLayout(self.getDirectoryLayout)
        self.configVBox.addWidget(self.readFilesButton)
        self.configVBox.addWidget(self.convertFilesButton)
        self.configVBox.addWidget(self.allFilesLabel)
        self.configVBox.addWidget(self.allFilesComboBox)
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
        self.emittanceCalcVBox = QtGui.QVBoxLayout()
        self.emittanceHBox = QtGui.QHBoxLayout()
        self.betaHBox = QtGui.QHBoxLayout()
        self.alphaHBox = QtGui.QHBoxLayout()
        self.gammaHBox = QtGui.QHBoxLayout()
        self.emitxNormLabel = QtGui.QLabel()
        self.emitxNorm = QtGui.QLabel()
        self.betaxLabel = QtGui.QLabel()
        self.betax = QtGui.QLabel()
        self.alphaxLabel = QtGui.QLabel()
        self.alphax = QtGui.QLabel()
        self.gammaxLabel = QtGui.QLabel()
        self.gammax = QtGui.QLabel()
        self.emityNormLabel = QtGui.QLabel()
        self.emityNorm = QtGui.QLabel()
        self.betayLabel = QtGui.QLabel()
        self.betay = QtGui.QLabel()
        self.alphayLabel = QtGui.QLabel()
        self.alphay = QtGui.QLabel()
        self.gammayLabel = QtGui.QLabel()
        self.gammay = QtGui.QLabel()
        self.emittanceHBox.addWidget(self.emitxNormLabel)
        self.emittanceHBox.addWidget(self.emitxNorm)
        self.emittanceHBox.addWidget(self.emityNormLabel)
        self.emittanceHBox.addWidget(self.emityNorm)
        self.betaHBox.addWidget(self.betaxLabel)
        self.betaHBox.addWidget(self.betax)
        self.betaHBox.addWidget(self.betayLabel)
        self.betaHBox.addWidget(self.betay)
        self.alphaHBox.addWidget(self.alphaxLabel)
        self.alphaHBox.addWidget(self.alphax)
        self.alphaHBox.addWidget(self.alphayLabel)
        self.alphaHBox.addWidget(self.alphay)
        self.gammaHBox.addWidget(self.gammaxLabel)
        self.gammaHBox.addWidget(self.gammax)
        self.gammaHBox.addWidget(self.gammayLabel)
        self.gammaHBox.addWidget(self.gammay)
        self.plotVBox.addWidget(self.makePlotsButton)
        self.plotVBox.addLayout(self.layoutVertical)
        self.plotVBox.addWidget(self.fileSlider)
        self.plotVBox.addWidget(self.clearPlotsButton)
        self.plotVBox.addLayout(self.emittanceHBox)
        self.plotVBox.addLayout(self.betaHBox)
        self.plotVBox.addLayout(self.alphaHBox)
        self.plotVBox.addLayout(self.gammaHBox)
        self.plotVBox.addStretch()
        self.plotsVBox.addLayout(self.plotVBox)

        self.sigmaXPlotVBox = QtGui.QVBoxLayout()
        self.sigmaXPlotWidget = self.addSigmaXPlotPanel()
        self.makeSigmaPlotsButton = QtGui.QPushButton('Make sigma plots', self)
        self.clearSigmaPlotsButton = QtGui.QPushButton('Clear sigma plots', self)
        self.clearCropButton = QtGui.QPushButton('Clear crop region', self)
        self.sigmaXPlotVBox.addLayout(self.sigmaxlayoutVertical)
        self.sigmaXPlotVBox.addWidget(self.makeSigmaPlotsButton)
        self.sigmaXPlotVBox.addWidget(self.clearSigmaPlotsButton)
        self.sigmaXPlotVBox.addWidget(self.clearCropButton)
        self.sigmaXPlotVBox.addStretch()
        self.sigmaYPlotVBox = QtGui.QVBoxLayout()
        self.sigmaYPlotWidget = self.addSigmaYPlotPanel()
        self.sigmaYPlotVBox.addLayout(self.sigmaylayoutVertical)
        self.sigmaYPlotVBox.addStretch()
        self.sigmaPlotsVBox.addLayout(self.sigmaXPlotVBox)
        self.sigmaPlotsVBox.addLayout(self.sigmaYPlotVBox)

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
        self.readFilesButton.setText(_translate('mainWindow', 'Read .dat files', None))
        self.allFilesLabel.setText(_translate('mainWindow', 'Files in folder', None))
        self.loadFileButton.setText(_translate('mainWindow', 'Load .dat file', None))
        self.keysLabel.setText(_translate('mainWindow', 'Keys in file', None))
        self.subKeysLabel.setText(_translate('mainWindow', 'Subkeys in file[key]', None))
        self.subSubKeysLabel.setText(_translate('mainWindow', 'Subkeys in subfile[key]', None))
        self.emitxNormLabel.setText(_translate('mainWindow', 'normalised x emittance (mm-mrad)', None))
        self.emityNormLabel.setText(_translate('mainWindow', 'normalised y emittance (mm-mrad)', None))
        self.betaxLabel.setText(_translate('mainWindow', 'beta x (m)', None))
        self.betayLabel.setText(_translate('mainWindow', 'beta y (m)', None))
        self.alphaxLabel.setText(_translate('mainWindow', 'alpha x', None))
        self.alphayLabel.setText(_translate('mainWindow', 'alpha y', None))
        self.gammaxLabel.setText(_translate('mainWindow', 'gamma x', None))
        self.gammayLabel.setText(_translate('mainWindow', 'gamma y', None))
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
        self.ax.set_xlabel('pixels')
        self.ax.set_ylabel('pixels')
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