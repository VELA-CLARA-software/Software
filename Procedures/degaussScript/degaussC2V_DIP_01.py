import sys

import time
sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\Release')

import VELA_CLARA_Magnet_Control as mag


magInit = mag.init()

magnets = magInit.physical_CLARA_PH1_Magnet_Controller()

deguassingList=['DIP01']
#else:
#    print('Magnet '+magnet+' is off or not selected to be deguassed.')
print('Magnet to be Deguassed: '+str(deguassingList))
activeMags = mag.std_vector_string()
activeMags.extend(deguassingList)
magnets.degauss(activeMags,True)

while magnets.isDegaussing('DIP01'):
    print 'Still deguassing...'
    print magnets.getRI('DIP01')
    time.sleep(0.5)
