#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DJS 2017
# part of MagtnetApp
from PyQt4 import QtGui, QtCore
from viewSource.Ui_mainView import Ui_mainView
#import magnetAppGlobals as globals
import numpy as np
from epics import caget
import pyqtgraph as pg

class mainView(QtGui.QMainWindow, Ui_mainView ):
    closing = QtCore.pyqtSignal()# custom close signal to send to controller


    def __init__(self):
        monitor = pg.GraphicsView()
        layout = pg.GraphicsLayout(border=(100, 100, 100))
        monitor.setCentralItem(layout)

        QtGui.QWidget.__init__(self)
        # startup crap
        self.setupUi(self)
        self.setWindowTitle("VELA - CLARA Virtual Cathode Setup")

        self.roi = pg.EllipseROI([0, 0], [500, 500], movable=False)

        # image stuff ...
        self.Image = pg.ImageItem(np.random.normal(size=(1280, 1080)))
        self.Image.scale(1,1)
        self.ImageBox = layout.addPlot(lockAspect=True)
        self.imageLayout.addWidget(monitor, 0, 2, 23, 3)
        STEPS = np.linspace(0, 1, 4)
        CLRS = ['k', 'r', 'y', 'w']
        a = np.array([pg.colorTuple(pg.Color(c)) for c in CLRS])
        clrmp = pg.ColorMap(STEPS, a)
        lut = clrmp.getLookupTable()
        self.Image.setLookupTable(lut)
        self.ImageBox.setRange(xRange=[0,1080],yRange=[0,1280])
        self.ImageBox.addItem(self.Image)
        self.getNewImage()
        self.addROIEllipse()


        # connect up ellipse boxes
        self.maskX_spinBox.valueChanged.connect(self.changeEllipse)
        self.maskY_spinBox.valueChanged.connect(self.changeEllipse)
        self.maskXRadius_spinBox.valueChanged.connect(self.changeEllipse)
        self.maskYRadius_spinBox.valueChanged.connect(self.changeEllipse)


    def getNewImage(self):
        data = caget('CLA-VCA-DIA-CAM-01:CAM2:ArrayData')
        print 'cagot'
        if data is not None:
            if len(data) == 1080 * 1280:
                    npData = np.array(data).reshape((1080, 1280))

            self.Image.setImage(np.flip(np.transpose(npData), 1))
            # self.Image.setLevels([self.view.spinBox_minLevel.value(),
            #                           self.view.spinBox_maxLevel.value()], update=True)

    def addROIEllipse(self):
        # print self.roi.handles[0]['item']
        #
        # self.roi.handleSize = 10
        # self.roi.removeHandle(self.roi.handles[0]['item'])
        self.roi.addTranslateHandle([0,0.5])
        #self.roi.addScaleHandle([1,1])
        self.ImageBox.addItem(self.roi)
        self.roi.sigRegionChangeFinished.connect(self.roiChanged)

    def roiChanged(self):
        x_rad,y_rad = 0.5 * self.roi.size()
        x,y = self.roi.pos() + [x_rad,y_rad]

        self.maskX_spinBox.setValue(x)
        self.maskY_spinBox.setValue(y)
        self.maskXRadius_spinBox.setValue(x_rad)
        self.maskYRadius_spinBox.setValue(y_rad)

    def changeEllipse(self):
        pass
        # x = self.maskX_spinBox.value() - self.maskXRadius_spinBox.value()
        # y = self.maskY_spinBox.value() - self.maskYRadius_spinBox.value()
        # xRad = 2 * self.maskXRadius_spinBox.value()
        # yRad = 2 * self.maskYRadius_spinBox.value()
        # point = QtCore.QPoint(x, y)
        # self.roi.setPos(point)
        # pointRad = QtCore.QPoint(xRad, yRad)
        # self.roi.setSize(pointRad)


#
    # collectAndSave_pushButton
    # last_filename
    # liveStream_pushButton
    # spinBox_maxLevel
    # spinBox_minLevel
    # maskX_spinBox_5
    # maskX_spinBox_4
    # int_read_2
    # int_spinBox_2
    # setPosition_pushButton
    # setInt_pushButton
    # setMask_pushButton_2
    # load_pushButton
    # save_pushButton_2
    # sum_val
    # sum_mean
    # sum_sd
    # x_val
    # x_mean
    # x_sd
    # y_val
    # y_mean
    # y_sd
    # sx_val
    # sx_mean
    # sx_sd
    # sy_val
    # sy_mean
    # sy_sd
    # cov_val
    # cov_mean
    # cov_sd
    # resetMeanSD_pushButton
    # analyse_pushButton
    # resetBackground_pushButton
    # useBackground_checkBox
    # useNPoint_checkBox
    # stepSize_spinBox
    # mask_x_read
    # maskX_spinBox
    # mask_y_read
    # maskY_spinBox
    # mas_y_rad
    # maskXRadius_spinBox
    # mask_y_rad
    # maskYRadius_spinBox
    # feed_back_check
    # setMask_pushButton
    # acquire_pushButton
    # numImages_spinBox
    # save_pushButton
    # getImages_pushButton
    # menubar
    # statusbar
    # liveStream_pushButton
    # spinBox_minLevel
    # spinBox_maxLevel
    # analyse_pushButton
    # resetBackground_pushButton
    # useBackground_checkBox
    # useNPoint_checkBox
    # stepSize_spinBox
    # maskX_spinBox
    # maskY_spinBox
    # maskXRadius_spinBox
    # maskYRadius_spinBox

    def closeEvent(self,event):
        self.closing.emit()

    def updateWidgets(self):
        pass


    def updateImage(self):
        pass

    def updateGraph(self):
        pass
