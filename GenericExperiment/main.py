import sys

sys.path.append('\\\\fed.cclrc.ac.uk\\org\\NLab\\ASTeC\\Projects\\VELA\\Software\\OnlineModel')
sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\Release')

import master_controller as mc
import onlineModel

input_file = 'Instructions_machine'


T = mc.master_controller( )

T.read_procedure_file(input_file)

print 'Settign environmnet'

T.SetEnvironment()