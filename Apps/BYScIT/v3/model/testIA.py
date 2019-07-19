import VELA_CLARA_Camera_IA_Control as ia
import model
import numpy as np
import time
print 'Now lets try'
h = ia.init()
#h.setVerbose()
cameras = h.offline_CLARA_Camera_IA_Controller()


offline = cameras.getOfflineIARef()
ha = model.Model()
ha.getImage('testImages\\im.raw')
imHeight = ha.imageHeight
imWidth = ha.imageWidth
IMM = np.flip(np.transpose(np.array(ha.imageData)), 1)
print "hi", len(IMM[0])
image = IMM.flatten().tolist()
ha.getImage('testImages\\bk.raw')
BK = np.flip(np.transpose(np.array(ha.imageData)), 1)
bkgrnd = BK.flatten().tolist()

im = ia.std_vector_double()
im.extend(image)

bk = ia.std_vector_double()
bk.extend(bkgrnd)

offline.loadImage(im, imHeight, imWidth)
offline.loadBackgroundImage(bk)

offline.useBackground(True)
offline.useESMask(True)
offline.setESMask(700,550,400,400)
#print offline.CoIA.maskYES
offline.useManualCrop(True)
#min and max x and y
offline.setManualCrop(500,400,300,350)
time.sleep(1)
print offline.CoIA.imageHeight
print offline.CoIA.imageWidth
print offline.CoIA.dataSize
offline.analyse()
raw_input()
print offline.CoIA.xMLE
print offline.CoIA.yMLE
print offline.CoIA.sxMLE
print offline.CoIA.syMLE
print offline.CoIA.cxyMLE
