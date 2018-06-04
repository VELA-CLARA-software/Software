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

import  model.data

mask_x_user  = 'mask_x_user'
mask_y_user  = 'mask_y_user'
mask_x_rad_user  = 'mask_x_rad_user'
mask_y_rad_user  = 'mask_y_rad_user'
mask_feedback = 'mask_feedback'
# imageCollection
num_images = 'num_images'
is_collecting_or_saving = 'is_collecting_or_saving'
last_filename = 'last_filename'

#imageview
is_acquiring = 'is_acquiring'
is_liverstream = 'is_liverstream'
min_level = 'min_level'
max_level = 'max_level'
# imageAnalysis
is_analysing = 'is_analysing'
use_background  = 'use_background'
use_npoint  = 'use_npoint'
ana_step_size = 'ana_step_size'


class mainView(QtGui.QMainWindow, Ui_mainView ):
    print('mainView')
    closing = QtCore.pyqtSignal()# custom close signal to send to controller

    def __init__(self):
        print('mainView init')
        monitor = pg.GraphicsView()
        layout = pg.GraphicsLayout(border=(100, 100, 100))
        monitor.setCentralItem(layout)

        QtGui.QWidget.__init__(self)

        self.data = model.data.data()

        # startup crap
        self.setupUi(self)
        self.setWindowTitle("VELA - CLARA Virtual Cathode Setup")


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

        #read roi
        self.roi2 = pg.EllipseROI([0, 0], [500, 500], movable=False)
        self.ImageBox.addItem(self.roi2)

        # user roi
        self.roi = pg.EllipseROI([0, 0], [500, 500], movable=False)


        self.addROIEllipse()


        # connect up ellipse boxes
        self.maskX_spinBox.valueChanged.connect(self.changeEllipse)
        self.maskY_spinBox.valueChanged.connect(self.changeEllipse)
        self.maskXRadius_spinBox.valueChanged.connect(self.changeEllipse)
        self.maskYRadius_spinBox.valueChanged.connect(self.changeEllipse)
        self.set_widget_name_dict()



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

    def update_gui(self):
        print 'update_gui'
        for key, value in self.widget_to_dataname.iteritems():
            if isinstance(self.data.values[value],float):
                key.setText("%.2f" % self.data.values[value])
            elif key == self.imageLayout:
                print 'imageLayout'
                self.Image.setImage(self.data.values[value])
                self.Image.setLevels([self.spinBox_minLevel.value(),
                                     self.spinBox_maxLevel.value()], update=True)
            elif key == self.mask_x_read:
                self.update_raed_roi()
            elif key == self.opencloseShut_pushButton:
                if self.data.values[value]:
                    key.setStyleSheet("background-color: green")
                    key.setText("CLOSE SHUTTER")
                else:
                    key.setStyleSheet("background-color: red")
                    key.setText("OPEN SHUTTER")
            elif key == self.acquire_pushButton:
                if self.data.values[value]:
                    key.setStyleSheet("background-color: green")
                    key.setText("STOP ACQUIRING")
                else:
                    key.setStyleSheet("background-color: red")
                    key.setText("START ACQUIRING")

            elif key == self.analyse_pushButton:
                if self.data.values[value]:
                    key.setStyleSheet("background-color: green")
                    key.setText("STOP ANALYZING")
                else:
                    key.setStyleSheet("background-color: red")
                    key.setText("START ANALYZING")

    def update_raed_roi(self):
        x = self.data.values[model.data.mask_x_rbv] - self.data.values[model.data.mask_x_rad_rbv]
        y = self.data.values[model.data.mask_y_rbv] - self.data.values[model.data.mask_y_rad_rbv]
        xRad = 2*self.data.values[model.data.mask_x_rad_rbv]
        yRad = 2*self.data.values[model.data.mask_y_rad_rbv]

        # make new ellipse here that track sRV ... #

        # point = QtCore.QPoint(x,y)
        # self.roi2.setPos(point)
        # pointRad = QtCore.QPoint(xRad,yRad)
        # self.roi2.setSize(pointRad)
        # #self.roi2.setColor('red')


    def set_widget_name_dict(self):
        self.widget_to_dataname = {}
        self.widget_to_dataname[self.x_val]=  model.data.x_val
        self.widget_to_dataname[self.x_mean]= model.data.x_mean
        self.widget_to_dataname[self.x_sd]= model.data.x_sd
        self.widget_to_dataname[self.y_val]= model.data.sy_val
        self.widget_to_dataname[self.y_mean]=model.data.y_mean
        self.widget_to_dataname[self.y_sd]=model.data.y_sd
        self.widget_to_dataname[self.sx_val]=model.data.sx_val
        self.widget_to_dataname[self.sx_mean]=model.data.sx_mean
        self.widget_to_dataname[self.sx_sd]=model.data.sx_sd
        self.widget_to_dataname[self.sy_val]=model.data.sy_val
        self.widget_to_dataname[self.sy_mean]=model.data.sy_mean
        self.widget_to_dataname[self.sy_sd]= model.data.sy_sd
        self.widget_to_dataname[self.cov_val]= model.data.cov_val
        self.widget_to_dataname[self.cov_mean]= model.data.cov_mean
        self.widget_to_dataname[self.cov_sd]= model.data.cov_sd
        self.widget_to_dataname[self.imageLayout]= model.data.image

        self.widget_to_dataname[self.mask_x_read]= model.data.mask_x_rbv
        self.widget_to_dataname[self.mask_y_read]= model.data.mask_y_rbv
        self.widget_to_dataname[self.mask_x_rad]= model.data.mask_x_rad_rbv
        self.widget_to_dataname[self.mask_y_rad]= model.data.mask_y_rad_rbv
        self.widget_to_dataname[self.opencloseShut_pushButton]= model.data.shutter_open
        self.widget_to_dataname[self.acquire_pushButton]= model.data.is_acquiring
        self.widget_to_dataname[self.analyse_pushButton]= model.data.is_analysing



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








    # def getNewImage(self):
    #     data = caget('CLA-VCA-DIA-CAM-01:CAM2:ArrayData')
    #     print 'cagot'
    #     if data is not None:
    #         if len(data) == 1080 * 1280:
    #                 npData = np.array(data).reshape((1080, 1280))
    #
    #         self.Image.setImage(np.flip(np.transpose(npData), 1))
            # self.Image.setLevels([self.view.spinBox_minLevel.value(),
            #                           self.view.spinBox_maxLevel.value()], update=True)

