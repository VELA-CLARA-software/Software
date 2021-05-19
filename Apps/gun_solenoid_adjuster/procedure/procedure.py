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
//  Last edit:   05-06-2018
//  FileName:    procedure.oy
//  Description: Generic template for procedure class for High Level Application
//
//
//*/
'''
from VELA_CLARA_Magnet_Control import MAG_PSU_STATE
import VELA_CLARA_Magnet_Control as mag
import VELA_CLARA_RF_Protection_Control  as prot
import os
import csv

class procedure(object):
    # initDAQ = daq.init()
    mag_init = mag.init()
    mag_init.setVerbose()
    #mag_init.setQuiet()
    mc = mag_init.physical_CLARA_PH1_Magnet_Controller()

    prot_init = prot.init()
    prot_init.setVerbose()
    prot_init.setQuiet()
    rfp = prot_init.physical_Gun_Protection_Controller()
    #objects["gun_prot"] = rfp.getRFProtObjConstRef()

    objects = {}
    objects["bsol"] = mc.getMagObjConstRef("LRG-BSOL")
    objects["sol"] = mc.getMagObjConstRef("LRG-SOL")

    # this dict  will be used by the view to update states
    data = {}
    data["can_degauss"] = False
    data["sol_seti_has_focus"] = False
    data["bsol_seti_has_focus"] = False


    def __init__(self):
        self.get_settings()


    def get_settings(self):
        file_path = os.path.join(os.getcwd(),"settings.txt")
        print("file_path = ",file_path)

        try:
            with open(file_path, mode='r') as inp:
                reader = csv.reader(inp)
                settings_dict = {rows[0]:float(rows[1]) for rows in reader}
            print(settings_dict)
        except:
            print("Settings file does not exist!")
            settings_dict = {'min_sol': 139.5, 'max_bsol': -125.5, 'max_sol': 210,
                             'min_bsol': -190}
        self.min_sol = settings_dict["min_sol"]
        self.max_sol =  settings_dict["max_sol"]
        self.min_bsol =  settings_dict["min_bsol"]
        self.max_bsol =  settings_dict["max_bsol"]



    # called external to update states
    def sol_seti(self, val):
        print(__name__," sol_seti")
        if val >= self.min_sol:
            if val <= self.max_sol:
                print("Set new sol val = ", val)
                procedure.objects["sol"].SI = val

    def bsol_seti(self, val):
        print(__name__," bsol_seti")
        if val >= self.min_bsol:
            if val <= self.max_bsol:
                print("Set new bsol val = ", val)
                procedure.objects["bsol"].SI = val


    def degauss(self, name, to_zero):
        if procedure.data["can_degauss"]:
            self.mc.degauss(name, to_zero)
        else:
            print("can't degauss")

    def toggle_psu(self, name):
        if procedure.objects[name].psuState == MAG_PSU_STATE.MAG_PSU_ON:
            procedure.objects[name].PSU = MAG_PSU_STATE.MAG_PSU_OFF
        elif procedure.objects[name].psuState == MAG_PSU_STATE.MAG_PSU_OFF:
            procedure.objects[name].PSU = MAG_PSU_STATE.MAG_PSU_ON
        else:
            print("ERROR tooggle psu state = ", procedure.objects[name].PSU)

    def update_data(self):
        #print(__name__," update_data")
        procedure.data["sol_seti"] = procedure.objects["sol"].SI
        procedure.data["sol_readi"] = procedure.objects["sol"].riWithPol
        procedure.data["sol_psu"] = procedure.objects["sol"].psuState
        procedure.data["sol_is_degaussing"] = procedure.objects["sol"].isDegaussing

        procedure.data["bsol_seti"] = procedure.objects["bsol"].SI
        procedure.data["bsol_readi"] = procedure.objects["bsol"].riWithPol
        procedure.data["bsol_psu"] = procedure.objects["bsol"].psuState
        procedure.data["bsol_is_degaussing"] = procedure.objects["bsol"].isDegaussing


        #procedure.data["rf_prot"] = procedure.objects["gun_prot"].isGood
        procedure.data["rf_prot"] = procedure.rfp.isGood("CLARA_LRRG")

        if procedure.data["rf_prot"]:
            procedure.data["can_degauss"] = False
        else:
            procedure.data["can_degauss"] = True
