

import sys,os

# the default are is Release, this can be overidden in the
# which version of the contorller does it load???
sys.path.append('\\\\fed.cclrc.ac.uk\\org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\Release\\')

import VELA_CLARA_BPM_Control as mag
import VELA_CLARA_MagnetControl as bpm
import VELA_CLARA_Vac_Valve_Control as val
import VELA_CLARA_Scope_Control as scope

class controllerManager()
    def __init__(self,argv):
        self.controllers[]
        self.setReleaseeArea()

    def setStageArea(self):
        sys.path.remove('\\\\fed.cclrc.ac.uk\\org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\Release\\')
        sys.path.append('\\\\fed.cclrc.ac.uk\\org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\stage\\')

    def setReleaseeArea(self):
        sys.path.append('\\\\fed.cclrc.ac.uk\\org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\Release\\')
        sys.path.remove('\\\\fed.cclrc.ac.uk\\org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\stage\\')

    def

    def setSIThenWait(self):
