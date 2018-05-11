from bpm_handler_base import bpm_handler_base
import data.bpm_calibrate_data_base as dat
import numpy

class bpm_handler(bpm_handler_base):
    #whoami
    my_name= 'bpm_handler'
    def __init__(self):
        bpm_handler_base.__init__(self)

    def set_bpm_buffer(self,pv,value):
        bpm_handler_base.bpm_control.setBufferSize(pv,value)
        bpm_handler_base.logger.message('setting SA1 = SA2 = ' + str(value) + ' for ' + pv, True)

    def set_attenuation(self,pv,value):
        bpm_handler_base.bpm_control.setSA1(pv,value)
        bpm_handler_base.bpm_control.setSA2(pv,value)
        bpm_handler_base.data.values[dat.set_sa1_current] = value
        bpm_handler_base.data.values[dat.set_sa2_current] = value
        bpm_handler_base.logger.message('setting SA1 = SA2 = ' + str(value) + ' for ' + pv, True)

    def read_attenuation(self, pv):
        bpm_handler_base.data.values[dat.get_ra1] = bpm_handler_base.bpm_control.getRA1(pv)
        bpm_handler_base.data.values[dat.get_ra2] = bpm_handler_base.bpm_control.getRA2(pv)
        bpm_handler_base.logger.message('RA1 = ' + str(bpm_handler_base.data.values[dat.get_ra1]) + ' for ' + pv, True)
        bpm_handler_base.logger.message('RA2 = ' + str(bpm_handler_base.data.values[dat.get_ra2]) + ' for ' + pv, True)

    def set_delay(self, pv, value):
        bpm_handler_base.bpm_control.setSD1(pv, value)
        bpm_handler_base.bpm_control.setSD2(pv, value)
        bpm_handler_base.logger.message('setting SD1 = SD2 = ' + str(value) + ' for ' + pv, True)

    def set_dly_1(self, pv, value):
        bpm_handler_base.bpm_control.setSD1(pv, value)
        bpm_handler_base.logger.message('setting SD1 = ' + str(value) + ' for ' + pv, True)

    def set_dly_2(self, pv, value):
        bpm_handler_base.bpm_control.setSD2(pv, value)
        bpm_handler_base.logger.message('setting SD2 = ' + str(value) + ' for ' + pv, True)

    def read_delay(self, pv):
        bpm_handler_base.data.values[dat.get_rd1] = bpm_handler_base.bpm_control.getRD1(pv)
        bpm_handler_base.data.values[dat.get_rd2] = bpm_handler_base.bpm_control.getRD2(pv)
        bpm_handler_base.logger.message('RD1 = ' + str(bpm_handler_base.data.values[dat.get_rd1]) + ' for ' + pv, True)
        bpm_handler_base.logger.message('RD2 = ' + str(bpm_handler_base.data.values[dat.get_rd2]) + ' for ' + pv, True)

    def update_bpm_att_voltages(self):
        if bpm_handler_base.data.values[dat.bpm_status] and bpm_handler_base.data.values[dat.scope_status]:
            # for i in bpm_handler_base.data.values[dat.bpm_u11]:
            #     print i
            bpm_handler_base.data.values[dat.bpm_raw_data_mean_v11] = abs(numpy.mean(bpm_handler_base.data.values[dat.bpm_u11]) - numpy.mean(bpm_handler_base.data.values[dat.bpm_u14]))
            bpm_handler_base.data.values[dat.bpm_raw_data_mean_v12] = abs(numpy.mean(bpm_handler_base.data.values[dat.bpm_u12]) - numpy.mean(bpm_handler_base.data.values[dat.bpm_u14]))
            bpm_handler_base.data.values[dat.bpm_raw_data_mean_v21] = abs(numpy.mean(bpm_handler_base.data.values[dat.bpm_u21]) - numpy.mean(bpm_handler_base.data.values[dat.bpm_u24]))
            bpm_handler_base.data.values[dat.bpm_raw_data_mean_v22] = abs(numpy.mean(bpm_handler_base.data.values[dat.bpm_u22]) - numpy.mean(bpm_handler_base.data.values[dat.bpm_u24]))
            bpm_handler_base.data.values[dat.bpm_v11_v12_sum][bpm_handler_base.data.values[dat.set_sa1_current]] = (bpm_handler_base.data.values[
                                                                                                      dat.bpm_raw_data_mean_v11] +
                                                                                                                    bpm_handler_base.data.values[
                                                                                                      dat.bpm_raw_data_mean_v12]) / 2
            bpm_handler_base.data.values[dat.bpm_v21_v22_sum][bpm_handler_base.data.values[dat.set_sa2_current]] = (bpm_handler_base.data.values[
                                                                                                      dat.bpm_raw_data_mean_v21] +
                                                                                                                    bpm_handler_base.data.values[
                                                                                                      dat.bpm_raw_data_mean_v22]) / 2
            print bpm_handler_base.data.values[dat.bpm_v11_v12_sum][bpm_handler_base.data.values[dat.set_sa1_current]]
            print bpm_handler_base.data.values[dat.bpm_v21_v22_sum][bpm_handler_base.data.values[dat.set_sa2_current]]

    def scan_dly1(self, dly_1):
        self.set_dly_1(bpm_handler_base.data.values[dat.bpm_name],dly_1)
        bpm_handler_base.data.values[dat.dv1_dly1][dly_1] = \
            (2 * numpy.mean(bpm_handler_base.data.values[dat.bpm_u11]) ) / (
                numpy.mean(bpm_handler_base.data.values[dat.bpm_u21]) + numpy.mean(bpm_handler_base.data.values[dat.bpm_u22]) )
        bpm_handler_base.data.values[dat.dv2_dly1][dly_1] = \
            (2 * numpy.mean(bpm_handler_base.data.values[dat.bpm_u12])) / (
                numpy.mean(bpm_handler_base.data.values[dat.bpm_u21]) + numpy.mean(bpm_handler_base.data.values[dat.bpm_u22]))

    def scan_dly(self, dly_1):
        self.set_dly_1(bpm_handler_base.data.values[dat.bpm_name],dly_1)
        self.set_dly_2(bpm_handler_base.data.values[dat.bpm_name],dly_1)
        bpm_handler_base.data.values[dat.dv1_dly1][dly_1] = \
            (2 * numpy.mean(bpm_handler_base.data.values[dat.bpm_u11]) ) / (
                numpy.mean(bpm_handler_base.data.values[dat.bpm_u21]) + numpy.mean(bpm_handler_base.data.values[dat.bpm_u22]) )
        bpm_handler_base.data.values[dat.dv2_dly1][dly_1] = \
            (2 * numpy.mean(bpm_handler_base.data.values[dat.bpm_u12])) / (
                numpy.mean(bpm_handler_base.data.values[dat.bpm_u21]) + numpy.mean(bpm_handler_base.data.values[dat.bpm_u22]))
        bpm_handler_base.data.values[dat.dv1_dly2][dly_1] = \
            (2 * numpy.mean(bpm_handler_base.data.values[dat.bpm_u21]) ) / (
                numpy.mean(bpm_handler_base.data.values[dat.bpm_u11]) + numpy.mean(bpm_handler_base.data.values[dat.bpm_u12]) )
        bpm_handler_base.data.values[dat.dv2_dly2][dly_1] = \
            (2 * numpy.mean(bpm_handler_base.data.values[dat.bpm_u22])) / (
                numpy.mean(bpm_handler_base.data.values[dat.bpm_u11]) + numpy.mean(bpm_handler_base.data.values[dat.bpm_u12]))

    def find_min_dly_1(self):
        print bpm_handler_base.data.values[dat.dv1_dly1].values()
        print bpm_handler_base.data.values[dat.dv2_dly1].values()
        self.x1 = bpm_handler_base.data.values[dat.dv1_dly1].values()
        self.x2 = bpm_handler_base.data.values[dat.dv2_dly1].values()
        self.minval1 = min(self.x1)
        self.minval2 = min(self.x2)
        for key, value in bpm_handler_base.data.values[dat.dv1_dly1].iteritems():
            if value == self.minval1:
                bpm_handler_base.data.values[dat.dv1_dly1_min_val] = key
        for key, value in bpm_handler_base.data.values[dat.dv2_dly1].iteritems():
            if value == self.minval2:
                bpm_handler_base.data.values[dat.dv2_dly1_min_val] = key
        print bpm_handler_base.data.values[dat.dv1_dly1_min_val]
        print bpm_handler_base.data.values[dat.dv2_dly1_min_val]
        bpm_handler_base.data.values[dat.new_dly_1] = int(numpy.mean(bpm_handler_base.data.values[dat.dv1_dly1_min_val] + bpm_handler_base.data.values[dat.dv2_dly1_min_val])/2)
        self.set_dly_1(bpm_handler_base.data.values[dat.bpm_name],bpm_handler_base.data.values[dat.new_dly_1])
        print bpm_handler_base.data.values[dat.new_dly_1]
        self.read_delay(bpm_handler_base.data.values[dat.bpm_name])
        bpm_handler_base.data.values[dat.new_dly_1_set] = True

    def scan_dly2(self, dly_2):
        self.set_dly_2(bpm_handler_base.data.values[dat.bpm_name], dly_2)
        bpm_handler_base.data.values[dat.dv1_dly2][dly_2] = \
            (2 * numpy.mean(bpm_handler_base.data.values[dat.bpm_u21]) ) / (
                numpy.mean(bpm_handler_base.data.values[dat.bpm_u11]) + numpy.mean(bpm_handler_base.data.values[dat.bpm_u12]) )
        bpm_handler_base.data.values[dat.dv2_dly2][dly_2] = \
            (2 * numpy.mean(bpm_handler_base.data.values[dat.bpm_u22])) / (
                numpy.mean(bpm_handler_base.data.values[dat.bpm_u11]) + numpy.mean(bpm_handler_base.data.values[dat.bpm_u12]))

    def find_min_dly_2(self):
        print bpm_handler_base.data.values[dat.dv1_dly2].values()
        print bpm_handler_base.data.values[dat.dv2_dly2].values()
        self.x1 = bpm_handler_base.data.values[dat.dv1_dly2].values()
        self.x2 = bpm_handler_base.data.values[dat.dv2_dly2].values()
        self.minval1 = min(self.x1)
        self.minval2 = min(self.x2)
        for key, value in bpm_handler_base.data.values[dat.dv1_dly2].iteritems():
            if value == self.minval1:
                bpm_handler_base.data.values[dat.dv1_dly2_min_val] = key
        for key, value in bpm_handler_base.data.values[dat.dv2_dly2].iteritems():
            if value == self.minval2:
                bpm_handler_base.data.values[dat.dv1_dly2_min_val] = key
        print bpm_handler_base.data.values[dat.dv1_dly2_min_val]
        print bpm_handler_base.data.values[dat.dv2_dly2_min_val]
        bpm_handler_base.data.values[dat.new_dly_2] = int(numpy.mean(bpm_handler_base.data.values[dat.dv1_dly2_min_val]))# + bpm_handler_base.data.values[dat.dv2_dly2_min_val])/2)
        self.set_dly_2(bpm_handler_base.data.values[dat.bpm_name],bpm_handler_base.data.values[dat.new_dly_2])
        print bpm_handler_base.data.values[dat.new_dly_2]
        self.read_delay(bpm_handler_base.data.values[dat.bpm_name])
        bpm_handler_base.data.values[dat.new_dly_2_set] = True