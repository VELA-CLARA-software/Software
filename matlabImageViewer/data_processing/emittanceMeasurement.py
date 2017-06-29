import numpy
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from lmfit import Model
import math

class emittanceMeasurement:
    # this class contains the functions for processing images to take emittance data
    # we pass in the main panel, the loaded file and the name of the matlab struct containing the image data

    # this loads in the image data arrays contained in the emittance ".dat" file
    def loadEmitData(self, view, currentFile, datastruct):
        self.startView = view
        self.arrayshape = []
        self.currentFile = currentFile
        self.datastruct = datastruct
        self.subKeyItems = [str(self.startView.subKeysComboBox.itemText(i)) for i in
                            range(self.startView.subKeysComboBox.count())]
        # the key each set of images for a given quad value is named "figureXX", for XX quad settings - I'm not sure what Fraw is but it appears to be the same thing
        for i in self.subKeyItems:
            if i.startswith('figure'):
                self.imagedata = str(self.startView.subKeysComboBox.currentText())
                break
        # this tells the function how to re-shape the 1-d array in "figureXX"
        self.arrayshape.append(self.currentFile[self.datastruct]['arrayy'])
        self.arrayshape.append(self.currentFile[self.datastruct]['arrayx'])
        self.numshots = len(self.currentFile[self.datastruct][self.imagedata]) / (self.arrayshape[0] * self.arrayshape[1])
        self.currentFile[self.datastruct]['numshots'] = self.numshots
        self.arrayshape.append(self.numshots)
        self.croppedArrayShape = [0, self.arrayshape[1], 0, self.arrayshape[0]]
        # we return the number of shots and the array size back to the main controller
        return self.numshots, self.croppedArrayShape, self.arrayshape, self.imagedata

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
            self.yMM = []
            self.xMM = []
            self.newarray = []
            self.x = range(0, self.xCropMax - self.xCropMin)
            self.y = range(0, self.yCropMax - self.yCropMin)
            # we slice the image vertically, then horizontally, each time taking the mean value of each slice
            for slice_2d in numpy.transpose(numpy.transpose(self.newdata)[i][self.xCropMin:self.xCropMax])[self.yCropMin:self.yCropMax]:
                self.n = len(slice_2d)  # the number of data
                self.mean = sum(slice_2d) / self.n  # note this correction
                self.sigma = sum(slice_2d * (slice_2d - self.mean) ** 2) / self.n
                self.sigmaY.append( self.sigma )
                # self.sigmaY.append( self.sigma * ( self.currentFile[self.datastruct]['pixelwidth'] ) )
            for slice_2d in numpy.transpose(self.newdata)[i][self.xCropMin:self.xCropMax]:
                self.n = len(slice_2d)  # the number of data
                self.mean = sum(slice_2d) / self.n  # note this correction
                self.sigma = sum(slice_2d * (slice_2d - self.mean) ** 2) / self.n
                self.sigmaX.append( self.sigma )
                # self.sigmaX.append( self.sigma * ( self.currentFile[self.datastruct]['pixelwidth'] ) )
            # the data is then arranged into 2-d arrays of the pixel value and the sigma value
            self.newarrayY = numpy.vstack((self.y, self.sigmaY))
            self.newarrayX = numpy.vstack((self.x, self.sigmaX))
            # we fit a gaussian - see scipy.io.curve_fit documentation for more info
            self.fitx, self.tmpx = curve_fit(self.gaussFit, self.newarrayX[0], self.newarrayX[1], p0=[max(self.newarrayX[1]), self.newarrayX[1][int(len(self.newarrayX[0])/2)], numpy.mean(self.newarrayX[1])])
            self.fity, self.tmpy = curve_fit(self.gaussFit, self.newarrayY[0], self.newarrayY[1], p0=[max(self.newarrayY[1]), self.newarrayY[1][int(len(self.newarrayY[0])/2)], numpy.mean(self.newarrayY[1])])
            # self.gModel = Model(self.gaussFit)
            # print(self.gModel.param_names, self.gModel.independent_vars)
            # self.result = self.gModel.fit(self.newarrayX[1], x=self.newarrayX[0], a=5, x0=50, sigma=1)
            # plt.plot(self.newarrayX[0], self.newarrayX[1])
            # plt.plot(self.newarrayX[0], self.gaussFit(self.newarrayX[0],*self.fitx))
            # plt.show()
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
        return (self.a/(numpy.sqrt(2*math.pi)*self.sigma)) * numpy.exp(-(self.x - self.x0) ** 2 / (2 * self.sigma ** 2))

    # for fitting a polynomial to the (sigma_x)^2 values
    def polyFit(self, x, a, b, c):
        self.x = x
        self.a = a
        self.b = b
        self.c = c
        return ( self.a * ( self.x ** self.b ) ) + c

    # this iterates through all of the "figureXX" arrays in the ".dat" file, takes projections using the getProjections function above
    # and returns (sigma_x-y)^2
    def getSigmaSquared(self, view, currentFile, datastruct, arrayshape, croppedarrayshape, numshots):
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
                self.sig.append((abs(a[2]) * (self.currentFile[self.datastruct]['pixelwidth']) ) ** 2 )
                # self.sig.append((abs(a[2]) * abs(a[2])))
            self.xSigmas.append(self.sig)
            self.meanSigma = numpy.mean(self.sig)
            self.xSigmaSquared.append(self.meanSigma)
            print i, self.meanSigma
        for k, l in sorted(self.yProjs.items()):
            self.sig = []
            for a in l:
                self.sig.append((abs(a[2]) * (self.currentFile[self.datastruct]['pixelwidth']) ) ** 2 )
                # self.sig.append((abs(a[2]) * abs(a[2])))
            self.ySigmas.append(self.sig)
            self.meanSigma = numpy.mean(self.sig)
            self.ySigmaSquared.append(self.meanSigma)
        return self.quadK, self.xSigmaSquared, self.xSigmas, self.ySigmaSquared, self.ySigmas

    # fit a polynomial (x^2) to (sigma_x-y)^2 and extract fit parameters to calculate emittance and Twiss
    def plotSigmaSquared(self, view, quadK, xSigmaSquared, xSigmas, ySigmaSquared, ySigmas):
        self.startView = view
        self.quadK = quadK
        self.xSigmaSquared = xSigmaSquared
        self.xSigmas = xSigmas
        self.ySigmaSquared = ySigmaSquared
        self.ySigmas = ySigmas
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
        # self.yemitax.plot(self.newarrayY[0], self.newarrayY[1])
        self.yemitax.set_xlabel('quad k')
        self.yemitax.set_ylabel('(sigma y)^2 (pix)')
        # self.xemitax.plot(self.newarrayX[0], self.newarrayX[1])
        self.xemitax.set_xlabel('quad k')
        self.xemitax.set_ylabel('(sigma x)^2 (pix)')
        # we fit a polynomial to the (sigma_x)^2 values as a function of quad strength
        self.x_new = numpy.linspace(self.newarrayX[0][0], self.newarrayX[0][-1], num=len(self.newarrayX[0]) * 10)
        self.fitpolyx = numpy.polynomial.polynomial.polyfit(self.newarrayX[0], self.newarrayX[1], 2, full=True)
        self.ffitx = numpy.polynomial.polynomial.polyval(self.x_new, self.fitpolyx[0])
        self.y_new = numpy.linspace(self.newarrayY[0][0], self.newarrayY[0][-1], num=len(self.newarrayY[0]) * 10)
        self.fitpolyy = numpy.polynomial.polynomial.polyfit(self.newarrayY[0], self.newarrayY[1], 2, full=True)
        self.ffity = numpy.polynomial.polynomial.polyval(self.y_new, self.fitpolyy[0])
        self.xemitax.plot(self.x_new, self.ffitx)
        self.yemitax.plot(self.y_new, self.ffity)
        self.xemitax.plot(self.newarrayX[0], self.newarrayX[1], color="black")
        self.yemitax.plot(self.newarrayY[0], self.newarrayY[1], color="black")
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
        print self.fitpolyx,"fitpolyx"
        print self.fitpolyy,"fitpolyy"
        return self.fitpolyx, self.fitpolyy

    # from fitted polynomials for x and y, calculate emittance and twiss
    def getEmittance(self, fitpolyx, fitpolyy, driftlength, energy):
        self.fitpolyx = fitpolyx
        self.fitpolyy = fitpolyy
        self.driftlength = driftlength
        self.energy = energy
        self.relativisticGamma = self.energy / 0.511
        self.aX = self.fitpolyx[0][0]
        self.bX = self.fitpolyx[0][1] / ( 2 * self.aX )
        self.cX = self.fitpolyx[0][2] - ( self.aX * ( self.bX ** 2 ) )
        self.aY = self.fitpolyy[0][0]
        self.bY = self.fitpolyy[0][1] / ( 2 * self.aY )
        self.cY = self.fitpolyy[0][2] - ( self.aY * ( self.bY ** 2 ) )
        self.emittanceX = numpy.sqrt( self.aX * self.cX ) / ( self.driftlength**2 )
        self.emittanceXNormalised = self.emittanceX * self.relativisticGamma
        self.alphaX = numpy.sqrt( self.aX / self.cX ) * ( self.bX + ( 1 / self.driftlength ) )
        self.betaX = numpy.sqrt( self.aX / self.cX )
        self.gammaX = ( 1 + ( self.alphaX * self.alphaX ) ) / ( self.betaX )
        self.emittanceY = numpy.sqrt( self.aY * self.cY ) / ( self.driftlength**2 )
        self.emittanceYNormalised = self.emittanceY * self.relativisticGamma
        self.alphaY = numpy.sqrt( self.aY / self.cY ) * ( self.bY + ( 1 / self.driftlength ) )
        self.betaY = numpy.sqrt( self.aY / self.cY )
        self.gammaY = ( 1 + ( self.alphaY * self.alphaY ) ) / ( self.betaY )
        self.xTwiss = [self.emittanceX, self.emittanceXNormalised, self.alphaX, self.betaX, self.gammaX]
        self.yTwiss = [self.emittanceY, self.emittanceYNormalised, self.alphaY, self.betaY, self.gammaY]
        return self.xTwiss, self.yTwiss