from paramiko import *
import itertools
from cycler import cycler
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import shutil
from copy import deepcopy
from paramiko import *
import subprocess

sys.path.append(os.path.join(os.path.dirname(os.getcwd()), 'catapillar-build', 'PythonInterface', 'Release'))
from CATAP.HardwareFactory import *
from CATAP.IMG import *


class Model(object):
    ip = '10.10.0.12'
    user = 'vmsim'
    password = 'password'

    def __init__(self, *args, **kwargs):
        object.__init__(self)
        self.my_name = 'model'

        self.client = SSHClient()
        self.state = STATE.VIRTUAL
        self.img_pressures = {}

    @property
    def img_pressures(self):
        return self.__img_pressures

    @property
    def state(self):
        return self.__state

    @img_pressures.setter
    def img_pressures(self, press_dict):
        self.__img_pressures = deepcopy(press_dict)

    @state.setter
    def state(self, state_new):
        if state_new == 'virtual':
            self.__state = STATE.VIRTUAL
        elif state_new == 'physical':
            self.__state = STATE.PHYSICAL
        else:
            self.__state = STATE.ERROR

    def setup_vm(self):
        subprocess.call('ping ' + self.ip)
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.connect(hostname=self.ip, username=self.user, password=self.password)
        stdin, stdout, stderr = self.client.exec_command('screen -ls')

    def get_img_pressures_from_img_factories(self):
        hw_factory = HardwareFactory(self.state)
        hw_factory.messagesOff()
        hw_factory.debugMessagesOff()
        img_factory = hw_factory.getIMGFactory()
        setattr(self, 'img_pressures', img_factory.getAllIMGPressure())

    def plotting_img_pressures(self, ax, time_pressure):
        color = [plt.cm.viridis(i) for i in  np.linspace(0, 1, len(self.img_pressures.keys()))]
        marker = itertools.cycle(('o', 's'))
        for i_key, (key,value) in enumerate(self.img_pressures.items()):
            ax.plot(time_pressure, float(value), \
                    linestyle='', marker=next(marker), color=color[i_key], \
                    label=key)
        return ax

