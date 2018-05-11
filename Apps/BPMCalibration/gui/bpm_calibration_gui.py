from PyQt4.QtGui import QMainWindow
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtCore import QString
from gui_mainwindow import Ui_MainWindow
import data.bpm_calibrate_data_base as dat
from pyqtgraph import mkPen
from base.base import base
import numpy as np
import pyqtgraph

class bpm_calibration_gui(QMainWindow, Ui_MainWindow, base):
	my_name = 'bpm_calibration_gui'
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
		self.setupUi(self)
		self.data = base.data
		self.append_pv_to_list()
		self.add_scope_name()
		# CONNECT BUTTONS TO FUNCTIONS
		self.calibrateButton.clicked.connect(self.handle_calibrate_button)
		self.attenuationButton.toggled.connect(lambda: self.handle_measure_type(self.attenuationButton))
		self.delayButton.toggled.connect(lambda: self.handle_measure_type(self.delayButton))
		# # widgets are held in dict, with same keys as data
		self.init_widget_dict(base.data)
		# # the clipboard has a string version of data
		self.clip_vals = base.data.values.copy()
		# # init to paused
		# update timer
		self.timer = QTimer()
		self.timer.timeout.connect(self.update_gui)
		self.timer.start(base.config.gui_config['GUI_UPDATE_TIME'])
        #
	# custom close function
	def closeEvent(self, event):
		self.closing.emit()

	def append_pv_to_list(self):
		self.comboBox.clear()
		self.pv_list = base.config.bpm_config['BPM_NAMES']
		for i in self.pv_list:
			self.comboBox.addItem((i))
		self.comboBox.update()

	def add_scope_name(self):
		self.bunchChargeOutputWidget.clear()
		self.scope_name = base.config.scope_config['SCOPE_NAME'][0]
		self.scope_channel = base.config.scope_config['SCOPE_CHANNEL']
		self.diag_type = base.config.scope_config['SCOPE_DIAG_TYPE']
		self.bunchChargeScopeLabel.setText(self.scope_name)
		self.bunchChargeChannelLabel.setText(str(self.scope_channel))
		self.bunchChargeDiagTypeLabel.setText(str(self.diag_type))

	def init_widget_dict(self, data):
		# MANUALLY CONNECT THESE UP :/
		# self.widget[dat.time_stamp] = self.time_stamp_outputwidget
		self.widget[dat.bunch_charge] = self.bunchChargeOutputWidget
		# self.widget[dat.set_sa_start] = self.lowerATTBoundOutputWidget
		# self.widget[dat.set_sa_end] = self.upperATTBoundOutputWidget
		# self.widget[dat.get_ra1] = self.get_ra1_outputwidget
		# self.widget[dat.get_ra2] = self.get_ra2_outputwidget
		# self.widget[dat.set_sa1_current] = self.set_sa1_current_outputwidget
		# self.widget[dat.set_sa2_current] = self.set_sa2_current_outputwidget
		# self.widget[dat.num_shots] = self.numShotsOutputWidget
		# self.widget[dat.bpm_u11] = self.bpm_u11_outputwidget
		# self.widget[dat.bpm_u12] = self.bpm_u12_outputwidget
		# self.widget[dat.bpm_u13] = self.bpm_u13_outputwidget
		# self.widget[dat.bpm_u13] = self.bpm_u13_outputwidget
		# self.widget[dat.bpm_u14] = self.bpm_u14_outputwidget
		# self.widget[dat.bpm_u21] = self.bpm_u21_outputwidget
		# self.widget[dat.bpm_u22] = self.bpm_u22_outputwidget
		# self.widget[dat.bpm_u23] = self.bpm_u23_outputwidget
		# self.widget[dat.bpm_u24] = self.bpm_u24_outputwidget
		# self.widget[dat.bpm_raw_data_mean_v11] = self.bpm_raw_data_mean_v11_outputwidget
		# self.widget[dat.bpm_raw_data_mean_v12] = self.bpm_raw_data_mean_v12_outputwidget
		# self.widget[dat.bpm_raw_data_mean_v21] = self.bpm_raw_data_mean_v21_outputwidget
		# self.widget[dat.bpm_raw_data_mean_v22] = self.bpm_raw_data_mean_v22_outputwidget
		# self.widget[dat.bpm_v11_v12_sum] = self.bpm_v11_v12_sum_outputwidget
		# self.widget[dat.bpm_v21_v22_sum] = self.bpm_v21_v22_sum_outputwidget
		# self.widget[dat.att_1_cal] = self.att_1_cal_outputwidget
		# self.widget[dat.att_2_cal] = self.att_2_cal_outputwidget
		# self.widget[dat.v_1_cal] = self.v_1_cal_outputwidget
		# self.widget[dat.v_2_cal] = self.v_2_cal_outputwidget
		# self.widget[dat.q_cal] = self.q_cal_outputwidget

	def update_gui(self):
		for key, val in self.widget.iteritems():
			if self.value_is_new(key, base.data.values[key]):
				self.update_widget(key, base.data.values[key], val)
		if self.data.values[dat.plots_done] and not self.data.values[dat.values_saved]:
			if self.data.values[dat.calibration_type] == 'attenuation':
				base.logger.message("BPM name " + str(self.data.values[dat.bpm_name]), True)
				base.logger.message("ATT1 Cal = " + str(self.data.values[dat.att_1_cal]), True)
				base.logger.message("ATT2 Cal = " + str(self.data.values[dat.att_2_cal]), True)
				base.logger.message("V1 Cal = " + str(self.data.values[dat.v_1_cal]), True)
				base.logger.message("V2 Cal = " + str(self.data.values[dat.v_2_cal]), True)
				base.logger.message("Q Cal = " + str(self.data.values[dat.q_cal]), True)
				self.newVals.setText("")
				self.newVals.setText("BPM name " + str(self.data.values[dat.bpm_name]) + "\n" +
										"ATT1 Cal = " + str(self.data.values[dat.att_1_cal]) + "\n" +
										"ATT2 Cal = " + str(self.data.values[dat.att_2_cal]) + "\n" +
										"V1 Cal = " + str(self.data.values[dat.v_1_cal]) + "\n" +
										"V2 Cal = " + str(self.data.values[dat.v_2_cal]) + "\n" +
										"Q Cal = " + str(self.data.values[dat.q_cal]))
			elif self.data.values[dat.calibration_type] == 'delay':
				base.logger.message("BPM name " + str(self.data.values[dat.bpm_name]), True)
				base.logger.message("New DLY1 = " + str(self.data.values[dat.new_dly_1]), True)
				base.logger.message("New DLY2 = " + str(self.data.values[dat.new_dly_2]), True)
				self.newVals.setText("")
				self.newVals.setText("BPM name " + str(self.data.values[dat.bpm_name]) + "\n" +
										"New DLY1 = " + str(self.data.values[dat.new_dly_1]) + "\n" +
										"New DLY2 = " + str(self.data.values[dat.new_dly_2]))
			self.data.values[dat.values_saved] = True
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

	# if a value is new we update the widget
	def value_is_new(self, key, val):
		if self.previous_values[key] != val:
			self.previous_values[key] = val
			return True
		else:
			return False

	def get_bpm_name(self):
		self.bpm_names_length = [self.comboBox.itemText(i) for i in range(self.comboBox.count())]
		if len(self.bpm_names_length) > 0:
			self.data.values[dat.bpm_name] = str(self.comboBox.currentText())
			self.bpm_name_set = True
			print self.data.values[dat.bpm_name]
			return True
		else:
			return False

	def get_start(self):
		self.set_start_text = self.lowerBoundOutputWidget.toPlainText()
		if len(self.set_start_text) > 0:
			self.data.values[dat.set_start] = long(self.set_start_text)
			self.set_start_set = True
			return True
		else:
			self.set_start_set = False
			return False

	def get_end(self):
		self.set_end_text = self.upperBoundOutputWidget.toPlainText()
		if len(self.set_end_text) > 0:
			self.data.values[dat.set_end] = long(self.set_end_text) + 1
			self.set_end_set = True
			return True
		else:
			self.set_end_set = False
			return False

	def get_num_shots(self):
		self.num_shots_text = self.numShotsOutputWidget.toPlainText()
		if len(self.num_shots_text) > 0:
			self.data.values[dat.num_shots] = int(self.num_shots_text)
			self.num_shots_set = True
			return True
		else:
			self.num_shots_set = False
			return False

	def is_measure_type_set(self):
		if self.data.values[dat.calibration_type] == 'attenuation':
			return True
		elif self.data.values[dat.calibration_type] == 'delay':
			return True
		else:
			return False

	def check_ready(self):
		if self.get_bpm_name() and self.get_start() and self.get_end() and self.get_num_shots() and self.is_measure_type_set():
			self.data.values[dat.all_values_set] = True
			if self.data.values[dat.scope_monitoring]:
				self.data.values[dat.ready_to_go] = True

	# button functions
	def handle_calibrate_button(self):
		self.check_ready()
		self.data.values[dat.values_saved] = False
		if self.data.values[dat.ready_to_go]:
			self.calibrateButton.setEnabled(False)
			base.logger.message('Starting scan', True)
		else:
			base.logger.message('NOT ready to go, is everything set?', True)

	def handle_measure_type(self, b):
		if b.text() == "Attenuation":
			if b.isChecked() == True:
				self.lowerBoundOutputWidget.setPlainText("2")
				self.upperBoundOutputWidget.setPlainText("20")
				self.data.values[dat.calibration_type] = 'attenuation'
		elif b.text() == "Delay":
			if b.isChecked() == True:
				self.lowerBoundOutputWidget.setPlainText("1")
				self.upperBoundOutputWidget.setPlainText("255")
				self.data.values[dat.calibration_type] = 'delay'

	def plot_bpm_vs_sa(self):
		self.bpmxPlot.clear()
		self.bpmyPlot.clear()
		self.vbx = self.bpmxPlot.vb
		self.vbx.setYRange(min(self.data.values[dat.bpm_v11_v12_sum].values()),max(self.data.values[dat.bpm_v11_v12_sum].values()))
		self.xplot = self.bpmxPlot.plot(pen=mkPen('b',width=3), symbol='o')
		self.xplot.setData(range(self.data.values[dat.set_start],self.data.values[dat.set_end]),
						   self.data.values[dat.bpm_v11_v12_sum].values())
		self.vby = self.bpmyPlot.vb
		self.vby.setYRange(min(self.data.values[dat.bpm_v21_v22_sum].values()),max(self.data.values[dat.bpm_v21_v22_sum].values()))
		self.yplot = self.bpmyPlot.plot(pen=mkPen('b', width=3), symbol='o')
		self.yplot.setData(range(self.data.values[dat.set_start], self.data.values[dat.set_end]),
						   self.data.values[dat.bpm_v21_v22_sum].values())
		self.data.values[dat.plots_done] = True

	def plot_bpm_vs_sd(self):
		self.bpmxPlot.clear()
		self.bpmyPlot.clear()
		self.vbx = self.bpmxPlot.vb
		self.vbx.setYRange(min(self.data.values[dat.dv1_dly1].values()),max(self.data.values[dat.dv1_dly1].values()))
		self.xplot = self.bpmxPlot.plot(pen=mkPen('b',width=3), symbol='o')
		self.xplot.setData(range(self.data.values[dat.set_start],self.data.values[dat.set_end]),
						   self.data.values[dat.dv1_dly1].values())
		self.xplot.setData(range(self.data.values[dat.set_start], self.data.values[dat.set_end]),
						   self.data.values[dat.dv2_dly1].values())
		self.vby = self.bpmyPlot.vb
		self.vby.setYRange(min(self.data.values[dat.dv1_dly2].values()),max(self.data.values[dat.dv1_dly2].values()))
		self.yplot = self.bpmyPlot.plot(pen=mkPen('b', width=3), symbol='o')
		self.yplot.setData(range(self.data.values[dat.new_dly_1] - 20, self.data.values[dat.new_dly_1] + 20),
						   self.data.values[dat.dv1_dly2].values())
		# self.yplot.setData(range(self.data.values[dat.new_dly_1] - 20, self.data.values[dat.new_dly_1] + 20),
		# 				   self.data.values[dat.dv2_dly2].values())
		self.data.values[dat.plots_done] = True