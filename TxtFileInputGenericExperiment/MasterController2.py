# Written by Michael Sullivan (Ogden Trust Internship)
# July-August 2017

# The Master Controller will use the FRC to read in and verify the data in the "instructions"
# test file and then use that set to use the existing controllers to set the necessary
# varibles to run the simulations
# This "Master Controller" py file will be imported into a "main" where the code will
# be ran from (Which will be a very short script!)

import FileReaderClass3 as FRC
import sys, os
import time
from epics import caget, caput, PV

import VELA_CLARA_Magnet_Control as mag
import VELA_CLARA_LLRFControl as llrf
import VELA_CLARA_BPM_Control as bpm
import VELA_CLARA_PILaserControl as las

class MasterController():

    filedata = None
    def __init__(self):
        print "An empty MasterController object has been created!"

    def __init__(self, name):
        print "A MasterController object has been created taking instructions from " + str(name) + ".txt"
        self.filedata = FRC.Reader(name) # so the MasterController obj can access data from txt file

    # Now use the Master Controller to set Variables using the existing Controllers!

    def ShutdownMags(self,):
        if self.CompareMags():
            for i in self.filedata.Magnets_Used:   # switch off magnets and set 0 currents
                magnets_VELA.switchOFFpsu(str(i))
                magnets_VELA.setSI(str(i), 0)
            print "Magnets have been successfully shutdown!"
        else: print "Error: Magnets have not been shutdown!"

    # Need to check if the given file names  match those that exist in the controller!
    def CompareMags(self):
        # create list of magnet names that already exist in the system
        sysMags_1 = magnets_VELA.getMagnetNames()
        sysMags_2 = magnets_CLARA.getMagnetNames()
        for x in range(0, len(self.filedata.Magnets_Used)):
            B = 0
            for y in range(0, len(sysMags_1)):
                if self.filedata.Magnets_Used[x] == sysMags_1[y]: B = 1
            for z in range(0, len(sysMags_2)):
                if self.filedata.Magnets_Used[x] == sysMags_2[z]: B = 1
            if B == 0: print "Requested Magnet does not exist!"; return False
        return True # if the code reaches here then all magnets have been verified

    def Setup(self, k, u): # This function will need to be updated as more controllers are added!
        Z = self.filedata.MasterDict()["Loop_" + str(k)]
        for i in self.filedata.VariableTypeList: # VariableTypeList = ["MAGNETS, LLRF, LASER"]
            P = Z[i] # get for example FRC.MasterDict()["Loop_1"]["MAGNETS"]
            time.sleep(1)
            if i == self.filedata.Magnets:
                for i,j in P.iteritems():
                    magnets_VELA.switchONpsu(str(i))
                    magnets_VELA.setSI(str(i), float(j[0]))
                    # print "MAGNETS SUCESSFULLY SETUP"
                # setup LLRF
            elif i == self.filedata.LLRF:
                for i, j in P.iteritems(): #self.LLRFKeywords = ["LLRF_Amplitude", "LLRF_Phase"]
                    if i == self.filedata.LLRFKeywords[0]:
                        gun.setAmpMVM(float(j[0]))
                    elif i == self.filedata.LLRFKeywords[1]:
                        gun.setPhiDEG(float(j[0]))
                # print "LLRF SUCESSFULLY SETUP"
            elif i == self.filedata.Laser:
                for i,j in P.iteritems():   #self.LaserKeywords = ["LASER_HPos", "LASER_VPos", "LASER_Intensity"]
                    if i == self.filedata.LaserKeywords[0]:
                        las_VELA.setHpos(float(j[0]))
                    elif i == self.filedata.LaserKeywords[1]:
                        las_VELA.setVpos(float(j[0]))
                    elif i == self.filedata.LaserKeywords[2]:
                        if u == 1: # laser on
                            las_VELA.setIntensity(float(j[0]))
                        elif u == 0: # laser off
                            las_VELA.setIntensity(0) # Use when the laser is off
                            print "Laser (dark) has been successfully set up!"
                # print "LASER SUCESSFULLY SETUP"
            else: print "Data exists in MasterDict that doesn't exist in VariableTypeList!"
            time.sleep(2) # to give the sytem time to set the variables before being used any further

    # CAM and BPM read functions will need to be changed when Controllers are in system instead of reading PVs

    def ReadBPM(self):
        for x in range(0, len(self.filedata.BPM_Names)):
            Xvalue = bpm_VELA.getXFromPV(self.filedata.BPM_Names[x])
            Yvalue = bpm_VELA.getYFromPV(self.filedata.BPM_Names[x])
            Qvalue = bpm_VELA.getQ(self.filedata.BPM_Names[x])
            if x == 0:
                BPMXList = [Xvalue]
                BPMYList = [Yvalue]
                BPMQList = [Qvalue]
            else:
                BPMXList = BPMXList + [Xvalue]
                BPMYList = BPMYList + [Yvalue]
                BPMQList = BPMQList + [Qvalue]
        return [BPMXList, BPMYList, BPMQList]

    def ReadCAM(self):
        for x in range(0, len(self.filedata.CAM_Names)+1):

            # CONVENTION: YAG-01 HAS CAMERA CAM-02

            CAMNum = str(x+1)

            CAMName = "VM-EBT-INJ-DIA-CAM-0" + CAMNum + ":CAM" # FIX THIS TO MAKE VIRTUAL OR PHYSICAL!
            CAMPVX = PV(CAMName + ":X")
            CAMPVY = PV(CAMName + ":Y")
            CAMPVSX = PV(CAMName + ":SigmaX")
            CAMPVSY = PV(CAMName + ":SigmaY")
            SXCAMvalue = CAMPVSX.get()
            SYCAMvalue = CAMPVSY.get()
            XCAMvalue = CAMPVX.get()
            YCAMvalue = CAMPVY.get()

            if x == 0:
                CAMXList = [XCAMvalue]
                CAMYList = [YCAMvalue]
                CAMSXList = [SXCAMvalue]
                CAMSYList = [SYCAMvalue]
            else:
                CAMXList = CAMXList + [XCAMvalue]
                CAMYList = CAMYList + [YCAMvalue]
                CAMSXList = CAMSXList + [SXCAMvalue]
                CAMSYList = CAMSYList + [SYCAMvalue]

        return [CAMXList, CAMYList, CAMSXList, CAMSYList]


