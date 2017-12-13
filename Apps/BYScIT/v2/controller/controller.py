from PyQt4 import QtCore
from PyQt4 import QtGui
import sys
import numpy as np
import pyqtgraph as pg
import model.model as modelFunctions
import pyqtgraph.opengl as gl
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\stage')
import VELA_CLARA_Camera_IA_Control as ia

class Controller():

    def __init__(self, view, model):
        # Define model and view
        self.view = view
        self.model = model

        pg.setConfigOptions(antialias=True)
        # Image
        monitor = pg.GraphicsView()
        layout = pg.GraphicsLayout(border=(100, 100, 100))
        monitor.setCentralItem(layout)
        #Backgroun Image
        monitorBkgrnd = pg.GraphicsView()
        layoutBkgrnd = pg.GraphicsLayout(border=(100, 100, 100))
        monitorBkgrnd.setCentralItem(layoutBkgrnd)
        # Display for x profile
        monitorX = pg.GraphicsView()
        layoutX = pg.GraphicsLayout(border=(100, 100, 100))
        monitorX.setCentralItem(layoutX)
        # Display for y profile
        monitorY = pg.GraphicsView()
        layoutY = pg.GraphicsLayout(border=(100, 100, 100))
        monitorY.setCentralItem(layoutY)
        self.tabWidget = QtGui.QTabWidget()

        self.w = gl.GLViewWidget()
        self.w.setCameraPosition(distance=300, azimuth=270)
        self.imarray = np.zeros((2560, 2160))
        x = np.linspace(0, 256, 256)
        y = np.linspace(0, 216, 216)
        z = np.divide(self.imarray[0:256, 0:216], 65535)
        colors = np.ones((256, 216, 4), dtype=float)
        colors[..., 0] = np.clip(np.cos(((x.reshape(256, 1) ** 2) + (y.reshape(1, 216) ** 2)) ** 0.5), 0, 1)
        colors[..., 1] = colors[..., 0]
        self.p3d = gl.GLSurfacePlotItem(x=x, y=y, z=z, shader='shaded',
                                        colors=colors.reshape(256 * 216, 4),
                                        computeNormals=True, smooth=False)
        self.p3d.translate(-128, -108, 0)
        self.w.addItem(self.p3d)
        self.w.setSizePolicy(QtGui.QSizePolicy.Expanding,
                             QtGui.QSizePolicy.Expanding)

        self.roi = pg.ROI([0, 0], [256, 216])
        self.customMaskROI = pg.EllipseROI([50, 50], [50, 50])


        self.ImageBox = layout.addPlot(lockAspect=True, colspan=1, rowspan=1)
        self.yProfBox = layoutY.addPlot()
        self.xProfBox = layoutX.addPlot()
        self.Image = pg.ImageItem(lockAspect=True)
        self.saturatedPixelImage = pg.ImageItem()
        self.ImageBox.addItem(self.Image)
        self.vLineMLE = self.ImageBox.plot(pen='g')
        self.hLineMLE = self.ImageBox.plot(pen='g')
        self.vLineBVN = self.ImageBox.plot(pen='b')
        self.hLineBVN = self.ImageBox.plot(pen='b')

        self.yProfBox.setYLink(self.ImageBox)
        self.xProfBox.setXLink(self.ImageBox)
        self.xProfBox.plot(pen='w')
        self.yProfBox.plot(pen='w')

        self.BkgrndBox = layoutBkgrnd.addPlot(colspan=1, rowspan=1)
        self.bkgrndImage = pg.ImageItem(lockAspect=True)
        self.BkgrndBox.addItem(self.bkgrndImage)
        self.tabWidget.addTab(self.w, '3D Lens')
        self.tabWidget.addTab(monitorBkgrnd, 'Background')

        self.view.gridLayout.addWidget(monitor, 0, 3, 10, 1)
        self.view.gridLayout.addWidget(monitorY, 0, 4, 10, 1)
        self.view.gridLayout.addWidget(monitorX, 10, 3, 10, 1)
        self.view.gridLayout.addWidget(self.tabWidget, 10, 4, 10, 1)

        STEPS = np.linspace(0, 1, 4)
        CLRS = ['k', 'r', 'y', 'w']
        a = np.array([pg.colorTuple(pg.Color(c)) for c in CLRS])
        clrmp = pg.ColorMap(STEPS, a)
        lut = clrmp.getLookupTable()
        self.Image.setLookupTable(lut)
        # Connections
        self.timer = QtCore.QTimer()
        self.view.pushButton_loadImage.clicked.connect(self.openImageDir)
        self.view.pushButton_loadBkgrnd.clicked.connect(self.openBkgrndImageDir)
        self.view.pushButton_analyse.clicked.connect(self.analyse)
        self.view.checkBox_showMLEFit.stateChanged.connect(self.showMLEFit)
        self.view.checkBox_showBVNFit.stateChanged.connect(self.showBVNFit)
        self.view.checkBox_useCustomMask.stateChanged.connect(self.useCustomMask)
        # Update View every 100 ms
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

    def useCustomMask(self):
        if self.view.checkBox_useCustomMask.isChecked() is True:
            self.ImageBox.addItem(self.customMaskROI)
        else:
            self.ImageBox.removeItem(self.customMaskROI)

    def showMLEFit(self):
        if self.view.checkBox_showMLEFit.isChecked() is True:
            self.ImageBox.addItem(self.vLineMLE)
            self.ImageBox.addItem(self.hLineMLE)
        else:
            self.ImageBox.removeItem(self.vLineMLE)
            self.ImageBox.removeItem(self.hLineMLE)

    def showBVNFit(self):
        if self.view.checkBox_showBVNFit.isChecked() == True:
            self.ImageBox.addItem(self.vLineBVN)
            self.ImageBox.addItem(self.hLineBVN)
        else:
            self.ImageBox.removeItem(self.vLineBVN)
            self.ImageBox.removeItem(self.hLineBVN)

    def openImageDir(self):
        self.yProfBox.clear()
        self.xProfBox.clear()
        self.view.pushButton_loadImage.setText('Loading...')
        filename = QtGui.QFileDialog.getOpenFileName(self.view.centralwidget, 'Image')
        self.model.getImage(str(filename))
        self.Image.setImage(self.model.imageData)
        self.imarray = self.model.imageData
        x = np.linspace(0, 256, 256)
        y = np.linspace(0, 216, 216)
        z = self.imarray[0:256, 0:216]
        sumX = np.sum(self.model.imageData, axis=1)
        sumY = np.sum(self.model.imageData, axis=0)
        self.p3d.setData(x=x, y=y, z=z)
        x = np.linspace(0, self.model.imageWidth, self.model.imageWidth)
        y = np.linspace(0, self.model.imageHeight, self.model.imageHeight)
        self.xProfBox.plot(x=x, y=sumX, pen='w')
        self.yProfBox.plot(x=sumY, y=y, pen='w')
        self.ImageBox.addItem(self.roi)
        self.view.spinBox_max.setValue(np.amax(self.model.imageData))
        self.view.pushButton_loadImage.setText('Load Image')

    def openBkgrndImageDir(self):
        self.view.pushButton_loadBkgrnd.setText('Loading...')
        filename = QtGui.QFileDialog.getOpenFileName(self.view.centralwidget, 'Background Image')
        self.backgroundData = modelFunctions.Model()
        self.backgroundData.getImage(str(filename))
        self.bkgrndImage.setImage(self.backgroundData.imageData)

        self.view.spinBox_max.setValue(np.amax(self.model.imageData))
        self.view.pushButton_loadBkgrnd.setText('Load Background')

    def update(self):
        self.Image.setLevels([self.view.spinBox_min.value(), self.view.spinBox_max.value()], update=True)
        self.bkgrndImage.setLevels([self.view.spinBox_min.value(), self.view.spinBox_max.value()], update=True)

        x = np.linspace(0,int(self.roi.size()[0]),int(self.roi.size()[0]))
        y = np.linspace(0,int(self.roi.size()[1]),int(self.roi.size()[1]))
        newArray = self.imarray[int(self.roi.pos()[0]):int(self.roi.pos()[0])+int(self.roi.size()[0]),
        int(self.roi.pos()[1]):int(self.roi.pos()[1])+int(self.roi.size()[1])]
        z = np.divide(newArray, np.amax(newArray)/50)
        colors = np.ones((256, 216, 4), dtype=float)
        colors[..., 0] = np.divide(z, 3)
        colors[..., 1] = np.divide(z, 9)
        colors[..., 2] = np.divide(z, 3 * 9) + 0.4
        self.p3d.setData(x=x, y=y, z=z, colors=colors.reshape(256 * 216, 4))
        self.view.label_customX.setText('X: ' + str(self.customMaskROI.pos[0]))
        self.view.label_customY.setText('Y: ' + str(self.customMaskROI.pos[1]))
        self.view.label_customRX.setText('Radius X: ' + str(self.customMaskROI.size[0]))
        self.view.label_customRY.setText('Radius Y: ' + str(self.customMaskROI.size[1]))

    def analyse(self):
        image = np.transpose(np.flip(self.model.imageData, 1))
        image = image.flatten().tolist()
        im = ia.std_vector_double()
        im.extend(image)

        self.model.offlineAnalysis.loadImage(im, self.model.imageHeight, self.model.imageWidth)
        if self.view.checkBox_useBackground.isChecked() is True:
            self.model.offlineAnalysis.useBackground(True)

            bk = np.transpose(np.flip(self.backgroundData.imageData, 1))
            bk = bk.flatten().tolist()
            b = ia.std_vector_double()
            b.extend(bk)
            self.model.offlineAnalysis.loadBackgroundImage(b)
        else:
            self.model.offlineAnalysis.useBackground(False)
        # This is where we will house expert settings
        manualCrop = False
        self.model.offlineAnalysis.useESMask(True)
        if manualCrop is True:
            self.model.offlineAnalysis.setESMask(700, 600, 300, 400)
        else:
            # make mask span full width of image
            x = int(self.model.imageWidth / 2)
            y = int(self.model.imageHeight / 2)
            self.model.offlineAnalysis.setESMask(x, y, x, y)


        self.model.offlineAnalysis.analyse()
        # Set Results Labels in GUI
        self.view.label_xMLE.setText(str(self.model.offlineAnalysis.CoIA.xMLE))
        self.view.label_yMLE.setText(str(self.model.offlineAnalysis.CoIA.yMLE))
        self.view.label_sxMLE.setText(str(self.model.offlineAnalysis.CoIA.sxMLE))
        self.view.label_syMLE.setText(str(self.model.offlineAnalysis.CoIA.syMLE))
        self.view.label_cxyMLE.setText(str(self.model.offlineAnalysis.CoIA.cxyMLE))
        self.view.label_xBVN.setText(str(self.model.offlineAnalysis.CoIA.xBVN))
        self.view.label_yBVN.setText(str(self.model.offlineAnalysis.CoIA.yBVN))
        self.view.label_sxBVN.setText(str(self.model.offlineAnalysis.CoIA.sxBVN))
        self.view.label_syBVN.setText(str(self.model.offlineAnalysis.CoIA.syBVN))
        self.view.label_cxyBVN.setText(str(self.model.offlineAnalysis.CoIA.cxyBVN))

        # Set crosshairs
        x = float(self.model.offlineAnalysis.CoIA.xMLE)
        y = float(self.model.offlineAnalysis.CoIA.yMLE)
        v1 = (float(self.model.offlineAnalysis.CoIA.yMLE) -
              float(self.model.offlineAnalysis.CoIA.syMLE))
        v2 = (float(self.model.offlineAnalysis.CoIA.yMLE) +
              float(self.model.offlineAnalysis.CoIA.syMLE))
        h1 = (float(self.model.offlineAnalysis.CoIA.xMLE) -
              float(self.model.offlineAnalysis.CoIA.sxMLE))
        h2 = (float(self.model.offlineAnalysis.CoIA.xMLE) +
              float(self.model.offlineAnalysis.CoIA.sxMLE))
        self.vLineMLE.setData(x=[x, x], y=[v1, v2])
        self.hLineMLE.setData(x=[h1, h2], y=[y, y])

        x = float(self.model.offlineAnalysis.CoIA.xBVN)
        y = float(self.model.offlineAnalysis.CoIA.yBVN)
        v1 = (float(self.model.offlineAnalysis.CoIA.yBVN) -
              float(self.model.offlineAnalysis.CoIA.syBVN))
        v2 = (float(self.model.offlineAnalysis.CoIA.yBVN) +
              float(self.model.offlineAnalysis.CoIA.syBVN))
        h1 = (float(self.model.offlineAnalysis.CoIA.xBVN) -
              float(self.model.offlineAnalysis.CoIA.sxBVN))
        h2 = (float(self.model.offlineAnalysis.CoIA.xBVN) +
              float(self.model.offlineAnalysis.CoIA.sxBVN))
        self.vLineBVN.setData(x=[x, x], y=[v1, v2])
        self.hLineBVN.setData(x=[h1, h2], y=[y, y])
