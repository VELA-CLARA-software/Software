from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal
from gui.gui_mainwindow import Ui_MainWindow
import data.charge_measurement_data_base as dat
from base.base import base
import numpy

class charge_measurement_gui(QMainWindow, Ui_MainWindow, base):
	my_name = 'charge_measurement_gui'
	# clipboard
	clip_app = QApplication([])
	clip = clip_app.clipboard()
	# global state
	pil_name_set = False
	vc_acquire_set = False
	set_ophir_start_set = False
	set_ophir_end_set = False
	set_ophir_step_set = False
	num_shots_set = False
	num_steps_set = False
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
	# [previous_values.update({x: None}) for x in dat.all_value_keys]

	#

	def __init__(self,
				 window_name="",
				 root="/"
				 ):
		QMainWindow.__init__(self)
		super(base, self).__init__()
		self.setupUi(self)
		# self.data = base.data
#		self.add_charge_name()
		# CONNECT BUTTONS TO FUNCTIONS
		self.scanButton.clicked.connect(self.handle_scan_button)
		self.saveButton.clicked.connect(self.handle_save_button)
		# # widgets are held in dict, with same keys as data
		self.init_widget_dict(base.data)
		# # the clipboard has a string version of data
		self.clip_vals = base.data.values.copy()
		self.defaults_start = True
		self.defaults_end = True
		self.get_start()
		self.get_end()
		self.data.values[dat.progress_bar]['scan_progress'] = self.progressBar
		# # init to paused
		# update timer
		# self.timer = QTimer()
		# self.timer.timeout.connect(self.update_gui)
		# self.timer.start(base.config.gui_config['GUI_UPDATE_TIME'])
        #
	# custom close function
	def closeEvent(self, event):
		self.closing.emit()

	def add_charge_name(self):
		self.bunchChargeOutputWidget.clear()
		self.charge_name = base.config.las_hwp_config['CHARGE_NAME'][0]
		self.diag_type = base.config.las_hwp_config['CHARGE_DIAG_TYPE']
		self.bunchChargeDiagTypeLabel.setText(str(self.diag_type))

	def init_widget_dict(self, data):
		# MANUALLY CONNECT THESE UP :/
		# self.widget[dat.time_stamp] = self.time_stamp_outputwidget
		self.widget[dat.bunch_charge] = self.bunchChargeOutputWidget

	def update_gui(self):
		for key, val in self.widget.items():
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
		elif type(val) is numpy.float64:
			widget.setText('%.3E' % val)
			self.clip_vals[key] = widget.text()
		elif type(val) is str:
			widget.setText('%i' % -1)
		else:
			print('update_widget error ' + str(val) + ' ' + str(type(val)))

	# if a value is new we update the widget
	def value_is_new(self, key, val):
		pass
		# if self.previous_values[key] != val:
		# 	self.previous_values[key] = val
		# 	return True
		# else:
		# 	return False

	def get_bpm_name(self):
		self.bpm_names_length = [self.comboBox.itemText(i) for i in range(self.comboBox.count())]
		if len(self.bpm_names_length) > 0:
			self.data.values[dat.bpm_name] = str(self.comboBox.currentText())
			self.bpm_name_set = True
			print(self.data.values[dat.bpm_name])
			return True
		else:
			return False

	def get_start(self):
		if self.defaults_start:
			self.set_start_text = base.config.las_hwp_config['LAS_HWP_START']
			self.lowerBoundOutputWidget.setProperty("value", float(self.set_start_text))
			self.defaults_start = False
		else:
			self.set_start_text = self.lowerBoundOutputWidget.value()
		self.data.values[dat.set_hwp_start] = float(self.set_start_text)
		self.set_start_set = True
		return True

	def get_end(self):
		if self.defaults_end:
			self.set_end_text = base.config.las_hwp_config['LAS_HWP_END']
			self.upperBoundOutputWidget.setProperty("value", float(self.set_end_text))
			self.defaults_end = False
		else:
			self.set_end_text = self.upperBoundOutputWidget.value()
		self.data.values[dat.set_hwp_end] = float(self.set_end_text)
		self.set_end_set = True
		return True

	def get_num_steps(self):
		self.num_steps_text = self.numStepsOutputWidget.value()
		self.data.values[dat.num_steps] = int(self.num_steps_text)
		self.num_steps_set = True
		return True

	def get_num_shots(self):
		self.num_shots_text = self.numShotsOutputWidget.value()
		self.data.values[dat.num_shots] = int(self.num_shots_text)
		self.num_shots_set = True
		return True

	def get_off_crest_phase(self):
		self.off_crest_phase_text = self.offCrestPhaseOutputWidget.value()
		self.data.values[dat.off_crest_phase] = int(self.off_crest_phase_text)
		self.off_crest_phase_set = True
		return True

	def get_comments(self):
		self.comments_text = self.newVals.toPlainText()
		print(self.comments_text)
		self.data.values[dat.comments] = str(self.comments_text)
		self.comments_set = True
		return True

	def is_measure_type_set(self):
		if self.data.values[dat.calibration_type] == 'attenuation':
			return True
		elif self.data.values[dat.calibration_type] == 'delay':
			return True
		else:
			return False

	def check_ready(self):
		if self.get_start() and self.get_end() and self.get_num_shots() and self.get_num_steps() and self.get_off_crest_phase() and self.get_comments():
		# 	base.logger.message('Starting scan', True)
		# 	self.data.values[dat.all_values_set] = True
		# 	self.data.values[dat.charge_status] = True
		# 	if self.data.values[dat.charge_status]:
			self.data.values[dat.ready_to_go] = True
			self.newVals.setDisabled(True)
			self.plotCanvas.axes.cla()
			self.defaults_start = False
			self.defaults_end = False

	# button functions
	def handle_scan_button(self):
		self.check_ready()
		self.progressBar.setValue(0)
		self.data.values[dat.values_saved] = False
		if self.data.values[dat.ready_to_go]:
			self.scanButton.setText("Cancel")
			self.data.values[dat.plots_done] = False
			self.messageLabel.setText('Starting scan')
			self.resultsLabel.setText("")
			base.logger.message('Starting scan', True)
		elif self.data.values[dat.scan_status] == 'scanning':
			self.data.values[dat.cancel] = True
			self.scanButton.setText("Scan laser attenuator")
			self.plot.clear()
		else:
			base.logger.message('NOT ready to go, is everything set?', True)
			self.messageLabel.setText('WARNING: NOT ready to go, is everything set?')

	def handle_save_button(self):
		if self.data.values[dat.scan_status] == "complete":
			self.data.values[dat.save_clicked] = True
			self.messageLabel.setText('Data saved')
			self.saveButton.setEnabled(False)
		else:
			self.messageLabel.setText("WARNING: SCAN not done!!!!")

	def set_results_label(self):
		pass
		# self.fitlabel = ["fit = " + str(self.data.values[dat.fit]) + "pC/uJ + " + str(
		# 	self.data.values[dat.cross]) + "\n QE = " + str(
		# 	self.data.values[dat.qe]) + " E-05"]
		# self.plotCanvas.axes.legend([['data'], self.fitlabel], loc='upper left')
		# self.plotCanvas.draw()

	def plot_fit(self):
		# self.plotCanvas.axes.cla()  # Clear the canvas.
		# self.plotCanvas.axes.set_title('wcm vs laser energy')
		# self.plotCanvas.axes.set_xlabel('laser energy (uJ)')
		# self.plotCanvas.axes.set_ylabel('bunch charge (pC)')
		# self.plotCanvas.axes.grid()
		# self.plotCanvas.axes.set_xlim(
		# 	[min(self.data.values[dat.ophir_mean]) - 0.02, max(self.data.values[dat.ophir_mean]) + 0.02])
		# self.plotCanvas.axes.set_ylim(
		# 	[min(self.data.values[dat.charge_mean]) - 10, max(self.data.values[dat.charge_mean]) + 10])
		# self.plotCanvas.axes.errorbar(self.data.values[dat.ophir_mean], self.data.values[dat.charge_mean],
		# 							  xerr=self.data.values[dat.ophir_stderr],
		# 							  yerr=self.data.values[dat.charge_stderr], fmt='bo')
		self.fitted = [(x * self.data.values[dat.fit]) + self.data.values[dat.cross] for x in
					   list(self.data.values[dat.ophir_mean].values())]
		self.plotCanvas.axes.plot(list(self.data.values[dat.ophir_mean].values()), self.fitted, "r")
		self.plotCanvas.axes.set_title(
			"fit = " + str(self.data.values[dat.fit]) + "pC/uJ + " + str(
				self.data.values[dat.cross]) + "\n QE = " + str(
				self.data.values[dat.qe] * 10**5) + " E-05")
		self.plotCanvas.draw()

	def update_plot(self, hwp=None):
		if not self.data.values[dat.plots_done]:
			self.messageLabel.setText('Scanning')
			self.ophirmean = []
			self.wcmmean = []
			self.ophirstderr = []
			self.wcmstderr = []
			self.plotdataitems = []
			self.plotCanvas.axes.cla()  # Clear the canvas.
			self.plotCanvas.axes.set_title('')
			self.plotCanvas.axes.set_xlabel('laser energy (uJ)')
			self.plotCanvas.axes.set_ylabel('bunch charge (pC)')
			self.plotCanvas.axes.set_xlim(
				[min(self.data.values[dat.ophir_mean].values()) - 0.02, max(self.data.values[dat.ophir_mean].values()) + 0.02])
			self.plotCanvas.axes.set_ylim(
				[min(self.data.values[dat.charge_mean].values()) - 10, max(self.data.values[dat.charge_mean].values()) + 10])
			self.plotCanvas.axes.errorbar(list(self.data.values[dat.ophir_mean].values()),
										  list(self.data.values[dat.charge_mean].values()),
										  xerr=list(self.data.values[dat.ophir_stderr].values()),
										  yerr=list(self.data.values[dat.charge_stderr].values()), fmt='bo')
			self.plotCanvas.axes.grid()
			# Trigger the canvas to update and redraw.
			self.plotCanvas.draw()