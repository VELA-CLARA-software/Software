## NOTE: HAVE 'temp-start.ini IN THE SAME LOCAL DIRECTORY AS THIS FILE WHEN RUNNING
import sys,os
import time
#Set up EPIC environment for Virtual Machine
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12" 
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
os.environ["EPICS_CA_SERVER_PORT"]="6000"

#Look on server for Hardware Controllers and Online Model
sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\Release')
sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\OnlineModel')

#Import online model and relevant controllers
import onlineModel
import VELA_CLARA_Magnet_Control as mag
import VELA_CLARA_LLRFControl as llrf

#Create controllers
magInit = 	mag.init()
llrfInit = 	llrf.init()
magnets_VELA = 		magInit.virtual_VELA_INJ_Magnet_Controller()
gun = 				llrfInit.virtual_CLARA_LRRG_LLRF_Controller()#using this because it have the same PVs
magnets_CLARA = 	magInit.virtual_CLARA_PH1_Magnet_Controller()

#Initialize Online Model
ASTRA = onlineModel.ASTRA(V_MAG_Ctrl=magnets_VELA,
						C_S01_MAG_Ctrl=None,
						C_S02_MAG_Ctrl=None,
						C2V_MAG_Ctrl=magnets_CLARA,
						V_RF_Ctrl=gun,
						C_RF_Ctrl=None,
						L01_RF_Ctrl=None,
						messages=True)
# The input variables I have set to 'None' you do not need to include when Initializing this.
# I've just put them in there so you can seen what the options are that you can have.

#Set up Dipole
magnets_CLARA.switchONpsu('DIP02')
magnets_CLARA.setSI('DIP02',-10)
#Set up Gun (10 Hz)
gun.setAmpMVM(65)#MV/m

#Run Online Model (VELA to Spectrometer line)
ASTRA.startElement = 'V1-GUN'
ASTRA.stopElement = 'SP-YAG04'
ASTRA.initDistrib = 'temp-start.ini'
ASTRA.run()

#To run this in one line and in a thread, use in a PyQt application. The function is:
#ASTRA.go('V1-GUN','SP-YAG04','temp-start.ini')
