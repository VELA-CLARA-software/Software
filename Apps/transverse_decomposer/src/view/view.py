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
//  Last edit:   24-11-2020
//  FileName:    view.py
//  Description: GUI view for simple laser transverse profile  decomposition
//
//*/
'''
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow
from src.view.viewSource.Ui_view import Ui_view
import pyqtgraph as pg
from numpy import amax

class view(QMainWindow, Ui_view):
    '''
    '''
    # custom close signal to send to controller
    # closing = QtCore.pyqtSignal()
    # dictionary to access valve widgets keyed by their names
    valves = {}

    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)  # setup the UI frnm the base class
        #self.setWindowIcon(QIcon('icon.ico'))  # set icon
        self.red = "#ff5733"  # some colors labels for convenience
        self.green = "#75ff33"
        self.magerta = "#ff00ff"
        self.yellow = "#ffff00"
        print(__name__ + ', class initialized')
        # graphics_view is a GraphicsView from QT
        # add  a PlotItem to the graphics_view

        self.plot_item = pg.PlotItem()
        self.graphics_area.setCentralWidget(self.plot_item)
        #
        '''
            vc_image is an ImageItem, the camera image data to plot
            For backward compatibility, image data is assumed to be in column-major order (column, 
            row). However, most image data is stored in row-major order (row, column) and will 
            need 
            to be transposed before calling setImage():
            this should fix it  
            self.vc_image.setOpts(axisOrder='row-major')

            this means x is y and y is x   
        '''
        self.vc_image = pg.ImageItem(view=pg.PlotItem())





    def update_image(self, array_data, x_pix_scale_factor, y_pix_scale_factor ):
        '''
            Update graphics view with new image data
        :param array_data: chunked array to update image with
        :param x_pix_scale_factor: pix to mm
        :param y_pix_scale_factor: pix to mm
        '''
        print("update_image")
        self.vc_image.scale(x_pix_scale_factor, y_pix_scale_factor)
        self.vc_image.setOpts(axisOrder='row-major')
        self.vc_image.setImage(image=array_data, autoDownsample=True)
        self.vc_image.setLevels([0, amax(array_data)], update=True)
        print("update_image FIN")
