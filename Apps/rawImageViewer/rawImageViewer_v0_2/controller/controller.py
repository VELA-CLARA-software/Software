from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import Qt

import os
import time
import urllib
import webbrowser
import numpy as np
import pyqtgraph as pg

class Controller():

    def __init__(self, view, model):
        '''define model and view'''
        monitor = pg.GraphicsView()
        layout = pg.GraphicsLayout(border=(100, 100, 100))
        monitor.setCentralItem(layout)
        self.view = view
        self.model = model
        self.timer = QtCore.QTimer()
        self.view.pushButton.clicked.connect(self.openImageDir)
        
        self.ImageBox = layout.addViewBox(lockAspect=True, colspan=2)
        self.Image = pg.ImageItem(np.random.normal(size=(2560, 2160)))
        self.ImageBox.addItem(self.Image)
        self.view.gridLayout.addWidget(monitor, 0, 2, 5, 1)
        STEPS = np.linspace(0, 1, 4)
        CLRS = ['k', 'r', 'y', 'w']
        a = np.array([pg.colorTuple(pg.Color(c)) for c in CLRS])
        clrmp = pg.ColorMap(STEPS, a)
        lut = clrmp.getLookupTable()
        self.Image.setLookupTable(lut)
        '''Update GUI'''
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    def openImageDir(self):
        self.view.pushButton.setText('Loading...')
        filename = QtGui.QFileDialog.getOpenFileName(self.view.centralwidget, 'Image',
                                          '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\Work\\2017')
        f = open(filename, "r")
        a = np.fromfile(f, dtype=np.uint16)
        a = a.reshape((2160, 2560))
        imarray =np.array(a)
        self.Image.setImage(np.flip(np.transpose(imarray), 1))

    def update(self):
        self.Image.setLevels([self.view.spinBox_min.value(), self.view.spinBox_max.value()], update=True)