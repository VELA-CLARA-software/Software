import numpy
import scipy
from matplotlib.colors import LogNorm
from numpy.polynomial import polynomial
import matplotlib.pyplot as plt

class energySpreadMeasurement:
    # this class contains the functions for processing images to take energy spread data
    # we pass in the main panel, the loaded file and the name of the matlab struct containing the image data

    # load in the data contained in "immagini", re-shape this 1-d array into "numshots" of images of "arrayx" by "arrayy" pixels,
    # and plot on the main plot canvas
    def loadEnergySpreadData(self, view, currentFile, datastruct, imagedata):
        self.startView = view
        self.currentFile = currentFile
        self.plotsLoaded = True
        self.datastruct = datastruct
        self.imagedata = imagedata
        self.arrayshape = []
        self.allplots = []
        self.numshots = self.currentFile[self.datastruct]['numshots']
        self.arrayshape.append(self.currentFile[self.datastruct]['arrayy'])
        self.arrayshape.append(self.currentFile[self.datastruct]['arrayx'])
        self.arrayshape.append(self.numshots)
        for i in range(0, self.numshots):
            self.plotfig = self.startView.plotWidget
            self.allplots.append(
                self.startView.makePlots(self.currentFile, self.datastruct,
                                         self.imagedata, self.arrayshape, i, self.plotfig))
        self.allplots[-1][0].canvas.draw()
        self.startView.fileSlider.setMaximum(self.numshots - 1)
        self.startView.fileSlider.setValue(self.numshots - 1)
        self.croppedArrayShape = [0, self.arrayshape[1], 0, self.arrayshape[0]]
        return self.numshots, self.croppedArrayShape, self.arrayshape, self.allplots

    def makeFit(self, view, currentFile, datastruct, imagedata, arrayshape, croppedarrayshape, index):
        self.startView = view
        self.currentFile = currentFile
        self.datastruct = datastruct
        self.imagedata = imagedata
        self.arrayshape = arrayshape
        self.croppedArrayShape = croppedarrayshape
        self.index = index
        # reshape the 1-d array contained in "immagini" (imagedata) based on the dimensions of "arrayshape"
        self.data = self.currentFile[self.datastruct][self.imagedata]
        self.newdata = numpy.reshape(self.data, self.arrayshape)
        self.fitfig = self.startView.currentPlotWidget
        self.fitfig.canvas.flush_events()
        # crops the image (if requested by user)
        self.xCropMax = max(self.croppedArrayShape[:2])
        self.xCropMin = min(self.croppedArrayShape[:2])
        self.yCropMax = max(self.croppedArrayShape[2:])
        self.yCropMin = min(self.croppedArrayShape[2:])
        self.sigmaY = []
        self.croppeddataY = numpy.transpose(numpy.transpose(self.newdata)[self.index][self.xCropMin:self.xCropMax])[self.yCropMin:self.yCropMax]
        self.croppeddataX = numpy.transpose(self.newdata)[self.index][self.xCropMin:self.xCropMax]
        self.x_new = numpy.linspace(self.croppeddataY[0][0], self.croppeddataY[0][-1], num=len(self.croppeddataY))
        self.coefs = polynomial.polyfit(self.croppeddataY[0], self.croppeddataY[1], 3, full=True)
        print type(self.croppeddataY)
        self.ffit = polynomial.polyval(self.x_new, self.coefs[0])
        print self.ffit
        self.fitax = self.fitfig.add_subplot(111)
        self.fitax.plot(self.x_new, self.ffit)
        self.fitax.set_aspect('auto')
        self.fitax.set_aspect('auto')
        self.fitfig.canvas.draw()

    # for a given shot, we take the sum of all the pixels in each slice (or over an averaged amount of slices),
    # and plot the vertical projection of the beam
    def getEnergySpread(self, view, currentFile, datastruct, imagedata, arrayshape, croppedarrayshape, index):
        self.startView = view
        self.currentFile = currentFile
        self.datastruct = datastruct
        self.imagedata = imagedata
        self.arrayshape = arrayshape
        self.croppedArrayShape = croppedarrayshape
        self.index = index
        # reshape the 1-d array contained in "immagini" (imagedata) based on the dimensions of "arrayshape"
        self.data = self.currentFile[self.datastruct][self.imagedata]
        self.newdata = numpy.reshape(self.data, self.arrayshape)
        self.currentplotfig = self.startView.currentPlotWidget
        self.currentplotfig.canvas.flush_events()
        self.energyspreadplotfig = self.startView.energySpreadPlotWidget
        self.energyspreadplotfig.canvas.flush_events()
        self.startView.currentaxis.cla()
        self.startView.energySpreadaxis.cla()
        # crops the image (if requested by user)
        self.xCropMax = max(self.croppedArrayShape[:2])
        self.xCropMin = min(self.croppedArrayShape[:2])
        self.yCropMax = max(self.croppedArrayShape[2:])
        self.yCropMin = min(self.croppedArrayShape[2:])
        self.croppeddataY = numpy.transpose(numpy.transpose(self.newdata)[self.index][self.xCropMin:self.xCropMax])[self.yCropMin:self.yCropMax]
        self.croppeddataX = numpy.transpose(self.newdata)[self.index][self.xCropMin:self.xCropMax]
        self. i = 0
        self.sigmaY = []
        self.sigmaYAvg = []
        self.yAvg = []
        self.sigmaX = []
        self.sigmaXAvg = []
        self.xAvg = []
        self.currentArray = []
        self.energySpreadArray = []
        self.x = range(0, self.xCropMax - self.xCropMin)
        self.y = range(0, self.yCropMax - self.yCropMin)
        # sums up each slice and takes a mean
        for slice_2d in self.croppeddataY:
            self.n = len(slice_2d)  # the number of data
            self.mean = sum(slice_2d) / self.n  # note this correction
            # self.sigma = sum(slice_2d * (self.mean) ** 2) / self.n
            self.sigma = sum(slice_2d * (slice_2d - self.mean) ** 2) / self.n
            self.sigmaY.append(self.sigma)
        for slice_2d in self.croppeddataX:
            self.n = len(slice_2d)  # the number of data
            self.mean = sum(slice_2d) / self.n  # note this correction
            # self.sigma = sum(slice_2d * (self.mean) ** 2) / self.n
            self.sigma = sum(slice_2d * (slice_2d - self.mean) ** 2) / self.n
            self.sigmaX.append(self.sigma)
        # does averaging if requested
        if self.startView.averaging.isChecked():
            self.averagingInterval = int(self.startView.intervalText.toPlainText())
            for i in range(0, len(self.sigmaY), self.averagingInterval):
                if not (len(self.sigmaY) - i) < self.averagingInterval:
                    self.sigmaYAvg.append(numpy.mean(self.sigmaY[i:i + self.averagingInterval]))
                    self.yAvg.append(numpy.mean(self.y[i:i + self.averagingInterval]))
                else:
                    self.sigmaYAvg.append(numpy.mean(self.sigmaY[i:-1]))
                    self.yAvg.append(numpy.mean(self.y[i:i - 1]))
            for i in range(0, len(self.sigmaX), self.averagingInterval):
                if not (len(self.sigmaX) - i) < self.averagingInterval:
                    self.sigmaXAvg.append(numpy.mean(self.sigmaX[i:i + self.averagingInterval]))
                    self.xAvg.append(numpy.mean(self.x[i:i + self.averagingInterval]))
                else:
                    self.sigmaXAvg.append(numpy.mean(self.sigmaX[i:-1]))
                    self.xAvg.append(numpy.mean(self.x[i:i - 1]))
            self.currentArray = numpy.vstack((self.yAvg, self.sigmaYAvg))
            self.energySpreadArray = numpy.vstack((self.xAvg, self.sigmaXAvg))
        elif self.startView.noAvg.isChecked():
            self.currentArray = numpy.vstack((self.x, self.sigmaX))
            self.energySpreadArray = numpy.vstack((self.y, self.sigmaY))
        else:
            print "choose averaging or unfiltered, fool"
        # plot projection
        self.currentax = self.currentplotfig.add_subplot(111)
        self.energyspreadax = self.energyspreadplotfig.add_subplot(111)
        # self.ax.plot(self.currentArray[0], self.currentArray[1], marker = "o")
        self.currentax.plot(self.currentArray[0], self.currentArray[1], marker="o")
        self.currentax.set_aspect('auto')
        self.currentax.set_xlabel('x projection')
        self.currentax.set_ylabel('avg(sum x pixels) per slice')
        self.energyspreadax.plot(self.energySpreadArray[0], self.energySpreadArray[1], marker="o")
        self.energyspreadax.set_aspect('auto')
        self.energyspreadax.set_xlabel('y projection')
        self.energyspreadax.set_ylabel('avg(sum y pixels) per slice')
        self.currentplotfig.canvas.draw()
        self.energyspreadplotfig.canvas.draw()

    def fourierAnalysis(self, view, currentFile, datastruct, imagedata, arrayshape, index):
        self.startView = view
        self.datastruct = datastruct
        self.imagedata = imagedata
        self.currentFile = currentFile
        self.arrayshape = arrayshape
        self.index = index
        self.Npoints = self.currentFile[self.datastruct]['numshots']
        self.Nloops = self.startView.allFilesComboBox.count()
        self.data = self.currentFile[self.datastruct][self.imagedata]
        self.imgs = numpy.reshape(self.data, self.arrayshape)
        self.res = 1
        self.form = numpy.array([self.arrayshape[0], self.arrayshape[1], self.Nloops])
        self.formaFFT = self.res * self.form
        self.esse = numpy.array([self.form[0], self.form[1]]) * self.res
        self.imgsempty = numpy.zeros_like(numpy.copy(self.imgs[:, :, 0]))
        self.imgsFFT2Dempty = numpy.zeros_like(numpy.abs(numpy.fft.fft2(self.imgs[:, :, 0], s=[self.esse[0], self.esse[1]])))
        self.fftSUM = numpy.copy(self.imgsFFT2Dempty)
        self.imgsSUM = numpy.copy(self.imgsempty)
        for p in range(self.Npoints):
            self.fftSUM += numpy.fft.fftshift(numpy.abs(numpy.fft.fft2(self.imgs[:, :, p], s=[self.esse[0], self.esse[1]])))
            self.imgsSUM += self.imgs[:, :, p]

        self.fftAv = self.fftSUM / self.Npoints
        self.imgsAv = self.imgsSUM / self.Npoints
        self.fft_imgsAv = numpy.fft.fftshift(numpy.abs(numpy.fft.fft2(self.imgsSUM, s=[self.esse[0], self.esse[1]])))

        self.center = [self.fftAv.shape[0] / 2, self.fftAv.shape[1] / 2]
        self.R = 50  # in pixel
        self.bordo = -self.R
        self.fi = 30  # in gradi
        self.num = self.R - self.bordo  # numero punti

        self.x0, self.y0 = self.center[1], self.center[0]
        self.x1, self.y1 = self.x0 + self.bordo * numpy.cos(numpy.deg2rad(self.fi)), self.y0 + self.bordo * numpy.sin(numpy.deg2rad(-self.fi))
        self.x2, self.y2 = self.x0 + self.R * numpy.cos(numpy.deg2rad(self.fi)), self.y0 + self.R * numpy.sin(numpy.deg2rad(-self.fi))
        print self.x1, self.x2, self.y1, self.y2, self.num
        print self.index
        self.x, self.y = numpy.linspace(self.x1, self.x2, self.num), numpy.linspace(self.y1, self.y2, self.num)

        self.currentplotfig = self.startView.currentPlotWidget
        # self.currentplotfig.canvas.flush_events()
        self.energyspreadplotfig = self.startView.energySpreadPlotWidget
        # self.energyspreadplotfig.canvas.flush_events()
        # self.startView.currentaxis.cla()
        # self.startView.energySpreadaxis.cla()
        self.currentax = self.currentplotfig.add_subplot(111)
        self.energyspreadax = self.energyspreadplotfig.add_subplot(111)
        # self.ax.plot(self.currentArray[0], self.currentArray[1], marker = "o")
        # self.currentax.imshow(self.fftSUM)
        # self.currentax.set_aspect('auto')
        # self.currentax.set_xlabel('x projection')
        # self.currentax.set_ylabel('avg(sum x pixels) per slice')
        self.loop = 0
        self.zi1 = scipy.ndimage.map_coordinates(self.fftAv[:,:], numpy.vstack((self.y,self.x)))
        # self.energyspreadax.plot(self.zi1*self.index)
        # self.energyspreadax.set_aspect('auto')
        # self.energyspreadax.set_xlabel('y projection')
        # self.energyspreadax.set_ylabel('avg(sum y pixels) per slice')
        # self.currentplotfig.canvas.draw()
        # self.energyspreadplotfig.canvas.draw()
        return self.fftSUM, self.zi1

    def fourierAnalysis1(self, view, imgs, attu):
        self.startView = view
        self.imgs = imgs
        self.attu = attu
        self.plot2fig = self.startView.currentPlotWidget
        self.plot2fig.canvas.flush_events()
        self.plot1fig = self.startView.energySpreadPlotWidget
        self.plot1fig.canvas.flush_events()

        self.imgNum = 1 # indice immagine da plottare
    # #line profile su una linea che parte dal centro, di lunghezza R ad un angolo fi dall'asse x
        self.center = [self.imgs.shape[0]/2, self.imgs.shape[1]/2]
        self.R = 50 # in pixel
        self.bordo = -self.R
        self.fi = 30 # in gradi
        self.num = self.R-self.bordo # numero punti

        self.x0, self.y0 = self.center[1], self.center[0]
        self.x1, self.y1 = self.x0+self.bordo*numpy.cos(numpy.deg2rad(self.fi)), self.y0+self.bordo*numpy.sin(numpy.deg2rad(-self.fi))
        self.x2, self.y2 = self.x0+self.R*numpy.cos(numpy.deg2rad(self.fi)), self.y0+self.R*numpy.sin(numpy.deg2rad(-self.fi))
        print self.x1, self.x2, self.y1, self.y2, self.num
        self.x, self.y = numpy.linspace(self.x1, self.x2, self.num), numpy.linspace(self.y1, self.y2, self.num)
    #
    # # Extract the values along the line, using cubic interpolation
        self.zi = scipy.ndimage.map_coordinates(self.imgs[:,:,self.imgNum], numpy.vstack((self.y,self.x)))
        self.plot1 = self.plot1fig.add_subplot(111)
        self.plot2 = self.plot2fig.add_subplot(111)
        # self.ax.plot(self.currentArray[0], self.currentArray[1], marker = "o")
        self.plot1.imshow(self.imgs[:, :, self.imgNum], norm=LogNorm())
        self.plot1.plot([self.x1, self.x2], [self.y1, self.y2], 'ro-')
        self.plot1.set_aspect('auto')
        self.plot1.set_xlabel('x projection')
        self.plot1.set_ylabel('avg(sum x pixels) per slice')
        self.loop = 0
        print self.imgs.shape[2]
        while self.loop < self.imgs.shape[2]:
            self.zi1 = scipy.ndimage.map_coordinates(self.imgs[:,:,self.loop], numpy.vstack((self.y,self.x)))
            self.plot2.plot(self.zi1+30000*self.loop)
            self.loop += 1
        # self.plot2.xlim(100, 300)
        # self.plot2.ylim(-10000,300000)
        self.plot2.set_aspect('auto')
        self.plot2.set_xlabel('y projection')
        self.plot2.set_ylabel('avg(sum y pixels) per slice')
        self.plot1fig.canvas.draw()
        self.plot2fig.canvas.draw()
    # plt.figure(1)
    # plt.clf()
    # plt.subplot(211)
    # plt.imshow(imgs[:,:,imgNum], norm=LogNorm())
    # plt.plot([x1, x2], [y1, y2], 'ro-')
    #
    # plt.subplot(212)
    # plt.plot(zi)
    #
    # plt.show()
    # plt.figure(2)
    # plt.clf()
    # loop = 0
    # print imgs.shape[2]
    # while loop < imgs.shape[2]:
    #     zi = scipy.ndimage.map_coordinates(imgs[:,:,loop], np.vstack((y,x)))
    #     plt.plot(zi+10000*loop)
    #     loop += 1
    #
    # plt.xlim(100,300)
    # plt.ylim(-10000,300000)
    #
    # # plt.show()