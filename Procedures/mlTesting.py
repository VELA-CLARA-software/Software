import sys, time, os
from datetime import datetime
import h5py
sys.path.append("../../")
from Software.Widgets.generic.pv import *
import Software.Widgets.MachineSnapshot.machine_snapshot as snap
sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\Release')

IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1280
IMAGE_DIMS = (IMAGE_HEIGHT, IMAGE_WIDTH)
IMAGE_WIDTH_FULL = IMAGE_WIDTH * 2
IMAGE_HEIGHT_FULL = IMAGE_HEIGHT * 2
IMAGE_DIMS_FULL = (IMAGE_HEIGHT_FULL, IMAGE_WIDTH_FULL)
IMAGE_WIDTH_VELA = 1392
IMAGE_HEIGHT_VELA = 1040
IMAGE_DIMS_VELA = (IMAGE_HEIGHT_VELA, IMAGE_WIDTH_VELA)
image_path = [r'.', 'CameraImages']
hdf5_image_folder = os.path.join(*image_path)

import VELA_CLARA_Camera_Control as camIA
camInit = camIA.init()
camInit.setQuiet()
camerasCtrl = camInit.physical_CLARA_Camera_Controller()

import VELA_CLARA_LLRF_Control as llrf
llrfInit = llrf.init()
llrfInit.setQuiet()
gunllrf = llrfInit.physical_CLARA_LRRG_LLRF_Controller()
linac1llrf = llrfInit.physical_L01_LLRF_Controller()

import VELA_CLARA_BPM_Control as bpm
from VELA_CLARA_BPM_Control import BPM_STATUS# as bpmstatus
bpmstatus = BPM_STATUS
bpmInit = bpm.init()
bpmInit.setQuiet()
bpmCtrl = bpmInit.physical_C2B_BPM_Controller()

import VELA_CLARA_Magnet_Control as mag
magInit = mag.init()
magInit.setQuiet()
magnetsCtrl = magInit.physical_C2B_Magnet_Controller()
time.sleep(0.01)

class emitter(object):

    def __init__(self, signal=None):
        super(emitter, self).__init__()
        self.signal = signal

    def emit(self, *args, **kwargs):
        if self.signal == 'print':
            print args
        elif self.signal is not None:
            self.signal.emit(*args, **kwargs)

