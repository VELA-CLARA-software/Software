# Written by Michael Sullivan (Ogden Trust Internship)
# July-August 2017

# The Master Controller will use the FRC to read in and verify the data in the "instructions"
# test file and then use that set to use the existing controllers to set the necessary
# varibles to run the simulations
# This "Master Controller" py file will be imported into a "main" where the code will
# be ran from (Which will be a short script!)
import sys, os

import file_reader as FRC
import parameter_setter as PS
import daq_getter as DG
import sys, os
import time
import global_keywords as gk

# sys.path.append('\\\\fed.cclrc.ac.uk\\org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\Release')

sys.path.append('\\\\fed.cclrc.ac.uk\\org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\stagetim')
import VELA_CLARA_Magnet_Control as mag
import VELA_CLARA_Camera_DAQ_Control as daq
import VELA_CLARA_BPM_Control as bpm
import VELA_CLARA_LLRF_Control as llrf
import VELA_CLARA_PILaser_Control as las

print "os.path.dirname(bpm.__file__)", os.path.dirname(bpm.__file__)

print "os.path.dirname(llrf.__file__)", os.path.dirname(llrf.__file__)

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
        self.bpmInit = bpm.init()
        self.bpm_control = None
        self.llrfInit = llrf.init()
        self.llrf_control = None
        self.daqInit = daq.init()
        self.daq_control = None
        self.input_file_name = None
        self.daq_getter = DG.daq_getter()

    def read_procedure_file(self,input_file_name):
        print "taking instructions from " + str(input_file_name)
        self.input_file_name = input_file_name # to pass to parameter setter
        self.filedata = FRC.file_reader(input_file_name)  # so the MasterController obj can access data from txt file
        print 'FILE PROCESSED'

    def create_magnet_controller(self):
        print self.filedata.machineMode
        print self.filedata.magnetType
        self.mag_control = self.magInit.getMagnetController( self.filedata.machineMode, self.filedata.magnetType )

    def create_llrf_controller(self):
        self.llrf_control = self.llrfInit.getLLRFController(self.filedata.machineMode, self.filedata.llrfType)
        print "CREATING LLRF CONTROLLER"

    def create_laser_controller(self):
        # THIS COULD BE DONE BETTER?
        if self.filedata.processed_header_data[gk.Machine_Type][0] == gk.Machine_type_keywords[0]:
            self.las_control = self.lasInit.virtual_PILaser_Controller()
            print "CREATING VIRTUAL LASER"
        elif self.filedata.processed_header_data[gk.Machine_Type][0] == gk.Machine_type_keywords[1]:
            self.las_control = self.lasInit.physical_PILaser_Controller()
            print "CREATING PHYSICAL LASER"

    def create_bpm_controller(self):
        self.bpm_control = self.bpmInit.getBPMController(self.filedata.machineMode, self.filedata.bpmType)

    def create_magnet_refs(self):
         for i in self.filedata.processed_header_data[gk.Magnets_Used]:
             self.MagRefs.append(self.mag_control.getMagObjConstRef(i))
         for i in self.MagRefs:
             self.MagRefsDict[i.name] = i

    def create_camera_daq_controller(self):
        print "CREATING DAQ CONTROLLER!!!"
        if self.filedata.processed_header_data[gk.CAM_Type][0] == gk.Cam_Type_Keywords[0]:
            if self.filedata.processed_header_data[gk.Machine_Type][0] == gk.Machine_type_keywords[0]:
                self.daq_control = self.daqInit.virtual_VELA_Camera_DAQ_Controller()
                print "CREATING VIRTUAL VELA DAQ"
            elif self.filedata.processed_header_data[gk.Machine_Type][0] == gk.Machine_type_keywords[1]:
                self.las_control = self.daqInit.physical_VELA_Camera_DAQ_Controller()
                print "CREATING PHYSICAL VELA DAQ"
        elif self.filedata.processed_header_data[gk.CAM_Type][0] == gk.Cam_Type_Keywords[1]:
            if self.filedata.processed_header_data[gk.Machine_Type][0] == gk.Machine_type_keywords[0]:
                self.daq_control = self.daqInit.virtual_CLARA_Camera_DAQ_Controller()
                print "CREATING VIRTUAL CLARA DAQ"
            elif self.filedata.processed_header_data[gk.Machine_Type][0] == gk.Machine_type_keywords[1]:
                self.daq_control = self.daqInit.physical_CLARA_Camera_DAQ_Controller()
                print "CREATING PHYSICAL CLARA DAQ"

    def SetEnvironment(self):
        if self.filedata.isVirtual():
            # set up the environment variables to the Virtual Machine
            print "USING VIRTUAL MACHINE!"
            os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
            os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
            os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
            os.environ["EPICS_CA_SERVER_PORT"] = "6000"

    def create_controllers(self):
        print 'Creating controllers..'

        self.SetEnvironment()
        self.MagRefs = []
        self.MagRefsDict = {}

        if not self.filedata.bpmType == None:
            self.create_bpm_controller()

        if not self.filedata.magnetType == None:
            self.create_magnet_controller()
            self.create_magnet_refs()

        if self.filedata.laserState:
            self.create_laser_controller()

        print "llrfTYPE: " , self.filedata.llrfType
        if not self.filedata.llrfType == None:
            self.create_llrf_controller()

        if self.filedata.daqState:
            self.create_camera_daq_controller()

        self.sysMags = self.mag_control.getMagnetNames()

    def setup_controllers(self, k, u): # kth loop, u is laser on/off
        self.parameter_setter = PS.parameter_setter(self.input_file_name)
        if not self.filedata.magnetType == None:
            self.parameter_setter.setup_magnets(k,self.sysMags,self.mag_control,self.MagRefsDict)
        if self.filedata.laserState:
            self.parameter_setter.setup_laser(k, u, self.las_control)
        if not self.filedata.llrfType == None:
            self.parameter_setter.setup_llrf(k, self.llrf_control)

    def get_daq(self,k, u): # kth loop
        if not self.filedata.bpmType == None:
            print self.daq_getter.ReadBPM(self.bpm_control, self.filedata.BPM_Names)
            self.daq_getter.write_bpm_to_file(k, u, self.filedata.BPM_Names)
            self.daq_getter.read_cam(self.daq_control, k, u, self.filedata.processed_header_data[gk.CAM_Names], self.filedata.master_loop_dict)
