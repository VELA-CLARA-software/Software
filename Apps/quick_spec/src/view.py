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
from procedure import procedure
from VELA_CLARA_Vac_Valve_Control import VALVE_STATE
from numpy import random
import pyqtgraph as pg
import data as data


class view(QMainWindow, Ui_mainView ):

    show_average = False

    data = None

    def __init__(self):
        QWidget.__init__(self)
        self.my_name = 'view'
        view.data = data.data()
        self.setupUi(self)
        self.setWindowIcon(QIcon('resources\\quick_spec\\icon.ico'))
        #print(self.my_name + ', class initiliazed')

        #pg.setConfigOptions(imageAxisOrder ='row-major' )
        pg.setConfigOptions(imageAxisOrder ='col-major' )

        self.plot_item = self.graphicsView.addPlot(lockAspect=True)
        self.plot_item.hideAxis('left')
        #self.plot_item.setRange(xRange=[0, self.xpix_full], yRange=[0, self.ypix_full])
        self.plot_item.setAspectLocked(True)

        self.image_item = pg.ImageItem(random.random((view.data.values[data.num_x_pix],
                                                      view.data.values[data.num_y_pix])))
        # self.image_item.scale(self.data.values[ model.data.x_pix_scale_factor],
        #                     self.data.values[model.data.y_pix_scale_factor])
        self.plot_item.addItem(self.image_item)


        #self.image_item = pg.ImageItem(random.random((view.procedure.x_pix, view.procedure.y_pix)))

        # self.plot_item.setRange(xRange=[0, view.procedure.x_pix], yRange=[0, view.procedure.y_pix])
        # self.plot_item.setAspectLocked(True)

        self.roi = pg.ROI([100, 100], [100, 100])
        self.roi.addScaleHandle([0.5, 1], [0.5, 0.5])
        self.roi.addScaleHandle([0, 0.5], [0.5, 0.5])
        self.plot_item.addItem(self.roi)

        self.x_proj_plot = self.x_proj.addPlot(lockAspect=True)
        self.x_curve1 = self.x_proj_plot.plot()
        self.x_curve2 = self.x_proj_plot.plot(pen=1)

        self.y_proj_plot = self.y_proj.addPlot(lockAspect=True)
        self.y_curve1 = self.y_proj_plot.plot()
        self.y_curve2 = self.y_proj_plot.plot(pen=1)

        self.x_proj_plot_lo_line = self.x_proj_plot.addLine(x=self.data.values[data.fwhm_lo])
        self.x_proj_plot_hi_line = self.x_proj_plot.addLine(x=self.data.values[data.fwhm_hi])


    def update_gui(self):

        # print 'update_image'
        self.image_item.setImage(image=view.data.values[data.image_data],autoDownsample=True)

        y_coords = range(len(view.data.values[data.y_proj]))

        self.x_curve1.setData(view.data.values[data.x_proj])
        self.y_curve1.setData(y = y_coords,
                              x = view.data.values[data.y_proj])

        if view.data.values[data.has_ref]:
            if view.data.values[data.ref_plotted]:
                pass
            else:
                self.x_curve2.setData(view.data.values[data.x_ref])
                self.y_curve2.setData(y =y_coords,
                                  x = view.data.values[data.y_ref])
                self.x_curve2.show()
                self.y_curve2.show()
                view.data.values[data.ref_plotted] = True
        else:
            self.x_curve2.hide()
            self.y_curve2.hide()

        self.cam_name_text.setText(view.data.values[data.current_cam])

        self.plot_item.setLimits(xMin = 0, xMax = view.data.values[data.num_x_pix],
                                 yMin = 0, yMax = view.data.values[data.num_y_pix],
                                 minXRange = 10, maxXRange=view.data.values[data.num_x_pix],
                                 minYRange = 10, maxYRange=view.data.values[data.num_y_pix])


        self.x_proj_plot_lo_line.setValue( v = self.data.values[data.fwhm_lo])
        self.x_proj_plot_hi_line.setValue( v = self.data.values[data.fwhm_hi])


        if self.max_text.hasFocus():
            pass
        else:
            self.max_text.setText( str( int(view.data.values[data.x_proj_max]) ))


        if self.max_pos_text.hasFocus():
            pass
        else:
            self.max_pos_text.setText(str(view.data.values[data.x_proj_max_index]))

        if self.fwhm_text.hasFocus():
            pass
        else:
            self.fwhm_text.setText( str( view.data.values[data.fwhm]) )



