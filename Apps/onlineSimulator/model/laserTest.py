
import sys,os
import time
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12" #BE SPECIFIC.... YOUR I.P. FOR YOUR VM
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
os.environ["EPICS_CA_SERVER_PORT"]="6000"
sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\stagetim')
sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\OnlineModel')


import onlineModel


import VELA_CLARA_PILaserControl as pil

pilInit = pil.init()

laser = pilInit.virtual_PILaser_Controller()
laser.setVpos(2)
laser.setHpos(3)
