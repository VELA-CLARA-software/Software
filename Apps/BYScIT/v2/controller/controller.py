from __future__ import division
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtGui import QApplication
import time
import sys
import os
import numpy as np
import pyqtgraph as pg
import model.model as modelFunctions
import pyqtgraph.opengl as gl
import threads
from decimal import *
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\stage')
import VELA_CLARA_Camera_IA_Control as ia


class Controller(QtCore.QThread):
    def __init__(self, view, model):
        # Define model and view
        QtCore.QThread.__init__(self)
        self.view = view
        self.model = model
        self.backgroundData = modelFunctions.Model()
        self.listOfImages = []
        self.listOfBkgrndImages = []
        self.progress = 0
        pg.setConfigOptions(antialias=True)
        # Image
        monitor = pg.GraphicsView()
        self.layout = pg.GraphicsLayout()
        monitor.setCentralItem(self.layout)
        # Background Image
        monitorBkgrnd = pg.GraphicsView()
        self.layoutBkgrnd = pg.GraphicsLayout()
        monitorBkgrnd.setCentralItem(self.layoutBkgrnd)
        # Image subtract Background Image
        monitorSub = pg.GraphicsView()
        self.layoutSub = pg.GraphicsLayout()
        monitorSub.setCentralItem(self.layoutSub)
        # Display for x profile
        monitorX = pg.GraphicsView()
        self.layoutX = pg.GraphicsLayout()
        monitorX.setCentralItem(self.layoutX)
        # Display for y profile
        monitorY = pg.GraphicsView()
        self.layoutY = pg.GraphicsLayout()
        monitorY.setCentralItem(self.layoutY)
        self.tabWidget = QtGui.QTabWidget()

        self.w = gl.GLViewWidget()
        self.w.setCameraPosition(distance=300, azimuth=270)
        self.imarray = np.zeros((2560, 2160))
        self.imarray[0][0]=1
        x = np.linspace(0, 256, 256)
        y = np.linspace(0, 216, 216)
        z = np.divide(self.imarray[0:256, 0:216], 65535)
        colors = np.ones((256, 216, 4), dtype=float)
        colors[..., 0] = np.clip(np.cos(((x.reshape(256, 1) ** 2) +
                                 (y.reshape(1, 216) ** 2)) ** 0.5), 0, 1)
        colors[..., 1] = colors[..., 0]
        self.p3d = gl.GLSurfacePlotItem(x=x, y=y, z=z, shader='shaded',
                                        colors=colors.reshape(256 * 216, 4),
                                        computeNormals=True, smooth=False)
        self.p3d.translate(-128, -108, 0)
        self.w.addItem(self.p3d)
        self.w.setSizePolicy(QtGui.QSizePolicy.Expanding,
                             QtGui.QSizePolicy.Expanding)

        self.roi = pg.ROI([0, 0], [256, 216])
        self.customMaskROI = pg.ROI([50, 50], [100, 100])
        self.customMaskROI.addScaleHandle([0.5, 1], [0.5, 0.5])
        self.customMaskROI.addScaleHandle([0, 0.5], [0.5, 0.5])

        self.ImageBox = self.layout.addPlot(lockAspect=True, row=1, col=0,
                                            colspan=1, rowspan=1)
        self.imageLabel = self.layout.addLabel(text='Image', row=0, col=0,
                                               rowspan=1, colspan=1)
        self.yProfBox = self.layoutY.addPlot(lockAspect=True, row=1, col=0,
                                             colspan=1, rowspan=1)
        self.xProfBox = self.layoutX.addPlot(lockAspect=True, row=1, col=0,
                                             colspan=1, rowspan=1)
        self.layoutX.addLabel(text='X Profile', row=0, col=0,
                              rowspan=1, colspan=1)
        self.layoutY.addLabel(text='Y Profile', row=0, col=0,
                              rowspan=1, colspan=1)
        self.Image = pg.ImageItem(lockAspect=True)
        self.saturatedPixelImage = pg.ImageItem(lockAspect=True)
        self.saturatedPixelImage.setZValue(5)
        self.ImageBox.addItem(self.Image)

        self.vLineMLE = self.ImageBox.plot(pen='g')
        self.hLineMLE = self.ImageBox.plot(pen='g')
        self.vLineBVN = self.ImageBox.plot(pen='b')
        self.hLineBVN = self.ImageBox.plot(pen='b')
        # Hide them
        self.ImageBox.removeItem(self.vLineBVN)
        self.ImageBox.removeItem(self.hLineBVN)
        self.ImageBox.removeItem(self.vLineMLE)
        self.ImageBox.removeItem(self.hLineMLE)
        self.yProfBox.setYLink(self.ImageBox)
        self.xProfBox.setXLink(self.ImageBox)

        self.xProfBox.plot(pen='w')
        self.yProfBox.plot(pen='w')

        self.BkgrndBox = self.layoutBkgrnd.addPlot(lockAspect=True,
                                                   row=1, col=0,
                                                   colspan=1, rowspan=1)
        self.bkgrndImageLabel = self.layoutBkgrnd.addLabel(text='Background Image',
                                                           row=0, col=0,
                                                           rowspan=1, colspan=1)
        self.bkgrndImage = pg.ImageItem(lockAspect=True)
        self.BkgrndBox.addItem(self.bkgrndImage)
        self.SubBox = self.layoutSub.addPlot(lockAspect=True,
                                                   row=1, col=0,
                                                   colspan=1, rowspan=1)
        self.subLabel = self.layoutSub.addLabel(text='Image - Background Image',
                                                           row=0, col=0,
                                                           rowspan=1, colspan=1)
        self.subtractedImage = pg.ImageItem(lockAspect=True)
        self.SubBox.addItem(self.subtractedImage)
        self.tabWidget.addTab(self.w, '3D Lens')
        self.tabWidget.addTab(monitorBkgrnd, 'Background')
        self.tabWidget.addTab(monitorSub, 'Background Subtracted Image')

        self.view.gridLayout_4.addWidget(monitor, 0, 0, 1, 1)
        self.view.gridLayout_4.addWidget(monitorY, 0, 1, 1, 1)
        self.view.gridLayout_4.addWidget(monitorX, 1, 0, 1, 1)
        self.view.gridLayout_4.addWidget(self.tabWidget, 1, 1, 1, 1)

        stepsFire = np.linspace(0, 1, 4)
        colorsFire = ['k', 'r', 'y', 'w']
        a = np.array([pg.colorTuple(pg.Color(c)) for c in colorsFire])
        self.lutFire = pg.ColorMap(stepsFire, a).getLookupTable()

        stepsGray = np.linspace(0, 1, 2)
        colorsGray = ['k', 'w']
        a = np.array([pg.colorTuple(pg.Color(c)) for c in colorsGray])
        self.lutGray = pg.ColorMap(stepsGray, a).getLookupTable()

        stepsInvGray = np.linspace(0, 1, 2)
        colorsInvGray = ['w', 'k']
        a = np.array([pg.colorTuple(pg.Color(c)) for c in colorsInvGray])
        self.lutInvGray = pg.ColorMap(stepsInvGray, a).getLookupTable()

        stepsRainbow = np.linspace(0, 1, 8)
        colorsRainbow  = ['k','b','m','c','g','r','y','w']
        a = np.array([pg.colorTuple(pg.Color(c)) for c in colorsRainbow])
        self.lutRainbow  = pg.ColorMap(stepsRainbow , a).getLookupTable()

        self.Image.setLookupTable(self.lutGray)
        # SATURATED PIXEL COLOURING
        STEPS = np.array([0.0, 1.0])
        CLRS = ['w', 'g']
        clrmp_sat = pg.ColorMap(STEPS, np.array([pg.colorTuple(pg.Color(c)) for c in CLRS]))
        lut_sat = clrmp_sat.getLookupTable(nPts=2)
        self.saturatedPixelImage.setLookupTable(lut_sat)

        # Connections
        self.analysethread = threads.GenericThread(self.model, self.view)
        self.timer = QtCore.QTimer()
        self.view.pushButton_loadImage.clicked.connect(self.openImageDir)
        self.view.pushButton_loadBkgrnd.clicked.connect(self.openBkgrndImageDir)
        self.view.pushButton_analyse.clicked.connect(self.analyse)
        self.view.checkBox_showMLEFit.stateChanged.connect(self.showMLEFit)
        self.view.checkBox_showBVNFit.stateChanged.connect(self.showBVNFit)
        self.view.checkBox_useCustomMask.stateChanged.connect(self.useCustomMask)
        self.view.checkBox_useCustomMask.stateChanged.connect(self.useCustomMask)
        self.view.checkBox_showSaturatedPixels.stateChanged.connect(self.showSatPix)
        self.view.checkBox_show3DLens.stateChanged.connect(self.show3DLens)
        self.view.pushButton_saveCurrentData.clicked.connect(self.saveCurrentData)
        self.view.pushButton_loadImagesBatch.clicked.connect(self.getListOfImages)
        self.view.comboBox_colourMap.currentIndexChanged.connect(self.changeColourMap)
        self.view.pushButton_loadBkgrndImagesBatch.clicked.connect(self.getListOfBackgroundImagesImages)
        self.view.pushButton_analyseBatch.clicked.connect(self.start)#self.batchAnalyse)
        self.ImageBox.sigRangeChanged.connect(self.matchRanges)
        # Update View every 100 ms
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)

    def matchRanges(self):
        self.SubBox.setRange(xRange=self.ImageBox.vb.state['viewRange'][0],
                             yRange=self.ImageBox.vb.state['viewRange'][1],
                             padding=0)
        self.BkgrndBox.setRange(xRange=self.ImageBox.vb.state['viewRange'][0],
                                yRange=self.ImageBox.vb.state['viewRange'][1],
                                padding=0)

    def run(self):
        NumberOfImages = self.listOfImages.count()
        if len(self.listOfImages)==1 and str(self.listOfImages[0]).split('.')[-1]=='hdf5':
            NumberOfImages=100
        for i in range(NumberOfImages):

            if len(self.listOfImages)==1 and str(self.listOfImages[0]).split('.')[-1]=='hdf5':
                self.model.getHDF5Images(str(self.listOfImages[0]),i)
            else:
                self.model.getImage(str(self.listOfImages[i]))
            image = np.transpose(np.flip(self.model.imageData, 1))
            image = image.flatten().tolist()
            im = ia.std_vector_double()
            im.extend(image)
            self.model.offlineAnalysis.loadImage(im, self.model.fullName, self.model.imageHeight, self.model.imageWidth)
            if len(self.listOfBkgrndImages) > 0:
                self.model.offlineAnalysis.useBackground(True)
                if self.backgroundData.imageHeight != self.model.imageHeight or self.backgroundData.imageWidth != self.model.imageWidth:
                    print 'ERROR: Image and Background are not the same dimensions!'
                    return
                if len(self.listOfBkgrndImages)==1:
                    self.backgroundData.getImage(str(self.listOfBkgrndImages[0]))
                elif len(self.listOfBkgrndImages) == len(self.listOfImages):
                    self.backgroundData.getImage(str(self.listOfBkgrndImages[i]))
                else:
                    print "ERROR: I correct number of background images! Either have one or an equal amount to the number of images being analysed in the batch."
                    return
                bk = np.transpose(np.flip(self.backgroundData.imageData, 1))
                bk = bk.flatten().tolist()
                b = ia.std_vector_double()
                b.extend(bk)
                self.model.offlineAnalysis.loadBackgroundImage(b, self.backgroundData.fullName)
            else:
                self.model.offlineAnalysis.useBackground(False)
            # This is where we will house expert settings
            self.model.offlineAnalysis.useESMask(True)
            if self.view.checkBox_useCustomMask.isChecked() is True:
                self.model.offlineAnalysis.setESMask(int(self.customMaskROI.pos()[0]+self.customMaskROI.size()[0]/2),
                                                     int(self.customMaskROI.pos()[1]+self.customMaskROI.size()[0]/2),
                                                     int(self.customMaskROI.size()[0]/2),
                                                     int(self.customMaskROI.size()[1]/2))
            else:
                # make mask span full width of image
                x = int(self.model.imageWidth / 2)
                y = int(self.model.imageHeight / 2)
                self.model.offlineAnalysis.setESMask(x, y, x, y)

            if self.view.checkBox_rollingAverage.isChecked() is True:
                self.model.offlineAnalysis.useESFilter(True)
                self.model.offlineAnalysis.setESFilter(int(self.view.lineEdit_rollingAverage.text()))
            else:
                self.model.offlineAnalysis.useESFilter(False)

            if self.view.checkBox_rSquared.isChecked() is True:
                self.model.offlineAnalysis.useESRRThreshold(True)
                self.model.offlineAnalysis.setESRRThreshold(float(self.view.lineEdit_rSquared.text()))
            else:
                self.model.offlineAnalysis.useESRRThreshold(False)

            if self.view.checkBox_lowestPixValue.isChecked() is True:
                self.model.offlineAnalysis.useESDirectCut(True)
                self.model.offlineAnalysis.setESDirectCut(float(self.view.lineEdit_lowestPixelValue.text()))
            else:
                self.model.offlineAnalysis.useESDirectCut(False)

            self.model.offlineAnalysis.analyse()
            while self.model.offlineAnalysis.isAnalysing()==True:
                time.sleep(1)
            self.model.offlineAnalysis.writeData(str(self.view.lineEdit_dataFileNameBatch.text()))

            self.progress=100*((i+1)/NumberOfImages)
            self.view.progressBar_batchMode.setValue(self.progress)
            del im
    def changeColourMap(self):
        if self.view.comboBox_colourMap.currentIndex() is 0:
            self.Image.setLookupTable(self.lutGray)
            self.bkgrndImage.setLookupTable(self.lutGray)
            self.subtractedImage.setLookupTable(self.lutGray)
        elif self.view.comboBox_colourMap.currentIndex() is 1:
            self.Image.setLookupTable(self.lutInvGray)
            self.bkgrndImage.setLookupTable(self.lutInvGray)
            self.subtractedImage.setLookupTable(self.lutInvGray)
        elif self.view.comboBox_colourMap.currentIndex() is 2:
            self.Image.setLookupTable(self.lutFire)
            self.bkgrndImage.setLookupTable(self.lutFire)
            self.subtractedImage.setLookupTable(self.lutFire)
        else: #must be on rainbow
            self.Image.setLookupTable(self.lutRainbow)
            self.bkgrndImage.setLookupTable(self.lutRainbow)
            self.subtractedImage.setLookupTable(self.lutRainbow)

    def getListOfImages(self):
        self.listOfImages = QtGui.QFileDialog.getOpenFileNames(self.view.centralwidget, 'Images')

    def getListOfBackgroundImagesImages(self):
        self.listOfBkgrndImagesImages = QtGui.QFileDialog.getOpenFileNames(self.view.centralwidget, 'Backgrounds')

    def saveCurrentData(self):
        self.view.pushButton_saveCurrentData.setText("Saving...")
        self.model.offlineAnalysis.writeData(str(self.view.lineEdit_dataFileName.text()))
        self.view.pushButton_saveCurrentData.setText("Save Current Results")

    def show3DLens(self):
        if self.view.checkBox_show3DLens.isChecked() is True:
            self.ImageBox.addItem(self.roi)
        else:
            self.ImageBox.removeItem(self.roi)

    def showSatPix(self):
        if self.view.checkBox_showSaturatedPixels.isChecked() is True:
            self.ImageBox.addItem(self.saturatedPixelImage)
        else:
            self.ImageBox.removeItem(self.saturatedPixelImage)

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
        if self.view.checkBox_showBVNFit.isChecked() is True:
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
        if str(filename) is '':
            self.view.pushButton_loadImage.setText('Load Image')
            return
        self.model.getImage(str(filename))
        self.Image.setImage(self.model.imageData)
        self.ImageBox.setLimits(xMin=0, yMin=0,
                                xMax=self.model.imageWidth,
                                yMax=self.model.imageHeight)
        self.imageLabel.setText(text=self.model.fullName.split('/')[-1])

        self.saturatedPixelImage.setImage(self.model.imageData, opacity=0.4)
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
        if self.view.checkBox_autoScale.isChecked() is True:
            self.view.spinBox_max.setValue(np.amax(self.model.imageData))
        self.view.spinBox_satLevel.setValue(int(np.amax(self.model.imageData)))
        self.view.pushButton_loadImage.setText('Load Image')
        self.setSubtarctedImage()

    def openBkgrndImageDir(self):
        self.view.pushButton_loadBkgrnd.setText('Loading...')
        filename = QtGui.QFileDialog.getOpenFileName(self.view.centralwidget, 'Background Image')
        if str(filename) is '':
            self.view.pushButton_loadBkgrnd.setText('Load Background')
            return
        self.backgroundData.getImage(str(filename))
        self.bkgrndImage.setImage(self.backgroundData.imageData)
        self.BkgrndBox.setLimits(xMin=0, yMin=0,
                                 xMax=self.backgroundData.imageWidth,
                                 yMax=self.backgroundData.imageHeight)
        self.bkgrndImageLabel.setText(self.backgroundData.fullName.split('/')[-1])
        # self.BkgrndBox.setYLink(self.ImageBox)
        # self.BkgrndBox.setXLink(self.ImageBox)
        self.view.pushButton_loadBkgrnd.setText('Load Background')
        self.setSubtarctedImage()

    def update(self):

        self.Image.setLevels([self.view.spinBox_min.value(), self.view.spinBox_max.value()], update=True)
        self.saturatedPixelImage.setLevels([0, self.view.spinBox_satLevel.value()], update=True)
        self.bkgrndImage.setLevels([self.view.spinBox_min.value(), self.view.spinBox_max.value()], update=True)
        self.subtractedImage.setLevels([self.view.spinBox_min.value(), self.view.spinBox_max.value()], update=True)

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
        if self.view.checkBox_useCustomMask.isChecked() is True:
            self.view.label_customX.setText('X: ' + str(int(self.customMaskROI.pos()[0]+self.customMaskROI.size()[0]/2)))
            self.view.label_customY.setText('Y: ' + str(int(self.customMaskROI.pos()[1]+self.customMaskROI.size()[0]/2)))
            self.view.label_customRX.setText('XRad: ' + str(int(self.customMaskROI.size()[0]/2)))
            self.view.label_customRY.setText('YRad: ' + str(int(self.customMaskROI.size()[1]/2)))
        if self.model.offlineAnalysis.isAnalysing()==True:
            self.view.pushButton_analyse.setText('Analysing ...')
            self.view.pushButton_analyseBatch.setText('Batch Analysing ...')
            self.view.pushButton_analyse.setEnabled(False)
            self.view.pushButton_analyseBatch.setEnabled(False)
        else:
            self.view.pushButton_analyse.setText('Analyse')
            self.view.pushButton_analyseBatch.setText('Batch Analyse')
            self.view.pushButton_analyse.setEnabled(True)
            self.view.pushButton_analyseBatch.setEnabled(True)
        pix2mm = self.model.offlineAnalysis.CoIA.pixToMM
        if pix2mm==1.0:
            self.view.label_3.setText("Results (pixels)")
        else:
            self.view.label_3.setText("Results (mm)")
        self.view.label_xMLE.setText(str(pix2mm*round(self.model.offlineAnalysis.CoIA.xMLE, 3))+
                                     '+/-'+str(pix2mm*round(self.model.offlineAnalysis.CoIA.xMLEerr, 3)))
        self.view.label_yMLE.setText(str(pix2mm*round(self.model.offlineAnalysis.CoIA.yMLE, 3))+
                                     '+/-'+str(pix2mm*round(self.model.offlineAnalysis.CoIA.yMLEerr, 3)))
        self.view.label_sxMLE.setText(str(pix2mm*round(self.model.offlineAnalysis.CoIA.sxMLE, 3))+
                                      '+/-'+str(pix2mm*round(self.model.offlineAnalysis.CoIA.sxMLEerr, 3)))
        self.view.label_syMLE.setText(str(pix2mm*round(self.model.offlineAnalysis.CoIA.syMLE, 3))+
                                      '+/-'+str(pix2mm*round(self.model.offlineAnalysis.CoIA.syMLEerr, 3)))
        self.view.label_cxyMLE.setText(str(pix2mm*pix2mm*round(self.model.offlineAnalysis.CoIA.cxyMLE, 3))+
                                       '+/-'+str(pix2mm*pix2mm*round(self.model.offlineAnalysis.CoIA.cxyMLEerr, 3)))
        self.view.label_xBVN.setText(str(pix2mm*round(self.model.offlineAnalysis.CoIA.xBVN, 3))+
                                     '+/-'+str(pix2mm*round(self.model.offlineAnalysis.CoIA.xBVNerr, 3)))
        self.view.label_yBVN.setText(str(pix2mm*round(self.model.offlineAnalysis.CoIA.yBVN, 3))+
                                     '+/-'+str(pix2mm*round(self.model.offlineAnalysis.CoIA.yBVNerr, 3)))
        self.view.label_sxBVN.setText(str(pix2mm*round(self.model.offlineAnalysis.CoIA.sxBVN, 3))+
                                      '+/-'+str(pix2mm*round(self.model.offlineAnalysis.CoIA.sxBVNerr, 3)))
        self.view.label_syBVN.setText(str(pix2mm*round(self.model.offlineAnalysis.CoIA.syBVN, 3))+
                                      '+/-'+str(pix2mm*round(self.model.offlineAnalysis.CoIA.syBVNerr, 3)))
        self.view.label_cxyBVN.setText(str(pix2mm*pix2mm*round(self.model.offlineAnalysis.CoIA.cxyBVN, 3))+
                                       '+/-'+str(pix2mm*pix2mm*round(self.model.offlineAnalysis.CoIA.cxyBVNerr, 3)))

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

    def analyse(self):
        image = np.transpose(np.flip(self.model.imageData, 1))
        image = image.flatten().tolist()
        im = ia.std_vector_double()
        im.extend(image)

        self.model
        self.model.offlineAnalysis.loadImage(im, self.model.fullName, self.model.imageHeight, self.model.imageWidth)
        if self.view.checkBox_useBackground.isChecked() is True:
            self.model.offlineAnalysis.useBackground(True)

            bk = np.transpose(np.flip(self.backgroundData.imageData, 1))
            bk = bk.flatten().tolist()
            b = ia.std_vector_double()
            b.extend(bk)
            self.model.offlineAnalysis.loadBackgroundImage(b, self.backgroundData.fullName)
            if self.backgroundData.imageHeight != self.model.imageHeight or self.backgroundData.imageWidth != self.model.imageWidth:
                print 'ERROR: Image and Background are not the same dimensions!'
                return
        else:
            self.model.offlineAnalysis.useBackground(False)
        # This is where we will house expert settings

        if self.view.checkBox_useCustomMask.isChecked() is True:
            self.model.offlineAnalysis.useESMask(True)
            self.model.offlineAnalysis.setESMask(int(self.customMaskROI.pos()[0]+self.customMaskROI.size()[0]/2),
                                                 int(self.customMaskROI.pos()[1]+self.customMaskROI.size()[0]/2),
                                                 int(self.customMaskROI.size()[0]/2),
                                                 int(self.customMaskROI.size()[1]/2))
        else:
            self.model.offlineAnalysis.useESMask(False)
            # make mask span full width of image
            x = int(self.model.imageWidth / 2)
            y = int(self.model.imageHeight / 2)
            self.model.offlineAnalysis.setESMask(x, y, x, y)

        if self.view.checkBox_rollingAverage.isChecked() is True:
            self.model.offlineAnalysis.useESFilter(True)
            self.model.offlineAnalysis.setESFilter(int(self.view.lineEdit_rollingAverage.text()))
        else:
            self.model.offlineAnalysis.useESFilter(False)

        if self.view.checkBox_rSquared.isChecked() is True:
            self.model.offlineAnalysis.useESRRThreshold(True)
            self.model.offlineAnalysis.setESRRThreshold(float(self.view.lineEdit_rSquared.text()))
        else:
            self.model.offlineAnalysis.useESRRThreshold(False)

        if self.view.checkBox_lowestPixValue.isChecked() is True:
            self.model.offlineAnalysis.useESDirectCut(True)
            self.model.offlineAnalysis.setESDirectCut(float(self.view.lineEdit_lowestPixelValue.text()))
        else:
            self.model.offlineAnalysis.useESDirectCut(False)
        self.model.offlineAnalysis.analyse()

    def setSubtarctedImage(self):
        if self.model.imageWidth == self.backgroundData.imageWidth:
            if self.model.imageHeight == self.backgroundData.imageHeight:
                label = (self.model.fullName.split('/')[-1] + ' - ' +
                         self.backgroundData.fullName.split('/')[-1])
                self.subLabel.setText(label)
                im = np.subtract(self.model.imageData.astype(int), self.backgroundData.imageData.astype(int))
                self.subtractedImage.setImage(im)
                self.SubBox.setLimits(xMin=0, yMin=0,
                                         xMax=self.model.imageWidth,
                                         yMax=self.model.imageHeight)
                # self.SubBox.setYLink(self.ImageBox)
                # self.SubBox.setXLink(self.ImageBox)
            else:
                self.subLabel.setText("Image and Background have different heights!")
        else:
            self.subLabel.setText("Image and Background have different widths!")
