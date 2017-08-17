# Written by Michael Sullivan (Ogden Trust Internship)
# July-August 2017

# This class takes in a txt file of instructions (variables) which will be used to run simulations on either the virtual
# or physical machine.  The Reader stores the raw data of the text file into a dictionary, which can be searched for
# certain keywords to extract relevant data
# Functions also exist to verify the information in the txt file for consistency
# A Reader object will be passed to the Master Controller to set the variables via the various controllers in the system

# This is the reader class for the txt file in the format of "Instructions2.txt"

class Reader:

    data = None
    name = None

    def __init__(self):
        print "An empty Reader object has been created!"

    def __init__(self, name):
        print "A Reader object has been created called " + str(name) + ".txt"
        self.name = name
        self.data = open(name + ".txt", 'r' )       # store text in a "data" attribute
        self.Magnets_Used_C = self.search("Magnets_Used_C")
        self.Magnets_Used_V = self.search("Magnets_Used_V")
        self.Magnets_Used_Total = self.Magnets_Used_C + self.Magnets_Used_V
        self.Machine_Type = self.search("Machine_Type")[0] # [0] as technically gives a list with 1 value
        self.Number_Magnets = self.search("Number_Magnets")[0]
        self.Num_Loops = self.search("Number_Loops")[0]
        self.BPM_Names = self.search("BPM_Names")
        self.CAM_Names = self.search("CAM_Names")
        self.Start_Element = self.search("Start_Element")[0]
        self.Stop_Element = self.search("Stop_Element")[0]
        self.Gun_Type = self.search("Gun_Type")[0]
        self.BPM_Type = self.search("BPM_Type")[0]
        self.BPM_TypeKeywords = ["VELA", "CLARA"]
        self.Gun_TypeKeywords = ["VELA", "CLARA", "L01"]
        self.LLRF_Amplitude = self.search("LLRF_Amplitude")[0]
        self.LLRF_Phase = self.search("LLRF_Phase")[0]
        self.LASER_HPos = self.search("LASER_HPos")[0]
        self.LASER_VPos = self.search("LASER_VPos")[0]
        self.LASER_Intensity = self.search("LASER_Intensity")[0]
        self.Magdict = {}
        self.LLRFdict = {}
        self.Laserdict = {}
        self.Magnets = "MAGNETS"
        self.LLRF = "LLRF"
        self.Laser = "LASER"
        self.VariableTypeList = ["MAGNETS", "LLRF", "LASER"]
        self.MagnetKeywords = ["QUAD01", "QUAD02", "QUAD03", "QUAD04", "QUAD05", "QUAD06", "QUAD07", "QUAD08", "QUAD09",
                               "QUAD10", "QUAD11", "QUAD12", "QUAD13", "QUAD14", "QUAD15", "SOL","DIP01","DIP02", "DIP03", "BSOL",
                               "HCOR02", "HCOR03", "HCOR04", "HCOR05", "HCOR06", "HCOR07", "HCOR08", "HCOR09",
                               "HCOR10", "HCOR11", "VCOR01", "VCOR02", "VCOR03", "VCOR04", "VCOR05", "VCOR06", "VCOR07","VCOR08",
                               "VCOR09", "VCOR10", "VCOR11", "C2V-HCOR1", "C2V-QUAD1", "C2V-QUAD2", "C2V-QUAD3", "C2V-VCOR1",
                                "L01-SOL1", "L01-SOL2", "LRG-BSOL", "LRG-SOL", "S01-HCOR1", "S01-HCOR2", "S01-VCOR1", "S01-VCOR2",
                               "S02-HCOR1", "S02-HCOR2", "S02-QUAD1", "S02-QUAD2", "S02-QUAD3", "S02-QUAD4", "S02-QUAD5", "S02-VCOR1",
                               "S02-VCOR2"]
        self.LLRFKeywords = ["LLRF_Amplitude", "LLRF_Phase"]
        self.LaserKeywords = ["LASER_HPos", "LASER_VPos", "LASER_Intensity"]
        self.BPMKeywords = ["BPM01", "BPM02", "BPM03", "BPM04"]
        self.CAMKeywords = ["YAG01", "YAG02", "YAG03", "YAG04"]

    def isPhysical(self):
        if self.Machine_Type == "V": # use virtual machine
            return False
        elif self.Machine_Type == "P": # use Physical machine
            return True
        else: print "Cannot determine from file if Physical or Virtual!"
        quit()

    def filedict(self): # extract required magnet currents from txt file
        fdict={}
        with open(self.name + ".txt", 'r') as dat:
            for line in dat:
                words = line.split()
                newwords=[]
                for i in words:
                    newi = i.replace(",", "")
                    newi2 = newi.replace(":", "")
                    newwords.append(newi2)
                # print newwords
                info=[]
                if not newwords: pass
                elif "#" in newwords: pass # ignores comments in txt file
                else:   # otherwise write to the dictionary
                    for i in range(1,len(newwords)):
                            info.append(newwords[i])
                    fdict[newwords[0]] = info
        return fdict

    def search(self, searchphrase):
        for i,j in self.filedict().iteritems():
            if i == searchphrase:
                return j
        print str(searchphrase) + " not found."

    def LoopsGiven(self):# Counts the number of Loops actually given in the txt file
        p = 0
        for i, j in self.filedict().iteritems(): #Dictionary gives number of Distinct loops in txt file
            if "Loop_" in i:
                p = p + 1
        return p

    def LoopData(self, k):
        with open('Instructions2.txt') as input_data:
            dict = {}
            # Skips text before the beginning of the interesting block:
            for line in input_data:
                if line.strip() == 'Loop_' + str(k):  # Or whatever test is needed
                    break
            # Reads text until the end of the block:
            for line in input_data:  # This keeps reading the file
                if line.strip() == 'Loop_' + str(k + 1):
                    break

                words = line.split()
                newwords = []
                for i in words:
                    newi = i.replace(",", "")
                    newi2 = newi.replace(":", "") # gets rid of the : from the txt file
                    newwords.append(newi2)
                #print newwords
                info = []
                if not newwords:  # gets rid of the empty lines
                    pass    # do nothing
                else:
                    for i in range(1, len(newwords)):       # add info into dictionary
                        info.append(newwords[i])
                    dict[newwords[0]] = info
                    # print newwords[0]
        return dict
        # Line is extracted (or block_of_lines.append(line), etc.)

    def CompareLoops(self):
        if int(self.Num_Loops) == self.LoopsGiven():
            print "Number of loops stated and loops given are consistent!" # do nothing
        else: print "Number of loops stated and loops given are not consistent or Loop number repeated!"; quit()
         # dont allow the code to continue!

    def CompareMagNum(self):
        if int(self.Number_Magnets) != (len(self.Magnets_Used_C) + len(self.Magnets_Used_V)):
            print "Number of stated magnets and named magnets given do not match!"
            quit()
        print "Number of magnets and named magnets matches!"

    def LoopMasterDict(self, k): # gives a nested dictionary with information from all loops
        M ={}
        LL ={}
        L = {}
        for i, j in self.LoopData(k).iteritems():
            if i in self.MagnetKeywords:
                M[i] = j
            elif i in self.LLRFKeywords:
                LL[i] = j
            elif i in self.LaserKeywords:
                L[i] = j
            else: M[i] = j # assume magnet if nothing else?
        LoopMaster = {"MAGNETS": M, "LLRF": LL, "LASER": L}
        return LoopMaster

    def MasterDict(self):
        Master ={}
        for i in range(1, int(self.Num_Loops) + 1):
            Master["Loop_" + str(i)] = self.LoopMasterDict(i)
        return Master

    def PrintSortedMD(self):
        for key, value in sorted(self.MasterDict().iteritems(), key=lambda (k, v): (v, k)):
            print "%s: %s" % (key, value)

    def CheckLoopLengths(self):
        M = []
        for i in range(1, int(self.Num_Loops) + 1):
            M.append(len(self.LoopData(i)))
        seen = set()  # creates empty set
        for number in M:
            if number in seen:
                pass  # number repeated
            seen.add(number)  # wont allow duplicates
        if len(seen) != 1:
            print "One or more loops is missing information! Check txt file!"
            quit()

# T = Reader("Instructions2")
# print T.MasterDict()["Loop_1"]["MAGNETS"]
#
# for i in T.Magnets_Used_Total:
#     print i
