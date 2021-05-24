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
from numpy import array
from numpy import linspace
from math import ceil
from numpy import random
from src.view.viewSource.ellipseROIoverloads import EllipseROI_OneHandle
from src.view.viewSource.ellipseROIoverloads import EllipseROI_NoHandle


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

        self.full_plot_item = pg.PlotItem()
        self.roi_plot_item = pg.PlotItem()
        self.graphics_area_full.setCentralWidget(self.full_plot_item)
        self.graphics_area_ROI.setCentralWidget(self.roi_plot_item)
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
        self.roi_image = pg.ImageItem(view=pg.PlotItem())

        # a color map
        STEPS = linspace(0, 1, 4)
        CLRS = ['k', 'r', 'y', 'w']
        a = array([pg.colorTuple(pg.Color(c)) for c in CLRS])
        clrmp = pg.ColorMap(STEPS, a)
        lut = clrmp.getLookupTable()
        self.vc_image.setLookupTable(lut)
        self.roi_image.setLookupTable(lut)
        #
        # add the vc_image to the plot_item
        self.full_plot_item.addItem(self.vc_image)
        self.roi_plot_item.addItem(self.roi_image)
        '''
            limits and axes in pixels and mm
        '''
        self.border = 50
        self.full_plot_item.setLimits(xMin=0, xMax=1000,
                                 yMin=0, yMax=1000,
                                 minXRange=10,
                                 maxXRange=1000,
                                 minYRange=10,
                                 maxYRange=1000)
        self.full_plot_item.setRange(
            xRange=[-self.border, 1000 + self.border],
            yRange=[-self.border, 1000  + self.border])
        '''
            for axes we'll have pixels and mm, so customize the tick marks
            fairly cancerous below, but we only do it once ... 
        '''
        self.full_plot_item.showAxis('top')
        self.full_plot_item.showAxis('right')
        self.x_axis_u = self.full_plot_item.getAxis(name='top')
        self.x_axis_d = self.full_plot_item.getAxis(name='bottom')
        self.y_axis_l = self.full_plot_item.getAxis(name='left')
        self.y_axis_r = self.full_plot_item.getAxis(name='right')

        self.x_axis_u.setZValue(70000)  # MAGIC_NUMBER Higher than max bin value
        self.x_axis_d.setZValue(70000)  # MAGIC_NUMBER Higher than max bin value
        self.y_axis_l.setZValue(70000)  # MAGIC_NUMBER Higher than max bin value
        self.y_axis_r.setZValue(70000)  # MAGIC_NUMBER Higher than max bin value

        # like a lot of QT use a css to define label styles ... meh
        pixlabelStyle = {'color': 'yellow', 'font-size': '14pt'}
        mmlabelStyle = {'color': 'white', 'font-size': '14pt'}
        self.x_axis_d.setLabel(text='horizontal (pixel)', **pixlabelStyle)
        self.x_axis_u.setLabel(text='horizontal (mm)', **mmlabelStyle)
        self.y_axis_l.setLabel(text='vertical (pixel)', **pixlabelStyle)
        self.y_axis_r.setLabel(text='vertical (mm)', **mmlabelStyle)
        self.x_axis_d.setPen('y')
        self.y_axis_l.setPen('y')
        self.x_axis_u.setPen('w')
        self.y_axis_r.setPen('w')
        '''
            custom tick marks, mm on the up and right axes, plus custom tick positions
            more cancer ...  
        '''
        x_u_major_ticks = []
        y_r_major_ticks = []
        x_u_minor_ticks = []
        y_r_minor_ticks = []
        major_tick = 1
        minor_tick = 0.5

        x_pix_to_mm = 0.06
        y_pix_to_mm = 0.06
        xpix_full = 1000
        ypix_full = 1000

        x_range = int(ceil( xpix_full * x_pix_to_mm))
        y_range = int(ceil( ypix_full * y_pix_to_mm))
        x_pm = x_pix_to_mm
        y_pm = y_pix_to_mm

        for i in range(2 * x_range):
            x_u_major_ticks.append([i * major_tick / x_pm, str(i * major_tick)])
            x_u_minor_ticks.append([i * minor_tick / x_pm, str(i * minor_tick)])

        for i in range(2 * y_range):
            y_r_major_ticks.append([i * major_tick / y_pm, str(i * major_tick)])
            y_r_minor_ticks.append([i * minor_tick / y_pm, str(i * minor_tick)])

        self.x_axis_u.setTicks([x_u_major_ticks, x_u_minor_ticks])
        self.y_axis_r.setTicks([y_r_major_ticks, y_r_minor_ticks])

        # pixels on the left and down axes
        x_d_major_ticks = []
        y_l_major_ticks = []
        x_d_minor_ticks = []
        y_l_minor_ticks = []
        xmajor_tick = 512  # MAGIC_NUMBER
        xminor_tick = 256  # MAGIC_NUMBER
        ymajor_tick = 360  # MAGIC_NUMBER
        yminor_tick = 180  # MAGIC_NUMBER

        for i in range(10):  # MAGIC_NUMBER
            x_d_major_ticks.append([i * xmajor_tick, str(i * xmajor_tick)])
            x_d_minor_ticks.append([i * xminor_tick, str(i * xminor_tick)])

        for i in range(12):  # MAGIC_NUMBER
            y_l_major_ticks.append([i * ymajor_tick, str(i * ymajor_tick)])
            y_l_minor_ticks.append([i * yminor_tick, str(i * yminor_tick)])

        self.x_axis_d.setTicks([x_d_major_ticks, x_d_minor_ticks])
        self.y_axis_l.setTicks([y_l_major_ticks, y_l_minor_ticks])

        # rows = self.values[self.data.num_pix_y]
        # columns = self.values[self.data.num_pix_x]
        # t_data = random.normal(size=(rows, columns), loc = 30000, scale = 7000)

        self.full_plot_item.show()
        self.roi_plot_item.show()

        '''
            The masks from the image analysis are indicated by an ROI overlay
            they are initialised with dummy numbers adn updated to the latest read numbers with 
            user_roiChanged()
            for fun and experience i tried overloading ROIs
            read_roi has no handles users can drag, its just a read of what the current mask is
            user_roi, i.e the one that can be moved 
            we connect the user_roi signal to self.user_roiChanged the function to call when the 
            user has changed the mask 
         '''
        self.read_roi = EllipseROI_NoHandle([0, 0], [500, 500], movable=False, pen='g')
        self.user_roi = EllipseROI_OneHandle([0, 0], [500, 500], movable=False, pen='w')
        self.user_roi.sigHoverEvent.connect(self.user_roi_hashover)
        self.user_roi.addTranslateHandle([0, 0.5])
        self.user_roi.sigRegionChangeFinished.connect(self.user_roiChanged)
        # add to our plot item
        self.full_plot_item.addItem(self.read_roi)
        self.full_plot_item.addItem(self.user_roi)
        self.user_roiChanged()
        '''
            the analysis gives a mean position and width, indicated via cross hairs added to 
            plot_item
        '''
        self.v_cross_hair = pg.PlotDataItem()
        self.h_cross_hair = pg.PlotDataItem()
        self.v_cross_hair.setData(x=[1000, 1000], y=[900, 1100], pen='g')
        self.h_cross_hair.setData(x=[900, 1100], y=[1000, 1000], pen='g')
        self.full_plot_item.addItem(self.v_cross_hair)
        self.full_plot_item.addItem(self.h_cross_hair)
        '''
            limits and axes in pixels and mm
        '''
        border = 50
        # self.full_plot_item.setLimits(xMin=0, xMax=self.model_data.values[self.model_data.xpix_full],
        #                          yMin=0, yMax=self.model_data.values[self.model_data.ypix_full],
        #                          minXRange=10,
        #                          maxXRange=self.model_data.values[self.model_data.xpix_full],
        #                          minYRange=10,
        #                          maxYRange=self.model_data.values[self.model_data.ypix_full])
        # self.full_plot_item.setRange(
        #     xRange=[-border, self.model_data.values[self.model_data.xpix_full] + border], \
        #     yRange=[-border, self.model_data.values[self.model_data.ypix_full] + border])
        '''
            for axes we'll have pixels and mm, so customize the tick marks
            fairly cancerous below, but we only do it once ... 
        '''
        # self.full_plot_item.showAxis('top')
        # self.full_plot_item.showAxis('right')
        # self.x_axis_u = self.plot_item.getAxis(name='top')
        # self.x_axis_d = self.plot_item.getAxis(name='bottom')
        # self.y_axis_l = self.plot_item.getAxis(name='left')
        # self.y_axis_r = self.plot_item.getAxis(name='right')
        #
        # self.x_axis_u.setZValue(70000)  # MAGIC_NUMBER Higher than max bin value
        # self.x_axis_d.setZValue(70000)  # MAGIC_NUMBER Higher than max bin value
        # self.y_axis_l.setZValue(70000)  # MAGIC_NUMBER Higher than max bin value
        # self.y_axis_r.setZValue(70000)  # MAGIC_NUMBER Higher than max bin value
        #
        # # like a lot of QT use a css to define label styles ... meh
        # pixlabelStyle = {'color': 'yellow', 'font-size': '14pt'}
        # mmlabelStyle = {'color': 'white', 'font-size': '14pt'}
        # self.x_axis_d.setLabel(text='horizontal (pixel)', **pixlabelStyle)
        # self.x_axis_u.setLabel(text='horizontal (mm)', **mmlabelStyle)
        # self.y_axis_l.setLabel(text='vertical (pixel)', **pixlabelStyle)
        # self.y_axis_r.setLabel(text='vertical (mm)', **mmlabelStyle)
        # self.x_axis_d.setPen('y')
        # self.y_axis_l.setPen('y')
        # self.x_axis_u.setPen('w')
        # self.y_axis_r.setPen('w')
        '''
            custom tick marks, mm on the up and right axes, plus custom tick positions
            more cancer ...  
        '''
        x_u_major_ticks = []
        y_r_major_ticks = []
        x_u_minor_ticks = []
        y_r_minor_ticks = []
        major_tick = 1
        minor_tick = 0.5

        # x_range = int(ceil(
        #     self.model_data.values[self.model_data.xpix_full] * self.model_data.values[
        #         self.model_data.x_pix_to_mm]))
        # y_range = int(ceil(
        #     self.model_data.values[self.model_data.ypix_full] * self.model_data.values[
        #         self.model_data.y_pix_to_mm]))
        # x_pm = self.model_data.values[self.model_data.x_pix_to_mm]
        # y_pm = self.model_data.values[self.model_data.y_pix_to_mm]
        #
        # for i in range(2 * x_range):
        #     x_u_major_ticks.append([i * major_tick / x_pm, str(i * major_tick)])
        #     x_u_minor_ticks.append([i * minor_tick / x_pm, str(i * minor_tick)])
        #
        # for i in range(2 * y_range):
        #     y_r_major_ticks.append([i * major_tick / y_pm, str(i * major_tick)])
        #     y_r_minor_ticks.append([i * minor_tick / y_pm, str(i * minor_tick)])
        #
        # self.x_axis_u.setTicks([x_u_major_ticks, x_u_minor_ticks])
        # self.y_axis_r.setTicks([y_r_major_ticks, y_r_minor_ticks])
        #
        # # pixels on the left and down axes
        # x_d_major_ticks = []
        # y_l_major_ticks = []
        # x_d_minor_ticks = []
        # y_l_minor_ticks = []
        # xmajor_tick = 512  # MAGIC_NUMBER
        # xminor_tick = 256  # MAGIC_NUMBER
        # ymajor_tick = 360  # MAGIC_NUMBER
        # yminor_tick = 180  # MAGIC_NUMBER
        #
        # for i in range(10):  # MAGIC_NUMBER
        #     x_d_major_ticks.append([i * xmajor_tick, str(i * xmajor_tick)])
        #     x_d_minor_ticks.append([i * xminor_tick, str(i * xminor_tick)])
        #
        # for i in range(12):  # MAGIC_NUMBER
        #     y_l_major_ticks.append([i * ymajor_tick, str(i * ymajor_tick)])
        #     y_l_minor_ticks.append([i * yminor_tick, str(i * yminor_tick)])
        #
        # self.x_axis_d.setTicks([x_d_major_ticks, x_d_minor_ticks])
        # self.y_axis_l.setTicks([y_l_major_ticks, y_l_minor_ticks])

    def user_roiChanged(self):
        '''
            I think analysis x,y from the VC are swopped .. ?
        :return:
        '''
        print('user_roiChanged called')
        x_rad, y_rad = 0.5 * self.user_roi.size()
        x, y = self.user_roi.pos() + [x_rad, y_rad]
        # self.maskX_spinBox.setValue(x)
        # self.maskY_spinBox.setValue(y)
        # self.maskXRadius_spinBox.setValue(x_rad)
        # self.maskYRadius_spinBox.setValue(y_rad)
        # self.setMask_pushButton.click()


    def user_roi_hashover(self):
        print('user_roi_hashover hover ')

    def update_vc_image(self, array_data, x_pix_scale_factor, y_pix_scale_factor):
        '''
            Update graphics view with new image data
        :param array_data: chunked array to update image with
        :param x_pix_scale_factor: pix to mm
        :param y_pix_scale_factor: pix to mm
        '''
        print("update_roi_image")
        self.vc_image.scale(x_pix_scale_factor, y_pix_scale_factor)
        self.vc_image.setOpts(axisOrder='row-major')
        self.vc_image.setImage(array_data)
        self.vc_image.setLevels([0, amax(array_data)], update=True)

    def update_roi_image(self, array_data, x_pix_scale_factor, y_pix_scale_factor):
        '''
            Update graphics view with new image data
        :param array_data: chunked array to update image with
        :param x_pix_scale_factor: pix to mm
        :param y_pix_scale_factor: pix to mm
        '''
        print("update_vc_image")
        self.roi_image.scale(x_pix_scale_factor, y_pix_scale_factor)
        self.roi_image.setOpts(axisOrder='row-major')
        self.roi_image.setImage(array_data)
        self.roi_image.setLevels([0, amax(array_data)], update=True)

        # # a color map
        # STEPS = linspace(0, 1, 4)
        # CLRS = ['k', 'r', 'y', 'w']
        # a = array([pg.colorTuple(pg.Color(c)) for c in CLRS])
        # clrmp = pg.ColorMap(STEPS, a)
        # lut = clrmp.getLookupTable()
        # self.vc_image.setLookupTable(lut)
        # #
        # # add the vc_image to the plot_item
        # self.plot_item.addItem(self.vc_image)
        print("update_image FIN")
