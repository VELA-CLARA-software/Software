
import file_reader as FRC
import global_keywords as gk
import time

class parameter_setter(object):
    def __init__(self, input_file_name):
        print "A parameter setter object has been created!"
        self.filedata = FRC.file_reader(input_file_name)

    def setup_magnets(self, k, sysMags, mag_control, MagRefsDict): # the kth loop
        print "Setting up magnets .."
        for key, val in self.filedata.master_loop_dict[gk.Loop_ +str(k)][gk.MAGNET_SETTINGS].iteritems():
            if key in sysMags:
                mag_control.switchONpsu(str(key))
                while mag_control.isOFF(MagRefsDict[key].name):
                    print "Waiting to switch ON ", MagRefsDict[key].name
                    time.sleep(1)
                mag_control.setSI(str(key), float(val))
                while not MagRefsDict[key].SETIequalREADI:  # waits until setI and readI are the same
                    print "waiting...to SETI " + str(MagRefsDict[key].name) + ' to ' + str(val)
                    time.sleep(1)
        print "MAGNETS SUCESSFULLY SETUP"

    def setup_llrf(self, k, llrf_control):
        if not self.filedata.llrfType == None:
            print "Setting up llrf .."
            for key, val in self.filedata.master_loop_dict[gk.Loop_ +str(k)][gk.LLRF_SETTINGS].iteritems():
                # self.LLRFKeywords = ["LLRF_Amplitude", "LLRF_Phase"]
                if key == gk.LLRFKeywords[0]:
                    llrf_control.setAmpMVM(float(val))
                elif key == gk.LLRFKeywords[1]:
                    llrf_control.setPhiDEG(float(val))
            print "LLRF SUCESSFULLY SETUP"

    def setup_laser(self, k, u, las_control):
        if self.filedata.laserState:
            for key, val in self.filedata.master_loop_dict[gk.Loop_ +str(k)][gk.LASER_SETTINGS].iteritems():
                # self.LaserKeywords = ["LASER_HPos", "LASER_VPos", "LASER_Intensity"]
                if key == gk.LaserKeywords[0]:
                    las_control.setHpos(float(val))
                elif key == gk.LaserKeywords[1]:
                    las_control.setVpos(float(val))
                elif key == gk.LaserKeywords[2]:
                    if u == 1:  # laser on
                        las_control.setIntensity(float(val))
                    elif u == 0:  # laser off
                        las_control.setIntensity(0)  # Use when the laser is off
            print "LASER SUCESSFULLY SETUP"