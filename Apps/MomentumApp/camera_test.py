import os, sys

sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release')
os.environ["PATH"] = os.environ["PATH"]+";\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\root_v5.34.34\\bin\\"

# import VELA_CLARA_Magnet_Control as mag
# import VELA_CLARA_BPM_Control as bpm
# import VELA_CLARA_LLRF_Control as llrf
# import VELA_CLARA_PILaser_Control as pil
import VELA_CLARA_Camera_DAQ_Control as daq
import VELA_CLARA_Camera_IA_Control as camIA
#
# magInit = mag.init()
# bpmInit = bpm.init()
# pilInit = pil.init()
# llrfInit = llrf.init()
#
Init = daq.init()
camInit = camIA.init()
#
# Cmagnets = magInit.physical_CB1_Magnet_Controller()
# laser = pilInit.physical_PILaser_Controller()
# Cbpms = bpmInit.physical_CLARA_PH1_BPM_Controller()
# gun = llrfInit.physical_CLARA_LRRG_LLRF_Controller()
# LINAC01 = llrfInit.physical_L01_LLRF_Controller()
#
cameras = Init.physical_CLARA_Camera_DAQ_Controller()
camerasIA = camInit.physical_CLARA_Camera_IA_Controller()

names = list(cameras.getCameraNames())
print names
names.remove('VC')
print names

for name in names:
    if cameras.isAcquiring(name):
        cameras.setCamera(name)
        cameras.stopAcquiring()
#print name

chosen_camera = 'S01-CAM-01'
cameras.setCamera(chosen_camera)
cameras.startAcquiring()
camerasIA.setCamera(chosen_camera)
print 'here1'
print cameras.selectedCamera()
print 'here2'

#for x in ('')
# cameras.setCamera('S02-CAM-01')
# print 'here1'
# print cameras.selectedCamera()
# print 'here2'
# cameras.stopAcquiring()

# camerasIA.setCamera('S01-CAM-01')
# selectedCameraIA = camerasIA.getSelectedIARef()
#camx1 = selectedCameraIA.IA.x
camx1 = camerasIA.getSelectedIARef().IA.x
print dir(camerasIA.getSelectedIARef().IA)
# print 'camx1', str(camx1)
# camy1 = camerasIA.getSelectedIARef().IA.y
# print 'camy1', str(camy1)
# camy1 = camerasIA.getSelectedIARef().IA.sigmaX
# print 'camy1', str(camy1)
# camy1 = camerasIA.getSelectedIARef().IA.sigmaY
# print 'camy1', str(camy1)
# camy1 = camerasIA.getSelectedIARef().IA.covXY
# print 'camy1', str(camy1)
ia = camerasIA.getSelectedIARef().IA
for x in dir(ia):
    print x, getattr(ia, x)
