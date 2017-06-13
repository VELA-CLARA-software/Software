import numpy
from scipy.optimize import curve_fit

class emittanceMeasurement:
    # this class contains the functions for processing images to take emittance data
    # we pass in the main panel, the loaded file and the name of the matlab struct containing the image data

    # this loads in the image data arrays contained in the emittance ".dat" file
    def loadEmitData(self, view, currentFile, datastruct):
        self.startView = view
        self.allplots = []
        self.arrayshape = []
        self.currentFile = currentFile
        self.datastruct = datastruct
        self.subKeyItems = [str(self.startView.subKeysComboBox.itemText(i)) for i in
                            range(self.startView.subKeysComboBox.count())]
        # the key each set of images for a given quad value is named "figureXX", for XX quad settings - I'm not sure what Fraw is but it appears to be the same thing
        for i in self.subKeyItems:
            if i.startswith('figure') or i.startswith('Fraw'):
                self.imagedata = str(self.startView.subKeysComboBox.currentText())
                break
        # this tells the function how to re-shape the 1-d array in "figureXX"
        self.arrayshape.append(self.currentFile[self.datastruct]['arrayy'])
        self.arrayshape.append(self.currentFile[self.datastruct]['arrayx'])
        self.numshots = len(self.currentFile[self.datastruct][self.imagedata]) / (self.arrayshape[0] * self.arrayshape[1])
        self.currentFile[self.datastruct]['numshots'] = self.numshots
        self.arrayshape.append(self.numshots)
        self.croppedArrayShape = [0, self.arrayshape[1], 0, self.arrayshape[0]]
        for i in range(0, self.numshots):
            self.plotfig = self.startView.plotWidget
            self.allplots.append(
                self.startView.makePlots(self.currentFile, self.datastruct,
                                         self.imagedata, self.arrayshape, i, self.plotfig))
        self.allplots[-1][0].canvas.draw()
        self.startView.fileSlider.setMaximum(self.numshots - 1)
        self.startView.fileSlider.setValue(self.numshots - 1)
        # we return the number of shots and the array size back to the main controller
        return self.numshots, self.croppedArrayShape, self.arrayshape

    # from a given "figureXX" key in the ".dat" file, we take the x and y projections for each show
    def getProjections(self, view, numshots, currentFile, datastruct, datastring, arrayshape, croppedArrayShape):
        self.startView = view
        self.numshots = numshots
        self.currentFile = currentFile
        self.datastruct = datastruct
        self.datastring = datastring
        self.arrayshape = arrayshape
        self.croppedArrayShape = croppedArrayShape
        self.tmpxvec = []
        self.tmpyvec = []
        self.fitxvec = []
        self.fityvec = []
        # the 1-d array containing "numshots" images is re-shaped according to the array size
        self.data = self.currentFile[self.datastruct][self.datastring]
        self.newdata = numpy.reshape(self.data, self.arrayshape)
        self.xCropMax = max(self.croppedArrayShape[:2])
        self.xCropMin = min(self.croppedArrayShape[:2])
        self.yCropMax = max(self.croppedArrayShape[2:])
        self.yCropMin = min(self.croppedArrayShape[2:])
        self. i = 0
        for i in range(0, self.numshots - 1):
            self.sigmaY = []
            self.sigmaYsquared = []
            self.sigmaX = []
            self.sigmaXsquared = []
            self.sigmaYAvg = []
            self.sigmaXAvg = []
            self.yAvg = []
            self.xAvg = []
            self.newarray = []
            self.x = range(0, self.xCropMax - self.xCropMin)
            self.y = range(0, self.yCropMax - self.yCropMin)
            # we slice the image vertically, then horizontally, each time taking the mean value of each slice
            for slice_2d in numpy.transpose(numpy.transpose(self.newdata)[i][self.xCropMin:self.xCropMax])[self.yCropMin:self.yCropMax]:
                self.n = len(slice_2d)  # the number of data
                self.mean = sum(slice_2d) / self.n  # note this correction
                self.sigma = sum(slice_2d * (slice_2d - self.mean) ** 2) / self.n
                self.sigmaY.append(self.sigma)
            for slice_2d in numpy.transpose(self.newdata)[i][self.xCropMin:self.xCropMax]:
                self.n = len(slice_2d)  # the number of data
                self.mean = sum(slice_2d) / self.n  # note this correction
                self.sigma = sum(slice_2d * (slice_2d - self.mean) ** 2) / self.n
                self.sigmaX.append(self.sigma)
            # the data is then arranged into 2-d arrays of the pixel value and the sigma value
            self.newarrayY = numpy.vstack((self.y, self.sigmaY))
            self.newarrayX = numpy.vstack((self.x, self.sigmaX))
            # we fit a gaussian see scipy.io.curve_fit documentation for more info
            # no doubt this will include our in-house image processing module in the future
            self.fitx, self.tmpx = curve_fit(self.gaussFit, self.x, self.sigmaX, p0=[1, 20, numpy.mean(self.sigmaX)])
            self.fity, self.tmpy = curve_fit(self.gaussFit, self.y, self.sigmaY, p0=[1, 20, numpy.mean(self.sigmaY)])

            self.fitxvec.append(self.fitx)
            self.fityvec.append(self.fity)
            # the vectors of all the fits are returned to the main controller
        return self.fitxvec, self.fityvec

    # for gaussian fitting of a set of data
    def gaussFit(self, x, a, x0, sigma):
        self.x = x
        self.a = a
        self.x0 = x0
        self.sigma = sigma
        return self.a * numpy.exp(-(self.x - self.x0) ** 2 / (2 * self.sigma ** 2))

    # this iterates through all of the "figureXX" arrays in the ".dat" file, takes projections using the getProjections function above,
    # and plots (sigmaX/Y)^2 for each shot
    def getEmittance(self, view, currentFile, datastruct, arrayshape, croppedarrayshape, numshots):
        self.startView = view
        self.currentFile = currentFile
        self.datastruct = datastruct
        self.arrayshape = arrayshape
        self.croppedArrayShape = croppedarrayshape
        self.numshots = numshots
        self.xProjs = {}
        self.yProjs = {}
        self.quadK = []
        self.xSigmas = []
        self.xSigmaSquared = []
        self.ySigmas = []
        self.ySigmaSquared = []
        self.j = 0
        self.subKeyItems = [str(self.startView.subKeysComboBox.itemText(i)) for i in
                            range(self.startView.subKeysComboBox.count())]
        # get X and Y projections for each "figureXX" in "DATA"
        for i in self.subKeyItems:
            if i.startswith("figure"):
                self.projections = self.getProjections(self.startView, self.numshots, self.currentFile,
                                                                            self.datastruct, i, self.arrayshape,
                                                                            self.croppedArrayShape)
                self.xProjs[int(i[6:])] = self.projections[0]
                self.yProjs[int(i[6:])] = self.projections[1]
                self.j = self.j + 1
            if i == "kq":
                self.quadK = self.currentFile[self.datastruct][i]
        # get the standard deviation of each gaussian fit in x and y for each shot and square it
        for i, j in sorted(self.xProjs.items()):
            self.sig = []
            for a in j:
                self.sig.append(abs(a[2]) * abs(a[2]))
            self.xSigmas.append(self.sig)
            self.meanSigma = numpy.mean(self.sig)
            self.xSigmaSquared.append(self.meanSigma)
        for k, l in sorted(self.yProjs.items()):
            self.sig = []
            for a in l:
                self.sig.append(abs(a[2]) * abs(a[2]))
            self.ySigmas.append(self.sig)
            self.meanSigma = numpy.mean(self.sig)
            self.ySigmaSquared.append(self.meanSigma)
        # lots o' plots
        self.xemitplotfig = self.startView.sigmaXPlotWidget
        self.yemitplotfig = self.startView.sigmaYPlotWidget
        self.xemitplotfig.canvas.flush_events()
        self.yemitplotfig.canvas.flush_events()
        self.startView.sigmaxaxis.cla()
        self.startView.sigmayaxis.cla()
        self.newarrayY = numpy.vstack((self.quadK, self.ySigmaSquared))
        self.newarrayX = numpy.vstack((self.quadK, self.xSigmaSquared))
        self.xemitax = self.xemitplotfig.add_subplot(111)
        self.yemitax = self.yemitplotfig.add_subplot(111)
        self.yemitax.plot(self.newarrayY[0], self.newarrayY[1])
        self.yemitax.set_xlabel('quad k')
        self.yemitax.set_ylabel('(sigma y)^2 (pix)')
        self.xemitax.plot(self.newarrayX[0], self.newarrayX[1])
        self.xemitax.set_xlabel('quad k')
        self.xemitax.set_ylabel('(sigma x)^2 (pix)')
        for xe, ye in zip(self.newarrayY[0], self.ySigmas):
            self.yemitax.scatter([xe] * len(ye), ye, color='red')
        for xe, ye in zip(self.newarrayX[0], self.xSigmas):
            self.xemitax.scatter([xe] * len(ye), ye, color='red')
        self.xleg = self.xemitax.legend(loc='upper center', fancybox=True, shadow=True)
        self.yleg = self.yemitax.legend(loc='upper center', fancybox=True, shadow=True)
        self.xemitax.set_aspect('auto')
        self.yemitax.set_aspect('auto')
        self.xemitplotfig.canvas.draw()
        self.yemitplotfig.canvas.draw()