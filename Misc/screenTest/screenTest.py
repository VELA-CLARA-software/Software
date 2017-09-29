import sys,os

counter = 0;
# THIS FILE SHOULD BE IN THE STAGE DIRECTORY
sys.path.append('\\\\fed.cclrc.ac.uk\\org\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\stage\\')


import VELA_CLARA_ScreenControl as scr
raw_input()


sc = scr.init()

#a  = vc.virtual_VELA_INJ_Magnet_Controller();

c  = scr.physical_VELA_Screen_Controller( );

c.Screen_Out("YAG-08")

raw_input()