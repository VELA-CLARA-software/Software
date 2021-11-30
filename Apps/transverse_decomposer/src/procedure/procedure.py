'''
/*
//              This file is part of VELA-CLARA-Software.                             //
//------------------------------------------------------------------------------------//
//    VELA-CLARA-Software is free software: you can redistribute it and/or modify     //
//    it under the terms of the GNU General Public License as published by            //
//    the Free Software Foundation, either version 3 of the License, or               //
//    (at your option) any later version.                                             //
//    VELA-CLARA-Software is distributed in the hope that it will be useful,          //
//    but WITHOUT ANY WARRANTY; without even the implied warranty of                  //
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                   //
//    GNU General Public License for more details.                                    //
//                                                                                    //
//    You should have received a copy of the GNU General Public License               //
//    along with VELA-CLARA-Software.  If not, see <http://www.gnu.org/licenses/>.    //
//
//  Author:      DJS
//  Last edit:   24-11-2020
//  FileName:    procedure.oy
//  Description: Procedure for simple laser transverse profile  decomposition
//*/
'''
import sys
# sys.path.append('\\\\claraserv3\\claranet\\test\\CATAP\\bin')

#sys.path.append('\\\\claraserv3.dl.ac.uk\\claranet\\test\\CATAP\\bin') # meh
import numpy as np

sys.path.append('\\\\claraserv3.dl.ac.uk\\claranet\\development\\CATAP\\djs56'
                '\\new_pc\\build\\PythonInterface\\Release\\CATAP') # meh
#sys.path.append('C:\\Users\\dlerlp\\Documents\\CATAP_Build\\PythonInterface\\Release\\')
from CATAP.EPICSTools import *
from CATAP.HardwareFactory import *
import json
import numpy
from src.procedure.allbeamqualitymetrics import *


