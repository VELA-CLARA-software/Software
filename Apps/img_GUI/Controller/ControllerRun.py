from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from copy import copy, deepcopy
import collections
import numpy as np
import time
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        self.axes.grid('on', color=[0,0,1])
        self.axes.set_xlabel('Time (s)', fontsize=13, color = [0,0,1])
        self.axes.set_ylabel('Pressure', fontsize=13, color =[0,0,1])
        self.axes.tick_params(which='both', colors=[0,0,1], labelcolor=[0,0,1])

    def legend_plotting(self):
        if self.axes.get_legend() is not None:
            leg = self.axes.legend(loc=9, handlelength=0, \
                                    bbox_to_anchor=(0.5, 1.4))
            for line, text in zip(leg.get_lines(), leg.get_texts()):
                text.set_color(line.get_color())


class GenericThread(QThread):
    signal = pyqtSignal()
    timeElapsed = pyqtSignal()

    def __init__(self, function, *args, **kwargs):
        QThread.__init__(self)
        self._stopped = pyqtSignal()
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.iterations = 100
        self.iterations_before = 0
        self.timerThread = TimerThread(self)

    def __del__(self):
        self.wait()

    def stop(self):
        self.finished.emit()

    def run(self):
        # self.signal.emit()
        # self.object = self.function(*self.args, **self.kwargs)
        self.timerThread.timeElapsed.connect(self.timeElapsed.emit)
        time_zero = time.time()
        self.timerThread.start(time_zero)

        while self.iterations:
            self.iterations_before = self.iterations
            self.signal.emit()
            self.object = self.function(*self.args, **self.kwargs)
            self.iterations -= 1


class TimerThread(QThread):
    timeElapsed = pyqtSignal(int)

    def __init__(self, parent=None):
        super(TimerThread, self).__init__(parent)
        self.timeStart = None

    def start(self, timeStart):
        self.timeStart = timeStart

        return super(TimerThread, self).start()

    def run(self):
        while self.parent().isRunning():
            self.timeElapsed.emit(time.time() - self.timeStart)
            time.sleep(1)


class ControllerRun(QObject):

    def __init__(self, app, view, model, *args, **kwargs):
        super(ControllerRun, self).__init__()
        self.my_name = 'ControllerRun'
        self.app = app
        self.model = model
        self.view = view
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.time = time.time()

        self.timer = QTimer()
        self.timer.start(1000)

        self.img_layout = [
            self.view.IMGButtonGridLayout,
            self.view.IMGPressuregridLayout
        ]
        self.imgs_qlcd = []
        self.imgs_pvs = []
        self.state_checkbox = []
        self.imgs_tot = collections.OrderedDict()
        for layout in self.img_layout:
            childCount = layout.count()
            for child in range(0, childCount):
                widget = layout.itemAt(child).widget()

                if widget is not None and widget.accessibleName() is not None:
                    if isinstance(widget, QLCDNumber):
                        self.imgs_qlcd.append(widget)
                    elif isinstance(widget, QLabel) and widget.text().startswith('EBT'):
                        self.imgs_pvs.append(widget.text())
                    elif isinstance(widget, QCheckBox):
                        self.state_checkbox.append(widget)
                else:
                    pass
        [self.imgs_tot.update({key: value}) for key, value in zip(self.imgs_pvs, self.imgs_qlcd)]

    def state_definition(self):
        if self.view.IMGVirtual_checkBox.isChecked():
            self.model.state = 'virtual'
        else:
            self.model.state = 'physical'

    def filling_in_lcd_boxes_with_pressures(self):
        for (keys, lcd) in self.imgs_tot.items():
            lcd.display(self.model.img_pressures[keys])

    def disable_run_button(self):
        self.view.IMGpushButton.setEnabled(False)
        self.view.IMGpushButton.clicked.disconnect()

    def enable_run_button(self):
        self.view.IMGpushButton.setEnabled(True)
        self.view.IMGpushButton.clicked.connect(self.run_app)

    def plot_pressures(self, time_pressure):
        self.canvas.axes = self.model.plotting_img_pressures(self.canvas.axes, time_pressure)
        self.canvas.legend_plotting()

        # toolbar = NavigationToolbar(sc, self)

    def set_plot_to_scene(self):
        toolbar = NavigationToolbar(self.canvas, self.view.tabWidget)
        self.view.PlotLayoutWidget.addWidget(toolbar)
        self.view.PlotLayoutWidget.addWidget(self.canvas)
        self.canvas.draw()

    def plotting_sequence(self, time_pressure):
        self.plot_pressures(time_pressure)
        self.set_plot_to_scene()

    def vm_setup_and_getting_pressure(self):
        self.state_definition()
        self.model.setup_vm()
        self.model.get_img_pressures_from_img_factories()
        print(self.model.img_pressures)
        self.filling_in_lcd_boxes_with_pressures()
        self.plotting_sequence(float(time.time()-self.time))

    def app_sequence(self):
        self.thread = GenericThread(self.vm_setup_and_getting_pressure)
        self.thread.finished.connect(self.enable_run_button)
        self.thread.start()

    def run_app(self):
        self.app_sequence()

    # def reset_progress_bar_timer(self):
    #    self.timer.setInterval(1000)
    #    self.timer.setSingleShot(True)
    #    self.timer.timeout.connect(self.view.progressBar.reset)
    #    self.timer.start()

    # TODO: Implement timer  to take data every n seconds and incorporate it into the app_sequence function
