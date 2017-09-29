import numpy
from PyQt4 import QtCore, QtGui
from file_manager.matlabFileWriter import matlabFileWriter
from file_manager.matlabFileRead import matlabFileRead
from data_processing.emittanceMeasurement import emittanceMeasurement
from data_processing.energySpreadMeasurement import energySpreadMeasurement
import matplotlib.pyplot as plt

class matlabImageViewerController(object):

    def __init__(self, view):
        # this class contains all the functions for processing both energy spread and emittance measurements
        # they could be separated in principle, but.... they're not
        self.fileRead = matlabFileRead()
        self.fileWriter = matlabFileWriter()
        self.emittanceMeasurement = emittanceMeasurement()
        self.energySpreadMeasurement = energySpreadMeasurement()
        self.maindict = {}
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
        self.startView.filekeychanged.connect(self.keyIndexChanged)
        self.startView.subfilekeychanged.connect(self.subKeyIndexChanged)
        self.startView.subsubfilekeychanged.connect(self.subSubKeyIndexChanged)
        self.startView.makePlotsButton.clicked.connect(self.loadPlots)
        self.startView.clearPlotsButton.clicked.connect(self.clearPlots)
        self.startView.clearCropButton.clicked.connect(self.clearCropRegion)
        if self.startView.measuretype == "energyspread":
            self.startView.makeAnalysisPlotButton.clicked.connect(self.analyseData)
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
        return self.xCropEnd, self.yCropEnd

    # individual files can be picked, or the user can load in a folder and read each file individually from within the GUI
    @QtCore.pyqtSlot()
    def setDirOrFile(self):
        if self.startView.setDirectory.isChecked():
            path = QtGui.QFileDialog.getExistingDirectory(None, 'Pick a Folder', 'D:\\FERMI\\Data')
            if path:
                self.startView.getDirectoryLineEdit.setText(path)
                self.isDirectorySet = True
                self.isFileSet = True
        elif self.startView.setFile.isChecked():
            file = QtGui.QFileDialog.getOpenFileName(None, "Pick a file", "D:\\FERMI\\Data")
            if file:
                self.startView.getDirectoryLineEdit.setText(file)
                self.isDirectorySet = False
                self.isFileSet = True
        return

    def clearCropRegion(self):
        if self.currentFile[self.datastruct]:
            self.arrayshape = [self.currentFile[self.datastruct]['arrayy'], self.currentFile[self.datastruct]['arrayx'], self.currentFile[self.datastruct]['numshots']]
            self.croppedArrayShape = [0, self.currentFile[self.datastruct]['arrayx'], 0, self.currentFile[self.datastruct]['arrayy']]
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
            self.directory = str(self.startView.getDirectoryLineEdit.text() + '\\')
            self.allFiles = self.fileRead.findAllFilesInDirectory(self.directory)
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
                self.currentFile = self.fileRead.getMatlabData(self.directory+str(self.startView.allFilesComboBox.currentText()), ".mat")
                self.isFilesLoaded = True
            else:
                print "choose a thing"
        elif self.isFileSet:
            if self.startView.measuretype == "emittance":
                self.currentFile = self.fileRead.getMatlabData(str(self.startView.getDirectoryLineEdit.text()), ".dat")
            elif self.startView.measuretype == "energyspread":
                self.currentFile = self.fileRead.getMatlabData(str(self.startView.getDirectoryLineEdit.text()), ".mat")
            else:
                print "choose a thing"
        print 'loaded all files'
        self.addKey(self.currentFile)
        return self.currentFile

    # add "top-level" keys (to the python dictionary, converted from the matlab struct) to the GUI combobox - the user can select these
    def addKey(self, data):
        self.startView.keysComboBox.clear()
        self.data = data
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
        elif self.startView.measuretype == "energyspread":
            self.currentFile[self.datastruct]['pixelwidth'] = 31.2 * ( 1 * ( 10 ** -6 ) )
            self.energySpreadMeasurement.getEnergySpread(self.startView, self.currentFile, self.datastruct, self.imagedata, self.arrayshape, self.croppedArrayShape, self.index)
        self.isDataAnalysed = True

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

    # def loadFiles(self):
    #     self.startView.allFilesComboBox.clear()
    #     self.directory = str(self.startView.getDirectoryLineEdit.text() + '\\')
    #     if self.isDirectorySet:
    #         self.fileRead.loadAllDataInDirectory(self.directory, self.maindict)
    #         self.isFilesLoaded = True
    #     print 'loaded all files'
    #     self.addFilesToList(self.directory)
    # def addKeys(self):
    #     self.currentIndex = self.startView.allFilesComboBox.currentIndex()
    #     for key in self.maindict[self.directory][self.currentIndex].keys():
    #         self.startView.keysComboBox.addItem(key)
    # def keyIndexChanged(self, keyname):
    #     self.keyname = str(keyname)
    #     self.keyvalue = self.maindict[self.directory][self.startView.allFilesComboBox.currentIndex()][self.keyname]
    #     if isinstance(self.keyvalue, dict):
    #         self.keylist = []
    #         self.startView.viewKeysText.setPlainText(self.keyname + ' :')
    #         for key, value in self.keyvalue.iteritems():
    #             self.keylist.append(key)
    #             self.values = []
    #             if isinstance(value, list):
    #                 for i in value:
    #                     self.values.append(str(i))
    #                     if i > 1:
    #                         self.values.append(', ...')
    #                         break
    #
    #                 self.values.append(' --- length ' + str(len(value)))
    #                 self.startView.viewKeysText.appendPlainText(' ' + key + ' : ' + ''.join(self.values))
    #             else:
    #                 self.startView.viewKeysText.appendPlainText(' ' + key + ' : ' + str(value))
    #
    #     elif isinstance(self.keyvalue, list):
    #         self.elemlist = []
    #         self.startView.viewKeysText.setPlainText(self.keyname + ' : ')
    #         for elem in self.keyvalue:
    #             self.elemlist.append(elem)
    #
    #     else:
    #         self.startView.viewKeysText.setPlainText(self.keyname + ' : ' + self.keyvalue)
    #
    # def loadPlots(self):
    #     self.allplots = []
    #     self.arrayshape = []
    #     self.fileindex = self.startView.allFilesComboBox.currentIndex()
    #     self.numshots = self.maindict[self.directory][self.fileindex]['img2save']['numshots']
    #     self.arrayshape.append(self.maindict[self.directory][self.fileindex]['img2save']['arrayy'])
    #     self.arrayshape.append(self.maindict[self.directory][self.fileindex]['img2save']['arrayx'])
    #     self.arrayshape.append(self.numshots)
    #     self.allplots = []
    #     for i in range(0, self.numshots):
    #         self.plotfig = self.startView.plotWidget
    #         self.allplots.append(self.startView.makePlots(self.maindict[self.directory][self.fileindex], self.datastruct, self.imagedata, self.arrayshape, i, self.plotfig))
    #         self.allplots[i].canvas.draw()
    #
    #     self.plotsLoaded = True
    #     self.startView.fileSlider.setMaximum(self.numshots - 1)
    #     self.startView.fileSlider.setValue(self.numshots - 1)
    #     return self.allplots
    #
    # def scrollPlots(self, index):
    #     self.index = index
    #     if self.plotsLoaded:
    #         self.plotfig = self.startView.plotWidget
    #         self.plotfigure = self.startView.makePlots(self.maindict[self.directory][0], self.datastruct, self.imagedata, self.arrayshape, self.index, self.plotfig)
    #         self.plotfigure.canvas.draw()
    #     else:
    #         print 'plots not loaded'
    #
    # def getProjections(self, numshots, datastring, index):
    #     self.index = index
    #     self.tmpxvec = []
    #     self.tmpyvec = []
    #     self.fitxvec = []
    #     self.fityvec = []
    #     self.numshots = numshots
    #     self.datastring = datastring
    #     self.data = self.currentFile[self.datastruct][self.datastring]
    #     self.newdata = numpy.reshape(self.data, self.arrayshape)
    #     self.croppedplotfig = self.startView.analysisPlotWidget
    #     self.croppedplotfig.canvas.flush_events()
    #     self.startView.analysisaxis.cla()
    #     # self.croppedPlot = self.startView.drawAnalysisPlot(self.currentFile, self.datastruct, self.imagedata,
    #     #                                                    self.arrayshape, self.index, self.croppedplotfig,
    #     #                                                    self.croppedArrayShape)
    #     # self.croppedplotfig.canvas.draw()
    #     self.xCropMax = max(self.croppedArrayShape[:2])
    #     self.xCropMin = min(self.croppedArrayShape[:2])
    #     self.yCropMax = max(self.croppedArrayShape[2:])
    #     self.yCropMin = min(self.croppedArrayShape[2:])
    #     #self.croppeddata = numpy.transpose(numpy.transpose(self.newdata)[self.index][self.xCropMin:self.xCropMax])[self.yCropMin:self.yCropMax]
    #     self. i = 0
    #     for i in range(0, self.numshots - 1):
    #         self.sigmaY = []
    #         self.sigmaX = []
    #         self.sigmaYAvg = []
    #         self.sigmaXAvg = []
    #         self.yAvg = []
    #         self.xAvg = []
    #         self.newarray = []
    #         self.x = range(0, self.xCropMax - self.xCropMin)
    #         self.y = range(0, self.yCropMax - self.yCropMin)
    #         for slice_2d in numpy.transpose(numpy.transpose(self.newdata)[i][self.xCropMin:self.xCropMax])[self.yCropMin:self.yCropMax]:
    #             self.n = len(slice_2d)  # the number of data
    #             self.mean = sum(slice_2d) / self.n  # note this correction
    #             self.sigma = sum(slice_2d * (slice_2d - self.mean) ** 2) / self.n
    #             # self.fit, self.tmp = curve_fit(self.gaussFit, self.x, slice_2d, p0=[max(slice_2d), self.mean, self.sigma])
    #             self.sigmaY.append(self.sigma)
    #         for slice_2d in numpy.transpose(self.newdata)[i][self.xCropMin:self.xCropMax]:
    #             self.n = len(slice_2d)  # the number of data
    #             self.mean = sum(slice_2d) / self.n  # note this correction
    #             self.sigma = sum(slice_2d * (slice_2d - self.mean) ** 2) / self.n
    #             # self.fit, self.tmp = curve_fit(self.gaussFit, self.x, slice_2d, p0=[max(slice_2d), self.mean, self.sigma])
    #             self.sigmaX.append(self.sigma)
    #         if self.startView.averaging.isChecked():
    #             self.averagingInterval = int(self.startView.intervalText.toPlainText())
    #             for i in range(0, len(self.sigmaY), self.averagingInterval):
    #                 if not (len(self.sigmaY) - i) < self.averagingInterval:
    #                     self.sigmaYAvg.append(numpy.mean(self.sigmaY[i:i + self.averagingInterval]))
    #                     self.yAvg.append(numpy.mean(self.y[i:i + self.averagingInterval]))
    #                 else:
    #                     self.sigmaYAvg.append(numpy.mean(self.sigmaY[i:-1]))
    #                     self.yAvg.append(numpy.mean(self.y[i:i - 1]))
    #             for i in range(0, len(self.sigmaX), self.averagingInterval):
    #                 if not (len(self.sigmaX) - i) < self.averagingInterval:
    #                     self.sigmaXAvg.append(numpy.mean(self.sigmaX[i:i + self.averagingInterval]))
    #                     self.xAvg.append(numpy.mean(self.x[i:i + self.averagingInterval]))
    #                 else:
    #                     self.sigmaXAvg.append(numpy.mean(self.sigmaX[i:-1]))
    #                     self.xAvg.append(numpy.mean(self.x[i:i - 1]))
    #             # self.ax = self.croppedplotfig.add_subplot(111)
    #             # self.newarrayY = numpy.vstack((self.yAvg, self.sigmaYAvg))
    #             # self.newarrayX = numpy.vstack((self.xAvg, self.sigmaXAvg))
    #         elif self.startView.noAvg.isChecked():
    #             # self.ax = self.croppedplotfig.add_subplot(111)
    #             self.newarrayY = numpy.vstack((self.y, self.sigmaY))
    #             self.newarrayX = numpy.vstack((self.x, self.sigmaX))
    #         else:
    #             print "choose a bloody thing"
    #         # self.ax.plot(self.newarrayY[0], self.newarrayY[1])
    #         # self.ax.plot(self.newarrayX[0], self.newarrayX[1])
    #         self.fitx, self.tmpx = curve_fit(self.gaussFit, self.x, self.sigmaX, p0=[1, 20, numpy.mean(self.sigmaX)])
    #         # self.ax.plot(self.x, self.gaussFit(self.x, *self.fitx), 'ro:', label='fitxs')
    #         self.fity, self.tmpy = curve_fit(self.gaussFit, self.y, self.sigmaY, p0=[1, 20, numpy.mean(self.sigmaY)])
    #         # self.ax.plot(self.y, self.gaussFit(self.y, *self.fity), 'ro:', label='fitys')
    #         self.fitxvec.append(self.fitx)
    #         self.fityvec.append(self.fity)
    #         # print self.fitx[2]
    #         # print self.fity[2]
    #         # self.ax.set_aspect('auto')
    #         # self.croppedplotfig.canvas.draw()
    #     return self.fitxvec, self.fityvec
    #
    #
    # def gaussFit(self, x, a, x0, sigma):
    #     self.x = x
    #     self.a = a
    #     self.x0 = x0
    #     self.sigma = sigma
    #     return self.a * numpy.exp(-(self.x - self.x0) ** 2 / (2 * self.sigma ** 2))

    # def makeSigmaPlot(self):
    #     self.sigmaxplotfig = self.startView.sigmaXPlotWidget
    #     self.sigmayplotfig = self.startView.sigmaYPlotWidget
    #     self.sigmaxplotfig.canvas.flush_events()
    #     self.sigmayplotfig.canvas.flush_events()
    #     self.startView.sigmaxaxis.cla()
    #     self.startView.sigmayaxis.cla()
    #     self.sigmaxax = self.sigmaxplotfig.add_subplot(111)
    #     self.sigmayax = self.sigmayplotfig.add_subplot(111)
    #     if self.isDataAnalysed:
    #         # self.ax.plot(range(self.croppedArrayShape[0],self.croppedArrayShape[1]), self.emittanceMeasurement.gaussFit(range(self.croppedArrayShape[0],self.croppedArrayShape[1]), *self.xProjs[1][2]), 'ro:', label='fitxs')
    #         if self.startView.emitMeas.isChecked():
    #             self.curtext = int(str(self.startView.subKeysComboBox.currentText()[6:]))
    #             self.xpos = range(self.croppedArrayShape[0], self.croppedArrayShape[1])
    #             self.ypos = range(self.croppedArrayShape[2], self.croppedArrayShape[3])
    #             # plt.plot(self.xpos, self.emittanceMeasurement.gaussFit(self.xpos, *self.xProjs[self.curtext][0]), 'ro:', label='fitxs')
    #             for i in range(0, self.numshots - 1):
    #                 self.sigmaxax.plot(self.xpos, self.emittanceMeasurement.gaussFit(self.xpos, *self.xProjs[self.curtext][i]), label='fitxs')
    #                 self.sigmayax.plot(self.ypos, self.emittanceMeasurement.gaussFit(self.ypos, *self.yProjs[self.curtext][i]), label='fitys')
    #             self.legx = self.sigmaxax.legend(loc='upper left', fancybox=True, shadow=True)
    #             self.legy = self.sigmayax.legend(loc='upper left', fancybox=True, shadow=True)
    #             self.sigmaxax.set_aspect('auto')
    #             self.sigmayax.set_aspect('auto')
    #             self.sigmaxplotfig.canvas.draw()
    #             self.sigmayplotfig.canvas.draw()
    #         # elif self.startView.energySpreadMeas.isChecked():
    #         #     self.imagedata = 'immagini'
    #         #     self.plotfig = self.startView.plotWidget
    #         #     self.plotfigure = self.startView.makePlots(self.currentFile, self.datastruct,
    #         #                                                self.imagedata, self.arrayshape, self.index, self.plotfig)
    #         #     self.plotfigure[0].canvas.draw()
    #     else:
    #         print 'plots not loaded'
    #
    # def getEnergySpread(self):
    #     self.data = self.currentFile[self.datastruct][self.imagedata]
    #     self.newdata = numpy.reshape(self.data, self.arrayshape)
    #     self.croppedplotfig = self.startView.analysisPlotWidget
    #     self.croppedplotfig.canvas.flush_events()
    #     self.startView.analysisaxis.cla()
    #     # self.croppedPlot = self.startView.drawAnalysisPlot(self.currentFile, self.datastruct, self.imagedata,
    #     #                                                    self.arrayshape, self.index, self.croppedplotfig,
    #     #                                                    self.croppedArrayShape)
    #     # self.croppedplotfig.canvas.draw()
    #     self.xCropMax = max(self.croppedArrayShape[:2])
    #     self.xCropMin = min(self.croppedArrayShape[:2])
    #     self.yCropMax = max(self.croppedArrayShape[2:])
    #     self.yCropMin = min(self.croppedArrayShape[2:])
    #     self.croppeddata = numpy.transpose(numpy.transpose(self.newdata)[self.index][self.xCropMin:self.xCropMax])[self.yCropMin:self.yCropMax]
    #     self. i = 0
    #     self.sigmaY = []
    #     self.sigmaYAvg = []
    #     self.yAvg = []
    #     self.newarray = []
    #     self.x = range(0, self.xCropMax - self.xCropMin)
    #     self.y = range(0, self.yCropMax - self.yCropMin)
    #     for slice_2d in self.croppeddata:
    #         self.n = len(slice_2d)  # the number of data
    #         self.mean = sum(slice_2d) / self.n  # note this correction
    #         self.sigma = sum(slice_2d * (self.mean) ** 2) / self.n
    #         # self.fit, self.tmp = curve_fit(self.gaussFit, self.x, slice_2d, p0=[max(slice_2d), self.mean, self.sigma])
    #         self.sigmaY.append(self.sigma)
    #         print self.sigma
    #     if self.startView.averaging.isChecked():
    #         self.averagingInterval = int(self.startView.intervalText.toPlainText())
    #         for i in range(0, len(self.sigmaY), self.averagingInterval):
    #             if not (len(self.sigmaY) - i) < self.averagingInterval:
    #                 self.sigmaYAvg.append(numpy.mean(self.sigmaY[i:i + self.averagingInterval]))
    #                 self.yAvg.append(numpy.mean(self.y[i:i + self.averagingInterval]))
    #             else:
    #                 self.sigmaYAvg.append(numpy.mean(self.sigmaY[i:-1]))
    #                 self.yAvg.append(numpy.mean(self.y[i:i - 1]))
    #         self.ax = self.croppedplotfig.add_subplot(111)
    #         self.newarray = numpy.vstack((self.yAvg, self.sigmaYAvg))
    #         self.ax.plot(self.newarray[0], self.newarray[1])
    #         self.ax.set_aspect('auto')
    #         self.croppedplotfig.canvas.draw()
    #     elif self.startView.noAvg.isChecked():
    #         self.ax = self.croppedplotfig.add_subplot(111)
    #         self.newarray = numpy.vstack((self.y, self.sigmaY))
    #         self.ax.plot(self.newarray[0], self.newarray[1])
    #         self.ax.set_aspect('auto')
    #         self.croppedplotfig.canvas.draw()
    #     else:
    #         print "choose a bloody thing"

            # self.xProjs = {}
            # self.yProjs = {}
            # self.quadK = []
            # self.xSigmas = []
            # self.xSigmaSquared = []
            # self.ySigmas = []
            # self.ySigmaSquared = []
            # self.j = 0
            # self.subKeyItems = [str(self.startView.subKeysComboBox.itemText(i)) for i in
            #                     range(self.startView.subKeysComboBox.count())]
            # for i in self.subKeyItems:
            #     if i.startswith("figure"):
            #         self.projections = self.emittanceMeasurement.getProjections(self.startView, self.numshots,
            #                                                                     self.currentFile, self.datastruct, i,
            #                                                                     self.arrayshape, self.croppedArrayShape)
            #         self.xProjs[int(i[6:])] = self.projections[0]
            #         self.yProjs[int(i[6:])] = self.projections[1]
            #         self.j = self.j + 1
            #     if i == "kq":
            #         self.quadK = self.currentFile[self.datastruct][i]
            # for i, j in sorted(self.xProjs.items()):
            #     self.sig = []
            #     for a in j:
            #         self.sig.append(abs(a[2]) * abs(a[2]))
            #     self.xSigmas.append(self.sig)
            #     self.meanSigma = numpy.mean(self.sig)
            #     self.xSigmaSquared.append(self.meanSigma)
            # for k, l in sorted(self.yProjs.items()):
            #     self.sig = []
            #     for a in l:
            #         self.sig.append(abs(a[2]) * abs(a[2]))
            #     self.ySigmas.append(self.sig)
            #     self.meanSigma = numpy.mean(self.sig)
            #     # self.meanSigma = numpy.mean(l[2]*l[2])
            #     self.ySigmaSquared.append(self.meanSigma)
            #
            # self.xemitplotfig = self.startView.sigmaXPlotWidget
            # self.yemitplotfig = self.startView.sigmaYPlotWidget
            # self.xemitplotfig.canvas.flush_events()
            # self.yemitplotfig.canvas.flush_events()
            # self.startView.sigmaxaxis.cla()
            # self.startView.sigmayaxis.cla()
            # self.newarrayY = numpy.vstack((self.quadK, self.ySigmaSquared))
            # self.newarrayX = numpy.vstack((self.quadK, self.xSigmaSquared))
            # self.xemitax = self.xemitplotfig.add_subplot(111)
            # self.yemitax = self.yemitplotfig.add_subplot(111)
            # # self.ax.plot(range(self.croppedArrayShape[0],self.croppedArrayShape[1]), self.emittanceMeasurement.gaussFit(range(self.croppedArrayShape[0],self.croppedArrayShape[1]), *self.xProjs[1][2]), 'ro:', label='fitxs')
            # self.yemitax.plot(self.newarrayY[0], self.newarrayY[1], label='sigmay^2')
            # self.xemitax.plot(self.newarrayX[0], self.newarrayX[1], label='sigmax^2')
            # for xe, ye in zip(self.newarrayY[0], self.ySigmas):
            #     self.yemitax.scatter([xe] * len(ye), ye, color='red')
            # for xe, ye in zip(self.newarrayX[0], self.xSigmas):
            #     self.xemitax.scatter([xe] * len(ye), ye, color='red')
            # self.xleg = self.xemitax.legend(loc='upper center', fancybox=True, shadow=True)
            # self.yleg = self.yemitax.legend(loc='upper center', fancybox=True, shadow=True)
            # # self.fitx, self.tmpx = curve_fit(self.gaussFit, self.x, self.sigmaX, p0=[1, 20, 10])
            # # self.ax.plot(self.x, self.gaussFit(self.x, *self.fitx), 'ro:', label='fitxs')
            # # self.fity, self.tmpy = curve_fit(self.gaussFit, self.y, self.sigmaY, p0=[1, 20, 10])
            # # self.ax.plot(self.y, self.gaussFit(self.y, *self.fity), 'ro:', label='fitys')
            # self.xemitax.set_aspect('auto')
            # self.yemitax.set_aspect('auto')
            # self.xemitplotfig.canvas.draw()
            # self.yemitplotfig.canvas.draw()