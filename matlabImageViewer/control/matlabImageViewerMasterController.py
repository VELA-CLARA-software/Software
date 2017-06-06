# uncompyle6 version 2.10.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.10 (default, May 23 2015, 09:40:32) [MSC v.1500 32 bit (Intel)]
# Embedded file name: D:\VELA-CLARA_software\Software\matlabImageViewer\control\matlabImageViewerMasterController.py
# Compiled at: 2017-06-01 15:51:09
import os
import sys
import numpy
from scipy.optimize import curve_fit
from PyQt4 import QtCore, QtGui
from file_manager.matlabFileWriter import matlabFileWriter
from file_manager.matlabFileRead import matlabFileRead
from view.matlabImageView import matlabImageView
from matplotlib.backend_bases import key_press_handler
from matplotlib.backend_bases import MouseEvent
import matplotlib.pyplot as plt
import time

class matlabImageViewerMasterController(object):

    def __init__(self):
        self.fileRead = matlabFileRead()
        self.maindict = {}
        self.isDirectorySet = False
        self.isFileSet = False
        self.isFilesLoaded = False
        self.isFilenamesAdded = False
        self.isArraySizeSet = False
        self.isFileChanged = False
        self.fileWriter = matlabFileWriter()
        self.filenamestr = 'filename'
        self.datastruct = 'img2save'
        self.imagedata = 'immagini'
        self.arrayshape = [520, 262, 20]
        self.startView = matlabImageView()
        self.startView.show()
        self.startView.getDirectoryButton.clicked.connect(self.setDirOrFile)
        #self.startView.loadFilesButton.clicked.connect(self.loadFiles)
        self.startView.readFilesButton.clicked.connect(self.readFiles)
        self.startView.loadFileButton.clicked.connect(self.loadFile)
        self.startView.filekeychanged.connect(self.keyIndexChanged)
        self.startView.subfilekeychanged.connect(self.subKeyIndexChanged)
        self.startView.subsubfilekeychanged.connect(self.subSubKeyIndexChanged)
        self.startView.makePlotsButton.clicked.connect(self.loadPlots)
        self.startView.fileSlider.valueChanged[int].connect(self.scrollPlots)
        self.startView.clearPlotsButton.clicked.connect(self.clearPlots)
        self.startView.makeAnalysisPlotButton.clicked.connect(self.analyseData)
        #self.startView.averagingGroupBox.changeEvent.connect(self.enableAveraging)
        #self.startView.makeAnalysisPlotButton.clicked.connect(self.makeAnalysisPlot)
        self.startView.canvas.mpl_connect('button_press_event', self.on_mouse_press)
        self.startView.canvas.mpl_connect('button_release_event', self.on_mouse_release)

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

    @QtCore.pyqtSlot()
    def fileChanged(self):
        self.isFileChanged = self.startView.isfilechanged
        print self.isFileChanged

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

    def enableAveraging(self):
        if self.startView.noAvg.isChecked():
            self.startView.intervalText.isReadOnly = True
            self.startView.intervalText.clear()
        else:
            self.startView.intervalText.isReadOnly = False
        return

    def readFiles(self):
        self.startView.allFilesComboBox.clear()
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

    def loadFile(self):
        self.startView.viewKeysText.clear()
        self.startView.keysComboBox.clear()
        self.startView.subKeysComboBox.clear()
        self.startView.subSubKeysComboBox.clear()
        self.clearPlots()
        self.directory = str(self.startView.getDirectoryLineEdit.text() + '\\')
        if self.isDirectorySet:
            self.currentFile = self.fileRead.getMatlabData(self.directory+str(self.startView.allFilesComboBox.currentText()))
            self.isFilesLoaded = True
        elif self.isFileSet:
            self.currentFile = self.fileRead.getMatlabData(str(self.startView.getDirectoryLineEdit.text()))
        print 'loaded all files'
        self.addKey(self.currentFile)
        return self.currentFile

    def addKey(self, data):
        self.startView.keysComboBox.clear()
        self.data = data
        for key, value in self.data.iteritems():
            self.startView.keysComboBox.addItem(key)
            # if isinstance(value, dict):
            #     for subkey in value.keys():
            #         self.startView.subKeysComboBox.addItem(subkey)

    def keyIndexChanged(self, keyname):
        self.keyname = str(keyname)
        self.keyvalue = self.currentFile[self.keyname]
        if isinstance(self.keyvalue, dict):
            self.keylist = []
            self.startView.viewKeysText.setPlainText(self.keyname + ' :')
            self.startView.subKeysComboBox.clear()
            for key, value in self.keyvalue.iteritems():
                self.startView.subKeysComboBox.addItem(key)
                # self.keylist.append(key)
                # self.values = []
                # if isinstance(value, list):
                #     for i in value:
                #         self.values.append(str(i))
                #         if i > 1:
                #             self.values.append(', ...')
                #             break
                #
                #     self.values.append(' --- length ' + str(len(value)))
                #     self.startView.viewKeysText.appendPlainText(' ' + key + ' : ' + ''.join(self.values))
                # else:
                #     self.startView.viewKeysText.appendPlainText(' ' + key + ' : ' + str(value))

        elif isinstance(self.keyvalue, list):
            self.elemlist = []
            self.startView.subKeysComboBox.clear()
            self.startView.subSubKeysComboBox.clear()
            self.startView.viewKeysText.setPlainText(self.keyname + ' : ')
            for elem in self.keyvalue:
                self.elemlist.append(elem)

        else:
            self.startView.viewKeysText.setPlainText(self.keyname + ' : ' + self.keyvalue)

    def subKeyIndexChanged(self, keyname):
        self.keyname = str(keyname)
        self.keyvalue = self.currentFile[str(self.startView.keysComboBox.currentText())][self.keyname]
        print type(self.keyvalue)
        self.startView.subSubKeysComboBox.clear()
        if isinstance(self.keyvalue, dict):
            self.keylist = []
            self.startView.subSubKeysComboBox.clear()
            self.startView.viewKeysText.setPlainText(self.keyname + ' :')
            for key, value in self.keyvalue.iteritems():
                self.startView.subSubKeysComboBox.addItem(key)
                # self.keylist.append(key)
                # self.values = []
                # if isinstance(value, list):
                #     for i in value:
                #         self.values.append(str(i)+", ")
                #         if len(self.values) > 20:
                #             self.values.append(', ...')
                #             break
                #
                #     self.values.append(' --- length ' + str(len(value)))
                #     self.startView.viewKeysText.appendPlainText(' ' + key + ' : ' + ''.join(self.values))
                # else:
                #     self.startView.viewKeysText.appendPlainText(' ' + key + ' : ' + str(value))
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


    def addFilesToList(self, directory):
        self.directory = directory
        for i in self.maindict[self.directory]:
            self.startView.allFilesComboBox.addItem(i['filename'])

        self.isFilenamesAdded = True
        print 'filenames added'
        self.addKeys()

    def loadPlots(self):
        self.allplots = []
        self.arrayshape = []
        self.numshots = self.currentFile['img2save']['numshots']
        self.arrayshape.append(self.currentFile['img2save']['arrayy'])
        self.arrayshape.append(self.currentFile['img2save']['arrayx'])
        self.arrayshape.append(self.numshots)
        self.allplots = []
        for i in range(0, self.numshots):
            self.plotfig = self.startView.plotWidget
            self.allplots.append(
                self.startView.makePlots(self.currentFile, self.datastruct,
                                         self.imagedata, self.arrayshape, i, self.plotfig))
            self.allplots[i][0].canvas.draw()

        self.plotsLoaded = True
        self.startView.fileSlider.setMaximum(self.numshots - 1)
        self.startView.fileSlider.setValue(self.numshots - 1)
        self.index = self.numshots - 1
        self.croppedArrayShape = [0, self.arrayshape[1], 0, self.arrayshape[0]]
        return self.allplots

    def makeAnalysisPlot(self):
        self.croppedplotfig = self.startView.analysisPlotWidget
        self.croppedPlot = self.startView.drawAnalysisPlot(self.currentFile, self.datastruct, self.imagedata, self.arrayshape, self.index, self.croppedplotfig, self.croppedArrayShape)
        self.croppedplotfig.canvas.draw()
        return self.croppedplotfig

    def analyseData(self):
        self.data = self.currentFile[self.datastruct][self.imagedata]
        self.newdata = numpy.reshape(self.data, self.arrayshape)
        self.croppedplotfig = self.startView.analysisPlotWidget
        self.croppedplotfig.canvas.flush_events()
        self.startView.analysisaxis.cla()
        # self.croppedPlot = self.startView.drawAnalysisPlot(self.currentFile, self.datastruct, self.imagedata,
        #                                                    self.arrayshape, self.index, self.croppedplotfig,
        #                                                    self.croppedArrayShape)
        # self.croppedplotfig.canvas.draw()
        self.xCropMax = max(self.croppedArrayShape[:2])
        self.xCropMin = min(self.croppedArrayShape[:2])
        self.yCropMax = max(self.croppedArrayShape[2:])
        self.yCropMin = min(self.croppedArrayShape[2:])
        self.croppeddata = numpy.transpose(numpy.transpose(self.newdata)[self.index][self.xCropMin:self.xCropMax])[self.yCropMin:self.yCropMax]
        self. i = 0
        self.sigmaY = []
        self.sigmaYAvg = []
        self.yAvg = []
        self.newarray = []
        self.x = range(0, self.xCropMax - self.xCropMin)
        self.y = range(0, self.yCropMax - self.yCropMin)
        for slice_2d in self.croppeddata:
            self.n = len(slice_2d)  # the number of data
            self.mean = sum(slice_2d) / self.n  # note this correction
            self.sigma = sum(slice_2d * (self.mean) ** 2) / self.n
            # self.fit, self.tmp = curve_fit(self.gaussFit, self.x, slice_2d, p0=[max(slice_2d), self.mean, self.sigma])
            self.sigmaY.append(self.sigma)
        if self.startView.averaging.isChecked():
            self.averagingInterval = int(self.startView.intervalText.toPlainText())
            for i in range(0, len(self.sigmaY), self.averagingInterval):
                if not (len(self.sigmaY) - i) < self.averagingInterval:
                    self.sigmaYAvg.append(numpy.mean(self.sigmaY[i:i + self.averagingInterval]))
                    self.yAvg.append(numpy.mean(self.y[i:i + self.averagingInterval]))
                else:
                    self.sigmaYAvg.append(numpy.mean(self.sigmaY[i:-1]))
                    self.yAvg.append(numpy.mean(self.y[i:i - 1]))
            self.ax = self.croppedplotfig.add_subplot(111)
            self.newarray = numpy.vstack((self.yAvg, self.sigmaYAvg))
            self.ax.plot(self.newarray[0], self.newarray[1])
            self.ax.set_aspect('auto')
            self.croppedplotfig.canvas.draw()
        elif self.startView.noAvg.isChecked():
            self.ax = self.croppedplotfig.add_subplot(111)
            self.newarray = numpy.vstack((self.y, self.sigmaY))
            self.ax.plot(self.newarray[0], self.newarray[1])
            self.ax.set_aspect('auto')
            self.croppedplotfig.canvas.draw()
        else:
            print "choose a bloody thing"

    def gaussFit(self, x, a, x0, sigma):
        self.x = x
        self.a = a
        self.x0 = x0
        self.sigma = sigma
        return self.a * numpy.exp(-(self.x - self.x0) ** 2 / (2 * self.sigma ** 2))

    def scrollPlots(self, index):
        self.index = index
        if self.plotsLoaded:
            self.plotfig = self.startView.plotWidget
            self.plotfigure = self.startView.makePlots(self.currentFile, self.datastruct,
                                                       self.imagedata, self.arrayshape, self.index, self.plotfig)
            self.plotfigure[0].canvas.draw()
        else:
            print 'plots not loaded'

    def clearPlots(self):
        self.startView.plotWidget.canvas.flush_events()

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