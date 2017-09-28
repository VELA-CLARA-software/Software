# import file_reader as FRC
import global_keywords as gk
import time
import datetime
from VELA_CLARA_Camera_DAQ_Control import CAPTURE_STATE as CS
from VELA_CLARA_Camera_DAQ_Control import WRITE_STATE as WS

class daq_getter(object):

    def __init__(self):
        print "A daq getter object has been created!"
        self.BPMXList = []
        self.BPMYList = []
        self.BPMQList = []
        self.already_opened = False
        # self.filedata = FRC.file_reader(input_file_name)

    def ReadBPM(self, bpm_control, BPM_Names):
        del self.BPMXList[:]
        del self.BPMYList[:]
        del self.BPMQList[:]
        for x in range(0, len(BPM_Names)):
            Xvalue = bpm_control.getXFromPV(BPM_Names[x])
            Yvalue = bpm_control.getYFromPV(BPM_Names[x])
            Qvalue = bpm_control.getQ(BPM_Names[x])
            if x == 0:
                self.BPMXList = [Xvalue]
                self.BPMYList = [Yvalue]
                self.BPMQList = [Qvalue]
            else:
                self.BPMXList = self.BPMXList + [Xvalue]
                self.BPMYList = self.BPMYList + [Yvalue]
                self.BPMQList = self.BPMQList + [Qvalue]
        return [self.BPMXList, self.BPMYList, self.BPMQList]

    def write_bpm_to_file(self, k, u, BPM_Names):
        if u == 0: LS = "OFF"
        elif u == 1: LS = "ON"
        print "self.already_opened", self.already_opened
        if not self.already_opened:
            self.bpm_file_name = "BPMData " + str('{:%Y.%m.%d %H.%M.%S}'.format(datetime.datetime.now())) + ".txt"
            self.already_opened = True

        with open(self.bpm_file_name, 'a+') as Bdat:  # to write data out to for later viewing
            # if k == 1:
            #     Bdat.write('Data collected at time: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) , "\n")
            Bdat.write("Loop " + str(k) + " Laser state: " + LS + "\n")
            for i in range(0, len(BPM_Names)):  # loop over the BPMs
                Bdat.write("BPM0" + str(i + 1) + "\n")
                Bdat.write(
                    "X = " + str(self.BPMXList[i]) + " Y = " + str(self.BPMYList[i]) + " Q = " + str(self.BPMQList[i]))
                Bdat.write("\n")
                Bdat.write("\n")

    def read_cam(self, daq_control, k, u, CAM_Names, master_loop_dict):
        # NOTE: CAMS only work on the physical machine!
        for cam_name in CAM_Names:
            daq_control.setCamera(cam_name)
            selectedCamera = daq_control.getSelectedDAQRef()
            print "cam_Name", cam_name
            print "self.daq_control.selectedCamera()", daq_control.selectedCamera()

            if daq_control.isON(cam_name):
                daq_control.startAcquiring()
                if daq_control.isAcquiring(cam_name):
                    print "COLLECTING ON LOOP ", k
                    if u == 0:
                        daq_control.collectAndSave(
                            int(master_loop_dict[gk.Loop_ + str(k)][gk.DAQ_SETTINGS][gk.DAQ_LASER_OFF]))
                    elif u == 1:
                        daq_control.collectAndSave(
                            int(master_loop_dict[gk.Loop_ + str(k)][gk.DAQ_SETTINGS][gk.DAQ_LASER_ON]))
                    time.sleep(1)
                    while selectedCamera.captureState == CS.CAPTURING or selectedCamera.writeState == WS.WRITING:
                        print cam_name + " is still Capturing or writing..."
                        time.sleep(0.5)
                daq_control.stopAcquiring()
                time.sleep(5)