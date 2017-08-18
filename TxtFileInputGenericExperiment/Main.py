# Written by Michael Sullivan (Ogden Trust Internship)
# July-August 2017

# This script is passed an object from the Master Controller with sets up the values for the Online Simulator.
# The code is looped such that multiple sets of data can be taken in one run, with (for the physical machine) runs
# with the laser turned off so data from the background can be taken (and eventually subtracted from the data).
# Data from the BPMs and CAMs are stored in arrays for each run and are also outputted to textfiles in the path.


import MasterController3 as MC
import onlineModel

T = MC.MasterController('Instructions2')
# SetEnvironment function isnt working at the moment!
# T.SetEnvironment() # sets to either Physical or Virtual Machine based on txt file
# Run checks here before starting up the online model
T.filedata.CompareLoops() # checks to see if the data given in the txt file is consistent!
T.filedata.CompareMagNum()
T.filedata.CheckLoopLengths()
AllBPMdata=[] # this will store array of arrays with all the BPM data from each loop
AllCAMdata=[] # this will store array of arrays with all the CAM data from each loop

if T.filedata.Gun_Type == T.filedata.Gun_TypeKeywords[0]: # using VELA line
	print "Using VELA LINE"
	ASTRA = onlineModel.ASTRA(V_MAG_Ctrl=T.magnets_VELA,
							C_S01_MAG_Ctrl=None,
							C_S02_MAG_Ctrl=None,
							C2V_MAG_Ctrl=T.magnets_CLARA,
							V_RF_Ctrl=T.gun,
							C_RF_Ctrl=None,
							L01_RF_Ctrl=None,
							messages=True)
elif T.filedata.Gun_Type == T.filedata.Gun_TypeKeywords[1]: # Using CLARA line
	print "Using CLARA LINE"
	ASTRA = onlineModel.ASTRA(V_MAG_Ctrl=T.magnets_VELA,
							C_S01_MAG_Ctrl=T.magnets_CLARA,	# CS01/2 & Clara Mags use same controller
							C_S02_MAG_Ctrl=T.magnets_CLARA,
							C2V_MAG_Ctrl=T.magnets_CLARA,
							V_RF_Ctrl=None,
							C_RF_Ctrl=T.gun, # C and L01 use same controller
							L01_RF_Ctrl=T.gun,
							messages=True)


# set the start and stop elements
Start_Element = T.filedata.Start_Element
Stop_Element = T.filedata.Stop_Element
print Start_Element
Bdat = open("BPMData.txt", 'w+') # to write data out to for later viewing
Cdat = open("CAMData.txt", 'w+')

# It is not possible to simulate dark current on the Online Simulation so it will be written in but cannot be tested until
# the script can be tested on the real machine!

# Need the script to take data with the full simulation and then take data with the gun off to record the "Dark Current"
# This will be done by looping over 2 * requested loop, one with gun and one without.
# The loop with x even will be the run with the dark current with the setting of the x-1 iteration


for x in range(1, 2 * int(T.filedata.Num_Loops)+1):  # Everything in this loop setups the 'experiment', runs sim, records data

	y = (x + 1) / 2  # shifts index so dark current loops dont affect the numbering!

	if (x % 2 == 0): # if the loop number is even, record data with no RF? Measure "dark current" in this way
		print "Dark current run of Loop Number :" + str(y)
		# T.Setup(y,0) # sets the laser intensity to 0 to get background information
		# do things
	else:

		print "LOOP NUMBER: " + str(y)

		T.Setup(y,1) # This will set up everything from the information in the dictionary (1=laser on)

		for i in T.filedata.Magnets_Used_V:	#checking
			print str(i) + " = " + str(T.magnets_VELA.getSI(i))
		for i in T.filedata.Magnets_Used_C:	#checking
			print str(i) + " = " + str(T.magnets_CLARA.getSI(i))

		# elif T.filedata.Gun_Type == T.filedata.Gun_TypeKeywords[1]: # using CLARA line
		# 	T.Setup(y, 1)
		# 	print "Here1"
		# 	for i in T.filedata.Magnets_Used:	#checking
		# 		print str(i) + " = " + str(T.magnets_CLARA.getSI(i))
		# 	print "Here2"

		ASTRA.startElement = Start_Element	# Takes start and stop elements for the sim from the txt file
		print "ASTRA.startElement = " + str(ASTRA.startElement)
		ASTRA.stopElement = Stop_Element
		ASTRA.initDistrib = 'temp-start.ini'
		ASTRA.initCharge = 0.25 #The units are in nC (ASTRA) and in the online Model 0.25nC is the default setting
		ASTRA.run()

		# Testing the CAM and BPM values
		print T.ReadBPM() # gives in format [BPMXList, BPMYList, BPMQList]
		print T.ReadCAM() # gives in format [CAMXList, CAMYList]

		AllBPMdata.append(T.ReadBPM())
		AllCAMdata.append(T.ReadCAM())

	# Can output BPM and CAM data to txt files?

		Bdat.write("Loop " + str(y) + "\n")
		Cdat.write("Loop " + str(y) + "\n")
		for i in range(0, len(T.filedata.BPM_Names)): # loop over the BPMs
			Bdat.write("BPM0" + str(i+1) + "\n")
			Bdat.write("X = " + str(T.ReadBPM()[0][i]) + " Y = " + str(T.ReadBPM()[1][i]) + " Q = " + str(T.ReadBPM()[2][i]))
			Bdat.write("\n")
			Bdat.write("\n")
		for i in range(0, len(T.filedata.CAM_Names)):
			Cdat.write("CAM0" + str(i + 1) + "\n")
			Cdat.write("X = " + str(T.ReadCAM()[0][i]) + " Y = " + str(T.ReadCAM()[1][i]) + " SigmaX = " + str(T.ReadCAM()[2][i]) + " SigmaY = " + str(T.ReadCAM()[3][i]))
			Cdat.write("\n")
			Cdat.write("\n")

T.ShutdownMags() # Shutdown the magnets when finished!
Cdat.close()	# Close the output files when finished!
Bdat.close()

