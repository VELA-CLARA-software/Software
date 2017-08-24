# Written by Michael Sullivan (Ogden Trust Internship)
# July-August 2017

# The Master Controller will use the FRC to read in and verify the data in the "instructions"
# test file and then use that set to use the existing controllers to set the necessary
# varibles to run the simulations
# This "Master Controller" py file will be imported into a "main" where the code will
# be ran from (Which will be a very short script!)

import file_reader as FRC
import worker   as worker

import sys, os
import time
from epics import caget, caput, PV

sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\Release')

import VELA_CLARA_Magnet_Control as mag


# we found a proper bug!!!!
# we found a proper bug!!!!
# we found a proper bug!!!!
# we found a proper bug!!!!
# we found a proper bug!!!!
# we found a proper bug!!!!
# we found a proper bug!!!!
# we found a proper bug!!!!
# we found a proper bug!!!!
# we found a proper bug!!!!
# we found a proper bug!!!!
# we found a proper bug!!!!
# FOR SOME REASON when you inlcude these the getMagnetController
# doesn't work


#import VELA_CLARA_LLRFControl as llrf
#import VELA_CLARA_BPM_Control as bpm
import VELA_CLARA_PILaserControl as las


class master_controller(object):
    def __init__(self):
        print "A MasterController object has been created"
        
        # create a filereader object and pass in file input_file_name 
        # the file is processed straight away 
        self.filedata = None
        self.magInit = mag.init()
        self.mag_control = None
        self.lasInit = las.init()
        self.las_control = None


    def read_procedure_file(self,input_file_name):
        print "taking instructions from " + str(input_file_name)
        self.filedata = FRC.file_reader(input_file_name)  # so the MasterController obj can access data from txt file
        print 'FILE PROCESSED'

    def create_magnet_controller(self):
        print(self.filedata.machineMode, self.filedata.magnetType)
        self.mag_control = self.magInit.getMagnetController( self.filedata.machineMode, self.filedata.magnetType )
        #self.magInit.getMagnetController(mag.MACHINE_MODE.VIRTUAL, mag.MACHINE_AREA.VELA_INJ)
        #
        # if USING_MAG == "VELA_INJ" and Machine_Type == 'V':
        # if USING_MAG == "VELA_INJ" and Machine_Type == 'P':
        # if USING_MAG == "CLARA_PH1" and Machine_Type == 'V':
        # if USING_MAG == "CLARA_PH1" and Machine_Type == 'P':
        # if USING_MAG == "VELA_BA1" and Machine_Type == 'V':
        # if USING_MAG == "VELA_BA1" and Machine_Type == 'P':

    # If there is enough symmetry about the "create_controller" functions then could perhaps merge into single function?

    def create_llrf_controller(self):
        # would be useful if there was a "getLlrfController" function for different modes and machine type
        pass

    def create_laser_controller(self):
        # THIS COULD BE DONE BETTER?
        if self.filedata.processed_header_data[self.filedata.Machine_Type][0] == "V": # MAGIC STRING
            self.las_control = self.lasInit.virtual_PILaser_Controller()
        elif self.filedata.processed_header_data[self.filedata.Machine_Type][0] == "P": # MAGIC STRING
            self.las_control = self.lasInit.physical_PILaser_Controller()

    def create_bpm_controller(self):
        pass

    def create_daq_controller(self):
        pass

    def SetEnvironment(self):

        self.create_magnet_controller()
        self.create_laser_controller()

        if self.filedata.isVirtual():
            # set up the environment variables and controllers to the Virtual Machine
            print "USING VIRTUAL MACHINE!"
            os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
            os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
            os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
            os.environ["EPICS_CA_SERVER_PORT"] = "6000"

        #     if not self.filedata.Using_Mag == self.filedata.True_False_Offline[1]:  # if not "False"
        #         self.magInit = mag.init()
        #         if self.filedata.Using_Mag == self.filedata.True_False_Offline[2]:  # if Offline
        #             self.magnets_VELA = self.magInit.offline_VELA_INJ_Magnet_Controller()
        #         else:
        #             self.magnets_VELA = self.magInit.virtual_VELA_INJ_Magnet_Controller()
        #     else: print "Magnets not being used"
        #
        #     if not self.filedata.Using_BPM == self.filedata.True_False_Offline[1]:  # if not "False"
        #         self.bpmInit = bpm.init()
        #         # self.bpmInit.setVerbose()
        #         if self.filedata.Using_BPM == self.filedata.True_False_Offline[2]: # if Offline
        #             print "Using offline BPMs"
        #             if self.filedata.BPM_Type == self.filedata.BPM_TypeKeywords[0]:
        #                 self.bpm_VELA = self.bpmInit.offline_VELA_INJ_BPM_Controller()
        #             elif self.filedata.BPM_Type == self.filedata.BPM_TypeKeywords[1]:
        #                 self.bpm_CLARA = self.bpmInit.offline_CLARA_INJ_BPM_Controller()
        #         else:
        #             if self.filedata.BPM_Type == self.filedata.BPM_TypeKeywords[0]:
        #                 self.bpm_VELA = self.bpmInit.virtual_VELA_INJ_BPM_Controller()
        #             elif self.filedata.BPM_Type == self.filedata.BPM_TypeKeywords[1]:
        #                 self.bpm_CLARA= self.bpmInit.virtual_CLARA_INJ_BPM_Controller()
        #     else: print "BPMs not being used"
        #
        #     if not self.filedata.Using_Laser == self.filedata.True_False_Offline[1]:  # if not "False"
        #         self.lasInit = las.init()
        #         if self.filedata.Using_Laser == self.filedata.True_False_Offline[2]:  # if Offline
        #             self.las_VELA = self.lasInit.offline_PILaser_Controller()
        #         else:
        #             self.las_VELA = self.lasInit.virtual_PILaser_Controller()
        #     else: print "Laser not being used"
        #
        # elif self.filedata.isPhysical():
        #     print "Physical"
        #     print "USING PHYSICAL MACHINE!"
        #     # set up the environment variables and controllers to the Physical Machine when known!
        #     # os.environ["EPICS_CA_AUTO_ADDR_LIST"] =
        #     # os.environ["EPICS_CA_ADDR_LIST"] =
        #     # os.environ["EPICS_CA_MAX_ARRAY_BYTES"] =
        #     # os.environ["EPICS_CA_SERVER_PORT"] =
        #
        #     if not self.filedata.Using_Mag == self.filedata.True_False_Offline[1]:  # if not "False"
        #         self.magInit = mag.init()
        #         if self.filedata.Using_Mag == self.filedata.True_False_Offline[2]:  # if Offline
        #             self.magnets_VELA = self.magInit.offline_VELA_INJ_Magnet_Controller()
        #         else:
        #             self.magnets_VELA = self.magInit.physical_VELA_INJ_Magnet_Controller()
        #     else: print "Magnets not being used"
        #
        #     if not self.filedata.Using_BPM == self.filedata.True_False_Offline[1]:  # if not "False"
        #         self.bpmInit = bpm.init()
        #         if self.filedata.Using_BPM == self.filedata.True_False_Offline[2]: # if Offline
        #             print "using offline BPMs"
        #             if self.filedata.BPM_Type == self.filedata.BPM_TypeKeywords[0]:
        #                 self.bpm_VELA = self.bpmInit.offline_VELA_INJ_BPM_Controller()
        #             elif self.filedata.BPM_Type == self.filedata.BPM_TypeKeywords[1]:
        #                 self.bpm_CLARA = self.bpmInit.offline_CLARA_INJ_BPM_Controller()
        #         else:
        #             if self.filedata.BPM_Type == self.filedata.BPM_TypeKeywords[0]:
        #                 self.bpm_VELA = self.bpmInit.physical_VELA_INJ_BPM_Controller()
        #             elif self.filedata.BPM_Type == self.filedata.BPM_TypeKeywords[1]:
        #                 self.bpm_CLARA= self.bpmInit.physical_CLARA_INJ_BPM_Controller()
        #     else: print "BPMs not being used"
        #
        #     if not self.filedata.Using_Laser == self.filedata.True_False_Offline[1]:  # if not "False"
        #         self.lasInit = las.init()
        #         if self.filedata.Using_Laser == self.filedata.True_False_Offline[2]:  # if Offline
        #             self.las_VELA = self.lasInit.offline_PILaser_Controller()
        #         else:
        #             self.las_VELA = self.lasInit.physical_PILaser_Controller()
        #     else: print "Laser not being used"



    def create_controllers(self):
        self.MagRefs = []
        self.MagRefsDict = {}
        self.magnets_VELA = None
        self.magnets_CLARA =None
        self.bpm_VELA = None
        self.las_VELA = None
        self.SetEnvironment()
        self.sysMags_V = self.magnets_VELA.getMagnetNames()
        self.gun = None
        self.llrfInit = None
        if not self.filedata.Using_Llrf == self.filedata.True_False_Offline[1]:  # if not "False"
            self.llrfInit = llrf.init()
            self.LLRFSetup()
        self.CreateRefList()
        self.CreateRefDict()


