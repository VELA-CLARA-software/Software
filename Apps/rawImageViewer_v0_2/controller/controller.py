from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import Qt

import numpy as np
import pyqtgraph as pg

import pyqtgraph.opengl as gl

## Create a GL View widget to display data
#app = QtGui.QApplication([])
#w = gl.GLViewWidget()
#w.show()
#w.setWindowTitle('pyqtgraph example: GLSurfacePlot')
#w.setCameraPosition(distance=50)


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

## Create a GL View widget to display data
        self.w = gl.GLViewWidget()
        #self.w.setWindowTitle('pyqtgraph example: GLSurfacePlot')
        self.w.setCameraPosition(distance=250)
        self.imarray = np.zeros((2560,2160))
        x = np.linspace(0,256,256)
        y = np.linspace(0,216,216)
        z = np.divide(self.imarray[0:256,0:216],65535/10) #np.random.normal(size=(216,256))#pg.gaussianFilter(np.random.normal(size=(216,256)), (1,1))
        self.p3d = gl.GLSurfacePlotItem(x=x, y=y, z=z, shader='heightColor', computeNormals=False, smooth=False)
        ## Add a grid to the view
        #g = gl.GLGridItem()
        #g.scale(2,2,1)
        #g.setDepthValue(100)  # draw grid after surfaces since they may be translucent
        self.w.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        g = gl.GLGridItem()
        #self.w.addItem(g)
        ## Simple surface plot example
        ## x, y values are not specified, so assumed to be 0:50

        self.roi = pg.ROI([0,0], [256,216])
        #self.roi.addScaleHandle([0.5, 0], [0.5, 0.5])
        #self.roi.addScaleHandle([1, 0.5], [0.5, 0.5])

        self.ImageBox = layout.addViewBox(lockAspect=True, colspan=2)
        self.Image = pg.ImageItem(np.random.normal(size=(2560, 2160)))
        self.ImageBox.addItem(self.Image)

        self.view.gridLayout.addWidget(monitor, 0, 2, 6, 1)
        self.view.gridLayout.addWidget(self.w, 0, 3, 6, 1)

        STEPS = np.linspace(0, 1, 4)
        CLRS = ['k', 'r', 'y', 'w']
        a = np.array([pg.colorTuple(pg.Color(c)) for c in CLRS])
        clrmp = pg.ColorMap(STEPS, a)
        lut = clrmp.getLookupTable()
        self.Image.setLookupTable(lut)
        '''Update GUI'''
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

    def openImageDir(self):
        self.view.pushButton.setText('Loading...')
        filename = QtGui.QFileDialog.getOpenFileName(self.view.centralwidget, 'Image',
                                          '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\Work\\2017')
        f = open(filename, "r")
        a = np.fromfile(f, dtype=np.uint16)
        a = a.reshape((2160, 2560))
        self.imarray = np.flip(np.transpose(np.array(a)), 1)
        self.Image.setImage(self.imarray)
        x = np.linspace(0,256,256)
        y = np.linspace(0,216,216)
        z = np.divide(self.imarray[0:256,0:216], self.view.spinBox_max.value())
        self.p3d = gl.GLSurfacePlotItem(x=x, y=y, z=z, shader='shaded', computeNormals=True, smooth=False) #color=(0.5, 0.5, 1, 50)
        #self.p3d.shader()['colorMap'] = np.array([0.2, 2, 0.5, 0.2, 1, 1, 0.2, 0, 2])
        #self.p3d.shader()['colorMap'] = np.array([])
        self.p3d.setData(x=x,y=y,z=z)
        self.p3d.translate(-128, -108, 0)
        self.w.addItem(self.p3d )
        self.ImageBox.addItem(self.roi)
        self.view.pushButton.setText('Load Image')
        #self.roi.setZValue(12)
    def update(self):
        self.Image.setLevels([self.view.spinBox_min.value(), self.view.spinBox_max.value()], update=True)

        x = np.linspace(0,int(self.roi.size()[0]),int(self.roi.size()[0]))
        y = np.linspace(0,int(self.roi.size()[1]),int(self.roi.size()[1]))
        newArray = self.imarray[int(self.roi.pos()[0]):int(self.roi.pos()[0])+int(self.roi.size()[0]),
        int(self.roi.pos()[1]):int(self.roi.pos()[1])+int(self.roi.size()[1])]
        z = np.divide(newArray, np.amax(newArray)/50)
        #self.p3d.shader()['colorMap'] = np.linspace(0,np.amax(newArray)/50,5)
        #self.p3d.scale(1., 1., 1.0)
        self.p3d.setData(x=x,y=y,z=z)
