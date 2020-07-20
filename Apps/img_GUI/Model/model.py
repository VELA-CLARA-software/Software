import itertools
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from copy import deepcopy
from paramiko import *
import subprocess
from collections import OrderedDict
sys.path.append(os.path.join(os.getcwd(), '..', '..', '..',
                             'catapillar-build', 'PythonInterface', 'Release'))
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
        self.__state = ''
        self.__img_pressures = OrderedDict()

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
        self.__state = deepcopy(state_new)

    def setup_vm(self):
        subprocess.call('ping ' + self.ip)
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.connect(hostname=self.ip, username=self.user, password=self.password)
        stdin, stdout, stderr = self.client.exec_command('screen -ls')

    def get_img_pressures_from_img_factories(self):
        for img_name in self.img_factory.getAllIMGNames():
            img_object = self.img_factory.getIMG(img_name)
            self.img_pressures.update({img_name: img_object.getIMGPressure()})

    def plotting_img_pressures(self, ax, time_pressure, i_iteration):
        if ax.get_legend() is not None:
            ax.get_legend().remove()
        color = [plt.cm.winter(i) for i in np.linspace(0, 1, len(self.img_pressures.keys()))]
        marker = itertools.cycle(('o', 's'))
        if i_iteration > 1:
            for i_key, (key, value) in enumerate(self.img_pressures.items()):
                ax.plot(time_pressure, float(value),
                        linestyle='', marker=next(marker), color=color[i_key])
        elif i_iteration:
            for i_key, (key, value) in enumerate(self.img_pressures.items()):
                ax.plot(time_pressure, float(value),
                        linestyle='', marker=next(marker), color=color[i_key],
                        label=key[key.find('IMG-'):])
            leg = ax.legend(loc=0, handlelength=0, ncol=2,
                            bbox_to_anchor=(1.1, 1.0))
            print(leg.get_texts())
            for line, text in zip(leg.get_lines(), leg.get_texts()):
                text.set_color(line.get_color())
            leg.set_title('EBT-INJ-VAC-IMG')
        return ax
