from monitor import monitor
from PyQt4.QtCore import QTimer
import data.blm_plotter_data_base as dat
import numpy, random
import time, collections
from itertools import compress
import epics

class blm_monitor(monitor):
    # whoami
    my_name = 'blm_monitor'
    set_success = False

    def __init__(self):
        self.my_name = 'blm_monitor'
        self.bunch_charge = 0
        # init base-class
        monitor.__init__(self,update_time=100)

        self.timer = QTimer()
        self.set_success = True
        self.timer.start(self.update_time)

        self.check_blm_is_monitoring()
        self.run()

    def run(self):
        monitor.logger.message(self.my_name, ' running')

    def check_blm_is_monitoring(self):
        # PLACEHOLDER
        # blm_data_buffer = monitor.blm_control.getBLMRawDataBuffer(monitor.data.values[dat.bpm_names[0]])
        # if len(blm_data_buffer) > 1:
        #     if blm_data_buffer[-1] != blm_data_buffer[-2]:
        #         monitor.data.values[dat.blm_status] = True
        # else:
        #     monitor.data.values[dat.blm_status] = False
        monitor.data.values[dat.blm_status] = True
        monitor.data.values[dat.blm_distance_start] = 0.0
        monitor.data.values[dat.blm_distance_end] = 1.0
        monitor.data.values[dat.blm_names] = monitor.blm_control.getBLMNames()
        monitor.data.values[dat.blm_pvs] = monitor.blm_control.getBLMPVs()
        monitor.data.values[dat.blm_time_pvs] = monitor.blm_control.getBLMTimePVs()
        monitor.data.values[dat.blm_waveform_pvs] = monitor.blm_control.getBLMWaveformPVs()
        monitor.data.values[dat.str_to_pv] = {"CH1": str(monitor.data.values[dat.blm_waveform_pvs][0]),
                                              "CH2": str(monitor.data.values[dat.blm_waveform_pvs][1]),
                                              "CH3": str(monitor.data.values[dat.blm_waveform_pvs][2]),
                                              "CH4": str(monitor.data.values[dat.blm_waveform_pvs][3])}
        monitor.data.values[dat.stream] = {monitor.data.values[dat.blm_waveform_pvs][0] : "upstream",
                                           monitor.data.values[dat.blm_waveform_pvs][1]: "upstream",
                                           monitor.data.values[dat.blm_waveform_pvs][2]: "upstream",
                                           monitor.data.values[dat.blm_waveform_pvs][3]: "upstream"}
        monitor.data.values[dat.fibre_config] = {str(monitor.data.values[dat.blm_waveform_pvs][0]): ["CLA-SP1","East"],
                                                 str(monitor.data.values[dat.blm_waveform_pvs][1]): ["CLA-YAG10","North"],
                                                 str(monitor.data.values[dat.blm_waveform_pvs][2]): ["CLA-YAG10","West"],
                                                 str(monitor.data.values[dat.blm_waveform_pvs][3]): ["CLA-SP1","South"]}
        monitor.data.values[dat.fibre_diameter] = {str(monitor.data.values[dat.blm_waveform_pvs][0]): "600mm",
                                                   str(monitor.data.values[dat.blm_waveform_pvs][1]): "600mm",
                                                   str(monitor.data.values[dat.blm_waveform_pvs][2]): "400mm",
                                                   str(monitor.data.values[dat.blm_waveform_pvs][3]): "400mm"}
        monitor.data.values[dat.calibration_factors] = {str(monitor.data.values[dat.blm_waveform_pvs][0]): [0.117051, -4.93788],
                                                        str(monitor.data.values[dat.blm_waveform_pvs][1]): [0.118302, -5.17389],
                                                        str(monitor.data.values[dat.blm_waveform_pvs][2]): [0.12249, -5.7186],
                                                        str(monitor.data.values[dat.blm_waveform_pvs][3]): [0.118302, -5.4186]}
        monitor.data.values[dat.blm_object] = monitor.blm_control.getBLMTraceDataStruct(monitor.data.values[dat.blm_name])
        for i, j in zip(self.data.values[dat.blm_waveform_pvs], self.data.values[dat.blm_time_pvs]):
            self.data.values[dat.blm_voltage_average][str(i)] = [[]]
            self.data.values[dat.blm_time_average][str(j)] = [[]]

    def update_blm_voltages(self):
        for i, j in zip(monitor.data.values[dat.blm_waveform_pvs],monitor.data.values[dat.blm_time_pvs]):
            monitor.data.values[dat.blm_buffer][str(i)] = monitor.data.values[dat.blm_object].traceDataBuffer[i]
            monitor.data.values[dat.blm_time_buffer][str(j)] = monitor.data.values[dat.blm_object].traceDataBuffer[j]
            # monitor.data.values[dat.blm_voltages][str(i)] = numpy.asarray(monitor.data.values[dat.blm_buffer][str(i)][-1])
            self.volt1 = numpy.asarray(monitor.data.values[dat.blm_buffer][str(i)][-1])
            self.time1 = numpy.asarray(monitor.data.values[dat.blm_time_buffer][str(j)][-1])
            # self.res = monitor.data.values[dat.blm_time_buffer][str(j)][-1][1] - monitor.data.values[dat.blm_time_buffer][str(j)][-1][0]
            if monitor.data.values[dat.stream][i] == "upstream":
                self.cal = abs(1 + 1.46)
                # epics.caput('CLA-C09-TIM-EVR-01:Pul5-Delay-SP',403.65)
                # time.sleep(0.1)
                # self.volt2 = numpy.append(self.volt1,numpy.asarray(monitor.data.values[dat.blm_buffer][str(i)][-1][2:-2]))
                # self.time2 = numpy.append(self.time1,[x + 400 for x in numpy.asarray(monitor.data.values[dat.blm_time_buffer][str(j)][-1][2:-2])])
                # epics.caput('CLA-C09-TIM-EVR-01:Pul5-Delay-SP', 403.45)
                # time.sleep(0.1)
                # self.volt3 = numpy.append(self.volt2, numpy.asarray(monitor.data.values[dat.blm_buffer][str(i)][-1][2:-2]))
                # self.time3 = numpy.append(self.time2, [x + 200 for x in numpy.asarray(monitor.data.values[dat.blm_time_buffer][str(j)][-1][2:-2])])
                self.res = 0.2
                monitor.data.values[dat.blm_voltages][str(i)] = self.volt1[2:-2]
                monitor.data.values[dat.blm_time][str(j)] = [x for x in ((self.time1[2:-2])*monitor.data.values[dat.calibration_factors][str(i)][0] + monitor.data.values[dat.calibration_factors][str(i)][1])]# * ((299792458 * self.res) / (self.cal * (1 * (10 ** 9)))))]
            else:
                self.cal = abs(1 + 1.46) #* (1-1.46/(20*1.46))
                self.res = 0.2
                monitor.data.values[dat.blm_voltages][str(i)] = self.volt1[2:-2]
                monitor.data.values[dat.blm_time][str(j)] = [x for x in ((self.time1[2:-2])*monitor.data.values[dat.calibration_factors][str(i)][0] + monitor.data.values[dat.calibration_factors][str(i)][1])]# * ((299792458*self.res)/(self.cal*(1*(10**9)))))]

            # epics.caput('CLA-C09-TIM-EVR-01:Pul5-Delay-SP', 403.25)
            # time.sleep(0.1)
            if monitor.data.values[dat.rolling_average] > 1:
                monitor.data.values[dat.blm_voltages][str(i)] = list(numpy.mean(monitor.data.values[dat.blm_buffer][str(i)],axis=1))
                monitor.data.values[dat.blm_time][str(j)] = list(numpy.mean(monitor.data.values[dat.blm_time_buffer][str(j)],axis=1))
                # if monitor.data.values[dat.rolling_average] == len(monitor.data.values[dat.blm_voltage_average][str(i)]):
                #     monitor.data.values[dat.blm_voltages][str(i)].pop(0)
                #     monitor.data.values[dat.blm_time][str(j)].pop(0)
            if len(monitor.data.values[dat.blm_voltages][str(i)]) > 0:
                self.maxval = max(monitor.data.values[dat.blm_voltages][str(i)])
                self.maxlocation = numpy.where(monitor.data.values[dat.blm_voltages][str(i)]==self.maxval)
                monitor.data.values[dat.peak_voltages][str(i)] = [self.maxval, numpy.mean(self.maxlocation)]
                monitor.data.values[dat.has_blm_data] = True
            else:
                monitor.data.values[dat.has_blm_data] = False

    def update_blm_buffer(self):
        for i, j in zip(monitor.data.values[dat.blm_waveform_pvs],monitor.data.values[dat.blm_time_pvs]):
            monitor.data.values[dat.blm_buffer][str(i)] = monitor.blm_control.getBLMTraceBuffer(monitor.data.values[dat.blm_names][0], i)
            # monitor.data.values[dat.blm_buffer][str(j)] = monitor.blm_control.getBLMTraceBuffer(monitor.data.values[dat.blm_names][0], j)
            self.timeTraceBuffer = monitor.blm_control.getBLMTraceBuffer(monitor.data.values[dat.blm_names][0], j)
            monitor.data.values[dat.blm_buffer][str(j)] = [[]] * len(self.timeTraceBuffer)
            for k in range(0,len(self.timeTraceBuffer)):
                monitor.data.values[dat.blm_buffer][str(j)][k] = [x for x in ((numpy.asarray(self.timeTraceBuffer[k])[2:-2]) * monitor.data.values[dat.calibration_factors][str(i)][0] +
                         monitor.data.values[dat.calibration_factors][str(i)][1])]
            monitor.data.values[dat.time_stamps][str(i)] = monitor.blm_control.getTimeStampsBuffer(monitor.data.values[dat.blm_names][0], i)
            monitor.data.values[dat.time_stamps][str(j)] = monitor.blm_control.getTimeStampsBuffer(monitor.data.values[dat.blm_names][0], j)
        monitor.data.values[dat.has_blm_data] = True

    def update_blm_distance(self):
        monitor.data.values[dat.blm_distance_start] = 0
        monitor.data.values[dat.blm_distance_end] = 1
        monitor.data.values[dat.blm_num_values] = numpy.linspace(monitor.data.values[dat.blm_distance_start],monitor.data.values[dat.blm_distance_end],
                                                                 len(monitor.data.values[dat.blm_voltages][str(monitor.data.values[dat.blm_waveform_pvs][0])]))
        monitor.data.values[dat.has_blm_data] = True

    def check_buffer(self):
        # PLACEHOLDER: REPLACE WITH REAL BLM BUFFER CHECK FUNCTION
        return True