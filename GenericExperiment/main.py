import sys

# sys.path.append('\\\\fed.cclrc.ac.uk\\org\\NLab\\ASTeC\\Projects\\VELA\\Software\\OnlineModel')
# sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\stage')
import global_keywords as gk
import master_controller as mc
import onlineModel

input_file = 'Instructions_machine.txt'


T = mc.master_controller( )
T.read_procedure_file(input_file)
T.create_controllers()

if T.filedata.isVirtual():
	ASTRA = onlineModel.ASTRA(V_MAG_Ctrl=T.mag_control,
							C_S01_MAG_Ctrl=None,
                            C_S02_MAG_Ctrl=None,
                            C2V_MAG_Ctrl=T.mag_control,
                            V_RF_Ctrl=T.llrf_control,
                            C_RF_Ctrl=None,
                            L01_RF_Ctrl=None,
                            messages=True)
	# set the start and stop elements
	Start_Element = T.filedata.Start_Element
	Stop_Element = T.filedata.Stop_Element

Cdat = open("CAMData.txt", 'w+')
open("BPMData.txt",'w').close()  # when first writing to file, delete all previous content

def main_run(k, u): # kth loop, u for laser on/off
    if u == 0: LS = "OFF"
    elif u == 1: LS = "ON"
    print "LOOP NUMBER: " + str(k) + "; Laser State: " + LS
    T.setup_controllers(k,u)

    for i in T.filedata.processed_header_data[gk.Magnets_Used]:  # checking
        print str(i) + " = " + str(T.mag_control.getSI(i))

    print "T.llrf_control.getAmpMVM()", T.llrf_control.getAmpMVM()

    if T.filedata.isVirtual():
        ASTRA.startElement = Start_Element  # Takes start and stop elements for the sim from the txt file
        print "ASTRA.startElement = " + str(ASTRA.startElement)
        ASTRA.stopElement = Stop_Element
        ASTRA.initDistrib = 'temp-start.ini'
        ASTRA.initCharge = 0.25  # The units are in nC (ASTRA) and in the online Model 0.25nC is the default setting
        ASTRA.run()

    T.get_daq(k, u)
    T.read_cam(k, u)

    # use the DAQ stuff here!


for i in range(1, T.filedata.number_loops + 1):
    if not T.filedata.master_loop_dict[gk.Loop_ +str(i)][gk.DAQ_SETTINGS][gk.DAQ_LASER_ON] == 0:
        main_run(i, 1)
    if not T.filedata.master_loop_dict[gk.Loop_ +str(i)][gk.DAQ_SETTINGS][gk.DAQ_LASER_OFF] == 0:
        main_run(i, 0)













