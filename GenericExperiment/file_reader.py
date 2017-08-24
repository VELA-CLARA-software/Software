# Written by Michael Sullivan (Ogden Trust Internship)
# July-August 2017

# This class takes in a txt file of instructions (variables) which will be used to run simulations on either the virtual
# or physical machine.  The Reader stores the raw data of the text file into a dictionary, which can be searched for
# certain keywords to extract relevant data
# Functions also exist to verify the information in the txt file for consistency
# A Reader object will be passed to the Master Controller to set the variables via the various controllers in the system

# This is the reader class for the txt file in the format of "Instructions_machine.txt"

from VELA_CLARA_Magnet_Control import MACHINE_AREA
from VELA_CLARA_Magnet_Control import MACHINE_MODE
import sys

class file_reader:

    data = None
    input_file_name = None
    # ALL KEYWORDS IN INPUT FILE 
    #Magnets_Used = "Magnets_Used"
    #MACHINE_MODE = "MACHINE_MODE"
    Machine_Type = "Machine_Type"
    USING_MAG = "USING_MAG"

    def __init__(self, input_file_name):

        self.LLRFKeywords = ["LLRF_Amplitude_MVM", "LLRF_Phase_DEG"]
        self.LaserKeywords = ["LASER_HPos", "LASER_VPos", "LASER_Intensity"]
        self.BPMKeywords = ["BPM01", "BPM02", "BPM03", "BPM04"]
        self.CAMKeywords = ["YAG01", "YAG02", "YAG03", "YAG04"]
        self.DAQKeywords = ["DAQ_LASER_ON", "DAQ_LASER_OFF"]
        self.magnetType  = None
        self.machineMode = None
        self.VariableTypeList = ["MAGNETS", "LLRF", "LASER"]
        self.MagnetKeywords = ["QUAD01", "QUAD02", "QUAD03", "QUAD04", "QUAD05", "QUAD06", "QUAD07", "QUAD08", "QUAD09",
                               "QUAD10", "QUAD11", "QUAD12", "QUAD13", "QUAD14", "QUAD15", "SOL", "DIP01", "DIP02",
                               "DIP03", "BSOL","HCOR02", "HCOR03", "HCOR04", "HCOR05", "HCOR06", "HCOR07", "HCOR08", "HCOR09",
                               "HCOR10", "HCOR11", "VCOR01", "VCOR02", "VCOR03", "VCOR04", "VCOR05", "VCOR06", "VCOR07",
                               "VCOR08", "VCOR09", "VCOR10", "VCOR11", "C2V-HCOR1", "C2V-QUAD1", "C2V-QUAD2", "C2V-QUAD3",
                               "C2V-VCOR1","L01-SOL1", "L01-SOL2", "LRG-BSOL", "LRG-SOL", "S01-HCOR1", "S01-HCOR2", "S01-VCOR1",
                               "S01-VCOR2","S02-HCOR1", "S02-HCOR2", "S02-QUAD1", "S02-QUAD2", "S02-QUAD3", "S02-QUAD4",
                               "S02-QUAD5", "S02-VCOR1","S02-VCOR2"]
        self.loop_keys = self.MagnetKeywords + self.LLRFKeywords + self.LaserKeywords + self.DAQKeywords

        print "A Reader object has been created called " + str(input_file_name) #MAGIC_STRING
        self.input_file_name = input_file_name
        # open the file for reading, if file is not a .txt this won't work
        # IS THIS AS SAFE AS IT COULD BE????
        # WHAT HAPPENS IF WE CAN'T OPEN input_file_name ???

        # Check if the file we are trying to open exists before doing anything else!
        if self.file_exists(input_file_name):
            self.data = open(input_file_name, 'r' )       # store text in a "data" attribute

            # read in the file data and save in fdict
            self.header_dict = {}
            # we could read JUST the header data (
            self.raw_header_data = self.get_raw_data('START_HEADER_DATA:', 'END_HEADER_DATA:')#MAGIC_STRING

            self.processed_header_data = self.get_header_values( self.raw_header_data )
            # get the values from the header dictionary, and put in member variables
            #self.get_header_values()

            print('len(self.processed_header_data["Number_Loops"]) = ',len(self.processed_header_data["Number_Loops"]))

            self.master_loop_dict = {}
            for i in range(0, int(self.processed_header_data["Number_Loops"][0]) ): # MAGIC STRING
                #print i
                start = 'Loop_' + str(i+1)#MAGIC_STRING
                stop  = 'Loop_' + str(i+2)#MAGIC_STRING
                # self.master_loop_dict[start] = self.get_raw_data(start, stop)
                self.master_loop_dict[start] = self.get_loop_values(self.get_raw_data(start, stop))

            self.get_machine_mode()
            self.get_magnet_controller_type()

    def file_exists(self, fn):
        try:
            p = open(fn, "r")
            p.close()
            return 1
        except IOError:
            print "Error: " + "'" + fn +"'" + " does not appear to exist."
            sys.exit() # Does allow the code to continue if cant find the instruction file!

    def get_machine_mode(self):
        if self.processed_header_data[self.Machine_Type][0] == "V":#MAGIC_STRING
            self.machineMode =  MACHINE_MODE.VIRTUAL
        elif self.processed_header_data[self.Machine_Type][0] == "P":#MAGIC_STRING
            self.machineMode = MACHINE_MODE.PHYSICAL

    # Maybe pass in some keyword here like "MAGNETS" so that can get specific controller types?
    def get_magnet_controller_type(self):
        if self.processed_header_data[self.USING_MAG][0] == "VELA_INJ":#MAGIC_STRING
            self.magnetType =  MACHINE_AREA.VELA_INJ
        elif self.processed_header_data[self.USING_MAG][0] == "VELA_BA1":#MAGIC_STRING
            self.magnetType =  MACHINE_AREA.VELA_BA1


    def print_loop_dict(self,dict):
        for key,val in dict.iteritems():
            print key
            for key2,val2 in val.iteritems():
                print(key2, val2)

    def get_loop_values(self, dict):
        # search through dict  and find data associated with loop_keys
        r_dict = {}
        for key in self.loop_keys:
             if self.search(key, dict) == None: pass
             # If cant find a value in the txt file, don't add to the dictionary
             else:
                r_dict[key] =  self.search(key,dict) # Add "found" key to the dictionary
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
        self.header_keys =["Magnets_Used",
                           "Number_Magnets",
                           "Number_Loops",
                           "BPM_Names",
                           "CAM_Names",
                           "Start_Element",
                           "Stop_Element",
                           "Gun_Type",
                           "BPM_Type",
                           "Machine_Type",
                           "USING_MAG",
                           "USING_BPM",
                           "USING_LLRF",
                           "USING_LASER"]#MAGIC_STRING

        for key in self.header_keys:
            r_dict[key] =  self.search(key,dict)
        return r_dict
        # self.Magnets_Used = self.search("Magnets_Used",self.header_dict)
        # self.Number_Magnets = self.search("Number_Magnets",self.header_dict)
        # self.Num_Loops = self.search("Number_Loops",self.header_dict)
        # self.BPM_Names = self.search("BPM_Names",self.header_dict)
        # self.CAM_Names = self.search("CAM_Names",self.header_dict)
        # self.Start_Element = self.search("Start_Element",self.header_dict)
        # self.Stop_Element = self.search("Stop_Element",self.header_dict)
        # self.Gun_Type = self.search("Gun_Type",self.header_dict)
        # self.BPM_Type = self.search("BPM_Type",self.header_dict)
        # self.Machine_Mode = self.search("MACHINE_MODE",self.header_dict)

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
        if self.processed_header_data[self.Machine_Type][0] == "P": # use virtual machine
            return True
        return False

    def isVirtual(self):
        if self.processed_header_data[self.Machine_Type][0] == "V": # use virtual machine
            return True
        return False

T = file_reader('Instructions_machine.txt')
T.print_dict(T.master_loop_dict)
T.print_dict(T.processed_header_data)
print T.processed_header_data[T.Machine_Type][0]
print T.isPhysical()
print T.isVirtual()