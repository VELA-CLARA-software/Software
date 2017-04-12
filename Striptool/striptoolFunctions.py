import time
from bisect import bisect_left, bisect_right

def takeClosestPosition(xvalues, myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    if len(myList) < 1 or myNumber < xvalues[0]:
        return [0,(0,0)]
    pos = bisect_left(xvalues, myNumber)
    if pos == 0:
        return [0,myList[0]]
    if pos == len(myList):
        return [-1,myList[-1]]
    before = myList[pos-1]
    after = myList[pos]
    if abs(after[0] - myNumber) < abs(myNumber - before[0]):
       return [pos,after]
    else:
       return [pos-1,before]

''' This filters the data based on the plotrange of the current viewbox. For small datasets this is ~pointless, but for moderately large datasets
and bigger it makes a noticeable speed up, despite the functions built in to PyQtGraph'''
def timeFilter(datain, timescale=None, currenttime=False):
    if not currenttime:
        currenttime = round(time.time(),2)
    else:
        currenttime = currenttime
    timescale = timescale
    if len(datain) > 0:
        if (datain[0][0] > (currenttime+timescale[0]) and datain[-1][0] <=  (currenttime+timescale[1])):
            return datain
        else:
            if datain[-1][0] <=  (currenttime+timescale[1]):
                datain = datain[bisect_left(datain[:,0], currenttime+timescale[0])-1:-1]
            else:
                if datain[0][0] >= (currenttime+timescale[0]):
                    datain = datain[0:bisect_left(datain[:,0], currenttime+timescale[1])+1]
                else:
                    datain = datain[bisect_left(datain[:,0], currenttime+timescale[0])-1:bisect_left(datain[:,0], currenttime+timescale[1])+1]
            return datain
    else:
        return datain