class procedure(object):
    '''
        A procedure class. This class is the 'model' in the Model-View_controller paradigm.  it
        instantiates and interfaces to  CATAP from which you can get data
    '''
    #  create a hardware factory for PHYSICAL CLARA
    #
    # Adding a STATE argument will specify which EPICS instance to use.
    ET = EPICSTools(STATE.PHYSICAL)

    roi_data_pv = 'CLA-VCA-DIA-CAM-01:CAM3:ArrayData'
    roi_num_pix_x_pv = 'CLA-VCA-DIA-CAM-01:ROI1:SizeX_RBV'
    roi_num_pix_y_pv = 'CLA-VCA-DIA-CAM-01:ROI1:SizeY_RBV'



    roi_data = None
    roi_num_pix_x = None
    roi_num_pix_y = None

    mask_x_pv = 'CLA-VCA-DIA-CAM-01:ANA:MaskXRad_RBV'
    mask_y_pv = 'CLA-VCA-DIA-CAM-01:ANA:MaskYRad_RBV'
    mask_centre_x_pv = 'CLA-VCA-DIA-CAM-01:ANA:MaskXCenter_RBV'
    mask_centre_y_pv = 'CLA-VCA-DIA-CAM-01:ANA:MaskYCenter_RBV'
    mask_x = None
    mask_y = None
    mask_centre_x = None
    mask_centre_y = None

    size_x_pv = 'CLA-VCA-DIA-CAM-01:ROI1:SizeX'
    size_y_pv = 'CLA-VCA-DIA-CAM-01:ROI1:SizeY'
    min_x_pv = 'CLA-VCA-DIA-CAM-01:ROI1:MinX'
    min_y_pv = 'CLA-VCA-DIA-CAM-01:ROI1:MinY'

    HF = HardwareFactory(STATE.PHYSICAL)

    cam_name = "VIRTUAL_CATHODE"
    #cam_name = "INJ-CAM-04"
    #cam_name = "BA1-YAG-01"

    cam_fac = HF.getCameraFactory(cam_name)
    cam_obj = cam_fac.getCamera(cam_name)

    image_data_raw = None
    full_image_data = None
    array_data_num_pix_x = cam_obj.getArrayDataPixelCountX()
    array_data_num_pix_y = cam_obj.getArrayDataPixelCountY()
    binary_data_num_pix_x = cam_obj.getBinaryDataPixelCountX()
    binary_data_num_pix_y = cam_obj.getBinaryDataPixelCountY()

    pix2mmX = cam_obj.getpix2mmX()
    pix2mmY = cam_obj.getpix2mmY()

    roi_data_ref = cam_obj.getROIDataConstRef()

    print("cam_name = {}".format(cam_name))
    print("array_data_num_pix_x = {}".format(array_data_num_pix_x))
    print("array_data_num_pix_y = {}".format(array_data_num_pix_y))

    def __init__(self):
        self.start_acquiring_analysing_etc()

        print(__name__ + ', class initialized')

    def get_full_image_paramters(self):
        r = {}
        r["array_data_num_pix_x"] = procedure.array_data_num_pix_x
        r["array_data_num_pix_y"] = procedure.array_data_num_pix_y
        r["binary_data_num_pix_x"] = procedure.binary_data_num_pix_x
        r["binary_data_num_pix_y"] = procedure.binary_data_num_pix_y
        r["pix2mmX"] = procedure.pix2mmX
        r["pix2mmY"] = procedure.pix2mmY
        return r

    def getAnalysisData(self):
        analysis_data = procedure.cam_obj.getAnalysisData()
        return analysis_data

    def start_acquiring_analysing_etc(self):
        procedure.cam_obj.startAcquiring()
        procedure.cam_obj.startAnalysing()
        procedure.cam_obj.useNPoint(True)
        procedure.cam_obj.setStepSize(5)

    def chunk(self, a, n):
        '''
            custom  list chunking  function, or get one from np when you can be bothered
        :param a: data to split
        :param n: chunk size
        :return: chunked array of a
        '''
        k, m = divmod(len(a), n)
        return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

    def print_values(self):
        print(self.get_mask())
        print(self.get_ROI())
        print(self.get_mask_and_ROI())

    def get_mask(self):
        return procedure.cam_obj.getMask()

    def get_ROI(self):
        return procedure.cam_obj.getROI()

    def get_mask_and_ROI(self):
        return procedure.cam_obj.getMaskandROI()

    def get_image(self):
        print("get_image")
        procedure.cam_obj.updateImageData()
        procedure.image_data_raw = procedure.cam_obj.getImageData()
        print(len(procedure.image_data_raw))
        print(procedure.array_data_num_pix_x)
        print(procedure.array_data_num_pix_y)
        npData = numpy.array(procedure.image_data_raw).reshape(
            (procedure.array_data_num_pix_y, procedure.array_data_num_pix_x))
        # never works :((((
        # npData = array(self.vc_image.data2D)
        # print('return image')
        procedure.full_image_data = np.flipud(npData)
        #procedure.full_image_data = npData

    def set_mask_ROI(self, roi_x, roi_y, x_rad, y_rad, **kwargs):
        r = {}
        r["roi_x"] = roi_x
        r["roi_y"] = roi_y
        r["x_rad"] = x_rad
        r["y_rad"] = y_rad
        return procedure.cam_obj.setMaskandROI(r)

    def get_roi_data(self):
        '''
        '''
        procedure.roi_num_pix_x = procedure.cam_obj.getROISizeX()
        print("roi_num_pix_x = {}".format(procedure.roi_num_pix_x))
        procedure.roi_num_pix_y = procedure.cam_obj.getROISizeY()
        print("roi_num_pix_y = {}".format(procedure.roi_num_pix_y))
        num_pix = procedure.roi_num_pix_x * procedure.roi_num_pix_y # + 1 # ha ! ;)
        procedure.cam_obj.updateROIData()
        procedure.roi_data_raw = procedure.cam_obj.getROIData()
        npData = numpy.array(procedure.roi_data_raw).reshape(
            (procedure.roi_num_pix_y, procedure.roi_num_pix_x))
        # never works :((((
        # npData = array(self.vc_image.data2D)
        # print('return image')
        procedure.roi_data = numpy.flipud(npData)

    def get_mask(self):
        return procedure.cam_obj.getMask()

    def set_roi_from_mask(self):
        print("set_roi_from_mask")
        mask_catap = self.get_mask()
        print("mask_catap")
        print(mask_catap)
        # set the ROI parameters based on the mask
        # min_x = mask_catap["mask_x"] - mask_catap["mask_rad_x"]
        # min_y = mask_catap["mask_y"] - mask_catap["mask_rad_y"]
        # size_x = 2 * mask_catap["mask_rad_x"]
        # size_y = 2 * mask_catap["mask_rad_x"]
        # print("min_x={}, min_y={}, size_x={}, size_y={}".format(min_x, min_y, size_x, size_y))
        new_roi = {}
        new_roi["roi_x"] = mask_catap["mask_x"]# + mask_catap["mask_rad_x"]
        new_roi["roi_y"] = mask_catap["mask_y"]# + mask_catap["mask_rad_y"]
        new_roi["x_rad"] = mask_catap["mask_rad_x"]
        new_roi["y_rad"] = mask_catap["mask_rad_y"]
        if self.set_mask_ROI(**new_roi):
            print("SET ROI success??? ")
        else:
            print("FAILED TO SET ROI, passed keywords are incorrect! ")

    def get_analysis_results(self):
        return procedure.cam_obj.getAnalysisResultsPixels()


    def analyse(self):
        '''
            function to analyze the ROI data
        :return:
        '''
        print("analysehandle_analyse_button")

        pix_data =self.get_analysis_results()
        roi_data =self.get_ROI()

        print("pix_data = {}".format(pix_data))
        print("roi_data = {}".format(roi_data))

        roi_beam_centre_x = pix_data["X"] - roi_data["x_min"]
        roi_beam_centre_y = pix_data["Y"] - roi_data["y_min"]
        roi_beam_width_x = pix_data["X_SIGMA"]
        roi_beam_width_y = pix_data["Y_SIGMA"]

        print("roi_beam_centre_x = {}".format(roi_beam_centre_x))
        print("roi_beam_centre_y = {}".format(roi_beam_centre_y))
        print("roi_beam_width_x = {}".format(roi_beam_width_x))
        print("roi_beam_width_y = {}".format(roi_beam_width_y))

        # widthi s3* RMS
        beam_width_x = (3*roi_beam_width_x)*(3*roi_beam_width_x)
        beam_width_y = (3*roi_beam_width_y)*(3*roi_beam_width_y)
        # add in quadrature fro radius
        beam_radius = np.sqrt(beam_width_x + beam_width_y)
        # print
        print("beam_width_x = {}".format(beam_width_x))
        print("beam_width_y = {}".format(beam_width_y))
        print("beam_radius = {}".format(beam_radius))
        #ROI_beam_center = 1

        input()

        beamquality(procedure.roi_data, [int(roi_beam_centre_x), int(roi_beam_centre_y)],
                    int(beam_radius))

