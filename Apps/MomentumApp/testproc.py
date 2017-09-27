import sys,os
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12" #BE SPECIFIC.... YOUR I.P. FOR YOUR VM
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
from epics import caget,caput
from PyQt4 import QtGui, QtCore
import time
sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\stagetim')
import VELA_CLARA_MagnetControl as mag
from multiprocessing import Process, Pipe

class view():
    def __init__(self):
        self.pi = 'hmmmm tasty'

def ha(conn):
    while(True):
        v=conn.recv()
        print(v.pi)
    #magInit = mag.init()
    #magnets = magInit.virtual_VELA_INJ_Magnet_Controller()
    #magnets.setSI('DIP01',I,0.001,10)

if __name__ == '__main__':
    v=view()
    parent_conn, child_conn = Pipe()
    caput('VM-EBT-INJ-MAG-DIP-01:RIRAN', 0)

    p=Process(target=ha,args = (child_conn,))
    #parent_conn.send(v)
    p.start()

    for i in range(10):
        v.pi=i
        parent_conn.send(v)
    #parent_conn.close()
    '''while(True):
        print('KBJADIFLKABJDGLKBJSDG')
        time.sleep(1)'''
