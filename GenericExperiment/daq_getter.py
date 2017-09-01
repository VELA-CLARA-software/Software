# import file_reader as FRC

class daq_getter(object):

    def __init__(self):
        print "A daq getter object has been created!"
        self.BPMXList = []
        self.BPMYList = []
        self.BPMQList = []
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
        with open("BPMData.txt", 'a+') as Bdat:  # to write data out to for later viewing
            Bdat.write("Loop " + str(k) + " Laser state: " + LS + "\n")
            for i in range(0, len(BPM_Names)):  # loop over the BPMs
                Bdat.write("BPM0" + str(i + 1) + "\n")
                Bdat.write(
                    "X = " + str(self.BPMXList[i]) + " Y = " + str(self.BPMYList[i]) + " Q = " + str(self.BPMQList[i]))
                Bdat.write("\n")
                Bdat.write("\n")
