# uncompyle6 version 2.10.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.10 (default, May 23 2015, 09:40:32) [MSC v.1500 32 bit (Intel)]
# Embedded file name: D:\VELA-CLARA_software\Software\matlabFileConverter\file_manager\matlabFileRead.py
# Compiled at: 2017-06-01 15:21:39
import os
import sys
import numpy
import scipy.io
import time
from PyQt4 import QtGui, QtCore

class matlabFileRead:

    def loadAllDataInDirectory(self, directory, maindict):
        self.maindict = maindict
        self.directory = directory
        self.allfiles = []
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file.endswith('.mat'):
                    print file
                    self.allfiles.append(self.getMatlabData(root + file))
                    QtGui.QApplication.processEvents()

        self.maindict[self.directory] = self.allfiles
        return self.maindict

    def findAllFilesInDirectory(self, directory):
        self.directory = directory
        self.allfiles = []
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file.endswith('.mat') or file.endswith('.dat'):
                    print file
                    self.allfiles.append(file)
                    QtGui.QApplication.processEvents()
        return self.allfiles

    def findAFile(self, file):
        self.file = file
        self.allfiles = []
        if self.file.endswith('.mat') or self.file.endswith('.dat'):
            print self.file
            self.allfiles.append(self.file)
            QtGui.QApplication.processEvents()
        return self.allfiles

    def getMatlabData(self, filename, filetype):
        self.filename = filename
        self.matlabData = self.loadmat(self.filename, filetype)
        self.matlabData['filename'] = self.filename
        return self.matlabData

    def loadmat(self, filename, filetype):
        """
        this function should be called instead of direct spio.loadmat
        as it cures the problem of not properly recovering python dictionaries
        from mat files. It calls the function check keys to cure all entries
        which are still mat-objects
        """
        self.filetype = filetype
        self.data = scipy.io.loadmat(filename, struct_as_record=False, squeeze_me=True)
        return self._check_keys(self.data, self.filetype)

    def _check_keys(self, dict, filetype):
        """
        checks if entries in dictionary are mat-objects. If yes
        todict is called to change them to nested dictionaries
        """
        self.filetype = filetype
        for key in dict:
            if isinstance(dict[key], scipy.io.matlab.mio5_params.mat_struct):
                dict[key] = self._todict(dict[key], self.filetype)
        return dict

    def _todict(self, matobj, filetype):
        """
        A recursive function which constructs from matobjects nested dictionaries
        """
        self.allFigs = []
        self.filetype = filetype
        self.dict = {}
        self.index = 0
        for strg in matobj._fieldnames:
            self.elem = matobj.__dict__[strg]
            if isinstance(self.elem, scipy.io.matlab.mio5_params.mat_struct):
                self.dict[strg] = self._todict(self.elem)
            elif isinstance(self.elem, numpy.ndarray):
                self.parameter_list = []
                self.dict[strg] = self._tolist(self.elem, self.parameter_list)
                if self.filetype == ".mat":
                    if len(self.elem)>0:
                        if isinstance(self.elem[0], numpy.ndarray):
                            if strg == 'immagini':
                                self.dict['arrayx'] = len(self.elem[0])
                                self.dict['arrayy'] = len(self.elem)
                        if self.parameter_list:
                            if strg == 'immagini':
                                self.dict['numshots'] = len(self.parameter_list) / (len(self.elem[0]) * len(self.elem))
                elif self.filetype == ".dat":
                    self.parameter_list = []
                    self.dict[strg] = self._tolist(self.elem, self.parameter_list)
                    if strg == 'roi_points':
                        self.dict['arrayx'] = self.elem[2] - self.elem[0]
                        self.dict['arrayy'] = self.elem[3] - self.elem[1]
                    # if isinstance(self.elem[0], numpy.ndarray):
                    #     if self.parameter_list and self.dict['arrayx'] and self.dict['arrayy']:
                    #         self.dict['numshots'] = len(self.parameter_list) / (self.dict['arrayx'] * self.dict['arrayy'])

                else:
                    print "you done fucked up"
            else:
                self.dict[strg] = self.elem

        return self.dict

    def _tolist(self, ndarray, parameter_list):
        """
        A recursive function which constructs lists from cellarrays 
        (which are loaded as numpy ndarrays), recursing into the elements
        if they contain matobjects.
        """
        self.elem_list = parameter_list
        for sub_elem in ndarray:
            if isinstance(sub_elem, scipy.io.matlab.mio5_params.mat_struct):
                self.elem_list.append(self._todict(sub_elem))
            elif isinstance(sub_elem, numpy.ndarray):
                self._tolist(sub_elem, self.elem_list)
            else:
                self.elem_list.append(sub_elem)

        return self.elem_list