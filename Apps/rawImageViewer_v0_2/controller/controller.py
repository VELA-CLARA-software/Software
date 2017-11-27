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
        pg.setConfigOptions(antialias=True)
        '''define model and view'''
        monitor = pg.GraphicsView()
        layout = pg.GraphicsLayout(border=(100, 100, 100))
        monitor.setCentralItem(layout)

        monitorX = pg.GraphicsView()
        layoutX = pg.GraphicsLayout(border=(100, 100, 100))
        monitorX.setCentralItem(layoutX)

        monitorY = pg.GraphicsView()
        layoutY = pg.GraphicsLayout(border=(100, 100, 100))
        monitorY.setCentralItem(layoutY)

        self.view = view
        self.model = model
        self.timer = QtCore.QTimer()
        self.view.pushButton.clicked.connect(self.openImageDir)
        self.w = gl.GLViewWidget()
        self.w.setCameraPosition(distance=300, azimuth=270)
        self.imarray = np.zeros((2560,2160))
        x = np.linspace(0,256,256)
        y = np.linspace(0,216,216)
        z = np.divide(self.imarray[0:256, 0:216], 65535 / 10 )
        self.p3d = gl.GLSurfacePlotItem(x=x, y=y, z=z, shader='shaded', computeNormals=True, smooth=False)
        self.p3d.translate(-128, -108, 0)
        self.w.addItem(self.p3d)

        self.w.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        self.roi = pg.ROI([0,0], [256,216])
        #self.roi.addScaleHandle([0.5, 0], [0.5, 0.5])
        #self.roi.addScaleHandle([1, 0.5], [0.5, 0.5])

        self.ImageBox = layout.addViewBox(lockAspect=True, colspan=1, rowspan=1)
        self.yProfBox = layoutY.addPlot()
        self.xProfBox = layoutX.addPlot()
        self.Image = pg.ImageItem(np.random.normal(size=(2560, 2160)))
        self.ImageBox.addItem(self.Image)


        self.yProfBox.setYLink(self.ImageBox)
        self.xProfBox.setXLink(self.ImageBox)

        self.xProfBox.plot(pen='w')
        self.yProfBox.plot(pen='w')

        self.view.gridLayout.addWidget(monitor, 0, 2, 3, 1)
        self.view.gridLayout.addWidget(monitorY, 0, 3, 3, 1)
        self.view.gridLayout.addWidget(monitorX, 3, 2, 3, 1)
        self.view.gridLayout.addWidget(self.w, 3, 3, 3, 1)

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
        self.yProfBox.clear()
        self.xProfBox.clear()
        self.view.pushButton.setText('Loading...')
        filename = QtGui.QFileDialog.getOpenFileName(self.view.centralwidget, 'Image',
                                          '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\Work\\2017')
        f = open(filename, "r")
        a = np.fromfile(f, dtype=np.uint16)
        a = a.reshape((2160, 2560))
        self.imarray = np.flip(np.transpose(np.array(a)), 1)
        self.Image.setImage(self.imarray)
        x = np.linspace(0, 256, 256)
        y = np.linspace(0, 216, 216)
        z = np.divide(self.imarray[0:256, 0:216], self.view.spinBox_max.value())
        sumX = np.sum(self.imarray, axis=1)
        sumY = np.sum(self.imarray, axis=0)
        self.p3d.setData(x=x, y=y, z=z)
        x = np.linspace(0, 2560, 2560)
        y = np.linspace(0, 2160, 2160)
        self.xProfBox.plot(x=x, y=sumX, pen='w')
        self.yProfBox.plot(x=sumY, y=y, pen='w')
        self.ImageBox.addItem(self.roi)
        self.view.pushButton.setText('Load Image')

    def update(self):
        self.Image.setLevels([self.view.spinBox_min.value(), self.view.spinBox_max.value()], update=True)

        x = np.linspace(0,int(self.roi.size()[0]),int(self.roi.size()[0]))
        y = np.linspace(0,int(self.roi.size()[1]),int(self.roi.size()[1]))
        newArray = self.imarray[int(self.roi.pos()[0]):int(self.roi.pos()[0])+int(self.roi.size()[0]),
        int(self.roi.pos()[1]):int(self.roi.pos()[1])+int(self.roi.size()[1])]
        z = np.divide(newArray, np.amax(newArray)/50)

        self.p3d.setData(x=x,y=y,z=z)
