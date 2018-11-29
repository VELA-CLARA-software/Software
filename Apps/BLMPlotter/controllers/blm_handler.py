from blm_handler_base import blm_handler_base
import data.blm_plotter_data_base as dat
import numpy, collections
from scipy import signal, constants
from scipy.fftpack import fft, ifft
from random import randint

class blm_handler(blm_handler_base):
    #whoami
    my_name= 'blm_handler'
    def __init__(self):
        blm_handler_base.__init__(self)

    def set_blm_buffer(self,value):
        blm_handler_base.blm_control.setBufferSize(int(value))
        blm_handler_base.logger.message('setting buffer = ' + str(value), True)
        for i in blm_handler_base.data.values[dat.blm_waveform_pvs]:
            blm_handler_base.data.values[dat.blm_voltages][i] = collections.deque(maxlen = value)
            for j in range(0,value-1):
                blm_handler_base.data.values[dat.blm_voltages][i].append([])

    def get_noise_data(self):
        self.noise_data = []
        with open( 'calibration_signals\\C18 december noise00000.dat' ) as f:
            self.content = f.readlines()
            for x in self.content:
                self.row = x.split()
                self.noise_data.append(float(self.row[1]))
        blm_handler_base.data.values[dat.noise_data] = self.noise_data
        blm_handler_base.data.values[dat.all_noise_data][blm_handler_base.data.values[dat.blm_waveform_pvs][0]] = self.noise_data
        with open( 'calibration_signals\\C28 december noise00000.dat' ) as f:
            self.content = f.readlines()
            for x in self.content:
                self.row = x.split()
                self.noise_data.append(float(self.row[1]))
        blm_handler_base.data.values[dat.noise_data] = self.noise_data
        blm_handler_base.data.values[dat.all_noise_data][blm_handler_base.data.values[dat.blm_waveform_pvs][1]] = self.noise_data
        with open( 'calibration_signals\\C38 december noise00000.dat' ) as f:
            self.content = f.readlines()
            for x in self.content:
                self.row = x.split()
                self.noise_data.append(float(self.row[1]))
        blm_handler_base.data.values[dat.noise_data] = self.noise_data
        blm_handler_base.data.values[dat.all_noise_data][blm_handler_base.data.values[dat.blm_waveform_pvs][2]] = self.noise_data
        with open( 'calibration_signals\\C48 december noise00000.dat' ) as f:
            self.content = f.readlines()
            for x in self.content:
                self.row = x.split()
                self.noise_data.append(float(self.row[1]))
        blm_handler_base.data.values[dat.noise_data] = self.noise_data
        blm_handler_base.data.values[dat.all_noise_data][blm_handler_base.data.values[dat.blm_waveform_pvs][3]] = self.noise_data

    def get_single_photon_data(self):
        self.single_photon_data = []
        with open( 'calibration_signals\\C18 december 1 photon00000.dat' ) as f:
            self.content = f.readlines()
            for x in self.content:
                self.row = x.split()
                self.single_photon_data.append(float(self.row[1]))
        blm_handler_base.data.values[dat.all_single_photon_data][blm_handler_base.data.values[dat.blm_waveform_pvs][0]] = self.single_photon_data
        with open( 'calibration_signals\\C28 december 1 photon00000.dat' ) as f:
            self.content = f.readlines()
            for x in self.content:
                self.row = x.split()
                self.single_photon_data.append(float(self.row[1]))
        blm_handler_base.data.values[dat.all_single_photon_data][blm_handler_base.data.values[dat.blm_waveform_pvs][1]] = self.single_photon_data
        blm_handler_base.data.values[dat.single_photon_data] = self.single_photon_data
        with open( 'calibration_signals\\C38 december 1 photon00000.dat' ) as f:
            self.content = f.readlines()
            for x in self.content:
                self.row = x.split()
                self.single_photon_data.append(float(self.row[1]))
        blm_handler_base.data.values[dat.single_photon_data] = self.single_photon_data
        blm_handler_base.data.values[dat.all_single_photon_data][blm_handler_base.data.values[dat.blm_waveform_pvs][2]] = self.single_photon_data
        with open( 'calibration_signals\\C48 december 1 photon00000.dat' ) as f:
            self.content = f.readlines()
            for x in self.content:
                self.row = x.split()
                self.single_photon_data.append(float(self.row[1]))
        blm_handler_base.data.values[dat.all_single_photon_data][blm_handler_base.data.values[dat.blm_waveform_pvs][3]] = self.single_photon_data
        blm_handler_base.data.values[dat.single_photon_data] = self.single_photon_data

    def sparsify_list(self,data1, data2):
        self.data2 = data2
        self.data1 = data1
        self.reduced_list = []
        if len(self.data2) < len(self.data1):
            self.ratio = int(len(self.data1)/len(self.data2))
            self.reduced_list = self.data1[0::self.ratio]
            blm_handler_base.data.values[dat.has_sparsified] = True
            while len(self.reduced_list) > len(self.data2):
                del self.reduced_list[randint(0,len(self.reduced_list))]
            return self.reduced_list
        else:
            blm_handler_base.data.values[dat.has_sparsified] = True
            return self.data2

    def deconvolution_filter(self, noise, single_photon):
        self.num_points = len(noise)
        self.noise_ft = fft(noise)
        self.single_photon_ft = fft(single_photon)
        self.wiener_filter = (abs(self.single_photon_ft)**2)/(abs(self.single_photon_ft)**2 + abs(self.noise_ft)**2)

        self.blackman_window = signal.blackman(blm_handler_base.data.values[dat.blackman_size])
        self.blackman_window_ft = fft(self.blackman_window,n=len(self.single_photon_ft))

        blm_handler_base.data.values[dat.deconvolution_filter] = ifft(( self.blackman_window_ft/self.single_photon_ft) * self.wiener_filter )

    def set_filters(self):
        for i in blm_handler_base.data.values[dat.blm_waveform_pvs]:
            blm_handler_base.data.values[dat.blm_voltages][str(i)] = blm_handler_base.data.values[dat.blm_voltages][str(i)] * abs(blm_handler_base.data.values[dat.deconvolution_filter])

    def calibrate_blm(self):
        self.str_to_pv_1 = blm_handler_base.data.values[dat.str_to_pv][
            blm_handler_base.data.values[dat.calibrate_channel_names][0]]
        self.str_to_pv_2 = blm_handler_base.data.values[dat.str_to_pv][
            blm_handler_base.data.values[dat.calibrate_channel_names][1]]
        print blm_handler_base.data.values[dat.peak_voltages]
        print blm_handler_base.data.values[dat.peak_voltages][self.str_to_pv_1][1]
        print blm_handler_base.data.values[dat.peak_voltages][self.str_to_pv_2][1]
        self.delta_t = blm_handler_base.data.values[dat.peak_voltages][self.str_to_pv_1][1] - blm_handler_base.data.values[dat.peak_voltages][self.str_to_pv_2][1]
        blm_handler_base.data.values[dat.delta_x] = self.delta_t / blm_handler_base.data.values[dat.fibre_speed]
        blm_handler_base.data.values[dat.calibration_time] = blm_handler_base.data.values[dat.delta_x] / constants.speed_of_light