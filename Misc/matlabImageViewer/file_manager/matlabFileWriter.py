# uncompyle6 version 2.10.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.10 (default, May 23 2015, 09:40:32) [MSC v.1500 32 bit (Intel)]
# Embedded file name: D:\VELA-CLARA_software\Software\matlabFileConverter\file_manager\matlabFileWriter.py
# Compiled at: 2017-06-01 09:30:24
import os
import sys
import numpy
import scipy.io
import matplotlib.pyplot as plt

class matlabFileWriter:

    def __init__(self):
        self.fileWriterInit = True

    def writeFile(self, datafile, directory, filenamestr, datastruct, imagedata, arrayshape):
        self.datafile = datafile
        self.arrayshape = arrayshape
        self.filenamestr = filenamestr
        self.datastruct = datastruct
        self.imagedata = imagedata
        self.filename = self.datafile[self.filenamestr]
        print self.filename
        self.data = self.datafile[self.datastruct][self.imagedata]
        self.newdata = numpy.reshape(self.data, self.arrayshape)
        self.completename = os.path.join(directory, self.filename)
        with file(self.completename + '.dat', 'w') as outfile:
            for slice_2d in numpy.transpose(self.newdata):
                numpy.savetxt(outfile, slice_2d, fmt='%i')

    def key_event(self, e):
        global curr_pos
        if e.key == 'right':
            curr_pos = curr_pos + 1
        elif e.key == 'left':
            curr_pos = curr_pos - 1
        else:
            return
        curr_pos = curr_pos % len(self.allplots)
        self.ax.cla()
        self.ax.plot(allplots)
        self.fig.canvas.draw()