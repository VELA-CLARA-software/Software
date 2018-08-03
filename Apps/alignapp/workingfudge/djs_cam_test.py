import VELA_CLARA_Camera_Control as cam
import time

cam_init = cam.init()
cam_init.setVerbose()

cam_control = cam_init.physical_Camera_Controller()

raw_input()
if cam_control.latestCollectAndSaveSuccess_VC():
	print 'collectAndSave Check Success'
else:
	print 'collectAndSave Check FAIL'

raw_input()
cam_control.startAcquiring_VC()
if cam_control.collectAndSave_VC(1):
	print 'collectAndSave SENT '
else:
	print 'collectAndSave FAIL'

while cam_control.isCollectingOrSaving_VC():
	print 'wait...'
	time.sleep(0.1)



raw_input()
if cam_control.latestCollectAndSaveSuccess():
	print 'collectAndSave Check Success'
else:
	print 'collectAndSave Check FAIL'
	

raw_input()

# if cam_control.collectAndSave(1):
	# print 'collectAndSave success'
# else:
	# print 'collectAndSave FAIL'

# while cam_control.isCollectingOrWriting():
	# print 'wait...'
	# time.sleep(0.1)

# raw_input()

# vc_data2 = [cam_control.getAnalysisObj_VC()]
# vc_cam  = [cam_control.getCameraObj_VC()]
# vc_mask  = [cam_control.getMaskObj_VC()]

# if cam_control.setMaskY_VC(11):
	# print 'set mask success'
# else:
	# print 'set mask  FAIL'
# raw_input()
# print('cam_control.setMaskY()',cam_control.getMaskY_VC())


# raw_input()

# name = 'S02-CAM-01'
# if cam_control.stopAnalysing(name):
	# print 'set stopAnalysing success'
# else:
	# print 'set stopAnalysing FAIL'
# raw_input()
# print('cam_control.isAnalysing',name,cam_control.isAnalysing(name))


# raw_input()

# if cam_control.startAnalysing(name):
	# print 'set startAnalysing success'
# else:
	# print 'set startAnalysing FAIL'
# raw_input()
# print('cam_control.isAnalysing',name,cam_control.isAnalysing(name))
# raw_input()

# # pil_control.setVstep(-50.0)


# # print("vstep = " , pil_control.getVstep())

# # raw_input()

# # a = pil_control.moveV()

# # if a:
	# # print 'moved?'
# # else:
	# # print 'failed'
	
# raw_input()

# pil_control.moveV()

# raw_input()
# pil_control.moveV()

raw_input()




# # print 'GET IMAGE on...'
# # raw_input()


# # d= pil_control.getFastImage()

# # print len(d)

# # raw_input()





# # print 'carry on...'
# # raw_input()
# # print pil_control.getHWP()
# # raw_input()



# # pil_control.setBufferSize(100)

# # while 1:
	# # if pil_control.isBufferFull:
		# # break
	# print 'waiting for buffer'
	# # time.sleep(1)
# # print "buffer full!"
	
# # for x in pil_control.getXBuffer():
	# # print x


# pil_control.setHstep(101.0)


# print("hstep = " , pil_control.getHstep())

# raw_input()

# pil_control.moveH()

# raw_input()

# pil_control.setVstep(101.0)

# print("vstep = " , pil_control.getVstep())

# raw_input()

# pil_control.moveV()



raw_input()