# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rf_condition_view_base.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_rf_condition_mainWindow(object):
    def setupUi(self, rf_condition_mainWindow):
        rf_condition_mainWindow.setObjectName(_fromUtf8("rf_condition_mainWindow"))
        rf_condition_mainWindow.resize(1604, 818)
        self.centralwidget = QtGui.QWidget(rf_condition_mainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 20, 1581, 781))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.layoutWidget = QtGui.QWidget(self.tab_3)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 10, 1571, 511))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.message_pad = QtGui.QTextEdit(self.layoutWidget)
        self.message_pad.setMinimumSize(QtCore.QSize(400, 0))
        self.message_pad.setMaximumSize(QtCore.QSize(400, 16777215))
        self.message_pad.setObjectName(_fromUtf8("message_pad"))
        self.horizontalLayout.addWidget(self.message_pad)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.llrf_enable_button_3 = QtGui.QPushButton(self.layoutWidget)
        self.llrf_enable_button_3.setMinimumSize(QtCore.QSize(225, 0))
        self.llrf_enable_button_3.setMaximumSize(QtCore.QSize(16777215, 25))
        self.llrf_enable_button_3.setCheckable(False)
        self.llrf_enable_button_3.setObjectName(_fromUtf8("llrf_enable_button_3"))
        self.gridLayout.addWidget(self.llrf_enable_button_3, 2, 0, 1, 2)
        self.copy_to_clipboard_button_3 = QtGui.QPushButton(self.layoutWidget)
        self.copy_to_clipboard_button_3.setMinimumSize(QtCore.QSize(225, 0))
        self.copy_to_clipboard_button_3.setMaximumSize(QtCore.QSize(16777215, 25))
        self.copy_to_clipboard_button_3.setCheckable(False)
        self.copy_to_clipboard_button_3.setObjectName(_fromUtf8("copy_to_clipboard_button_3"))
        self.gridLayout.addWidget(self.copy_to_clipboard_button_3, 0, 0, 1, 2)
        self.start_pause_ramp_button_3 = QtGui.QPushButton(self.layoutWidget)
        self.start_pause_ramp_button_3.setMaximumSize(QtCore.QSize(16777215, 25))
        self.start_pause_ramp_button_3.setObjectName(_fromUtf8("start_pause_ramp_button_3"))
        self.gridLayout.addWidget(self.start_pause_ramp_button_3, 1, 0, 1, 2)
        self.breakdown_rate_limit_outputwidget = QtGui.QLabel(self.layoutWidget)
        self.breakdown_rate_limit_outputwidget.setFrameShape(QtGui.QFrame.Box)
        self.breakdown_rate_limit_outputwidget.setFrameShadow(QtGui.QFrame.Sunken)
        self.breakdown_rate_limit_outputwidget.setAlignment(QtCore.Qt.AlignAbsolute|QtCore.Qt.AlignBottom|QtCore.Qt.AlignCenter|QtCore.Qt.AlignHCenter|QtCore.Qt.AlignHorizontal_Mask|QtCore.Qt.AlignJustify|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignVertical_Mask)
        self.breakdown_rate_limit_outputwidget.setObjectName(_fromUtf8("breakdown_rate_limit_outputwidget"))
        self.gridLayout.addWidget(self.breakdown_rate_limit_outputwidget, 5, 1, 1, 1)
        self.breakdown_rate_limit_label = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.breakdown_rate_limit_label.setFont(font)
        self.breakdown_rate_limit_label.setFrameShape(QtGui.QFrame.Box)
        self.breakdown_rate_limit_label.setFrameShadow(QtGui.QFrame.Sunken)
        self.breakdown_rate_limit_label.setScaledContents(False)
        self.breakdown_rate_limit_label.setObjectName(_fromUtf8("breakdown_rate_limit_label"))
        self.gridLayout.addWidget(self.breakdown_rate_limit_label, 5, 0, 1, 1)
        self.last_106_count_label = QtGui.QLabel(self.layoutWidget)
        self.last_106_count_label.setFrameShape(QtGui.QFrame.Box)
        self.last_106_count_label.setFrameShadow(QtGui.QFrame.Sunken)
        self.last_106_count_label.setAlignment(QtCore.Qt.AlignAbsolute|QtCore.Qt.AlignBottom|QtCore.Qt.AlignCenter|QtCore.Qt.AlignHCenter|QtCore.Qt.AlignHorizontal_Mask|QtCore.Qt.AlignJustify|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignVertical_Mask)
        self.last_106_count_label.setObjectName(_fromUtf8("last_106_count_label"))
        self.gridLayout.addWidget(self.last_106_count_label, 6, 0, 1, 1)
        self.last_106_count_outputwidget = QtGui.QLabel(self.layoutWidget)
        self.last_106_count_outputwidget.setFrameShape(QtGui.QFrame.Box)
        self.last_106_count_outputwidget.setFrameShadow(QtGui.QFrame.Sunken)
        self.last_106_count_outputwidget.setAlignment(QtCore.Qt.AlignAbsolute|QtCore.Qt.AlignBottom|QtCore.Qt.AlignCenter|QtCore.Qt.AlignHCenter|QtCore.Qt.AlignHorizontal_Mask|QtCore.Qt.AlignJustify|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignVertical_Mask)
        self.last_106_count_outputwidget.setObjectName(_fromUtf8("last_106_count_outputwidget"))
        self.gridLayout.addWidget(self.last_106_count_outputwidget, 6, 1, 1, 1)
        self.llrf_interlock_outputwidget = QtGui.QLabel(self.layoutWidget)
        self.llrf_interlock_outputwidget.setFrameShape(QtGui.QFrame.Box)
        self.llrf_interlock_outputwidget.setFrameShadow(QtGui.QFrame.Sunken)
        self.llrf_interlock_outputwidget.setAlignment(QtCore.Qt.AlignAbsolute|QtCore.Qt.AlignBottom|QtCore.Qt.AlignCenter|QtCore.Qt.AlignHCenter|QtCore.Qt.AlignHorizontal_Mask|QtCore.Qt.AlignJustify|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignVertical_Mask)
        self.llrf_interlock_outputwidget.setObjectName(_fromUtf8("llrf_interlock_outputwidget"))
        self.gridLayout.addWidget(self.llrf_interlock_outputwidget, 9, 1, 1, 1)
        self.vac_valve_status_outputwidget = QtGui.QLabel(self.layoutWidget)
        self.vac_valve_status_outputwidget.setFrameShape(QtGui.QFrame.Box)
        self.vac_valve_status_outputwidget.setFrameShadow(QtGui.QFrame.Sunken)
        self.vac_valve_status_outputwidget.setAlignment(QtCore.Qt.AlignAbsolute|QtCore.Qt.AlignBottom|QtCore.Qt.AlignCenter|QtCore.Qt.AlignHCenter|QtCore.Qt.AlignHorizontal_Mask|QtCore.Qt.AlignJustify|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignVertical_Mask)
        self.vac_valve_status_outputwidget.setObjectName(_fromUtf8("vac_valve_status_outputwidget"))
        self.gridLayout.addWidget(self.vac_valve_status_outputwidget, 17, 1, 1, 1)
        self.llrf_trigger_label = QtGui.QLabel(self.layoutWidget)
        self.llrf_trigger_label.setFrameShape(QtGui.QFrame.Box)
        self.llrf_trigger_label.setFrameShadow(QtGui.QFrame.Sunken)
        self.llrf_trigger_label.setScaledContents(False)
        self.llrf_trigger_label.setObjectName(_fromUtf8("llrf_trigger_label"))
        self.gridLayout.addWidget(self.llrf_trigger_label, 10, 0, 1, 1)
        self.vac_spike_label = QtGui.QLabel(self.layoutWidget)
        self.vac_spike_label.setFrameShape(QtGui.QFrame.Box)
        self.vac_spike_label.setFrameShadow(QtGui.QFrame.Sunken)
        self.vac_spike_label.setScaledContents(False)
        self.vac_spike_label.setObjectName(_fromUtf8("vac_spike_label"))
        self.gridLayout.addWidget(self.vac_spike_label, 16, 0, 1, 1)
        self.llrf_ff_amp_locked_outputwidget = QtGui.QLabel(self.layoutWidget)
        self.llrf_ff_amp_locked_outputwidget.setFrameShape(QtGui.QFrame.Box)
        self.llrf_ff_amp_locked_outputwidget.setFrameShadow(QtGui.QFrame.Sunken)
        self.llrf_ff_amp_locked_outputwidget.setAlignment(QtCore.Qt.AlignAbsolute|QtCore.Qt.AlignBottom|QtCore.Qt.AlignCenter|QtCore.Qt.AlignHCenter|QtCore.Qt.AlignHorizontal_Mask|QtCore.Qt.AlignJustify|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignVertical_Mask)
        self.llrf_ff_amp_locked_outputwidget.setObjectName(_fromUtf8("llrf_ff_amp_locked_outputwidget"))
        self.gridLayout.addWidget(self.llrf_ff_amp_locked_outputwidget, 13, 1, 1, 1)
        self.llrf_output_label_2 = QtGui.QLabel(self.layoutWidget)
        self.llrf_output_label_2.setFrameShape(QtGui.QFrame.Box)
        self.llrf_output_label_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.llrf_output_label_2.setScaledContents(False)
        self.llrf_output_label_2.setObjectName(_fromUtf8("llrf_output_label_2"))
        self.gridLayout.addWidget(self.llrf_output_label_2, 12, 0, 1, 1)
        self.trace_rep_rate_outpuwidget = QtGui.QLabel(self.layoutWidget)
        self.trace_rep_rate_outpuwidget.setFrameShape(QtGui.QFrame.Box)
        self.trace_rep_rate_outpuwidget.setFrameShadow(QtGui.QFrame.Sunken)
        self.trace_rep_rate_outpuwidget.setScaledContents(False)
        self.trace_rep_rate_outpuwidget.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing)
        self.trace_rep_rate_outpuwidget.setIndent(-1)
        self.trace_rep_rate_outpuwidget.setObjectName(_fromUtf8("trace_rep_rate_outpuwidget"))
        self.gridLayout.addWidget(self.trace_rep_rate_outpuwidget, 12, 1, 1, 1)
        self.llrf_ff_ph_locked_outputwidget = QtGui.QLabel(self.layoutWidget)
        self.llrf_ff_ph_locked_outputwidget.setFrameShape(QtGui.QFrame.Box)
        self.llrf_ff_ph_locked_outputwidget.setFrameShadow(QtGui.QFrame.Sunken)
        self.llrf_ff_ph_locked_outputwidget.setAlignment(QtCore.Qt.AlignAbsolute|QtCore.Qt.AlignBottom|QtCore.Qt.AlignCenter|QtCore.Qt.AlignHCenter|QtCore.Qt.AlignHorizontal_Mask|QtCore.Qt.AlignJustify|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignVertical_Mask)
        self.llrf_ff_ph_locked_outputwidget.setObjectName(_fromUtf8("llrf_ff_ph_locked_outputwidget"))
        self.gridLayout.addWidget(self.llrf_ff_ph_locked_outputwidget, 14, 1, 1, 1)
        self.mod_state_outputwidget = QtGui.QLabel(self.layoutWidget)
        self.mod_state_outputwidget.setFrameShape(QtGui.QFrame.Box)
        self.mod_state_outputwidget.setFrameShadow(QtGui.QFrame.Sunken)
        self.mod_state_outputwidget.setAlignment(QtCore.Qt.AlignAbsolute|QtCore.Qt.AlignBottom|QtCore.Qt.AlignCenter|QtCore.Qt.AlignHCenter|QtCore.Qt.AlignHorizontal_Mask|QtCore.Qt.AlignJustify|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignVertical_Mask)
        self.mod_state_outputwidget.setObjectName(_fromUtf8("mod_state_outputwidget"))
        self.gridLayout.addWidget(self.mod_state_outputwidget, 8, 1, 1, 1)
        self.rf_mod_label = QtGui.QLabel(self.layoutWidget)
        self.rf_mod_label.setFrameShape(QtGui.QFrame.Box)
        self.rf_mod_label.setFrameShadow(QtGui.QFrame.Sunken)
        self.rf_mod_label.setScaledContents(False)
        self.rf_mod_label.setObjectName(_fromUtf8("rf_mod_label"))
        self.gridLayout.addWidget(self.rf_mod_label, 8, 0, 1, 1)
        self.llrf_trigger_outputwidget = QtGui.QLabel(self.layoutWidget)
        self.llrf_trigger_outputwidget.setFrameShape(QtGui.QFrame.Box)
        self.llrf_trigger_outputwidget.setFrameShadow(QtGui.QFrame.Sunken)
        self.llrf_trigger_outputwidget.setAlignment(QtCore.Qt.AlignAbsolute|QtCore.Qt.AlignBottom|QtCore.Qt.AlignCenter|QtCore.Qt.AlignHCenter|QtCore.Qt.AlignHorizontal_Mask|QtCore.Qt.AlignJustify|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignVertical_Mask)
        self.llrf_trigger_outputwidget.setObjectName(_fromUtf8("llrf_trigger_outputwidget"))
        self.gridLayout.addWidget(self.llrf_trigger_outputwidget, 10, 1, 1, 1)
        self.RF_protection_label = QtGui.QLabel(self.layoutWidget)
        self.RF_protection_label.setFrameShape(QtGui.QFrame.Box)
        self.RF_protection_label.setFrameShadow(QtGui.QFrame.Sunken)
        self.RF_protection_label.setScaledContents(False)
        self.RF_protection_label.setObjectName(_fromUtf8("RF_protection_label"))
        self.gridLayout.addWidget(self.RF_protection_label, 7, 0, 1, 1)
        self.RF_protection_outputwidget = QtGui.QLabel(self.layoutWidget)
        self.RF_protection_outputwidget.setFrameShape(QtGui.QFrame.Box)
        self.RF_protection_outputwidget.setFrameShadow(QtGui.QFrame.Sunken)
        self.RF_protection_outputwidget.setAlignment(QtCore.Qt.AlignAbsolute|QtCore.Qt.AlignBottom|QtCore.Qt.AlignCenter|QtCore.Qt.AlignHCenter|QtCore.Qt.AlignHorizontal_Mask|QtCore.Qt.AlignJustify|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignVertical_Mask)
        self.RF_protection_outputwidget.setObjectName(_fromUtf8("RF_protection_outputwidget"))
        self.gridLayout.addWidget(self.RF_protection_outputwidget, 7, 1, 1, 1)
        self.llrf_ff_amp_locked_label = QtGui.QLabel(self.layoutWidget)
        self.llrf_ff_amp_locked_label.setFrameShape(QtGui.QFrame.Box)
        self.llrf_ff_amp_locked_label.setFrameShadow(QtGui.QFrame.Sunken)
        self.llrf_ff_amp_locked_label.setScaledContents(False)
        self.llrf_ff_amp_locked_label.setObjectName(_fromUtf8("llrf_ff_amp_locked_label"))
        self.gridLayout.addWidget(self.llrf_ff_amp_locked_label, 13, 0, 1, 1)
        self.llrf_interlock_label = QtGui.QLabel(self.layoutWidget)
        self.llrf_interlock_label.setFrameShape(QtGui.QFrame.Box)
        self.llrf_interlock_label.setFrameShadow(QtGui.QFrame.Sunken)
        self.llrf_interlock_label.setScaledContents(False)
        self.llrf_interlock_label.setObjectName(_fromUtf8("llrf_interlock_label"))
        self.gridLayout.addWidget(self.llrf_interlock_label, 9, 0, 1, 1)
        self.llrf_output_label = QtGui.QLabel(self.layoutWidget)
        self.llrf_output_label.setFrameShape(QtGui.QFrame.Box)
        self.llrf_output_label.setFrameShadow(QtGui.QFrame.Sunken)
        self.llrf_output_label.setScaledContents(False)
        self.llrf_output_label.setObjectName(_fromUtf8("llrf_output_label"))
        self.gridLayout.addWidget(self.llrf_output_label, 11, 0, 1, 1)
        self.llrf_output_outputwidget = QtGui.QLabel(self.layoutWidget)
        self.llrf_output_outputwidget.setFrameShape(QtGui.QFrame.Box)
        self.llrf_output_outputwidget.setFrameShadow(QtGui.QFrame.Sunken)
        self.llrf_output_outputwidget.setAlignment(QtCore.Qt.AlignAbsolute|QtCore.Qt.AlignBottom|QtCore.Qt.AlignCenter|QtCore.Qt.AlignHCenter|QtCore.Qt.AlignHorizontal_Mask|QtCore.Qt.AlignJustify|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignVertical_Mask)
        self.llrf_output_outputwidget.setObjectName(_fromUtf8("llrf_output_outputwidget"))
        self.gridLayout.addWidget(self.llrf_output_outputwidget, 11, 1, 1, 1)
        self.DC_spike_label = QtGui.QLabel(self.layoutWidget)
        self.DC_spike_label.setMinimumSize(QtCore.QSize(0, 21))
        self.DC_spike_label.setFrameShape(QtGui.QFrame.Box)
        self.DC_spike_label.setFrameShadow(QtGui.QFrame.Sunken)
        self.DC_spike_label.setScaledContents(False)
        self.DC_spike_label.setObjectName(_fromUtf8("DC_spike_label"))
        self.gridLayout.addWidget(self.DC_spike_label, 15, 0, 1, 1)
        self.DC_spike_status_outputwidget = QtGui.QLabel(self.layoutWidget)
        self.DC_spike_status_outputwidget.setFrameShape(QtGui.QFrame.Box)
        self.DC_spike_status_outputwidget.setFrameShadow(QtGui.QFrame.Sunken)
        self.DC_spike_status_outputwidget.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.DC_spike_status_outputwidget.setObjectName(_fromUtf8("DC_spike_status_outputwidget"))
        self.gridLayout.addWidget(self.DC_spike_status_outputwidget, 15, 1, 1, 1)
        self.vac_valve_status_label = QtGui.QLabel(self.layoutWidget)
        self.vac_valve_status_label.setFrameShape(QtGui.QFrame.Box)
        self.vac_valve_status_label.setFrameShadow(QtGui.QFrame.Sunken)
        self.vac_valve_status_label.setScaledContents(False)
        self.vac_valve_status_label.setObjectName(_fromUtf8("vac_valve_status_label"))
        self.gridLayout.addWidget(self.vac_valve_status_label, 17, 0, 1, 1)
        self.vac_spike_status_outputwidget = QtGui.QLabel(self.layoutWidget)
        self.vac_spike_status_outputwidget.setFrameShape(QtGui.QFrame.Box)
        self.vac_spike_status_outputwidget.setFrameShadow(QtGui.QFrame.Sunken)
        self.vac_spike_status_outputwidget.setAlignment(QtCore.Qt.AlignAbsolute|QtCore.Qt.AlignBottom|QtCore.Qt.AlignCenter|QtCore.Qt.AlignHCenter|QtCore.Qt.AlignHorizontal_Mask|QtCore.Qt.AlignJustify|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignVertical_Mask)
        self.vac_spike_status_outputwidget.setObjectName(_fromUtf8("vac_spike_status_outputwidget"))
        self.gridLayout.addWidget(self.vac_spike_status_outputwidget, 16, 1, 1, 1)
        self.llrf_ff_ph_locked_label = QtGui.QLabel(self.layoutWidget)
        self.llrf_ff_ph_locked_label.setFrameShape(QtGui.QFrame.Box)
        self.llrf_ff_ph_locked_label.setFrameShadow(QtGui.QFrame.Sunken)
        self.llrf_ff_ph_locked_label.setScaledContents(False)
        self.llrf_ff_ph_locked_label.setObjectName(_fromUtf8("llrf_ff_ph_locked_label"))
        self.gridLayout.addWidget(self.llrf_ff_ph_locked_label, 14, 0, 1, 1)
        self.breakdown_count_outputwidget = QtGui.QLabel(self.layoutWidget)
        self.breakdown_count_outputwidget.setFrameShape(QtGui.QFrame.Box)
        self.breakdown_count_outputwidget.setFrameShadow(QtGui.QFrame.Sunken)
        self.breakdown_count_outputwidget.setAlignment(QtCore.Qt.AlignAbsolute|QtCore.Qt.AlignBottom|QtCore.Qt.AlignCenter|QtCore.Qt.AlignHCenter|QtCore.Qt.AlignHorizontal_Mask|QtCore.Qt.AlignJustify|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignVertical_Mask)
        self.breakdown_count_outputwidget.setObjectName(_fromUtf8("breakdown_count_outputwidget"))
        self.gridLayout.addWidget(self.breakdown_count_outputwidget, 3, 1, 1, 1)
        self.breakdown_count_label = QtGui.QLabel(self.layoutWidget)
        self.breakdown_count_label.setFrameShape(QtGui.QFrame.Box)
        self.breakdown_count_label.setFrameShadow(QtGui.QFrame.Sunken)
        self.breakdown_count_label.setAlignment(QtCore.Qt.AlignAbsolute|QtCore.Qt.AlignBottom|QtCore.Qt.AlignCenter|QtCore.Qt.AlignHCenter|QtCore.Qt.AlignHorizontal_Mask|QtCore.Qt.AlignJustify|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignVertical_Mask)
        self.breakdown_count_label.setObjectName(_fromUtf8("breakdown_count_label"))
        self.gridLayout.addWidget(self.breakdown_count_label, 3, 0, 1, 1)
        self.pulse_count_label = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.pulse_count_label.setFont(font)
        self.pulse_count_label.setFrameShape(QtGui.QFrame.Box)
        self.pulse_count_label.setFrameShadow(QtGui.QFrame.Sunken)
        self.pulse_count_label.setScaledContents(False)
        self.pulse_count_label.setObjectName(_fromUtf8("pulse_count_label"))
        self.gridLayout.addWidget(self.pulse_count_label, 4, 0, 1, 1)
        self.pulse_count_outputwidget = QtGui.QLabel(self.layoutWidget)
        self.pulse_count_outputwidget.setFrameShape(QtGui.QFrame.Box)
        self.pulse_count_outputwidget.setFrameShadow(QtGui.QFrame.Sunken)
        self.pulse_count_outputwidget.setAlignment(QtCore.Qt.AlignAbsolute|QtCore.Qt.AlignBottom|QtCore.Qt.AlignCenter|QtCore.Qt.AlignHCenter|QtCore.Qt.AlignHorizontal_Mask|QtCore.Qt.AlignJustify|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignVertical_Mask)
        self.pulse_count_outputwidget.setObjectName(_fromUtf8("pulse_count_outputwidget"))
        self.gridLayout.addWidget(self.pulse_count_outputwidget, 4, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.graphicsView = PlotWidget(self.layoutWidget)
        self.graphicsView.setMinimumSize(QtCore.QSize(900, 0))
        self.graphicsView.setMaximumSize(QtCore.QSize(900, 16777215))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.horizontalLayout.addWidget(self.graphicsView)
        self.label = QtGui.QLabel(self.tab_3)
        self.label.setGeometry(QtCore.QRect(1250, 530, 311, 171))
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayoutWidget = QtGui.QWidget(self.tab_3)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 540, 1131, 171))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.breakdown_graphicsView = PlotWidget(self.tab_4)
        self.breakdown_graphicsView.setGeometry(QtCore.QRect(10, 10, 1111, 651))
        self.breakdown_graphicsView.setMinimumSize(QtCore.QSize(900, 0))
        self.breakdown_graphicsView.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.breakdown_graphicsView.setObjectName(_fromUtf8("breakdown_graphicsView"))
        self.tabWidget.addTab(self.tab_4, _fromUtf8(""))
        self.message_pad.raise_()
        self.graphicsView.raise_()
        self.verticalLayoutWidget.raise_()
        self.tabWidget.raise_()
        rf_condition_mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(rf_condition_mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1604, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        rf_condition_mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(rf_condition_mainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        rf_condition_mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(rf_condition_mainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(rf_condition_mainWindow)

    def retranslateUi(self, rf_condition_mainWindow):
        rf_condition_mainWindow.setWindowTitle(_translate("rf_condition_mainWindow", "MainWindow", None))
        self.llrf_enable_button_3.setText(_translate("rf_condition_mainWindow", "ENABLE / DISABLE LLRF RF", None))
        self.copy_to_clipboard_button_3.setToolTip(_translate("rf_condition_mainWindow", "For the log!", None))
        self.copy_to_clipboard_button_3.setText(_translate("rf_condition_mainWindow", "Copy status to clipboard", None))
        self.start_pause_ramp_button_3.setText(_translate("rf_condition_mainWindow", "Pause ramp", None))
        self.breakdown_rate_limit_outputwidget.setText(_translate("rf_condition_mainWindow", "0", None))
        self.breakdown_rate_limit_label.setText(_translate("rf_condition_mainWindow", "Breakdownrate aim (per 10^6)", None))
        self.last_106_count_label.setText(_translate("rf_condition_mainWindow", "Last 10^6 BD count", None))
        self.last_106_count_outputwidget.setText(_translate("rf_condition_mainWindow", "-1", None))
        self.llrf_interlock_outputwidget.setText(_translate("rf_condition_mainWindow", "UK", None))
        self.vac_valve_status_outputwidget.setText(_translate("rf_condition_mainWindow", "Open", None))
        self.llrf_trigger_label.setText(_translate("rf_condition_mainWindow", "LLRF Trigger", None))
        self.vac_spike_label.setText(_translate("rf_condition_mainWindow", "Vacuum spike", None))
        self.llrf_ff_amp_locked_outputwidget.setText(_translate("rf_condition_mainWindow", "locked?", None))
        self.llrf_output_label_2.setText(_translate("rf_condition_mainWindow", "Trace Rep-Rate", None))
        self.trace_rep_rate_outpuwidget.setText(_translate("rf_condition_mainWindow", "0", None))
        self.llrf_ff_ph_locked_outputwidget.setText(_translate("rf_condition_mainWindow", "locked?", None))
        self.mod_state_outputwidget.setText(_translate("rf_condition_mainWindow", "UK", None))
        self.rf_mod_label.setText(_translate("rf_condition_mainWindow", "Modulator state", None))
        self.llrf_trigger_outputwidget.setText(_translate("rf_condition_mainWindow", "-9", None))
        self.RF_protection_label.setText(_translate("rf_condition_mainWindow", "RF Protection", None))
        self.RF_protection_outputwidget.setText(_translate("rf_condition_mainWindow", "UK", None))
        self.llrf_ff_amp_locked_label.setText(_translate("rf_condition_mainWindow", "LLRF Amp Locked", None))
        self.llrf_interlock_label.setText(_translate("rf_condition_mainWindow", "LLRF Interlock", None))
        self.llrf_output_label.setText(_translate("rf_condition_mainWindow", "LLRF Output", None))
        self.llrf_output_outputwidget.setText(_translate("rf_condition_mainWindow", "output?", None))
        self.DC_spike_label.setText(_translate("rf_condition_mainWindow", "Dark current spike", None))
        self.DC_spike_status_outputwidget.setText(_translate("rf_condition_mainWindow", "No", None))
        self.vac_valve_status_label.setText(_translate("rf_condition_mainWindow", "Vacuum valve status", None))
        self.vac_spike_status_outputwidget.setText(_translate("rf_condition_mainWindow", "No", None))
        self.llrf_ff_ph_locked_label.setText(_translate("rf_condition_mainWindow", "LLRF Phase Locked", None))
        self.breakdown_count_outputwidget.setText(_translate("rf_condition_mainWindow", "-1", None))
        self.breakdown_count_label.setText(_translate("rf_condition_mainWindow", "Breakdown count", None))
        self.pulse_count_label.setText(_translate("rf_condition_mainWindow", "Active pulse count", None))
        self.pulse_count_outputwidget.setText(_translate("rf_condition_mainWindow", "Terrible", None))
        self.label.setText(_translate("rf_condition_mainWindow", "TextLabel", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("rf_condition_mainWindow", "Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("rf_condition_mainWindow", "Tab 2", None))

from pyqtgraph import PlotWidget
