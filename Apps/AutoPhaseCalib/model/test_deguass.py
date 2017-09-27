
import sys,os
import time
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
os.environ["EPICS_CA_SERVER_PORT"]="6000"

sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\stagetim\\')


import VELA_CLARA_MagnetControl as mag

magInit = mag.init()

magnets = magInit.virtual_VELA_INJ_Magnet_Controller()

magnets.switchONpsu('QUAD01')
#magnets.setSI('QUAD01',0.3)
ah = mag.std_vector_string()
ah.extend(['QUAD01'])#
magnets.degauss(ah,True)
while magnets.isDegaussing('QUAD01'):
	time.sleep(5)
	print 'waiting...'
magnets.switchOFFpsu('QUAD01')
