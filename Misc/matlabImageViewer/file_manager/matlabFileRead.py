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
        #self.matlabData = self.loadmat1(self.filename)
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
        self.filetype = filetype
        self.dict = {}
        self.index = 0
        for strg in matobj._fieldnames:
            self.elem = matobj.__dict__[strg]
            if isinstance(self.elem, scipy.io.matlab.mio5_params.mat_struct):
                self.dict[strg] = self._todict(self.elem, self.filetype)
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

    def print_mat_nested(self, d, indent=0, nkeys=0):
        """Pretty print nested structures from .mat files   
        Inspired by: `StackOverflow <http://stackoverflow.com/questions/3229419/pretty-printing-nested-dictionaries-in-python>`_
        """

        # Subset dictionary to limit keys to print.  Only works on first level
        self.d = d
        self.indent = indent
        self.nkeys = nkeys
        if self.nkeys > 0:
            self.d = {k: self.d[k] for k in self.d.keys()[:self.nkeys]}  # Dictionary comprehension: limit to first nkeys keys.

        if isinstance(self.d, dict):
            for key, value in self.d.iteritems():  # iteritems loops through key, value pairs
                print '\t' * self.indent + 'Key: ' + str(key)
                self.print_mat_nested(value, indent + 1)

        if isinstance(self.d, numpy.ndarray) and self.d.dtype.names is not None:  # Note: and short-circuits by default
            for n in self.d.dtype.names:  # This means it's a struct, it's bit of a kludge test.
                print '\t' * self.indent + 'Field: ' + str(n)
                self.print_mat_nested(self.d[n], self.indent + 1)

    def loadmat1(self, filename):
        '''
        this function should be called instead of direct spio.loadmat
        as it cures the problem of not properly recovering python dictionaries
        from mat files. It calls the function check keys to cure all entries
        which are still mat-objects
    
        from: `StackOverflow <http://stackoverflow.com/questions/7008608/scipy-io-loadmat-nested-structures-i-e-dictionaries>`_
        '''
        self.data = scipy.io.loadmat(filename, struct_as_record=False, squeeze_me=True)
        return self._check_keys1(self.data)

    def _check_keys1(self, dict):
        '''
        checks if entries in dictionary are mat-objects. If yes
        todict is called to change them to nested dictionaries
        '''
        self.dict = dict
        for key in self.dict:
            if isinstance(self.dict[key], scipy.io.matlab.mio5_params.mat_struct):
                self.dict[key] = self._todict1(self.dict[key])
        return self.dict

    def _todict1(self, matobj):
        '''
        A recursive function which constructs from matobjects nested dictionaries
        '''
        self.dictt = {}
        self.matobj = matobj
        for strg in self.matobj._fieldnames:
            self.elem = self.matobj.__dict__[strg]
            if isinstance(self.elem, scipy.io.matlab.mio5_params.mat_struct):
                self.dictt[strg] = self._todict1(self.elem)
            elif isinstance(self.elem, numpy.ndarray):
                self.parameter_list = []
                self.dictt[strg] = self._tolist(self.elem, self.parameter_list)
            else:
                print type(self.elem)
                print strg
                self.dictt[strg] = self.elem
        return self.dictt

