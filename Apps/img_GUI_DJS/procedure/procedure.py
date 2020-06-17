import os.path
import sys

# CHANGE TO YOUR PATH
catap_path = os.path.join('C:\\Users', 'djs56', 'GitHub', 'CATAP','caterpillar-build',
                          'PythonInterface','Release')
sys.path.append(catap_path)

from CATAP.HardwareFactory import *

class procedure(object):
    # init HWC
    hw_factory = HardwareFactory(STATE.VIRTUAL)
    hw_factory.messagesOff()
    hw_factory.debugMessagesOff()
    img_factory = hw_factory.getIMGFactory()



    # get names
    img_names = img_factory.getAllIMGNames()

    print(img_names)

    # empty dict to store latest state in
    img_values = {}

    for name in img_names:
        img_values[name] = img_factory.getIMGPressure(name)  # print(name + '
        # pres = ' + str(procedure.img_values[name]))

    def __init__(self):
        self.my_name = 'procedure'
        print(self.my_name + ', class initiliazed')

    # called external to update states
    def update_states(self):
        for name in procedure.img_names:
            procedure.img_values[name] = procedure.img_factory.getIMGPressure(name)
            print(name + ' pres = ' + str(procedure.img_values[name]))

