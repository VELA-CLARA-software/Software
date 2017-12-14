from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import Qt
from PyQt4 import QtWebKit
import os
import time
import urllib
import webbrowser
import numpy as np
from bokeh.plotting import figure, save, output_file
from bokeh.io import gridplot
from bokeh.layouts import row, column
from bokeh.models import Spacer
from bokeh.models.widgets import Panel, Tabs
from PIL import Image
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
        self.view.pushButton_2.clicked.connect(self.openImageDirs)
        self.ImageBox = layout.addViewBox(lockAspect=True, colspan=2)
        self.Image = pg.ImageItem(np.random.normal(size=(2560, 2160)))

        self.ImageBox.addItem(self.Image)
        self.view.gridLayout.addWidget(monitor, 0, 2, 2, 3)
        STEPS = np.linspace(0, 1, 4)
        CLRS = ['k', 'r', 'y', 'w']
        a = np.array([pg.colorTuple(pg.Color(c)) for c in CLRS])
        clrmp = pg.ColorMap(STEPS, a)
        lut = clrmp.getLookupTable()
        self.Image.setLookupTable(lut)

    def openImageDir(self):
        self.view.pushButton.setText('Loading...')
        filename = QtGui.QFileDialog.getOpenFileName(self.view.centralwidget, 'Image',
                                          '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\Work\\2017\\CurrentCamera')
        f = open(filename, "r")
        #im = Image.open(str(filename))
        a = np.fromfile(f, dtype=np.uint16)
        a = a.reshape((2160, 2560))

        imarray =np.array(a)
        self.Image.setImage(np.flip(np.transpose(imarray), 1))
        #imarray = np.array(im)
        sumX = np.sum(np.flipud(imarray),axis=0)
        sumY = np.sum(np.flipud(imarray),axis=1)
        hX = np.linspace(1,2560,2560)
        vY = np.linspace(1,2160,2160)

        TOOLS="pan,wheel_zoom,box_zoom,box_select,reset"
        p = figure(tools=TOOLS, plot_width=700, plot_height=600, min_border=10, min_border_left=50,
                   toolbar_location="above", #x_axis_location=None, y_axis_location=None,
                   x_range=(0, 2560), y_range=(0, 2160), title=str(filename).split('/')[-1])

        imagey = p.image(image=[np.flipud(imarray)],
                         x=0, y=0, dw=2560, dh=2160, palette="Spectral11")

        hProfile = sumX
        hzeros = np.zeros(len(sumX))
        hmax = max(sumX) + 10
        hmin = min(sumX) - 10

        LINE_ARGS = dict(color="#3A5785", line_color=None)

        ph = figure(tools=TOOLS,toolbar_location=None, plot_width=p.plot_width, plot_height=200, x_range=p.x_range,
                    y_range=(hmin, hmax), min_border=10, min_border_left=50, y_axis_location="right")
        ph.xgrid.grid_line_color = None
        ph.yaxis.major_label_orientation = np.pi/4
        ph.background_fill_color = "#fafafa"
        ph.vbar(x=hX, width=1, bottom=0, top=hProfile,
                fill_alpha=0.8, fill_color="#3A5785", line_color=None)

        vProfile = sumY
        vzeros = np.zeros(len(sumY))
        vmax = max(sumY) + 10
        vmin = min(sumY) - 10

        pv = figure(tools=TOOLS, toolbar_location=None, plot_width=200, plot_height=p.plot_height, x_range=(vmin, vmax),
                    y_range=p.y_range, min_border=10, y_axis_location="right")
        pv.ygrid.grid_line_color = None
        pv.xaxis.major_label_orientation = np.pi/4
        pv.background_fill_color = "#fafafa"

        pv.hbar(y=vY, height=1, left=0, right=vProfile,
                fill_alpha=0.8, fill_color="#3A5785", line_color=None)

        layout = column(row(p, pv), row(ph, Spacer(width=200, height=200)))
        output_file("singleImage.html", title="Single Image")
        save(layout)
        webbrowser.open("singleImage.html");
        self.view.pushButton.setText('Single Image')
        #show(layout)

    def openImageDirs(self):
        self.view.pushButton_2.setText('Loading...')
        filenames = QtGui.QFileDialog.getOpenFileNames(self.view.centralwidget, 'Images',
                                          '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\Work\\2017\\CurrentCamera')

        tabs=[]
        for name in filenames:
            #im = Image.open(str(name))
            #imarray = np.array(im)
            f = open(name, "r")
            a = np.fromfile(f, dtype=np.uint16)
            a = a.reshape((2160, 2560))
            #imarray = np.delete(imarray, [0,1,2,3,4,5,6,7,8,9], 0)
            imarray =np.array(a)
            sumX = np.sum(np.flipud(imarray),axis=0)
            sumY = np.sum(np.flipud(imarray),axis=1)
            hX = np.linspace(1,2560,2560)
            vY = np.linspace(1,2150,2150)

            TOOLS="pan,wheel_zoom,box_zoom,box_select,reset"
            p = figure(tools=TOOLS, plot_width=700, plot_height=600, min_border=10, min_border_left=50,
                       toolbar_location="above", #x_axis_location=None, y_axis_location=None,
                       x_range=(0, 2560), y_range=(0, 2150), title=str(name).split('\\')[-1])

            imagey = p.image(image=[np.flipud(imarray)],
                             x=0, y=0, dw=2560, dh=2150)#, palette="Spectral11")

            hProfile = sumX
            hzeros = np.zeros(len(sumX))
            hmax = max(sumX) + 10
            hmin = min(sumX) - 10

            LINE_ARGS = dict(color="#3A5785", line_color=None)

            ph = figure(tools=TOOLS,toolbar_location=None, plot_width=p.plot_width, plot_height=200, x_range=p.x_range,
                        y_range=(hmin, hmax), min_border=10, min_border_left=50, y_axis_location="right")
            ph.xgrid.grid_line_color = None
            ph.yaxis.major_label_orientation = np.pi/4
            ph.background_fill_color = "#fafafa"
            ph.vbar(x=hX, width=1, bottom=0, top=hProfile,
                    fill_alpha=0.8, fill_color="#3A5785", line_color=None)

            vProfile = sumY
            vzeros = np.zeros(len(sumY))
            vmax = max(sumY) + 10
            vmin = min(sumY) - 10

            pv = figure(tools=TOOLS, toolbar_location=None, plot_width=200, plot_height=p.plot_height, x_range=(vmin, vmax),
                        y_range=p.y_range, min_border=10, y_axis_location="right")
            pv.ygrid.grid_line_color = None
            pv.xaxis.major_label_orientation = np.pi/4
            pv.background_fill_color = "#fafafa"

            pv.hbar(y=vY, height=1, left=0, right=vProfile,
                    fill_alpha=0.8, fill_color="#3A5785", line_color=None)



            layout = column(row(p, pv), row(ph, Spacer(width=200, height=200)))
            tabs.append(Panel(child=layout, title=str(name).split('\\')[-1]))
        output_file("batchImages.html", title="Images")
        tables = Tabs(tabs=tabs)
        save(tables)
        webbrowser.open("batchImages.html");
        self.view.pushButton_2.setText('Batch of Images')
