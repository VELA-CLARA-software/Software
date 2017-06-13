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
        self.croppedplotfig = self.startView.analysisPlotWidget
        self.croppedplotfig.canvas.flush_events()
        self.startView.analysisaxis.cla()
        # crops the image (if requested by user)
        self.xCropMax = max(self.croppedArrayShape[:2])
        self.xCropMin = min(self.croppedArrayShape[:2])
        self.yCropMax = max(self.croppedArrayShape[2:])
        self.yCropMin = min(self.croppedArrayShape[2:])
        self.croppeddata = numpy.transpose(numpy.transpose(self.newdata)[self.index][self.xCropMin:self.xCropMax])[self.yCropMin:self.yCropMax]
        self. i = 0
        self.sigmaY = []
        self.sigmaYAvg = []
        self.yAvg = []
        self.newarray = []
        self.x = range(0, self.xCropMax - self.xCropMin)
        self.y = range(0, self.yCropMax - self.yCropMin)
        # sums up each slice and takes a mean
        for slice_2d in self.croppeddata:
            self.n = len(slice_2d)  # the number of data
            self.mean = sum(slice_2d) / self.n  # note this correction
            self.sigma = sum(slice_2d * (self.mean) ** 2) / self.n
            self.sigmaY.append(self.sigma)
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
            self.newarray = numpy.vstack((self.yAvg, self.sigmaYAvg))
        elif self.startView.noAvg.isChecked():
            self.newarray = numpy.vstack((self.y, self.sigmaY))
        else:
            print "choose averaging or unfiltered, fool"
        # plot projection
        self.ax = self.croppedplotfig.add_subplot(111)
        self.ax.plot(self.newarray[0], self.newarray[1])
        self.ax.set_aspect('auto')
        self.ax.set_xlabel('y projection')
        self.ax.set_ylabel('avg(sum y pixels) per slice')
        self.croppedplotfig.canvas.draw()