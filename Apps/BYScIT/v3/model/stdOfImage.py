import model
import numpy as np
ha = model.Model()
ha.getImage('C:\\Users\\wln24624\\Pictures\\S02-CAM-02\\S02-CAM-02_001.bin')
print ha.imageHeight
print ha.imageWidth

cutTimeStamp = ha.imageData[:,:(ha.imageHeight-50)]
print 'max: ', np.max(cutTimeStamp)
print 'std: ', np.std(cutTimeStamp)
