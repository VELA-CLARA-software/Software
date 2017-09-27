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

sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\Debug')


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

        self.MagRefs = []
        self.MagRefsDict = {}
        self.magnets_VELA = None
        self.magnets_CLARA =None
        self.bpm_VELA = None
        self.las_VELA = None

        self.SetEnvironment()
        self.sysMags_V = self.magnets_VELA.getMagnetNames()
        self.sysMags_C = self.magnets_CLARA.getMagnetNames()
        self.gun = None
        self.llrfInit = None
        self.llrfInit = llrf.init()
        self.LLRFSetup()
        self.CreateRefList()
        self.CreateRefDict()

    def LLRFSetup(self):
        if not self.filedata.isPhysical(): # using virtual machine
            if self.filedata.Gun_Type == self.filedata.Gun_TypeKeywords[0]:  # self.Gun_TypeKeywords = ["VELA, CLARA, L01"]
                self.gun = self.llrfInit.virtual_CLARA_LRRG_LLRF_Controller()  # this has same PVs so can use this controller
                print "Using virtual VELA Gun"
            elif self.filedata.Gun_Type == self.filedata.Gun_TypeKeywords[1]:
                self.gun = self.llrfInit.virtual_CLARA_LRRG_LLRF_Controller()
                print "Using virtual CLARA Gun"
            elif self.filedata.Gun_Type == self.filedata.Gun_TypeKeywords[2]:
                self.gun = self.llrfInit.virtual_L01_LLRF_Controller()
                print "Using virtual L01 Gun"
        elif self.filedata.isPhysical():    # using physical machine
            if self.filedata.Gun_Type == self.filedata.Gun_TypeKeywords[0]:  # self.Gun_TypeKeywords = ["VELA, CLARA, L01"]
                self.gun = self.llrfInit.physical_CLARA_LRRG_LLRF_Controller()  # this has same PVs so can use this controller
                print "Using physical VELA Gun"
            elif self.filedata.Gun_Type == self.filedata.Gun_TypeKeywords[1]:
                self.gun = self.llrfInit.physical_CLARA_LRRG_LLRF_Controller()
                print "Using physical CLARA Gun"
            elif self.filedata.Gun_Type == self.filedata.Gun_TypeKeywords[2]:
                self.gun = self.llrfInit.physical_L01_LLRF_Controller()
                print "Using physical L01 Gun"

    # Now use the Master Controller to set Variables using the existing Controllers!

    def ShutdownMags(self):
        if self.CompareMags():
            for i in self.filedata.Magnets_Used_Total:   # switch off magnets and set 0 currents
                if i in self.sysMags_V:
                    self.magnets_VELA.switchOFFpsu(str(i))
                    self.magnets_VELA.setSI(str(i), 0)
                elif i in self.sysMags_C:
                    self.magnets_CLARA.switchOFFpsu(str(i))
                    self.magnets_CLARA.setSI(str(i), 0)
            print "Magnets have been successfully shutdown!"
        else: print "Error: Magnets have not been shutdown!"

    # Need to check if the given file names  match those that exist in the controller!
    def CompareMags(self):
        # create list of magnet names that already exist in the system
        for x in range(0, len(self.filedata.Magnets_Used_Total)):
            B = 0
            for y in range(0, len(self.sysMags_C)):
                if self.filedata.Magnets_Used_Total[x] == self.sysMags_C[y]: B = 1
            for z in range(0, len(self.sysMags_V)):
                if self.filedata.Magnets_Used_Total[x] == self.sysMags_V[z]: B = 1
            if B == 0: print "Requested Magnets does not exist!"; return False
        return True # if the code reaches here then all magnets have been verified


    # for this function u=0 is with laser off, u=1 for laser on

    # This uses self to get controllers but the gun doent work at the moment!
    def Setup(self, k, u): # This function will need to be updated as more controllers are added!
        print "Setting up..."
        Z = self.filedata.MasterDict()["Loop_" + str(k)] #MAGIC_STRING
        for i in self.filedata.VariableTypeList: # VariableTypeList = ["MAGNETS, LLRF, LASER"]
            P = Z[i] # get for example FRC.MasterDict()["Loop_1"]["MAGNETS"]
            time.sleep(1)# take a break...
            if i == self.filedata.Magnets:
                for i,j in P.iteritems():
                    if i in self.sysMags_V: # if its a magnet on the VELA line
                        print "Switching ON Magnet in VELA: " + str(i)
                        self.magnets_VELA.switchONpsu(str(i))
                        #while not self.MagRefsDict[i].psuState == MAG_PSU_STATE.ON : # waits until setI and readI are the same
                        while self.magnets_VELA.isOFF(self.MagRefsDict[i].name): # waits until setI and readI are the same
                            print "waiting... to switch ON" + str(self.MagRefsDict[i].name)
                            time.sleep(1)


                        self.magnets_VELA.setSI(str(i), float(j[0]))
                        while not self.MagRefsDict[i].SETIequalREADI: # waits until setI and readI are the same
                            print "waiting...to SETI " + str(self.MagRefsDict[i].name) + ' to ' + str(float(j[0]))
                            time.sleep(1)
                    # elif i in self.sysMags_C: # if its a magnet on the VELA line
                    #     print "Magnet in Clara: " + str(i)
                    #     self.magnets_CLARA.switchONpsu(str(i))
                    #     self.magnets_CLARA.setSI(str(i), float(j[0]))
                    #     while not self.MagRefsDict[i].SETIequalREADI:
                    #         print "waiting..."
                    #         time.sleep(1)
                    print "MAGNETS SUCESSFULLY SETUP"
                # setup LLRF
            elif i == self.filedata.LLRF:
                for i, j in P.iteritems(): #self.LLRFKeywords = ["LLRF_Amplitude", "LLRF_Phase"]
                    if i == self.filedata.LLRFKeywords[0]:
                        self.gun.setAmpMVM(float(j[0]))
                    elif i == self.filedata.LLRFKeywords[1]:
                        self.gun.setPhiDEG(float(j[0]))
                # print "LLRF SUCESSFULLY SETUP"
            elif i == self.filedata.Laser:
                for i,j in P.iteritems():   #self.LaserKeywords = ["LASER_HPos", "LASER_VPos", "LASER_Intensity"]
                    if i == self.filedata.LaserKeywords[0]:
                        self.las_VELA.setHpos(float(j[0]))
                    elif i == self.filedata.LaserKeywords[1]:
                        self.las_VELA.setVpos(float(j[0]))
                    elif i == self.filedata.LaserKeywords[2]:
                        if u == 1: # laser on
                            self.las_VELA.setIntensity(float(j[0]))
                        elif u == 0: # laser off
                            self.las_VELA.setIntensity(0) # Use when the laser is off
                            print "Laser (dark) has been successfully set up!"
                # print "LASER SUCESSFULLY SETUP"
            else: print "Data exists in MasterDict that doesn't exist in VariableTypeList!"
            time.sleep(2) # to give the sytem time to set the variables before being used any further

    # CAM and BPM read functions will need to be changed when Controllers are in system instead of reading PVs

    def ReadBPM(self):
        for x in range(0, len(self.filedata.BPM_Names)):
            if self.filedata.BPM_Type == self.filedata.BPM_TypeKeywords[0]: # self.BPM_TypeKeywords = ["VELA", "CLARA"]
                Xvalue = self.bpm_VELA.getXFromPV(self.filedata.BPM_Names[x])
                Yvalue = self.bpm_VELA.getYFromPV(self.filedata.BPM_Names[x])
                Qvalue = self.bpm_VELA.getQ(self.filedata.BPM_Names[x])
            elif self.filedata.BPM_Type == self.filedata.BPM_TypeKeywords[1]:
                Xvalue = self.bpm_CLARA.getXFromPV(self.filedata.BPM_Names[x])
                Yvalue = self.bpm_CLARA.getYFromPV(self.filedata.BPM_Names[x])
                Qvalue = self.bpm_CLARA.getQ(self.filedata.BPM_Names[x])
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
            if not self.filedata.isPhysical():  # using virtual machine
                CAMName = "VM-EBT-INJ-DIA-CAM-0" + CAMNum + ":CAM"
            elif self.filedata.isPhysical():  # using physical machine
                CAMName = "EBT-INJ-DIA-CAM-0" + CAMNum + ":CAM"

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

    def SetEnvironment(self):
        if not self.filedata.isPhysical():
            # set up the environment variables and controllers to the Virtual Machine
            print "USING VIRTUAL MACHINE!"
            os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
            os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
            os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
            os.environ["EPICS_CA_SERVER_PORT"] = "6000"

            self.magInit = mag.init()
            self.bpmInit = bpm.init()
            self.lasInit = las.init()

            self.magnets_VELA = self.magInit.virtual_VELA_INJ_Magnet_Controller()
            self.magnets_CLARA = self.magInit.virtual_CLARA_PH1_Magnet_Controller()

            # CURRENTLY AN ISSUE WITH THE VIRTUAL BPM CONTROLLERS!

            # self.bpm_VELA = self.bpmInit.virtual_VELA_INJ_BPM_Controller()
            # self.bpm_CLARA= self.bpmInit.virtual_CLARA_INJ_BPM_Controller()
            self.bpm_VELA = self.bpmInit.offline_VELA_INJ_BPM_Controller()
            self.bpm_CLARA = self.bpmInit.offline_CLARA_INJ_BPM_Controller()

            self.las_VELA = self.lasInit.virtual_PILaser_Controller()

            # THESE DONT EXIST AT THE MOMENT!
            # self.bpm_C2V = bpmInit.virtual_CLARA_2_VELA_BPM_Controller()
            # self.bpm_CLARA = bpmInit.virtual_CLARA_INJ_BPM_Controller()

        elif self.filedata.isPhysical():
            print "Physical"
            print "USING PHYSICAL MACHINE!"
            # set up the environment variables and controllers to the Physical Machine when known!
            # os.environ["EPICS_CA_AUTO_ADDR_LIST"] =
            # os.environ["EPICS_CA_ADDR_LIST"] =
            # os.environ["EPICS_CA_MAX_ARRAY_BYTES"] =
            # os.environ["EPICS_CA_SERVER_PORT"] =

            self.magInit = mag.init()
            self.bpmInit = bpm.init()
            self.lasInit = las.init()

            # GUN CONTROLLER ASSIGNMENT WILL NEED UPDATING IN THE FUTURE!

            self.magnets_VELA = self.magInit.physical_VELA_INJ_Magnet_Controller()
            #self.gun = self.llrfInit.physical_CLARA_LRRG_LLRF_Controller()  # using this because it have the same PVs
            self.magnets_CLARA = self.magInit.physical_CLARA_PH1_Magnet_Controller()
            self.bpm_VELA = self.bpmInit.physical_VELA_INJ_BPM_Controller()
            self.las_VELA = self.lasInit.physical_PILaser_Controller()

    def CreateRefList(self):
        # for i in self.filedata.Magnets_Used_C:
        #     self.MagRefs.append(self.magnets_CLARA.getMagObjConstRef(i))
        for i in self.filedata.Magnets_Used_V:
            self.MagRefs.append(self.magnets_VELA.getMagObjConstRef(i))

    def CreateRefDict(self):
        for i in self.MagRefs:
            self.MagRefsDict[i.name] = i





#
# F = MasterController("Instructions2")
# # F.Setup(1,1)
# print F.magnets_VELA.getMagObjConstRef("QUAD01").name
# print F.magnets_VELA.getMagObjConstRef("QUAD01").magType
# print F.magnets_VELA.getMagObjConstRef("QUAD01").riTolerance
# print F.magnets_VELA.getMagObjConstRef("QUAD01").SETIequalREADI
# print F.magnets_VELA.getSI("QUAD01")
#
# for i in F.MagRefs:
#     print i.SETIequalREADI
#
# for i,j in F.MagRefsDict.iteritems():
#     print i, j.SETIequalREADI
# print F.MagRefsDict["QUAD01"].SETIequalREADI
# print not F.MagRefsDict["QUAD01"].SETIequalREADI