from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import sys
import shutil
import multiprocessing
import numpy as np
from copy import copy, deepcopy
import collections
import numpy as np
from View import view
import time


class GenericThread(QThread):
    signal = pyqtSignal()

    def __init__(self, function, *args, **kwargs):
        QThread.__init__(self)
        self._stopped = False
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __del__(self):
        self.wait()

    def stop(self):
        self._stopped = True

    def run(self):
        self.signal.emit()
        if not self._stopped:
            self.object = self.function(*self.args, **self.kwargs)


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class ControllerPostProcessing(QObject):
    def __init__(self, app, view, model):
        super(ControllerPostProcessing, self).__init__()
        self.my_name = 'ControllerPostProcessing'
        self.app = app
        self.model = model
        self.view = view
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)

    def plot_pressures(self, time_pressure):
        self.canvas.axes = self.model.plotting_img_pressures(self.canvas.axes, time_pressure)
        # toolbar = NavigationToolbar(sc, self)

    def set_plot_to_scene(self):
        self.view.scene.add_widget(self.canvas)
        self.view.graphicsView.setScene(self.view.scene)

    def plotting_sequence(self, time_pressure):
        self.plot_pressure(time_pressure)
        self.set_plot_to_scene()

    def run_thread(self, time_pressure):
        self.thread = GenericThread(self.plotting_sequence(time_pressure))
        self.thread.start()


    # TODO: implementation of the routines to update the IMGs and plot them in the Scene Object
