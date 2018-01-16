import numpy

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