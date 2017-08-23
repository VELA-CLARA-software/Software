# Written by Michael Sullivan (Ogden Trust Internship)
# July-August 2017

# This class takes in a txt file of instructions (variables) which will be used to run simulations on either the virtual
# or physical machine.  The Reader stores the raw data of the text file into a dictionary, which can be searched for
# certain keywords to extract relevant data
# Functions also exist to verify the information in the txt file for consistency
# A Reader object will be passed to the Master Controller to set the variables via the various controllers in the system

# This is the reader class for the txt file in the format of "Instructions2.txt"

from VELA_CLARA_Magnet_Control import MACHINE_AREA
from VELA_CLARA_Magnet_Control import MACHINE_MODE

class file_reader:

    data = None
    input_file_name = None
    # ALL KEYWORDS IN INPUT FILE 
    #Magnets_Used = "Magnets_Used"
    #MACHINE_MODE = "MACHINE_MODE"

    def __init__(self, input_file_name):

        self.LLRFKeywords = ["LLRF_Amplitude", "LLRF_Phase"]
        self.LaserKeywords = ["LASER_HPos", "LASER_VPos", "LASER_Intensity"]
        self.BPMKeywords = ["BPM01", "BPM02", "BPM03", "BPM04"]
        self.CAMKeywords = ["YAG01", "YAG02", "YAG03", "YAG04"]
        self.DAQKeywords = ["DAQ_LASER_ON", "DAQ_LASER_OFF"]
        self.magnetType  = None
        self.machineMode = None

        print "A Reader object has been created called " + str(input_file_name) + ".txt"#MAGIC_STRING
        self.input_file_name = input_file_name
        # open the file for reading, if file is not a .txt this won't work
        # IS THIS AS SAFE AS IT COULD BE????
        # WHAT HAPPENS IF WE CAN'T OPEN input_file_name ???
        self.data = open(input_file_name + ".txt", 'r' )       # store text in a "data" attribute

        # read in the file data and save in fdict
        self.header_dict = {}
        # we could read JUST the header data (
        self.raw_header_data = self.get_raw_data('START_HEADER_DATA:', 'END_HEADER_DATA:')#MAGIC_STRING

        self.processed_header_data = self.get_header_values( self.raw_header_data )
        # get the values from the ehader dictionary, and put in meember variables
        #self.get_header_values()

        print('len(self.processed_header_data["Number_Loops"]) = ',len(self.processed_header_data["Number_Loops"]))

        self.master_loop_dict = {}
        for i in range(0, int(self.processed_header_data["Number_Loops"][0]) ):
            #print i
            start = 'Loop_' + str(i+1)#MAGIC_STRING
            stop  = 'Loop_' + str(i+2)#MAGIC_STRING
            self.master_loop_dict[start] = self.get_raw_data(start, stop)
        #print 'PRINTING LOOP DICT'
        #self.print_loop_dict(self.master_loop_dict )
        self.get_machine_mode()
        self.get_magnet_controller_type()

    def get_machine_mode(self):
        if self.processed_header_data["Machine_Type"][0] == "V":#MAGIC_STRING
            self.machineMode =  MACHINE_MODE.PHYSICAL
        elif self.processed_header_data["Machine_Type"][0] == "P":#MAGIC_STRING
            self.machineMode = MACHINE_MODE.PHYSICAL

    def get_magnet_controller_type(self):
        if self.processed_header_data["USING_MAG"][0] == "VELA_INJ":#MAGIC_STRING
            self.magnetType =  MACHINE_AREA.VELA_INJ
        elif self.processed_header_data["USING_MAG"][0] == "VELA_BA1":#MAGIC_STRING
            self.magnetType =  MACHINE_AREA.VELA_BA1


    def print_loop_dict(self,dict):
        for key,val in dict.iteritems():
            print key
            for key2,val2 in val.iteritems():
                print(key2, val2)

    def get_loop_values(self, dict):
        M ={}
        LL ={}
        L = {}
        D = {}
        for i, j in dict.iteritems():
            if i in self.MagnetKeywords:
                M[i] = j
            elif i in self.LLRFKeywords:
                LL[i] = j
            elif i in self.LaserKeywords:
                L[i] = j
            elif i in self.DAQKeywords:
                D[i]= j
            else: M[i] = j # assume magnet if nothing else?
        LoopMaster = {"MAGNETS": M, "LLRF": LL, "LASER": L, "DAQ": D}
        return LoopMaster

    def get_raw_data(self, start_keyword, end_keyword):
        # read input file line by line and appned the data between
        # start_keyword and end_keyword into the retrun dict
        # the return dict is formatted sucj that ':' seperates keys nad values
        # values are ALWAYS in a list. multiple values are ',' delimited
        with open(self.input_file_name + ".txt") as input_data:
            dict = {}
            can_append = False
            # Skips text before the beginning of the interesting block:
            for line in input_data:
                #
                if line.strip() == end_keyword:
                    break
                if line.strip() == start_keyword:  # Or whatever test is needed
                    can_append = True
                if can_append:
                    words = line.strip().split(':')
                    if len(words) > 1:
                        dict[ words[0] ] = words[1].strip().split(',')
        # for key,val in dict.iteritems():
        #     print('key = ', key, 'val = ', val)
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
                           "USING_MAG"]#MAGIC_STRING

        for key in self.header_keys:
            r_dict[key] =  self.search(key,dict)
            #print( key,r_dict[key]  )
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
            #print i, j
            if i == searchphrase:
                return j
        print '!WARNING!' + str(searchphrase) + " not found."
        return None

