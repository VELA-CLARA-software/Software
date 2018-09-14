#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DJS 2017
# part of MagtnetApp
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QPushButton
from viewSource.Ui_mainView import Ui_mainView
from procedure.procedure import procedure
from VELA_CLARA_Vac_Valve_Control import VALVE_STATE
from numpy import random
import pyqtgraph as pg


class view(QMainWindow, Ui_mainView ):
    procedure = procedure()

    show_average = False

    def __init__(self):
        QWidget.__init__(self)
        self.my_name = 'view'
        self.setupUi(self)
        self.setWindowIcon(QIcon('resources\\quick_spec\\icon.ico'))
        #print(self.my_name + ', class initiliazed')
        self.plot_item = self.graphicsView.addPlot(lockAspect=True)
        self.plot_item.hideAxis('left')
        #self.plot_item.setRange(xRange=[0, self.xpix_full], yRange=[0, self.ypix_full])
        self.plot_item.setAspectLocked(True)

        self.image_item = pg.ImageItem(random.random((view.procedure.x_pix, view.procedure.y_pix)))
        # self.image_item.scale(self.data.values[ model.data.x_pix_scale_factor],
        #                     self.data.values[model.data.y_pix_scale_factor])
        self.plot_item.addItem(self.image_item)

        #self.image_item = pg.ImageItem(random.random((view.procedure.x_pix, view.procedure.y_pix)))

        self.plot_item.setRange(xRange=[0, view.procedure.x_pix], yRange=[0, view.procedure.y_pix])
        self.plot_item.setAspectLocked(True)
        self.plot_item.setLimits(xMin=0, xMax=view.procedure.x_pix, yMin=0,
                                 yMax=view.procedure.y_pix,
                                 minXRange=10, maxXRange=view.procedure.x_pix, minYRange=10,
                                 maxYRange=view.procedure.y_pix)

        self.x_proj_plot = self.x_proj.addPlot(lockAspect=True)
        self.my_x_plot = self.x_proj_plot.plot()

        self.y_proj_plot = self.y_proj.addPlot(lockAspect=True)
        self.my_y_plot = self.y_proj_plot.plot()

    def update_gui(self):
        # print 'update_image'
        self.image_item.setImage(image=view.procedure.last_image,autoDownsample=True)

        if self.average_cbox.isChecked():
            print 'show average'
            self.my_x_plot.setData( view.procedure.x_proj_mean )
            self.my_y_plot.setData( y=procedure.y_coords ,x=view.procedure.y_proj_mean )
        else:
            print 'DO NOT show average'
            self.my_x_plot.setData( view.procedure.x_proj)
            self.my_y_plot.setData( y=procedure.y_coords ,x=view.procedure.y_proj )

        self.cam_name_text.setText(procedure.current_cam)