# This needs to be done in the MasterController py file as system controllers need to be accessed
F = MasterController('Instructions2')
if not F.filedata.isPhysical():
    # set up the environment variables and controllers to the Virtual Machine
    print "USING VIRTUAL MACHINE!"
    os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
    os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
    os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
    os.environ["EPICS_CA_SERVER_PORT"] = "6000"

    magInit = mag.init()
    llrfInit = llrf.init()
    bpmInit = bpm.init()
    lasInit = las.init()

    magnets_VELA = magInit.virtual_VELA_INJ_Magnet_Controller()
    magnets_CLARA = magInit.virtual_CLARA_PH1_Magnet_Controller()
    bpm_VELA = bpmInit.virtual_VELA_INJ_BPM_Controller()
    las_VELA = lasInit.virtual_PILaser_Controller()

    # THIS BLOCK IS COMMENTED OUT AS CONFUSION ABOUT GUN NAME CONVENTION
    #  BUT MAY BE USED WHE UPDATED IN THE FUTURE
    # # Can either use CLARA, L01 or VELA gun
    # if F.filedata.Gun_Type == F.filedata.Gun_TypeKeywords[0]: #   self.Gun_TypeKeywords = ["VELA, CLARA, L01"]
    #     gun = llrfInit.virtual_VELA_HRRG_LLRF_Controller()
    # elif F.filedata.Gun_Type == F.filedata.Gun_TypeKeywords[1]:
    #     gun = llrfInit.virtual_CLARA_LRRG_LLRF_Controller()
    # elif F.filedata.Gun_Type == F.filedata.Gun_TypeKeywords[2]:
    #     gun = llrfInit.virtual_L01_LLRF_Controller()

    # USE THIS CONTROLLER FOR THE GUN FOR NOW!
    gun = llrfInit.virtual_CLARA_LRRG_LLRF_Controller()

elif F.filedata.isPhysical():
    print "Physical"
    print "USING PHYSICAL MACHINE!"
    # set up the environment variables and controllers to the Physical Machine when known!
    # os.environ["EPICS_CA_AUTO_ADDR_LIST"] =
    # os.environ["EPICS_CA_ADDR_LIST"] =
    # os.environ["EPICS_CA_MAX_ARRAY_BYTES"] =
    # os.environ["EPICS_CA_SERVER_PORT"] =

    magInit = mag.init()
    llrfInit = llrf.init()
    bpmInit = bpm.init()
    lasInit = las.init()

    # GUN CONTROLLER ASSIGNMENT WILL NEED UPDATING IN THE FUTURE!

    magnets_VELA = magInit.physical_VELA_INJ_Magnet_Controller()
    gun = llrfInit.physical_CLARA_LRRG_LLRF_Controller()  # using this because it have the same PVs
    magnets_CLARA = magInit.physical_CLARA_PH1_Magnet_Controller()
    bpm_VELA = bpmInit.physical_VELA_INJ_BPM_Controller()
    las_VELA = lasInit.physical_PILaser_Controller()
