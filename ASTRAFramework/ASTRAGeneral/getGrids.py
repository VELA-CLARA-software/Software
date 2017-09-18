import numpy as np

class getGrids(object):

    def __init__(self, npart=1000):
        self.powersof8 = np.asarray([ 2**(j) for j in range(1,20) ])
        self.n = npart
        self.gridSizes = self.calculateGridSizes(int(self.n))

    def getGridSizes(self):
        return self.gridSizes

    def calculateGridSizes(self, x):
        self.x = abs(x)
        self.cuberoot = int(round(self.x ** (1. / 3)))
        return max([1,self.find_nearest(self.powersof8, self.cuberoot)])

    def find_nearest(self, array, value):
        self.array = array
        self.value = value
        self.idx = (np.abs(self.array - self.value)).argmin()
        return self.array[self.idx]
