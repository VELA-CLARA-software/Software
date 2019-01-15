#import os, sys
import pyqtgraph as pg
import numpy as np
import VELA_CLARA_Camera_Control as cam
import time
# initialise etc.
camInit = cam.init()
cameras = camInit.physical_CLARA_Camera_Controller()

# get list of camera names
names = list(cameras.getCameraNames())
print names

# remove any you're not interested in e.g. VC
#names.remove('VIRTUAL_CATHODE')
#print names

# print the names of cameras that are acquiring
for name in names:
    if cameras.isAcquiring(name):
        print name
        #cameras.collectAndSave(1, name)
        #print 'it worked?'
        #cameras.takeAndGetFastImage(name)
        #cameras.setCamera(name)
        cameras.stopAcquiring()
        time.sleep(1)
print 'here'
cameras.startAcquiring('C2V-CAM-01')
time.sleep(1)

for name in names:
    if cameras.isAcquiring(name):
        print name
time.sleep(1)

print 'here2'
cameras.collectAndSave(1)
time.sleep(1)
exit()




print cameras.latestCollectAndSaveSuccess_VC()
exit()
if cameras.latestCollectAndSaveSuccess():
	print 'collectAndSave Check Success'
else:
	print 'collectAndSave Check FAIL'

if cameras.collectAndSave(1):
	print 'collectAndSave SENT '
else:
	print 'collectAndSave FAIL'

exit()
#imageData = cameras.takeAndGetFastImage('S01-CAM-01')
#imageData = cameras.takeAndGetFastImage('CAM14')
#imageData = cameras.getFastImage('CAM14')

#cameras.setCamera('VC')
#time.sleep(1)
#cameras.startAcquiring()
#time.sleep(1)
#cameras.collectAndSave(1)
#time.sleep(1)
#cameras.stopAcquiring()
#time.sleep(1)

exit()
imageData = cameras.takeAndGetFastImage('CAM14')
print imageData[:10]
print len(imageData)
xpix = cameras.getNumPixX()
ypix =  cameras.getNumPixY()
#imageData = np.array(imageData)
imageData2 = np.reshape(imageData, (xpix, ypix))
print len(imageData2)

pg.image(imageData2, min(imageData), max(imageData))
raw_input("Press Enter to continue...")
