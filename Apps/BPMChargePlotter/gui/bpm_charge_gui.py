from PyQt4.QtGui import QMainWindow
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtCore import QString
from pyqtgraph import BarGraphItem, plot
from gui_mainwindow import Ui_MainWindow
import data.bpm_charge_plotter_data_base as dat
from pyqtgraph import mkPen
from base.base import base
from random import randint
import numpy as np
import pyqtgraph

class bpm_charge_plotter_gui(QMainWindow, Ui_MainWindow, base):
	my_name = 'bpm_charge_plotter_gui'
	# clipboard
	clip_app = QApplication([])
	clip = clip_app.clipboard()
	# global state
	can_ramp = True
	bpm_name_set = False
	set_sa_start_set = False
	set_sa_end_set = False
	num_shots_set = False
	# constant colors
	good = open = trig = 'green'
	bad = error = closed = 'red'
	err = 'orange'
	unknown = 'magenta'
	major_error = 'cyan'
	timing = 'yellow'

	# custom close signal to send to controller
	closing = pyqtSignal()
	#
	update_via_controller = {}
	# [update_via_controller.update({x: False}) for x in dat.all_value_keys]
	widget = {}
	previous_values = {}
	[previous_values.update({x: None}) for x in dat.all_value_keys]

	#

	def __init__(self,
				 window_name="",
				 root="/"
				 ):
		QMainWindow.__init__(self)
		super(base, self).__init__()
		self.numBPMs = self.data.values[dat.num_bpms]
		self.setupUi(self, self.numBPMs)
		self.data = base.data
		# CONNECT BUTTONS TO FUNCTIONS
		self.calibrateButton.clicked.connect(self.handle_recalibrate_button)
		self.clip_vals = base.data.values.copy()
		self.timer = QTimer()
		self.timer.timeout.connect(self.update_gui)
		self.timer.start(base.config.gui_config['GUI_UPDATE_TIME'])
		self.xlab = self.data.values[dat.bpm_names]
		print self.xlab
		self.xdict = [list(zip(range(len(self.xlab)), (self.xlab)))]
		self.bpmChargePlotxax = self.bpmChargePlot.getAxis('bottom')
		self.bpmChargePlotxax.setTicks(self.xdict)
		self.data.values[dat.ready_to_go] = True
        #
	# custom close function
	def closeEvent(self, event):
		self.closing.emit()

	def update_gui(self):
		self.bpmChargeBarGraph.setOpts(height=np.random.randint(1,10,size=len(self.data.values[dat.bpm_names])))
		self.wcmChargeBarGraph.setOpts(height=self.data.values[dat.bunch_charge])
		self.calibrateButton.setEnabled(True)

	# the outputwidget is update based on data type
	def update_widget(self, key, val, widget):
		if type(val) is long:
			widget.setText('%i' % val)
			self.clip_vals[key] = widget.text()
		elif type(val) is int:
			widget.setText('%i' % val)
			self.clip_vals[key] = widget.text()
		elif type(val) is float:
			widget.setText('%.3E' % val)
			self.clip_vals[key] = widget.text()
		elif type(val) is bool:
			self.set_locked_enabled(widget, val, key)
		elif type(val) is np.float64:
			widget.setText('%.3E' % val)
			self.clip_vals[key] = widget.text()
		elif type(val) is str:
			widget.setText('%i' % -1)
		else:
			print 'update_widget error ' + str(val) + ' ' + str(type(val))

	def check_ready(self):
		self.data.values[dat.ready_to_go] = True

	# button functions
	def handle_recalibrate_button(self):
		self.check_ready()
		self.data.values[dat.recalibrate_go] = True
		if self.data.values[dat.ready_to_go]:
			self.calibrateButton.setEnabled(False)
			self.data.values[dat.plots_done] = False
			base.logger.message('Starting scan', True)
			self.messageLabel.setText('Starting scan')
		else:
			base.logger.message('NOT ready to go, is everything set?', True)
			self.messageLabel.setText('WARNING: NOT ready to go, is everything set?')