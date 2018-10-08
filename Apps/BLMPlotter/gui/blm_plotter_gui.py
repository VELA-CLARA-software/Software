from PyQt4.QtGui import QMainWindow
from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtCore import QString
from gui_mainwindow import Ui_MainWindow
import data.blm_plotter_data_base as dat
from pyqtgraph import mkPen
from base.base import base
import numpy as np
import pyqtgraph

class blm_plotter_gui(QMainWindow, Ui_MainWindow, base):
	my_name = 'blm_plotter_gui'
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
		# self.append_pv_to_list()
		self.add_charge_name()
		# CONNECT BUTTONS TO FUNCTIONS
		self.saveDataButton.clicked.connect(self.handle_save_data)
		self.setNumShotsButton.clicked.connect(self.set_num_shots)
		# self.attenuationButton.toggled.connect(lambda: self.handle_measure_type(self.attenuationButton))
		# self.delayButton.toggled.connect(lambda: self.handle_measure_type(self.delayButton))
		# # widgets are held in dict, with same keys as data
		self.init_widget_dict(base.data)
		# # the clipboard has a string version of data
		self.clip_vals = base.data.values.copy()
		# # init to paused
		# update timer
		self.timer = QTimer()
		self.timer.timeout.connect(self.update_gui)
		self.timer.start(100)
        #
	# custom close function
	def closeEvent(self, event):
		self.closing.emit()

	# def append_pv_to_list(self):
	# 	self.comboBox.clear()
	# 	self.pv_list = base.config.blm_config['BLM_NAMES']
	# 	for i in self.pv_list:
	# 		self.comboBox.addItem((i))
	# 	self.comboBox.update()

	def add_charge_name(self):
		self.bunchChargeOutputWidget.clear()
		self.diag_type = base.config.charge_config['CHARGE_NAME']
		self.bunchChargeDiagTypeLabel.setText(str(self.diag_type))

	def handle_save_data(self):
		if self.data.values[dat.save_request] == False:
			self.data.values[dat.save_request] = True
			base.logger.message('Saving data...', True)
		else:
			base.logger.message('NOT ready to go, is everything set?', True)
			self.messageLabel.setText('WARNING: NOT ready to go, is everything set?')

	def set_num_shots(self):
		self.data.values[dat.num_shots_request] = True
		self.data.values[dat.num_shots] = int(self.numShotsOutputWidget.toPlainText())

	def init_widget_dict(self, data):
		if self.data.values[dat.save_request] == False:
			self.saveDataButton.setEnabled(True)
		# MANUALLY CONNECT THESE UP :/
		# self.widget[dat.time_stamp] = self.time_stamp_outputwidget
		self.widget[dat.bunch_charge] = self.bunchChargeOutputWidget
		# self.widget[dat.set_sa_start] = self.lowerATTBoundOutputWidget
		# self.widget[dat.set_sa_end] = self.upperATTBoundOutputWidget
		# self.widget[dat.get_ra1] = self.get_ra1_outputwidget
		# self.widget[dat.get_ra2] = self.get_ra2_outputwidget
		# self.widget[dat.set_sa1_current] = self.set_sa1_current_outputwidget
		# self.widget[dat.set_sa2_current] = self.set_sa2_current_outputwidget
		self.widget[dat.num_shots] = self.numShotsOutputWidget
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
	# 	if self.data.values[dat.plots_done] and not self.data.values[dat.values_saved]:
	# 		if self.data.values[dat.calibration_type] == 'attenuation':
	# 			base.logger.message("BPM name " + str(self.data.values[dat.bpm_name]), True)
	# 			base.logger.message("ATT1 Cal = " + str(self.data.values[dat.att_1_cal]), True)
	# 			base.logger.message("ATT2 Cal = " + str(self.data.values[dat.att_2_cal]), True)
	# 			base.logger.message("V1 Cal = " + str(self.data.values[dat.v_1_cal]), True)
	# 			base.logger.message("V2 Cal = " + str(self.data.values[dat.v_2_cal]), True)
	# 			base.logger.message("Q Cal = " + str(self.data.values[dat.q_cal]), True)
	# 			self.newVals.setText("")
	# 			self.newVals.setText("BPM name " + str(self.data.values[dat.bpm_name]) + "\n" +
	# 									"ATT1 Cal = " + str(self.data.values[dat.att_1_cal]) + "\n" +
	# 									"ATT2 Cal = " + str(self.data.values[dat.att_2_cal]) + "\n" +
	# 									"V1 Cal = " + str(self.data.values[dat.v_1_cal]) + "\n" +
	# 									"V2 Cal = " + str(self.data.values[dat.v_2_cal]) + "\n" +
	# 									"Q Cal = " + str(self.data.values[dat.q_cal]))
	# 		elif self.data.values[dat.calibration_type] == 'delay':
	# 			base.logger.message("BPM name " + str(self.data.values[dat.bpm_name]), True)
	# 			base.logger.message("New DLY1 = " + str(self.data.values[dat.new_dly_1]), True)
	# 			base.logger.message("New DLY2 = " + str(self.data.values[dat.new_dly_2]), True)
	# 			self.newVals.setText("")
	# 			self.newVals.setText("BPM name " + str(self.data.values[dat.bpm_name]) + "\n" +
	# 									"New DLY1 = " + str(self.data.values[dat.new_dly_1]) + "\n" +
	# 									"New DLY2 = " + str(self.data.values[dat.new_dly_2]))
	# 		self.data.values[dat.values_saved] = True
	# 		self.calibrateButton.setEnabled(True)

	# the outputwidget is update based on data type
	def update_widget(self, key, val, widget):
		if type(val) is long:
			widget.setText('%i' % val)
			self.clip_vals[key] = widget.text()
		elif type(val) is int:
			widget.setPlainText('%i' % val)
			self.clip_vals[key] = widget.toPlainText()
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

	def plot_blm_values(self):
		self.blmPlot.clear()
		self.pen_vals = ['b','r','y','g']
		self.vbx = self.blmPlot.vb
		self.min_vals = []
		self.max_vals = []
		self.j = 0
		for i in self.data.values[dat.blm_waveform_pvs]:
			self.min_vals.append(min(self.data.values[dat.blm_voltages][str(i)]))
			self.max_vals.append(max(self.data.values[dat.blm_voltages][str(i)]))
		for i, k in zip(self.data.values[dat.blm_waveform_pvs],self.data.values[dat.blm_time_pvs]):
			self.vbx.setYRange(min(self.min_vals),max(self.max_vals))
			self.blmplot = self.blmPlot.plot(pen=mkPen(self.pen_vals[self.j],width=1))
			# self.blmplot = self.blmPlot.plot()
			self.blmplot.setData(self.data.values[dat.blm_num_values],
							   self.data.values[dat.blm_voltages][str(i)])
			self.j = self.j+1
		self.data.values[dat.plots_done] = True