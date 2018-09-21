'''
/*
//              This file is part of VELA-CLARA-Software.                             //
//------------------------------------------------------------------------------------//
//    VELA-CLARA-Software is free software: you can redistribute it and/or modify     //
//    it under the terms of the GNU General Public License as published by            //
//    the Free Software Foundation, either version 3 of the License, or               //
//    (at your option) any later version.                                             //
//    VELA-CLARA-Software is distributed in the hope that it will be useful,          //
//    but WITHOUT ANY WARRANTY; without even the implied warranty of                  //
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                   //
//    GNU General Public License for more details.                                    //
//                                                                                    //
//    You should have received a copy of the GNU General Public License               //
//    along with VELA-CLARA-Software.  If not, see <http://www.gnu.org/licenses/>.    //
//
//  Author:      DJS
//  Last edit:   21-09-2018
//  FileName:    view.py
//  Description: quick_spec main view
//
//
//*/
'''
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


    data = None

    def __init__(self):
        QWidget.__init__(self)
        self.my_name = 'view'
        view.data = data.data()
        self.setupUi(self)
        # belwo string should move to o global def file
        self.setWindowIcon(QIcon('resources\\quick_spec\\icon.ico'))

        pg.setConfigOptions(imageAxisOrder ='col-major' )

        self.plot_item = self.graphicsView.addPlot(lockAspect=True)
        self.plot_item.hideAxis('left')
        self.plot_item.setAspectLocked(True)

        self.image_item = pg.ImageItem(random.random((view.data.values[data.num_x_pix],
                                                      view.data.values[data.num_y_pix])))
        self.plot_item.addItem(self.image_item)

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

        # update main image
        self.image_item.setImage(image=view.data.values[data.image_data],autoDownsample=True)

        # projection ycoords
        y_coords = range(len(view.data.values[data.y_proj]))


        # projection latest data
        self.x_curve1.setData(view.data.values[data.x_proj])
        self.y_curve1.setData(y = y_coords,
                              x = view.data.values[data.y_proj])

        # do we have projection reference data?
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

        self.plot_item.setLimits(xMin = 0, xMax = view.data.values[data.num_x_pix],
                                 yMin = 0, yMax = view.data.values[data.num_y_pix],
                                 minXRange = 10, maxXRange=view.data.values[data.num_x_pix],
                                 minYRange = 10, maxYRange=view.data.values[data.num_y_pix])

        # update cam name
        self.cam_name_text.setText(view.data.values[data.current_cam])

        #update FWHM lines ..
        self.x_proj_plot_lo_line.setValue( v = self.data.values[data.fwhm_lo])
        self.x_proj_plot_hi_line.setValue( v = self.data.values[data.fwhm_hi])

        #update max, positino adn fwhm ... unless widgets have focus
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



