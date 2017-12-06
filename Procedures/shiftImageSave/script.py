import sys
sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\Release')
import VELA_CLARA_Camera_DAQ_Control as daq
import time
import os

Init = daq.init()
cameras = Init.physical_CLARA_Camera_DAQ_Controller()

onShift = True

#os.system('mkdir \\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\'+time.strftime("%Y")+'\\'+time.strftime("%m")+'\\'+time.strftime("%d")+'\\VirtualCathode_Images\\')

while onShift:
    leaveAcquiring=True
    if cameras.isAcquiring('VC')==False:
        leaveAcquiring=False
        cameras.startVCAcquiring()
    time.sleep(1)
    cameras.collectAndSaveVC(1)

    # Stop acquiring
    time.sleep(1)
    if leaveAcquiring==False:
        cameras.stopVCAcquiring()
    os.system('copy \\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\2017\\VirtualCathodeCamera\\VCA-CAM-01_001.bin \\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\2017\\todaysVirtualCathodeImages\\VCimage_'+ time.strftime("%Y-%m-%d_%H-%M-%S")+'.bin')
    #time.sleep(10)
    time.sleep(600)
    if int(time.strftime("%H"))>=17:
        if  int(time.strftime("%M"))>0:
            onShift = False
            print "Shift has Ended"