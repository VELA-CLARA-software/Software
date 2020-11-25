import os
import numpy
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
import scipy.ndimage
import h5py
from PyQt4 import QtGui, QtCore

class hdf5FileRead:

    def getHDF5Data(self, filename):
        self.filename = filename
        self.allfiles = []
        if self.filename.endswith('.hdf5'):
            print self.filename
            self.fh5 = h5py.File(self.filename, 'r')
            self.imgs = numpy.copy(numpy.array(self.fh5['fftAv']))
            self.attu = numpy.copy(numpy.array(self.fh5['attuAv']))
            QtGui.QApplication.processEvents()
            self.fh5.close()
        return self.imgs, self.attu

    def findAllHDF5FilesInDirectory(self, directory):
        self.directory = directory
        self.allfiles = []
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file.endswith('.hdf5'):
                    print file
                    self.allfiles.append(file)
                    QtGui.QApplication.processEvents()
        return self.allfiles


# raw_input("")