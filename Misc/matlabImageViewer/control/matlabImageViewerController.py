import numpy
import h5py
import os, sys
from PyQt4 import QtCore, QtGui
from file_manager.matlabFileWriter import matlabFileWriter
from file_manager.matlabFileRead import matlabFileRead
from file_manager.hdf5FileRead import hdf5FileRead
from data_processing.emittanceMeasurement import emittanceMeasurement
from data_processing.energySpreadMeasurement import energySpreadMeasurement
import matplotlib.pyplot as plt

class matlabImageViewerController(object):

    def __init__(self, view):
        # this class contains all the functions for processing both energy spread and emittance measurements
        # they could be separated in principle, but.... they're not
        self.fileRead = matlabFileRead()
        self.hdf5fileRead = hdf5FileRead()
        self.fileWriter = matlabFileWriter()
        self.emittanceMeasurement = emittanceMeasurement()
        self.energySpreadMeasurement = energySpreadMeasurement()
        self.maindict = {}
        self.fftSUM = []
        self.zi1 = []
        # lots of bools to check whether things are done in the correct order
        self.isDirectorySet = False
        self.isFileSet = False
        self.isFilesLoaded = False
        self.isFilenamesAdded = False
        self.isArraySizeSet = False
        self.isDataAnalysed = False
        # we show the panel requested from the launcher and connect all the buttons to the functions below
        self.startView = view
        self.startView.show()
        self.startView.getDirectoryButton.clicked.connect(self.setDirOrFile)
        self.startView.readFilesButton.clicked.connect(self.readFiles)
        self.startView.loadFileButton.clicked.connect(self.loadFile)
        self.startView.convertFilesButton.clicked.connect(self.convertToHDF5)
        self.startView.filekeychanged.connect(self.keyIndexChanged)
        self.startView.subfilekeychanged.connect(self.subKeyIndexChanged)
        self.startView.subsubfilekeychanged.connect(self.subSubKeyIndexChanged)
        self.startView.makePlotsButton.clicked.connect(self.loadPlots)
        self.startView.clearPlotsButton.clicked.connect(self.clearPlots)
        self.startView.clearCropButton.clicked.connect(self.clearCropRegion)
        if self.startView.measuretype == "energyspread":
            self.startView.makeAnalysisPlotButton.clicked.connect(self.analyseData)
            self.startView.metaAnalysisPlotButton.clicked.connect(self.metaAnalyseData)
            self.startView.clearCurrentFileButton.clicked.connect(self.clearCurrentFile)
        elif self.startView.measuretype == "emittance":
            self.startView.makeSigmaPlotsButton.clicked.connect(self.analyseData)
        self.startView.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        self.startView.canvas.mpl_connect('button_release_event', self.on_mouse_release)

    # these functions are linked to the "main" canvas containing the images - the user can drag the mouse over the beam to view a cropped image
    # if this is not done, processing of the full image is done
    def on_mouse_press(self, event):
        self.croppedArrayShape = []
        self.event = event
        if self.arrayshape:
            self.xCropStart = int(self.event.xdata)
            self.yCropStart = int(self.event.ydata)
        else:
            print "load plots first"
        return self.xCropStart, self.yCropStart

    def on_mouse_release(self, event):
        self.event = event
        if self.arrayshape:
            self.xCropEnd = int(self.event.xdata)
            self.yCropEnd = int(self.event.ydata)
        else:
            print "load plots first"
        self.croppedArrayShape.append(self.xCropStart)
        self.croppedArrayShape.append(self.xCropEnd)
        self.croppedArrayShape.append(self.yCropStart)
        self.croppedArrayShape.append(self.yCropEnd)
        self.rect = plt.Rectangle((min(self.xCropStart, self.xCropEnd), min(self.yCropStart, self.yCropEnd)), numpy.abs(self.xCropStart - self.xCropEnd), numpy.abs(self.yCropStart - self.yCropEnd), fill = None)
        self.startView.axis.add_patch(self.rect)
        self.startView.canvas.draw()
        return self.xCropEnd, self.yCropEnd

    def convertToHDF5(self):
        if self.startView.measuretype == "energyspread":
            self.datastruct = "img2save"
        self.Npoints = self.currentFile[self.datastruct]['numshots']
        self.Nloops = self.startView.allFilesComboBox.count()
        self.res = 1
        self.form = numpy.array([self.arrayshape[0], self.arrayshape[1], self.Nloops])
        self.imgsAvForm = numpy.array([self.arrayshape[0], self.arrayshape[1], self.Nloops])
        self.imgsForm = numpy.array([self.arrayshape[0], self.arrayshape[1], self.Npoints, self.Nloops])
        print self.arrayshape
        self.formaFFT = self.res * self.form
        self.esse = numpy.array([self.form[0], self.form[1]]) * self.res
        self.fh5FFT = h5py.File(self.currentFile['filename']+".hdf5", 'w')
        # self.fh5FFT.create_dataset('fftAv', data=numpy.zeros((self.formaFFT[0], self.formaFFT[1], self.formaFFT[2])),
        #                       dtype=numpy.dtype(numpy.int32, (self.formaFFT[0], self.formaFFT[1], self.formaFFT[2])))
        # self.fh5FFT.create_dataset('fft_imgsAv', data=numpy.zeros((self.formaFFT[0], self.formaFFT[1], self.formaFFT[2])),
        #                       dtype=numpy.dtype(numpy.int32, (self.formaFFT[0], self.formaFFT[1], self.formaFFT[2])))
        # self.fh5FFT.create_dataset('attuAv', data=numpy.zeros((self.form[2])))
        # self.fh5FFT.create_dataset('imgsAv', data=numpy.zeros((self.imgsAvForm[0], self.imgsAvForm[1], self.imgsAvForm[2])),
        #                            dtype=numpy.dtype(numpy.int32, (self.imgsAvForm[0], self.imgsAvForm[1], self.imgsAvForm[2])))
        self.fh5FFT.create_dataset('imgs', data=numpy.zeros((self.imgsForm[0], self.imgsForm[1], self.imgsForm[2])),
                                   dtype=numpy.dtype(numpy.int32,
                                                     (self.imgsForm[0], self.imgsForm[1], self.imgsForm[2])))
        self.file_names = os.listdir(str(self.startView.getDirectoryLineEdit.text()))
        self.file_names.sort()
        self.loop = 0
        self.imdata = self.fileRead.getMatlabData(self.currentFile['filename'], '.mat')
        self.imgs = numpy.reshape(self.imdata['img2save']['immagini'], self.arrayshape)
        for p in range(self.Npoints):
            self.fh5FFT['imgs'][:, :, p] = self.imgs[:, :, p]
        # while self.loop <= self.Nloops:
        #     print self.loop
        #     for f in self.file_names:
        #         if f.find('loop_%03d' % (self.loop)) != -1:
        #             print f, self.loop
        #
        #             '''
        #             FFT2D analisys of loop imgs
        #             '''
        #             self.directory = str(self.startView.getDirectoryLineEdit.text() + '\\')
        #             self.imdata = self.fileRead.getMatlabData(self.directory+f, ".mat")
        #             self.imgs = numpy.reshape(self.imdata['img2save']['immagini'], self.arrayshape)
        #             self.attu = self.imdata['img2save']['attuatore']
        #
        #             self.imgsempty = numpy.zeros_like(numpy.copy(self.imgs[:, :, 0]))
        #             self.imgsFFT2Dempty = numpy.zeros_like(numpy.abs(numpy.fft.fft2(self.imgs[:, :, 0], s=[self.esse[0], self.esse[1]])))
        #
        #             self.fftSUM = numpy.copy(self.imgsFFT2Dempty)
        #             self.imgsSUM = numpy.copy(self.imgsempty)
        #             print numpy.shape(self.imgsSUM)
        #             print numpy.shape(self.imgs)
        #             print self.fh5FFT['imgsAv'].shape
        #
        #             for p in range(self.Npoints):
        #                 self.fftSUM += numpy.fft.fftshift(numpy.abs(numpy.fft.fft2(self.imgs[:, :, p], s=[self.esse[0], self.esse[1]])))
        #                 self.imgsSUM += self.imgs[:, :, p]
        #                 self.fh5FFT['imgs'][:, :, p, self.loop - 1] = self.imgs[:, :, p]
        #
        #             self.fftAv = self.fftSUM / self.Npoints
        #             self.imgsAv = self.imgsSUM / self.Npoints
        #             self.fft_imgsAv = numpy.fft.fftshift(numpy.abs(numpy.fft.fft2(self.imgsSUM, s=[self.esse[0], self.esse[1]])))
        #             self.attuAv = numpy.average(self.attu)
        #             print numpy.shape(self.imgsSUM)
        #
        #             self.fh5FFT['fftAv'][:, :, self.loop - 1] = self.fftAv
        #             self.fh5FFT['fft_imgsAv'][:, :, self.loop - 1] = self.fft_imgsAv
        #             self.fh5FFT['attuAv'][self.loop - 1] = self.attuAv
        #             #self.fh5FFT['imgsAv'][:, :, self.loop - 1] = self.imgsAv
        #
        #             # plt.figure(10)
        #             # plt.imshow(fftAv, norm=LogNorm())
        #             #            plt.pcolor(fftAv, norm = LogNorm())
        #
        #             # plt.figure(20)
        #             # plt.imshow(fft_imgsAv, norm=LogNorm())
        #             #            plt.pcolor(fft_imgsAv, norm = LogNorm())
        #
        #             break
        #     self.loop += 1

        self.fh5FFT.close()

    # individual files can be picked, or the user can load in a folder and read each file individually from within the GUI
    @QtCore.pyqtSlot()
    def setDirOrFile(self):
        if self.startView.setDirectory.isChecked():
            path = QtGui.QFileDialog.getExistingDirectory(None, 'Pick a Folder', 'D:\FERMI\Benchmarking\Microbunching Measurements')
            if path:
                self.startView.getDirectoryLineEdit.setText(path)
                self.isDirectorySet = True
                self.isFileSet = True
        elif self.startView.setFile.isChecked():
            file = QtGui.QFileDialog.getOpenFileName(None, "Pick a file", "D:\FERMI\Benchmarking\Microbunching Measurements")
            if file:
                self.startView.getDirectoryLineEdit.setText(file)
                self.isDirectorySet = False
                self.isFileSet = True
        return

    def clearCurrentFile(self):
        print sys.getsizeof(self.currentFile)
        del self.currentFile[self.datastruct]
        self.currentFile.clear()
        self.startView.plotWidget.clear()
        print sys.getsizeof(self.currentFile)


    def clearCropRegion(self):
        if self.currentFile[self.datastruct]:
            self.arrayshape = [self.currentFile[self.datastruct]['arrayy'], self.currentFile[self.datastruct]['arrayx'], self.currentFile[self.datastruct]['numshots']]
            self.croppedArrayShape = [0, self.currentFile[self.datastruct]['arrayx'], 0, self.currentFile[self.datastruct]['arrayy']]
            if self.rect:
                self.rect.remove()
        print self.croppedArrayShape

    # set flags for averaging of energy spread images
    def enableAveraging(self):
        if self.startView.noAvg.isChecked():
            self.startView.intervalText.isReadOnly = True
            self.startView.intervalText.clear()
        else:
            self.startView.intervalText.isReadOnly = False
        return

    # read the specified files
    def readFiles(self):
        self.startView.allFilesComboBox.clear()
        self.allFiles = []
        if self.isDirectorySet:
            if self.startView.setMAT.isChecked():
                self.directory = str(self.startView.getDirectoryLineEdit.text() + '\\')
                self.allFiles = self.fileRead.findAllFilesInDirectory(self.directory)
                self.isFilesLoaded = True
            elif self.startView.setHDF5.isChecked():
                self.directory = str(self.startView.getDirectoryLineEdit.text() + '\\')
                self.allFiles = self.hdf5fileRead.findAllHDF5FilesInDirectory(self.directory)
                self.isFilesLoaded = True
        elif self.isFileSet:
            self.file = str(self.startView.getDirectoryLineEdit.text())
            print self.file
            self.allFiles = self.fileRead.findAFile(self.file)
        print 'loaded all files'
        self.addFilesToComboBox(self.allFiles)

    def addFilesToComboBox(self, allFiles):
        self.allFiles = allFiles
        for i in self.allFiles:
            self.startView.allFilesComboBox.addItem(i)
        self.isFilenamesAdded = True
        print 'filenames added'

    # use the functions in matlabFileReader to convert a matlab struct into a python dictionary
    def loadFile(self):
        self.startView.viewKeysText.clear()
        self.startView.keysComboBox.clear()
        self.startView.subKeysComboBox.clear()
        self.startView.subSubKeysComboBox.clear()
        self.clearPlots()
        self.directory = str(self.startView.getDirectoryLineEdit.text() + '\\')
        if self.isDirectorySet:
            if self.startView.measuretype == "emittance":
                self.currentFile = self.fileRead.getMatlabData(self.directory+str(self.startView.allFilesComboBox.currentText()), ".dat")
                self.isFilesLoaded = True
            elif self.startView.measuretype == "energyspread":
                if self.startView.setMAT.isChecked():
                    self.currentFile = self.fileRead.getMatlabData(self.directory+str(self.startView.allFilesComboBox.currentText()), ".mat")
                    self.isFilesLoaded = True
                    self.isMATFile = True
                elif self.startView.setHDF5.isChecked():
                    self.currentFile = self.hdf5fileRead.getHDF5Data(self.directory + str(self.startView.allFilesComboBox.currentText()))
                    self.isFilesLoaded = True
                    self.isHDF5File = True
            else:
                print "choose a thing"
        elif self.isFileSet:
            if self.startView.measuretype == "emittance":
                self.currentFile = self.fileRead.getMatlabData(self.directory+str(self.startView.getDirectoryLineEdit.text()), ".dat")
            elif self.startView.measuretype == "energyspread":
                if self.startView.setMAT.isChecked():
                    self.currentFile = self.fileRead.getMatlabData(self.directory+str(self.startView.getDirectoryLineEdit.text()), ".mat")
                    self.isMATFile = True
                elif self.startView.setHDF5.isChecked():
                    self.currentFile = self.hdf5fileRead.getHDF5Data(self.directory+str(self.startView.getDirectoryLineEdit.text()))
                    self.isHDF5File = True
            else:
                print "choose a thing"
        print 'loaded all files'
        self.addKey(self.currentFile)
        return self.currentFile

    # add "top-level" keys (to the python dictionary, converted from the matlab struct) to the GUI combobox - the user can select these
    def addKey(self, data):
        self.startView.keysComboBox.clear()
        self.data = data
        if self.startView.setMAT.isChecked():
            for key, value in self.data.iteritems():
                self.startView.keysComboBox.addItem(key)

    # this lets the program know if the value of the combo box containing the top-level keys has changed
    # if the value of the key is not itself a struct, the value of this key is outputted to the text box below
    # if the value of the key is a struct (aka python dict) containing "sub-keys", then these sub-keys populate the combo box below
    def keyIndexChanged(self, keyname):
        self.keyname = str(keyname)
        self.keyvalue = self.currentFile[self.keyname]
        if isinstance(self.keyvalue, dict):
            self.keylist = []
            self.startView.viewKeysText.setPlainText(self.keyname + ' :')
            self.startView.subKeysComboBox.clear()
            for key, value in self.keyvalue.iteritems():
                self.startView.subKeysComboBox.addItem(key)
        elif isinstance(self.keyvalue, list):
            self.elemlist = []
            self.startView.subKeysComboBox.clear()
            self.startView.subSubKeysComboBox.clear()
            self.startView.viewKeysText.setPlainText(self.keyname + ' : ')
            for elem in self.keyvalue:
                self.elemlist.append(elem)

        else:
            self.startView.viewKeysText.setPlainText(self.keyname + ' : ' + self.keyvalue)

    # this lets the program know if the user has changed the value of the sub-key combo box
    # if the value of the sub-key is not itself a struct, the value of this key is outputted to the text box below
    # if the value of the sub-key is a struct (aka python dict) containing "sub-sub-keys", then these sub-sub-keys populate the combo box below
    # we only output the first few values if the value of the key is a massive array
    def subKeyIndexChanged(self, keyname):
        self.keyname = str(keyname)
        self.keyvalue = self.currentFile[str(self.startView.keysComboBox.currentText())][self.keyname]
        self.startView.subSubKeysComboBox.clear()
        if isinstance(self.keyvalue, dict):
            self.keylist = []
            self.startView.subSubKeysComboBox.clear()
            self.startView.viewKeysText.setPlainText(self.keyname + ' :')
            for key, value in self.keyvalue.iteritems():
                self.startView.subSubKeysComboBox.addItem(key)
        elif isinstance(self.keyvalue, list):
            self.elemlist = []
            self.startView.viewKeysText.setPlainText(self.keyname + ' : ')
            for i in self.keyvalue:
                self.elemlist.append(str(i)+", ")
                if len(self.elemlist) > 20:
                    self.elemlist.append(', ...')
                    break

            self.elemlist.append(' --- length ' + str(len(self.keyvalue)))
            self.startView.viewKeysText.appendPlainText(' ' + ''.join(self.elemlist))

        else:
            self.startView.viewKeysText.setPlainText(self.keyname + ' : ' + str(self.keyvalue))

    # this lets the program know if the user has changed the value of the sub-key combo box
    # you know the drill by now...
    def subSubKeyIndexChanged(self, keyname):
        self.keyname = str(keyname)
        self.keyvalue = self.currentFile[str(self.startView.keysComboBox.currentText())][str(self.startView.subKeysComboBox.currentText())][self.keyname]
        if isinstance(self.keyvalue, dict):
            self.keylist = []
            self.startView.viewKeysText.setPlainText(self.keyname + ' :')
            for key, value in self.keyvalue.iteritems():
                self.keylist.append(key)
                self.values = []
                if isinstance(value, list):
                    for i in value:
                        self.values.append(str(i) + ", ")
                        if len(self.values) > 20:
                            self.values.append(', ...')
                            break
                    self.values.append(' --- length ' + str(len(value)))
                    self.startView.viewKeysText.appendPlainText(' ' + key + ' : ' + ''.join(self.values))
                else:
                    self.startView.viewKeysText.appendPlainText(' ' + key + ' : ' + str(value))

        elif isinstance(self.keyvalue, list):
            self.elemlist = []
            self.startView.viewKeysText.setPlainText(self.keyname + ' : ')
            for i in self.keyvalue:
                self.elemlist.append(str(i)+", ")
                if len(self.elemlist) > 20:
                    self.elemlist.append(', ...')
                    break
            self.elemlist.append(' --- length ' + str(len(self.keyvalue)))
            self.startView.viewKeysText.appendPlainText(' ' + ''.join(self.elemlist))
            # for elem in self.keyvalue:
            #     self.elemlist.append(elem)

        else:
            self.startView.viewKeysText.setPlainText(self.keyname + ' : ' + str(self.keyvalue))

    # this function takes in the measurement type (passed from the launcher) and runs the appropriate function to read in the images
    def loadPlots(self):
        self.allplots = []
        self.arrayshape = []
        if self.startView.measuretype == "energyspread":
            # these are keys to the matlab data containing the images
            # all of the image data is contained in "immagini" - "numshots" images of x by y pixels in a 1-d array
            self.datastruct = 'img2save'
            self.imagedata = 'immagini'
            self.numshots = self.currentFile[self.datastruct]['numshots']
            self.energySpreadData = self.energySpreadMeasurement.loadEnergySpreadData(self.startView, self.currentFile, self.datastruct, self.imagedata)
            self.plotsLoaded = True
            # tells the GUI to load the plot corresponding to the slider value
            self.startView.fileSlider.valueChanged[int].connect(self.scrollPlots)
            self.numshots = self.energySpreadData[0]
            self.croppedArrayShape = self.energySpreadData[1]
            self.arrayshape = self.energySpreadData[2]
            self.allplots = self.energySpreadData[3]
            self.index = self.numshots - 1
            self.fileSliderIndex = 1
        elif self.startView.measuretype == "emittance":
            # these are keys to the matlab data containing the images
            # within "DATA" there are "n" keys containing "numshots" images of x by y pixels in a 1-d array for each quad setting
            # along with quad K values, quad length, and lots of other data
            self.datastruct = 'DATA'
            self.loadEmitData = self.emittanceMeasurement.loadEmitData(self.startView, self.currentFile, self.datastruct)
            self.plotsLoaded = True
            self.numshots = self.loadEmitData[0]
            self.croppedArrayShape = self.loadEmitData[1]
            self.arrayshape = self.loadEmitData[2]
            self.imagedata = self.loadEmitData[3]
            self.index = self.numshots - 1
            self.allplots = []
            for i in range(0, self.numshots - 1):
                self.plotfig = self.startView.plotWidget
                self.allplots.append(
                    self.startView.makePlots(self.currentFile, self.datastruct,
                                             self.imagedata, self.arrayshape, i, self.plotfig))
            self.allplots[-1][0].canvas.draw()
            self.startView.fileSlider.setMaximum(self.numshots - 1)
            self.startView.fileSlider.setValue(self.numshots - 1)
            self.startView.fileSlider.valueChanged[int].connect(self.scrollPlots)
        #self.croppedArrayShape = [0, self.arrayshape[1], 0, self.arrayshape[0]]
        return self.allplots

    # this tells the data_processing classes to get and plot the measured values
    def analyseData(self):
        if self.startView.measuretype == "emittance":
            # 19.6 micron per pixel for emittance scans
            self.currentFile[self.datastruct]['pixelwidth'] = 0.0000196
            self.sigSquaredVals = self.emittanceMeasurement.getSigmaSquared(self.startView, self.currentFile, self.datastruct, self.arrayshape, self.croppedArrayShape, self.numshots)
            self.quadK = self.sigSquaredVals[0]
            self.sigmaXSquared = self.sigSquaredVals[1]
            self.xSigmas = self.sigSquaredVals[2]
            self.xSigmaRMS = self.sigSquaredVals[3]
            self.sigmaYSquared = self.sigSquaredVals[4]
            self.ySigmas = self.sigSquaredVals[5]
            self.ySigmaRMS = self.sigSquaredVals[6]
            self.plotandfit = self.emittanceMeasurement.plotSigmaSquared(self.startView, self.quadK, self.sigmaXSquared, self.xSigmas,
                                                                         self.xSigmaRMS, self.sigmaYSquared, self.ySigmas, self.ySigmaRMS)
            self.driftlength = self.currentFile[self.datastruct]['drift']
            self.quadlength = self.currentFile[self.datastruct]['Lq']
            self.energy = self.currentFile[self.datastruct]['energy']
            self.twiss = self.getEmittanceAndTwiss = self.emittanceMeasurement.getEmittance(self.plotandfit[0], self.plotandfit[1], self.driftlength, self.energy)
            for i in self.twiss[0]:
                print i
            for i in self.twiss[1]:
                print i
            self.startView.emitxNorm.setText(str(self.twiss[0][1]))
            self.startView.betax.setText(str(self.twiss[0][3]))
            self.startView.alphax.setText(str(self.twiss[0][2]))
            self.startView.gammax.setText(str(self.twiss[0][4]))
            self.startView.emityNorm.setText(str(self.twiss[1][1]))
            self.startView.betay.setText(str(self.twiss[1][3]))
            self.startView.alphay.setText(str(self.twiss[1][2]))
            self.startView.gammay.setText(str(self.twiss[1][4]))
        elif self.startView.measuretype == "energyspread":
            if self.startView.setMAT.isChecked():
            #     self.currentFile[self.datastruct]['pixelwidth'] = 31.2 * (1 * (10 ** -6))
            #     self.energySpreadMeasurement.getEnergySpread(self.startView, self.currentFile, self.datastruct, self.imagedata, self.arrayshape, self.croppedArrayShape, self.index)
            # elif self.startView.setHDF5.isChecked():
            #     for i in range(0, self.currentFile[self.datastruct]["numshots"]):
                self.results = self.energySpreadMeasurement.makeFit(self.startView, self.currentFile, self.datastruct, self.imagedata, self.arrayshape, self.croppedArrayShape, self.index)
                self.results = self.energySpreadMeasurement.fourierAnalysis(self.startView, self.currentFile, self.datastruct, self.imagedata, self.arrayshape, self.index)
                self.fftSUM.append(self.results[0])
                self.zi1.append(self.results[1])
        self.isDataAnalysed = True

    def metaAnalyseData(self):
        self.energyspreadplotfig = self.startView.energySpreadPlotWidget
        self.energyspreadplotfig.canvas.flush_events()
        self.energyspreadax = self.energyspreadplotfig.add_subplot(111)
        self.loop = 0
        for i in range(0, len(self.zi1)):
            self.energyspreadax.plot(self.zi1[i]+(100000*(i+1)))
        self.energyspreadax.set_aspect('auto')
        self.energyspreadax.set_xlabel('y projection')
        self.energyspreadax.set_ylabel('avg(sum y pixels) per slice')
        self.energyspreadplotfig.canvas.draw()

    # this tells the GUI to update the main image plot when the file slider is changed
    def scrollPlots(self, index):
        self.index = index
        self.fileSliderIndex = self.index
        if self.plotsLoaded:
            if self.startView.measuretype == "emittance":
                self.imagedata = str(self.startView.subKeysComboBox.currentText())
                self.plotfig = self.startView.plotWidget
                self.plotfigure = self.startView.makePlots(self.currentFile, self.datastruct,
                                                           self.imagedata, self.arrayshape, self.index, self.plotfig)
                self.plotfigure[0].canvas.draw()
            elif self.startView.measuretype == "energyspread":
                self.imagedata = 'immagini'
                self.plotfig = self.startView.plotWidget
                self.plotfigure = self.startView.makePlots(self.currentFile, self.datastruct,
                                                           self.imagedata, self.arrayshape, self.index, self.plotfig)
                self.plotfigure[0].canvas.draw()
        else:
            print 'plots not loaded'

    def clearPlots(self):
        self.startView.plotWidget.canvas.flush_events()
        plt.cla()
        plt.clf()