class MLTest(object):

    pvNameDetect = 'CLA-S01-DIA-BPM-01:RDY'
    pvWCMQName = 'CLA-S01-DIA-WCM-01:Q'
    pvFCUPQName = 'CLA-S02-DIA-FCUP-01:Q'
    pvUsefulNames = 'AllowLaser'
    nominalTiming = 1

    def __init__(self, bpms=True, magnets=True, cameras=True, rf=True):
        super(MLTest, self).__init__()
        self.app = None
        # self.pvWCMQ = PVObject(self.pvWCMQName)
        # self.pvFCUPQ = PVObject(self.pvFCUPQName)
        if bpms:
            self.bpm_ctrl = bpmCtrl
            self.bpmDataObjects = {}
        if magnets:
            self.magnet_ctrl = magnetsCtrl
        if cameras:
            self.cam_ctrl = camerasCtrl
        if rf:
            self.gun_ctrl = gunllrf
            self.linac_ctrl = linac1llrf
        self.logger = emitter('print')

    def collectAndSave(self, comment=''):
        numberOfImages = 1
        self.cam_ctrl.startAcquiring('C2V-SCR-01')
        if self.cam_ctrl.isAcquiring():
            # print 'we are acquiring!'
            # print ' collectAndSave = ', self.cam_ctrl.collectAndSave(numberOfImages)
            if True:#not self.cam_ctrl.collectAndSave(numberOfImages):
                # collectAndSave doesn't work - implement it ourselves
                # print 'collect and save failed!'
                data = self.cam_ctrl.takeAndGetFastImage()
                if self.cam_ctrl.isVelaCam():
                    dims = IMAGE_DIMS_VELA
                    size_factor = 1
                else:  # CLARA cameras give us a cut-down image
                    dims = IMAGE_DIMS
                    size_factor = 2
                npData = np.array(data).reshape(dims)
                # self.Image.setImage(np.flip(np.transpose(npData), 1))
                timestamp = datetime.now()
                folder = hdf5_image_folder + timestamp.strftime(r'\%Y\%#m\%#d')  # omit leading zeros from month and day
                try:
                    os.makedirs(folder)
                except OSError as e:
                    if e.errno != 17:  # dir already exists
                        raise
                filename = r'{}\{}_{}_{}_{}_images.hdf5'.format(folder, 'C2V-SCR-01', timestamp.strftime('%Y-%#m-%#d_%#H-%#M-%#S'), numberOfImages,comment)
                with h5py.File(filename, 'w') as file:
                    file.create_dataset('Capture000001', data=npData)
                    # TODO: magnet/RF settings in attributes?
                    # TODO: save more than one image?
            else:
                print 'collect and save TRUE!'
            # self.camerasDAQ.collectAndSaveJPG()
        elif self.cam_ctrl.isCollectingOrSaving():
            self.camerasDAQ.killCollectAndSave()  # TODO: this isn't right any more
        # self.camerasDAQ.killCollectAndSaveJPG()

    def setGunPhase(self, phase):
        self.gun_ctrl.setPhiSP(np.mod(180+phase,360)-180)

    def getGunPhase(self):
        return self.gun_ctrl.getPhiSP()

    def setLinacPhase(self, phase):
        self.linac_ctrl.setPhiSP(np.mod(180+phase,360)-180)

    def getLinacPhase(self):
        return self.linac_ctrl.getPhiSP()

    def setGunAmplitude(self, amp):
        self.gun_ctrl.setAmpSP(amp)

    def setLinacAmplitude(self, amp):
        self.linac_ctrl.setAmpSP(amp)

    def getGunAmplitude(self):
        return self.gun_ctrl.getAmpSP()

    def getLinacAmplitude(self):
        return self.linac_ctrl.getAmpSP()

    def getSolAmplitude(self):
        return self.magnet_ctrl.getSI('LRG-SOL')

    def setSolAmplitude(self, I):
        self.magnet_ctrl.setSI('LRG-SOL', I)

    def getWCMCharge(self):
        return self.pvWCMQ.value - 5 ## Measured DC offset 03/12/2018

    def getFCUPCharge(self):
        return self.pvFCUPQ.value

    def getBPMDataObject(self, bpm):
        if bpm not in self.bpmDataObjects:
            self.bpmDataObjects[bpm] = self.bpm_ctrl.getBPMDataObject(bpm)
        return self.bpmDataObjects[bpm]

    def getBPM03Charge(self):
        obj = self.getBPMDataObject('S02-BPM02')
        return obj.q

    def getTimeStr(self):
        return time.strftime("%H%M%S")

    def getWorkFolder(self):
        return '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\'+time.strftime("%Y\\%m\\%d")+'\\'

    def getFileName(self, q=None, n=None, pos=None, energy=None, comment=None):
        filename = self.getWorkFolder()+self.getTimeStr()+'_VHEE_'
        filename = filename + '_' + str(q)+'pC' if q is not None else filename
        filename = filename + '_' + str(n)+'_Shots' if n is not None else filename
        filename = filename + '_' + str(pos) + 'mm' if pos is not None else filename
        filename = filename + '_' + str(energy) + 'MeV' if energy is not None else filename
        filename = filename + '_' + str(comment) if comment is not None else filename
        filename = filename +'.txt'
        return filename

    def printer(self, *args):
        outstr = ''
        for a in args:
            outstr += str(a)+' '
        return outstr

    def doLinacPhaseScan(self):
        start = self.getLinacPhase()
        print 'start = ', start
        for val in np.arange(int(start)-25, int(start)+25+1, 1):
            print 'linac Phase = ', val
            self.setLinacPhase(val)
            time.sleep(0.5)
            self.collectAndSave('linacPhase='+str(val))
        self.setLinacPhase(start)

    def doGunPhaseScan(self):
        start = self.getGunPhase()
        print 'gun start = ', start
        for val in np.arange(int(start)-25, int(start)+25+1, 1):
            print 'gun Phase = ', val
            self.setGunPhase(val)
            time.sleep(0.5)
            self.collectAndSave('gunPhase='+str(val))
        self.setGunPhase(start)

    def doLinacAmpScan(self):
        start = self.getLinacAmplitude()
        print 'linac start = ', start
        for val in np.arange(int(start)-10000, int(start)+1, 200):
            print 'linac Amplitude = ', val
            self.setLinacAmplitude(val)
            time.sleep(0.5)
            self.collectAndSave('linacAmp='+str(val))
        self.setLinacAmplitude(start)

    def doGunAmpScan(self):
        start = self.getGunAmplitude()
        print 'gun start = ', start
        for val in np.arange(int(start)-10000, int(start)+1, 200):
            print 'gun Amplitude = ', val
            self.setGunAmplitude(val)
            time.sleep(0.5)
            self.collectAndSave('gunAmp='+str(val))
        self.setGunAmplitude(start)

    def doSolScan(self):
        start = self.getSolAmplitude()
        print 'solSI start = ', start
        for val in np.arange(int(start)-50, int(start)+50+1, 2):
            print 'solSI Amplitude = ', val
            self.setSolAmplitude(val)
            time.sleep(0.5)
            self.collectAndSave('solAmp='+str(val))
        self.setSolAmplitude(start)


if __name__ == "__main__":
    data = snap.MachineSnapshot(MAG_Ctrl=magnetsCtrl, BPM_Ctrl=bpmCtrl, CHG_Ctrl=None,
                 SCR_Ctrl=None, CAM_Ctrl=camerasCtrl, GUN_Ctrl=gunllrf,
                 GUN_Type=None, GUN_Crest=0.0, L01_Ctrl=linac1llrf, L01_Crest=0.0,
                PIL_Ctrl=None, MACHINE_MODE=snap.vce.MACHINE_MODE.PHYSICAL, MACHINE_AREA=snap.vce.MACHINE_AREA.CLARA_2_BA1_BA2, bufferSize=10, messages=False)
    # data.writetojson()
    data.writetohdf5(directory='.')
    mltest = MLTest()
    # mltest.collectAndSave('Baseline_Image')
    # mltest.doLinacPhaseScan()
    # mltest.doLinacAmpScan()
    # mltest.doGunPhaseScan()
    # mltest.doGunAmpScan()
    print mltest.getSolAmplitude()
