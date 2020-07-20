from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import collections
import time
import matplotlib
import sys
import os
import datetime

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
sys.path.append(os.path.join(os.getcwd(), '..', '..', '..',
                             'catapillar-build', 'PythonInterface', 'Release'))
from CATAP.HardwareFactory import *


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=120):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        self.axes.grid('on', color=[0, 0, 1])
        self.axes.set_xlabel('Time (s)', fontsize=13, color=[0, 0, 1])
        self.axes.set_ylabel('Pressure', fontsize=13, color=[0, 0, 1])
        self.axes.tick_params(which='both', colors=[0, 0, 1], labelcolor=[0, 0, 1])


class FixFigureCanvas(MplCanvas):
    def resizeEvent(self, event):
        if event.size().width() <= 0 or event.size().height() <= 0:
            return
        super(FixFigureCanvas, self).resizeEvent(event)


class GenericThread(QThread):
    signal = pyqtSignal()
    timeElapsed = pyqtSignal()

    def __init__(self, function, *args, **kwargs):
        QThread.__init__(self)
        self._stopped = pyqtSignal()
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.iterations = 50
        self.iterations_before = 0

    def __del__(self):
        self.wait()

    def stop(self):
        self.finished.emit()

    def run(self):
        while self.iterations > 0:
            time.sleep(0.15)
            self.iterations_before = self.iterations
            self.signal.emit()
            self.object = self.function(*self.args, **self.kwargs)
            self.iterations -= 1


class ControllerRun(QObject):

    def __init__(self, app, view, model, *args, **kwargs):
        super(ControllerRun, self).__init__()
        self.my_name = 'ControllerRun'
        self.app = app
        self.model = model
        self.view = view
        self.canvas = FixFigureCanvas(self, width=5, height=4, dpi=100)
        self.time = time.time()
        self.timer = QTimer()

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
                    elif isinstance(widget, QLabel) and (widget.text().find('EBT-INJ-VAC-IMG-') != -1):
                        self.imgs_pvs.append(widget.text())
                    elif isinstance(widget, QCheckBox):
                        self.state_checkbox.append(widget)
                else:
                    pass
        [self.imgs_tot.update({key: value}) for key, value in zip(self.imgs_pvs, self.imgs_qlcd)]

    def filling_in_lcd_boxes_with_pressures(self):
        for keys, lcd in self.imgs_tot.items():
            lcd.display(self.model.img_pressures[keys])

    def disable_run_button(self):
        self.view.IMGpushButton.setEnabled(False)
        self.view.IMGpushButton.clicked.disconnect()

    def enable_run_button(self):
        self.view.IMGpushButton.setEnabled(True)
        self.view.IMGpushButton.clicked.connect(self.run_app)

    def plot_pressures(self, time_pressure):
        self.canvas.axes = self.model.plotting_img_pressures(self.canvas.axes, time_pressure, self.thread.iterations)

    def set_plot_to_scene(self):
        self.toolbar = NavigationToolbar(self.canvas, self.view.tabWidget)
        self.view.PlotLayoutWidget.addWidget(self.toolbar)
        self.view.PlotLayoutWidget.addWidget(self.canvas)
        if self.thread.iterations > 1:
            self.canvas.draw()
        elif self.thread.iterations == 1:
            self.canvas.print_png(os.path.join(os.getcwd(), 'IMGs_Pressure_' +
                                               datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.png'),
                                  dpi=120)
            self.canvas.draw()

    def plotting_sequence(self, time_pressure):
        self.plot_pressures(time_pressure)
        self.set_plot_to_scene()

    def vm_setup_and_getting_pressure(self):
        self.model.setup_vm()
        self.model.get_img_pressures_from_img_factories()
        self.filling_in_lcd_boxes_with_pressures()
        self.plotting_sequence(float(time.time() - self.time))

    def app_sequence(self):
        if self.state_checkbox[-1].isChecked():
            self.model.hw_factory = HardwareFactory(STATE.VIRTUAL)
        else:
            self.model.hw_factory = HardwareFactory(STATE.PHYSICAL)
        self.model.hw_factory.messagesOff()
        self.model.hw_factory.debugMessagesOff()
        self.model.img_factory = self.model.hw_factory.getIMGFactory()
        self.thread = GenericThread(self.vm_setup_and_getting_pressure)
        self.thread.finished.connect(self.enable_run_button)
        self.thread.start()

    def run_app(self):
        self.app_sequence()
