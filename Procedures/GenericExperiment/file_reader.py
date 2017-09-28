# Written by Michael Sullivan (Ogden Trust Internship)
# July-August 2017

# This class takes in a txt file of instructions (variables) which will be used to run simulations on either the virtual
# or physical machine.  The Reader stores the raw data of the text file into a dictionary, which can be searched for
# certain keywords to extract relevant data
# Functions also exist to verify the information in the txt file for consistency
# A Reader object will be passed to the Master Controller to set the variables via the various controllers in the system

# This is the reader class for the txt file in the format of "Instructions_machine.txt"
import sys, os
import global_keywords as gk




sys.path.remove('\\\\fed.cclrc.ac.uk\\org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\stage')
sys.path.append('\\\\fed.cclrc.ac.uk\\org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\stagetim')
from VELA_CLARA_LLRF_Control import MACHINE_AREA
from VELA_CLARA_LLRF_Control import MACHINE_MODE
from VELA_CLARA_LLRF_Control import LLRF_TYPE
# from VELA_CLARA_BPM_Control import MACHINE_AREA as bpm_MACHINE_AREA


class file_reader:

    data = None
    input_file_name = None

    def __init__(self, input_file_name):

        self.magnetType  = None
        self.llrfType = None
        self.bpmType = None
        self.laserState = None
        self.llrfState = None
        self.machineMode = None
        self.camType = None
        self.daqState = None


        print "A Reader object has been created called " + str(input_file_name) #MAGIC_STRING
        self.input_file_name = input_file_name
        # open the file for reading, if file is not a .txt this won't work

        # Check if the file we are trying to open exists before doing anything else!
        if self.file_exists(input_file_name):
            self.data = open(input_file_name, 'r' )       # store text in a "data" attribute

            # read in the file data and save in fdict
            self.header_dict = {}
            # we could read JUST the header data (
            self.raw_header_data = self.get_raw_data('START_HEADER_DATA:', 'END_HEADER_DATA:')#MAGIC_STRING

            self.processed_header_data = self.get_header_values( self.raw_header_data )
            # get the values from the header dictionary, and put in member variables

            self.number_loops = int(self.processed_header_data[gk.Number_Loops][0])

            self.master_loop_dict = {}
            for i in range(0, self.number_loops ): # MAGIC STRING
                #print i
                start = gk.Loop_ + str(i+1)#MAGIC_STRING
                stop  = gk.Loop_ + str(i+2)#MAGIC_STRING
                # self.master_loop_dict[start] = self.get_raw_data(start, stop)
                self.master_loop_dict[start] = self.get_loop_values(self.get_raw_data(start, stop))

            self.number_loops = int(self.processed_header_data[gk.Number_Loops][0])
            self.Start_Element = self.processed_header_data[gk.Start_Element][0]
            self.Stop_Element = self.processed_header_data[gk.Stop_Element][0]
            self.BPM_Names = self.processed_header_data[gk.BPM_Names]
            # for names in self.BPM_Names:
            #     print names
            self.get_machine_mode()
            self.get_magnet_controller_type()
            # self.get_llrf_controller_state()
            self.get_laser_controller_state()
            self.get_bpm_controller_type()
            self.get_llrf_controller_type()
            self.get_daq_controller_state()

    def file_exists(self, fn):
        try:
            p = open(fn, "r")
            p.close()
            return 1
        except IOError:
            print "Error: " + "'" + fn +"'" + " does not appear to exist."
            sys.exit() # Does allow the code to continue if cant find the instruction file!

    def get_machine_mode(self):
        if self.processed_header_data[gk.Machine_Type][0] == gk.Machine_type_keywords[0]:
            self.machineMode =  MACHINE_MODE.VIRTUAL
        elif self.processed_header_data[gk.Machine_Type][0] == gk.Machine_type_keywords[1]:
            self.machineMode = MACHINE_MODE.PHYSICAL

    # Maybe pass in some keyword here like "bpmNETS" so that can get specific controller types?
    def get_magnet_controller_type(self):
        # MachineAreaList = ["CLARA_2_VELA","CLARA_INJ", "VELA_BA1", "VELA_BA2", "VELA_INJ", "CLARA_L01", "CLARA_S01", "CLARA_S02", "CLARA_PH1"]

        if self.processed_header_data[gk.USING_MAG][0] == gk.MachineAreaList[4]:
            self.magnetType =  MACHINE_AREA.VELA_INJ
        elif self.processed_header_data[gk.USING_MAG][0] == gk.MachineAreaList[2]:
            self.magnetType =  MACHINE_AREA.VELA_BA1
        elif self.processed_header_data[gk.USING_MAG][0] == gk.MachineAreaList[0]:
            self.magnetType =  MACHINE_AREA.CLARA_2_VELA
        elif self.processed_header_data[gk.USING_MAG][0] == gk.MachineAreaList[1]:
            self.magnetType =  MACHINE_AREA.CLARA_INJ
        elif self.processed_header_data[gk.USING_MAG][0] == gk.MachineAreaList[3]:
            self.magnetType =  MACHINE_AREA.VELA_BA2

    def get_bpm_controller_type(self):
        # MachineAreaList = ["CLARA_2_VELA","CLARA_INJ", "VELA_BA1", "VELA_BA2", "VELA_INJ", "CLARA_L01", "CLARA_S01", "CLARA_S02", "CLARA_PH1"]
        if self.processed_header_data[gk.USING_BPM][0] == gk.MachineAreaList[4]:#MAGIC_STRING
            self.bpmType =  MACHINE_AREA.VELA_INJ
        elif self.processed_header_data[gk.USING_BPM][0] == gk.MachineAreaList[2]:#MAGIC_STRING
            self.bpmType =  MACHINE_AREA.VELA_BA1
        elif self.processed_header_data[gk.USING_BPM][0] == gk.MachineAreaList[0]:
            self.bpmType = MACHINE_AREA.CLARA_2_VELA
        elif self.processed_header_data[gk.USING_BPM][0] == gk.MachineAreaList[1]:
            self.bpmType = MACHINE_AREA.CLARA_INJ
        elif self.processed_header_data[gk.USING_BPM][0] == gk.MachineAreaList[3]:
            self.bpmType = MACHINE_AREA.VELA_BA2 # DOESNT EXIST YET!
        elif self.processed_header_data[gk.USING_BPM][0] == gk.MachineAreaList[5]:
            self.bpmType = MACHINE_AREA.CLARA_L01 # DOESNT EXIST YET!
        elif self.processed_header_data[gk.USING_BPM][0] == gk.MachineAreaList[6]:
            self.bpmType = MACHINE_AREA.CLARA_S01 # DOESNT EXIST YET!
        elif self.processed_header_data[gk.USING_BPM][0] == gk.MachineAreaList[7]:
            self.bpmType = MACHINE_AREA.CLARA_S02 # DOESNT EXIST YET!
        elif self.processed_header_data[gk.USING_BPM][0] == gk.MachineAreaList[8]:
            self.bpmType = MACHINE_AREA.CLARA_PH1 # DOESNT EXIST YET!

    def get_llrf_controller_type(self):
        # self.llrf_TypeList = ["CLARA_HRRG", "CLARA_LRRG", "L01", "VELA_HRRG", "VELA_LRRG"]
        if self.processed_header_data[gk.USING_LLRF][0] == gk.llrf_TypeList[4]:#MAGIC_STRING
            self.llrfType =  LLRF_TYPE.VELA_LRRG
        elif self.processed_header_data[gk.USING_LLRF][0] == gk.llrf_TypeList[1]:
            self.llrfType =  LLRF_TYPE.CLARA_LRRG
        elif self.processed_header_data[gk.USING_LLRF][0] == gk.llrf_TypeList[2]:
            self.llrfType =  LLRF_TYPE.L01
        elif self.processed_header_data[gk.USING_LLRF][0] == gk.llrf_TypeList[0]:
            self.llrfType =  LLRF_TYPE.CLARA_HRRG
        elif self.processed_header_data[gk.USING_LLRF][0] == gk.llrf_TypeList[3]:
            self.llrfType =  LLRF_TYPE.VELA_HRRG

    def get_laser_controller_state(self):
        if self.processed_header_data[gk.USING_LASER][0] == "T":#MAGIC_STRING
            self.laserState =  True
        elif self.processed_header_data[gk.USING_LASER][0] == "F":#MAGIC_STRING
            self.laserState =  False

    def get_daq_controller_state(self):
        if self.processed_header_data[gk.USING_DAQ][0] == "T":#MAGIC_STRING
            self.daqState =  True
        elif self.processed_header_data[gk.USING_DAQ][0] == "F":#MAGIC_STRING
            self.daqState =  False

    def print_loop_dict(self,dict):
        for key,val in dict.iteritems():
            print key
            for key2,val2 in val.iteritems():
                print(key2, val2)

    def get_loop_values(self, dict):
        # search through dict  and find data associated with loop_keys
        r_dict = {}
        for setting_key in gk.setting_keywords:
             if self.search(setting_key, dict) == None: pass
             # If cant find a value in the txt file, don't add to the dictionary
             else:
                # clear the t_dict for each run.
                t_dict = {} # temporary dictionay
                for key in self.search(setting_key,dict):
                    # for each key to the left of the ":", split up from either side of "=" and put into dict
                    # t_dict stores all information of settings to right of :
                    # t_dict is then inserted as a value in r_dict with key of setting_key
                    t_dict[key.split('=')[0]] = key.split('=')[1]
                r_dict[setting_key] =  t_dict # Add "found" key to the dictionary
        return r_dict

    def get_raw_data(self, start_keyword, end_keyword):
        # read input file line by line and append the data between
        # start_keyword and end_keyword into the retrun dict
        # the return dict is formatted such that ':' seperates keys and values
        # values are ALWAYS in a list. multiple values are ',' delimited
        with open(self.input_file_name) as input_data:
            dict = {}
            can_append = False
            # Skips text before the beginning of the interesting block:
            for line in input_data:
                if line.strip() == end_keyword:
                    break
                if line.strip() == start_keyword:  # Or whatever test is needed
                    can_append = True
                if can_append:
                    words = line.strip().split(':')
                    if len(words) > 1:
                        dict[ words[0] ] = words[1].strip().replace(' ','').split(',') # gets rid of all whitespace and commas etc
        return dict

    def get_header_values(self, dict):
        # search through dict  and find data associated with header_keys
        r_dict = {}
        for key in gk.header_keys:
            r_dict[key] =  self.search(key,dict)
        return r_dict

    def search(self, searchphrase,dict):
        # searches fdict for searchphrase
        # and returns list with data from input keyed with searchphrase
        # else return None
        for i,j in dict.iteritems():
            if i == searchphrase:
                return j
        print '!WARNING!' + str(searchphrase) + " not found."
        # Perhap WARNING can be handled differently as this can get quite annoying!
        return None

    def print_dict(self, dict):
        for key, val in dict.iteritems():
            print key, val

    def isPhysical(self):
        if self.processed_header_data[gk.Machine_Type][0] == gk.Machine_type_keywords[1]: # use virtual machine
            return True
        return False

    def isVirtual(self):
        if self.processed_header_data[gk.Machine_Type][0] == gk.Machine_type_keywords[0]: # use virtual machine
            return True
        return False
