# uncompyle6 version 2.10.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.10 (default, May 23 2015, 09:40:32) [MSC v.1500 32 bit (Intel)]
# Embedded file name: D:\VELA-CLARA_software\Software\matlabImageViewer\control\matlabImageViewerMasterController.py
# Compiled at: 2017-06-01 15:51:09
import os
import sys
import numpy
import scipy.io
from PyQt4 import QtCore, QtGui
from file_manager.matlabFileWriter import matlabFileWriter
from file_manager.matlabFileRead import matlabFileRead
from view.matlabImageView import matlabImageView
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt
import time

class matlabImageViewerMasterController(object):

    def __init__(self):
        self.fileRead = matlabFileRead()
        self.maindict = {}
        self.isDirectorySet = False
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
        self.startView.getDirectoryButton.clicked.connect(self.setDirectory)
        #self.startView.loadFilesButton.clicked.connect(self.loadFiles)
        self.startView.readFilesButton.clicked.connect(self.readFiles)
        self.startView.loadFileButton.clicked.connect(self.loadFile)
        self.startView.filekeychanged.connect(self.keyIndexChanged)
        self.startView.makePlotsButton.clicked.connect(self.loadPlots)
        self.startView.fileSlider.valueChanged[int].connect(self.scrollPlots)
        self.startView.clearPlotsButton.clicked.connect(self.clearPlots)

    @QtCore.pyqtSlot()
    def fileChanged(self):
        self.isFileChanged = self.startView.isfilechanged
        print self.isFileChanged

    @QtCore.pyqtSlot()
    def setDirectory(self):
        path = QtGui.QFileDialog.getExistingDirectory(None, 'Pick a Folder', 'D:\\FERMI\\Data')
        if path:
            self.startView.getDirectoryLineEdit.setText(path)
            self.isDirectorySet = True
        return

    def readFiles(self):
        self.startView.allFilesComboBox.clear()
        self.directory = str(self.startView.getDirectoryLineEdit.text() + '\\')
        if self.isDirectorySet:
            self.allFiles = self.fileRead.findAllFilesInDirectory(self.directory)
            self.isFilesLoaded = True
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
        self.clearPlots()
        self.directory = str(self.startView.getDirectoryLineEdit.text() + '\\')
        if self.isDirectorySet:
            self.currentFile = self.fileRead.getMatlabData(self.directory+str(self.startView.allFilesComboBox.currentText()))
            self.isFilesLoaded = True
        print 'loaded all files'
        self.addKey(self.currentFile)
        return self.currentFile

    def addKey(self, data):
        self.startView.keysComboBox.clear()
        self.data = data
        for key in self.data.keys():
            self.startView.keysComboBox.addItem(key)

    def keyIndexChanged(self, keyname):
        self.keyname = str(keyname)
        self.keyvalue = self.currentFile[self.keyname]
        if isinstance(self.keyvalue, dict):
            self.keylist = []
            self.startView.viewKeysText.setPlainText(self.keyname + ' :')
            for key, value in self.keyvalue.iteritems():
                self.keylist.append(key)
                self.values = []
                if isinstance(value, list):
                    for i in value:
                        self.values.append(str(i))
                        if i > 1:
                            self.values.append(', ...')
                            break

                    self.values.append(' --- length ' + str(len(value)))
                    self.startView.viewKeysText.appendPlainText(' ' + key + ' : ' + ''.join(self.values))
                else:
                    self.startView.viewKeysText.appendPlainText(' ' + key + ' : ' + str(value))

        elif isinstance(self.keyvalue, list):
            self.elemlist = []
            self.startView.viewKeysText.setPlainText(self.keyname + ' : ')
            for elem in self.keyvalue:
                self.elemlist.append(elem)

        else:
            self.startView.viewKeysText.setPlainText(self.keyname + ' : ' + self.keyvalue)


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
            self.allplots[i].canvas.draw()

        self.plotsLoaded = True
        self.startView.fileSlider.setMaximum(self.numshots - 1)
        self.startView.fileSlider.setValue(self.numshots - 1)
        return self.allplots

    def scrollPlots(self, index):
        self.index = index
        if self.plotsLoaded:
            self.plotfig = self.startView.plotWidget
            self.plotfigure = self.startView.makePlots(self.currentFile, self.datastruct,
                                                       self.imagedata, self.arrayshape, self.index, self.plotfig)
            self.plotfigure.canvas.draw()
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