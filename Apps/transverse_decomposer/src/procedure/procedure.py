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
sys.path.append('\\\\claraserv3.dl.ac.uk\\claranet\\development\\CATAP\\djs56'
                '\\new_pc\\build\\PythonInterface\\Release\\CATAP') # meh
#sys.path.append('C:\\Users\\dlerlp\\Documents\\CATAP_Build\\PythonInterface\\Release\\')
from CATAP.EPICSTools import *
from CATAP.HardwareFactory import *
import json
import numpy

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
    #cam_name = "C2V-SCR-01"

    cam_fac = HF.getCameraFactory(cam_name)
    cam_obj = cam_fac.getCamera(cam_name)

    image_data_raw = None
    image_data = None
    array_data_num_pix_x = cam_obj.getArrayDataPixelCountX()
    array_data_num_pix_y = cam_obj.getArrayDataPixelCountY()
    roi_data_ref = cam_obj.getROIDataConstRef()

    def __init__(self):
        print(__name__ + ', class initialized')

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
        procedure.cam_obj.updateImageData()
        procedure.image_data_raw = procedure.cam_obj.getImageData()
        print(procedure.image_data_raw)
        npData = numpy.array(procedure.image_data_raw).reshape(
            (procedure.array_data_num_pix_y, procedure.array_data_num_pix_x))
        # never works :((((
        # npData = array(self.vc_image.data2D)
        # print('return image')
        procedure.image_data = numpy.flipud(npData)

# #TODO
#     add in ROI graphics overlays for teh read nad the set
#         and check they make sense for the ROI and teh mask!

    def get_roi_data(self):
        '''
        '''
        mask = self.get_mask()
        roi = self.get_ROI()

        print("mask")
        print(mask)
        print("roi")
        print(roi)

        procedure.roi_num_pix_x = procedure.cam_obj.getROISizeX()
        print("roi_num_pix_x = {}".format(procedure.roi_num_pix_x))
        #procedure.roi_num_pix_y = procedure.ET.get(procedure.roi_num_pix_y_pv)
        procedure.roi_num_pix_y = procedure.cam_obj.getROISizeY()
        print("roi_num_pix_y = {}".format(procedure.roi_num_pix_y))

        num_pix = procedure.roi_num_pix_x * procedure.roi_num_pix_y # + 1 # ha ! ;)
        procedure.cam_obj.updateROIData()
        procedure.roi_data_raw = procedure.cam_obj.getROIData()

        #procedure.roi_data_raw =  procedure.ET.getArray(procedure.roi_data_pv, num_pix)
        print("len( procedure.roi_data_raw = {}".format(len( procedure.roi_data_raw)))

        # for i in range(0,10):
        #     print( procedure.roi_data_raw[i] )
        # t = numpy.array(procedure.roi_data _raw)
        # for i in range(0,10):
        #     print( t[i] )
        #
        # t2 = t.reshape(procedure.roi_num_pix_y,procedure.roi_num_pix_x)
        # for i in range(0,10):
        #     print(t2[i] )
        # procedure.roi_dat = numpy.flipud(t2)
        #
        # for i in range(0,10):
        #     print( procedure.roi_dat[i] )
       # procedure.roi_data = self.chunk(procedure.roi_data_raw[:-1], procedure.roi_num_pix_x)
        npData = numpy.array(procedure.roi_data_raw).reshape(
            (procedure.roi_num_pix_y, procedure.roi_num_pix_x))
        #  never works :((((
        #  npData = array(self.vc_image.data2D)
        # print('return image')

        procedure.roi_data = numpy.flipud(npData)
        # print("len( procedure.roi_data[0] = {}".format(len( procedure.roi_data[0])))
        # print("len( procedure.roi_data = {}".format(len( procedure.roi_data)))
        print("len(procedure.roi_data_raw) = {} ".format(len(procedure.roi_data_raw)))
        print("len(procedure.roi_data) = {} ".format(len(procedure.roi_data)))
        print("procedure.roi_num_pix_x = {} ".format(procedure.roi_num_pix_x))
        print("procedure.roi_num_pix_y = {} ".format(procedure.roi_num_pix_y))
        print("num_pix = {} ".format(num_pix))
        print("max(procedure.roi_data_raw) = {} ".format(max(procedure.roi_data_raw)))
        print(procedure.roi_data)


    def set_roi_from_mask(self):
        print("set_roi_from_mask")
        # procedure.mask_x = procedure.ET.get(procedure.mask_x_pv)
        # procedure.mask_y = procedure.ET.get(procedure.mask_y_pv)
        # procedure.mask_centre_x = procedure.ET.get(procedure.mask_centre_x_pv)
        # procedure.mask_centre_y = procedure.ET.get(procedure.mask_centre_y_pv)
        # print("mask_x = {}, mask_y = {}, mask_centre_x = {}, mask_centre_y = {}".format(
        #     procedure.mask_x , procedure.mask_y, procedure.mask_centre_x,
        #        procedure.mask_centre_y))

        mask_catap = procedure.cam_obj.getMask()
        print("mask_catap")
        print(mask_catap)
        # set the ROI parameters based on the mask
        min_x = mask_catap["mask_x"] - mask_catap["mask_rad_x"]
        min_y = mask_catap["mask_y"] - mask_catap["mask_rad_y"]
        size_x = 2 * mask_catap["mask_rad_x"]
        size_y = 2 * mask_catap["mask_rad_x"]
        print("min_x={}, min_y={}, size_x={}, size_y={}".format(min_x, min_y, size_x, size_y))
        new_roi = {}
        new_roi["x_pos"] = min_x
        new_roi["y_pos"] = min_y
        new_roi["x_size"] = size_x
        new_roi["y_size"] = size_y

        if procedure.cam_obj.setMaskandROI(new_roi):
            print("SET ROI success??? ")
        else:
            print("FAILED TO SET ROI, passed keywords are incorrect! ")

        input()

        # min_x = procedure.mask_centre_x - procedure.mask_x
        # min_y = procedure.mask_centre_y - procedure.mask_y
        # size_x = 2 * procedure.mask_x
        # size_y = 2 * procedure.mask_y
        # print("min_x={}, min_y={}, size_x={}, size_y={}".format(min_x, min_y, size_x, size_y))
        # procedure.ET.put( procedure.size_x_pv, size_x )
        # procedure.ET.put( procedure.size_y_pv, size_y )
        # procedure.ET.put( procedure.min_x_pv, min_x )
        # procedure.ET.put( procedure.min_y_pv, min_y )

    def analyse(self):
        '''
            function to analyze the ROI data
        :return:
        '''
        print("analysehandle_analyse_button")