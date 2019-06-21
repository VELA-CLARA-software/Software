class BDRollingAverage:

    bdHist = []
    pulseCount = 0
    bdCount = 0
    
    def __init__(self, averagingPulses, bdNormalRate):
        self.averagingPulses = averagingPulses
        self.bdNormalRate = bdNormalRate

    def addPulse(self, isBd):
        self.bdHist.append(isBd)
        self.pulseCount += 1
        
        if isBd == True:
            self.bdCount += 1
        
        if self.pulseCount > self.averagingPulses:
            self.pulseCount -= 1
            if self.bdHist.last() == True:
                self.bdCount -= 1
            self.bdHist.pop(0)
            
    def getBdRate(self):
        # Avoid division by zero
        if self.pulseCount > 0:
            return float(self.bdCount) / float(self.pulseCount)
        else:
            return 0
            
    def isBdRateExceeded(self):
        return self.getBdRate() > self.bdNormalRate
