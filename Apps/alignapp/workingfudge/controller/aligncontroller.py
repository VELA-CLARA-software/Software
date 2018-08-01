import sys, os
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\view')
from draftgui import draftappgui
from rfalign import gunrfaligner

#################
# OLD STUFF  start
#################

#get the magnet enums used to define magnet types and  PSU states
#We should probably create magnet module to make importing stuff easier
#sys.path.append('D:\\VELA\\GIT Projects\\VELA-CLARA-Controllers\\bin\\Release')

# magnet controllers path
#sys.path.append('\\\\fed.cclrc.ac.uk\\org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VM-Controllers\\VELA-CLARA'
#                '-Controllers\\bin\\Release\\')

# Import Python Module:        
#import VELA_CLARA_MagnetControl as mag

#dburtLocation = "\\\\fed.cclrc.ac.uk\\org\\NLab\\ASTeC\\Projects\\VELA\\Snapshots\\DBURT\\"
#appIcon = 'magpic.jpg'


# set EPICS variables  (change as needed)
# i.e you need to change depending on your virtual machine set up 
#os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
#os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
#os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"

#import VELA_CLARA_MagnetControl as mag

#from PyQt4 import QtGui, QtCore
#from draftgui import draftappgui 
#from GUI_magnetAppMainView import GUI_magnetAppMainView
#from GUI_FileLoad import GUI_FileLoad
#################
# OLD STUFF  end
#################

class alignAppController(object):
    def __init__(self,argv):
        # startup view
        print "alignAppController constructor"
        self.startView = draftappgui()
        self.startView.show()
        # create the actual magnet controller you want (VELA INJ magnets, can also have VELA BA1 magnets etc)
        # you need to have the virtual machine up and running for this to work properly
        #self.localMagnetController = self.magInit.virtual_VELA_INJ_Magnet_Controller() 
        self.mygunalign = gunrfaligner(argv)
        self.startView.dorfalign.clicked.connect(self.falign)
		
    def falign(self):
        print "falign function"
        self.setparams()
#        raw_input("ready to do scan? Press enter to continue")
        self.mygunalign.doscan()

    def setparams(self):
        self.mygunalign.setscangrid(self.startView.vcxminbox.value(),
                                    self.startView.vcmaxxbox.value(),
                                    self.startView.npxbox.value(),
                                    self.startView.vcminybox.value(),
                                    self.startView.vcmaxybox.value(),
                                    self.startView.npybox.value())
        self.mygunalign.setrfphases(self.startView.rfphi1box.value(),
                                    self.startView.rfphi2box.value())
        self.mygunalign.setsolval(self.startView.rfphi2box_4.value())
        self.mygunalign.printtheparams()
 