import os, sys, time
import numpy
import CATAP.HardwareFactory
import CATAP.EPICSTools
from CATAP.HardwareFactory import STATE
import src.unit_conversion as unit_conversion
import src.aliases as aliases

catap_modules = ['BPM', 'Charge', 'Screen', 'Magnet']
vc_controller_modules = ['Camera', 'LLRF', 'PILaser']

class GetDataFromCATAP(object):

    def __init__(self, buffer=False):
        object.__init__(self)
        self.my_name = "GetDataFromCATAP"
        self.unitConversion = unit_conversion.UnitConversion()
        self.alias_names = aliases.alias_names
        self.type_alias = aliases.type_alias
        self.screen_alias = aliases.screen_alias
        self.energy = {}
        self.magDict = {}
        self.gunRFDict = {}
        self.l01RFDict = {}
        self.pilaserDict = {}
        self.chargeDict = {}
        self.cameraDict = {}
        self.bpmDict = {}
        self.screenDict = {}
        self.allDataDict = {}
        self.allDictStatus = {}

        self.epics_tools_types = {'llrf': True,
                                  'camera': False}
        self.epics_tools_monitors = {}
        self.monitors = {}

        self.bpmdata = {}
        self.chargedata = {}
        self.cameradata = {}
        self.screendata = {}
        self.magnetdata = {}
        self.pildata = {}
        self.gundata = {}
        self.linacdata = {}
        self.alldata = {}
        self.default_lattice = ["INJ", "CLA-S01", "L01", "CLA-S02", "CLA-C2V", "EBT-INJ", "EBT-BA1", "VCA"]
        self.online_model_lattice = ["Gun", "Linac", "CLA-S02", "CLA-C2V", "EBT-INJ", "EBT-BA1"]
        for i in self.default_lattice:
            self.alldata.update({i: {}})
        self.alldataset = False
        self.use_online_model_lattice = False
        self.linacnames = {}
        self.gunStartTime = 1.0  # MAGIC NUMBER
        self.gunEndTime = 1.4  # MAGIC NUMBER
        self.linacStartTimes = {}
        self.linacEndTimes = {}
        self.guntraces = ['CAVITY_FORWARD_POWER']  # , "CAVITY_FORWARD_PHASE"]
        self.linactraces = ['CAVITY_FORWARD_POWER']  # , "CAVITY_FORWARD_PHASE"]
        self.gunDataSet = False
        self.linacDataSet = {}
        self.gunEnergyGain = 0.0
        self.linacEnergyGain = {}
        self.gun_length = 0.17  # MAGIC NUMBER (BUT IT WON'T CHANGE)
        self.gun_position = 0.17  # MAGIC NUMBER (BUT IT WON'T CHANGE)
        self.linac_length = {}
        self.linac_length.update({"L01": 2.033})  # MAGIC NUMBER (BUT IT WON'T CHANGE)
        self.linac_position = {}
        self.linac_position.update({"L01": 3.2269})  # MAGIC NUMBER (BUT IT WON'T CHANGE)

        self.CATAPmodeToVCControllermode = {}

        self.dictsSet = False

        def initCATAP(self, mode, crest_phases=None,
                      gun_calibration_data='\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\2021\\07\\27\\Gun_power_momentum_scan_cathode22.xlsx',
                      l01_calibration_data='\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\2021\\07\\28\\Linac_power_momentum_scan_cathode22.xlsx'):
        # setup environment
        if mode == 'VIRTUAL' or mode == CATAP.HardwareFactory.STATE.VIRTUAL:
            os.environ['EPICS_CA_ADDR_LIST'] = "192.168.83.246"
            os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
            os.environ['EPICS_CA_SERVER_PORT'] = "6020"
            os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "1000000000"
        elif mode == 'PHYSICAL' or mode == CATAP.HardwareFactory.STATE.PHYSICAL:
            os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255"
            # os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
            # os.environ["EPICS_CA_SERVER_PORT"] = "5064"
            os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000000"
        # get factories / controllers
        if mode == 'VIRTUAL' or mode == CATAP.HardwareFactory.STATE.VIRTUAL:
            self.mode = CATAP.HardwareFactory.STATE.VIRTUAL
        elif mode == 'PHYSICAL' or mode == CATAP.HardwareFactory.STATE.PHYSICAL:
            self.mode = CATAP.HardwareFactory.STATE.PHYSICAL
        else:
            self.mode = CATAP.HardwareFactory.STATE.OFFLINE
        self.hf = CATAP.HardwareFactory.HardwareFactory(self.mode)
        self.epics_tools = CATAP.HardwareFactory.EPICSTools(self.mode)

        self.llrf_types = [CATAP.HardwareFactory.TYPE.LRRG_GUN, CATAP.HardwareFactory.TYPE.L01]
        # self.gun_llrf_type = CATAP.HardwareFactory.TYPE.LRRG_GUN
        self.llrf_factory = self.hf.getLLRFFactory(self.llrf_types)
        time.sleep(1)
        # self.llrf_factory.messagesOff()
        # self.llrf_factory.debugMessagesOff()
        self.llrf_names = self.llrf_factory.getLLRFNames()
        self.gunname = self.llrf_names[0]
        self.linacnames = self.llrf_names[1:]
        self.gunLLRFObj = self.llrf_factory.getLLRF(self.llrf_names[0])
        time.sleep(1)
        # self.gunLLRFObj.messagesOff()
        # self.gunLLRFObj.debugMessagesOff()
        self.linacLLRFObj = {}
        if crest_phases is not None:
            self.crest_phases = crest_phases
        else:
            self.crest_phases = {}
            self.crest_phases.update({aliases.alias_names[self.gunname]: 0})
            for i in self.linacnames:
                self.crest_phases.update({aliases.alias_names[self.linacNameConvert(i)]: 0})
        if self.mode == CATAP.HardwareFactory.STATE.VIRTUAL:
            self.setGunStartEndTime(self.gunStartTime, self.gunEndTime)
        for key in self.linacnames:
            self.linacLLRFObj[key] = self.llrf_factory.getLLRF(key)
            time.sleep(1)
            # self.linacLLRFObj[key].messagesOff()
            # self.linacLLRFObj[key].debugMessagesOff()
            self.linacStartTimes.update({key: 0.1})  # MAGIC NUMBER
            self.linacEndTimes.update({key: 1.0})  # MAGIC NUMBER
            if self.mode == CATAP.HardwareFactory.STATE.VIRTUAL:
                self.setLinacStartEndTime(key, self.linacStartTimes[key], self.linacEndTimes[key])
            self.linacDataSet.update({key: False})
            self.linacEnergyGain.update({key: 0.0})
        self.chargeFac = self.hf.getChargeFactory()
        time.sleep(1)
        self.bpmFac = self.hf.getBPMFactory()
        time.sleep(1)
        self.scrFac = self.hf.getScreenFactory()
        time.sleep(1)
        self.magFac = self.hf.getMagnetFactory()
        time.sleep(1)
        # self.chargeFac.messagesOff()
        # self.chargeFac.debugMessagesOff()
        # self.bpmFac.messagesOff()
        # self.bpmFac.debugMessagesOff()
        # self.magFac.messagesOff()
        # self.magFac.debugMessagesOff()
        if self.mode == CATAP.HardwareFactory.STATE.VIRTUAL:
            self.magFac.switchOnAll()
        if not self.epics_tools_types['camera']:
            self.camFac = self.hf.getCameraFactory()
            time.sleep(1)
            # self.camFac.messagesOff()
            # self.camFac.debugMessagesOff()

        # #self.pilFac = hf.getPILa()
        # #self.camFac = hf.getcam()
        self.hf.debugMessagesOff()
        self.hf.messagesOff()
        if gun_calibration_data is not None:
            self.gun_calibrate = True
            self.gun_calibration_data = gun_calibration_data
        else:
            self.gun_calibration_data = None
        if l01_calibration_data is not None:
            self.l01_calibrate = True
            self.l01_calibration_data = l01_calibration_data
        else:
            self.l01_calibration_data = None
        return True

    def useOnlineModelLattice(self, om=False):
        if om:
            self.use_online_model_lattice = True
            self.alldata = {}
            for i in self.online_model_lattice:
                self.alldata.update({i: {}})
        else:
            self.use_online_model_lattice = False

    def getMachineAreaString(self, name):
        # if "INJ" in name or "GUN" in name or "LRG1" in name:
        if "GUN" in name or "LRG1" in name:
            if self.use_online_model_lattice:
                return aliases.lattice_to_online_model["GUN"]
            else:
                return "INJ"
        elif "S01" in name:
            if self.use_online_model_lattice:
                return aliases.lattice_to_online_model["CLA-S01"]
            else:
                return "CLA-S01"
        elif "S02" in name:
            if self.use_online_model_lattice:
                return aliases.lattice_to_online_model["CLA-S02"]
            else:
                return "CLA-S02"
        elif "L01" in name:
            if self.use_online_model_lattice:
                return aliases.lattice_to_online_model["L01"]
            else:
                return "L01"
        elif "C2V" in name:
            if self.use_online_model_lattice:
                return aliases.lattice_to_online_model["CLA-C2V"]
            else:
                return "CLA-C2V"
        elif "EBT" in name:
            if "BA1" in name:
                if self.use_online_model_lattice:
                    return aliases.lattice_to_online_model["EBT-BA1"]
                else:
                    return "EBT-BA1"
            elif "INJ" in name:
                if self.use_online_model_lattice:
                    return aliases.lattice_to_online_model["EBT-INJ"]
                else:
                    return "EBT-INJ"
        elif "VCA" in name:
            if self.use_online_model_lattice:
                return aliases.lattice_to_online_model["VCA"]
            else:
                return "VCA"

    def setBPMDict(self):
        self.bpmnames = self.bpmFac.getAllBPMNames()
        for i in self.bpmnames:
            self.bpmDict[i] = self.bpmFac.getBPM(i)
        self.allDataDict.update({"BPM": self.bpmDict})

    def setMagDict(self):
        self.magnames = self.magFac.getAllMagnetNames()
        for i in self.magnames:
            self.magDict[i] = self.magFac.getMagnet(i)
        self.allDataDict.update({"Magnet": self.magDict})

    def setChargeDict(self):
        # self.chargenames = self.chargeFac.getAllChargeDiagnosticNames()
        self.chargenames = ['CLA-S01-DIA-WCM-01']
        for i in self.chargenames:
            self.chargeDict[i] = self.chargeFac.getChargeDiagnostic(i)
        self.allDataDict.update({"Charge": self.chargeDict})

    def setCameraDict(self):
        if not self.epics_tools_types['camera']:
            self.camnames = self.camFac.getCameraNames()
            for i in self.camnames:
                self.cameraDict[i] = self.camFac.getCamera(i)
                if i == "CLA-VCA-DIA-CAM-01" and self.mode == CATAP.HardwareFactory.STATE.VIRTUAL:
                    self.cameraDict[i].setX(0)
                    self.cameraDict[i].setY(0)
                    self.cameraDict[i].setSigX(0.35)
                    self.cameraDict[i].setSigY(0.35)
                    self.cameraDict[i].setSigXY(0.35)
            self.allDataDict.update({"Camera": self.cameraDict})
        else:
            self.camnames = list(aliases.screen_to_camera.values())
            self.vc_name = 'CLA-VCA-DIA-CAM-01'
            self.camnames.append(self.vc_name)
            for name in self.camnames:
                self.epics_tools_monitors[name] = {}
                for key, value in aliases.camera_epics_tools.items():
                    self.epics_tools.monitor(name + ':ANA:' + value)
                    self.epics_tools_monitors[name][key] = self.epics_tools.getMonitor(name + ':ANA:' + value)
                self.cameraDict[name] = self.epics_tools_monitors[name]

    def setScreenDict(self):
        self.screennames = self.scrFac.getAllScreenNames()
        for i in self.screennames:
            self.screenDict[i] = self.scrFac.getScreen(i)
        self.allDataDict.update({"Screen": self.screenDict})

    def setGunLLRFDict(self):
        self.allDataDict.update({"LRRG_GUN": self.gunLLRFObj})
        self.gunLLRFObj.startTraceMonitoring()
        if self.epics_tools_types['llrf']:
            self.epics_tools_monitors[self.llrf_names[0]] = {}
            for key, value in aliases.llrf_epics_tools.items():
                self.epics_tools.monitor(self.llrf_names[0] + ':' + value)
                self.epics_tools_monitors[self.llrf_names[0]][key] = self.epics_tools.getMonitor(
                    self.llrf_names[0] + ':' + value)

    def linacNameConvert(self, key):
        if key == 'CLA-L01-LRF-CTRL-01':
            return 'L01'
        else:
            return key

    def setLinacLLRFDict(self):
        for key in self.linacnames:
            self.keyupdate = self.linacNameConvert(key)
            self.linacLLRFObj[self.keyupdate] = self.llrf_factory.getLLRF(key)
            self.linacdata.update({self.keyupdate: {}})
            self.allDataDict.update({self.keyupdate: self.linacLLRFObj[self.keyupdate]})
            if self.epics_tools_types['llrf']:
                self.epics_tools_monitors[key] = {}
                for key1, value in aliases.llrf_epics_tools.items():
                    self.epics_tools.monitor(key + ':' + value)
                    self.epics_tools_monitors[key][key1] = self.epics_tools.getMonitor(key + ':' + value)

    def setAllDicts(self):
        self.setBPMDict()
        self.setMagDict()
        self.setChargeDict()
        self.setCameraDict()
        self.setScreenDict()
        self.setGunLLRFDict()
        self.setLinacLLRFDict()
        self.dictsSet = True
        return self.allDataDict

    def getBPMData(self, name):
        if self.dictsSet:
            self.bpmdata[name] = {}
            self.bpmdata[name]['x'] = self.bpmDict[name].x
            self.bpmdata[name]['y'] = self.bpmDict[name].y
            self.bpmdata[name]['q'] = self.bpmDict[name].q
            self.bpmdata[name]['resolution'] = self.bpmDict[name].resolution
            self.bpmdata[name]['type'] = "bpm"
            # self.bpmdata[name]['status'] = aliases.state_alias[self.bpmFac.getStatus(name)]
            self.alldata[self.getMachineAreaString(name)].update({name: self.bpmdata[name]})
        else:
            self.setAllDicts()
            self.getBPMData(name)

    def getCameraData(self, name):
        if self.dictsSet:
            self.cameradata[name] = {}
            if not self.epics_tools_types['camera']:
                self.cameradata[name]['acquiring'] = self.cameraDict[name].isAcquiring()
                self.cameradata[name]['screen'] = self.cameraDict[name].getScreen()
                if self.cameradata[name]['screen'] in self.screen_alias.keys():
                    self.cameradata[name].update({'screen': self.screen_alias[self.cameradata[name]['screen']]})
                if self.cameradata[name]['acquiring'] or name == 'CLA-VCA-DIA-CAM-01':
                    self.cameradata[name]['x_pix_abs'] = self.cameraDict[name].getXPix()
                    self.cameradata[name]['y_pix_abs'] = self.cameraDict[name].getYPix()
                    self.cameradata[name]['x_pix'] = self.cameradata[name]['x_pix_abs'] - \
                                                     aliases.vc_mechanical_centre[
                                                         'x_pix']
                    self.cameradata[name]['y_pix'] = self.cameradata[name]['y_pix_abs'] - \
                                                     aliases.vc_mechanical_centre[
                                                         'y_pix']
                    # self.cameradata[name]['xy_pix'] = self.cameraDict[name].getXYPix()
                    self.cameradata[name]['x_mm_abs'] = self.cameraDict[name].getXmm()
                    self.cameradata[name]['y_mm_abs'] = self.cameraDict[name].getYmm()
                    self.cameradata[name]['x_mm'] = self.cameradata[name]['x_mm_abs'] - \
                                                    aliases.vc_mechanical_centre[
                                                        'x_mm']
                    self.cameradata[name]['y_mm'] = self.cameradata[name]['y_mm_abs'] - \
                                                    aliases.vc_mechanical_centre[
                                                        'y_mm']
                    # self.cameradata[name]['xy_mm'] = self.cameraDict[name].getXYmm()
                    self.cameradata[name]['x_pix_sig'] = self.cameraDict[name].getSigXPix()
                    self.cameradata[name]['y_pix_sig'] = self.cameraDict[name].getSigYPix()
                    # self.cameradata[name]['xy_pix_sig'] = self.cameraDict[name].getSigXYPix()
                    self.cameradata[name]['x_mm_sig'] = self.cameraDict[name].getSigXmm()
                    self.cameradata[name]['y_mm_sig'] = self.cameraDict[name].getSigYmm()
                    # self.cameradata[name]['xy_mm_sig'] = self.cameraDict[name].getSigXYmm()
                    self.cameradata[name]['sum_intensity'] = self.cameraDict[name].getSumIntensity()
                    self.cameradata[name]['avg_intensity'] = self.cameraDict[name].getAvgIntensity()
            else:
                for key, value in aliases.camera_epics_tools.items():
                    self.cameradata[name][key] = float(
                        numpy.mean(self.epics_tools_monitors[name][key].getBuffer()))
            self.cameradata[name]['type'] = "camera"
            self.alldata[self.getMachineAreaString(name)].update({name: self.cameradata[name]})
        else:
            self.setAllDicts()
            self.getCameraData(name)

    def getChargeData(self, name):
        if self.dictsSet:
            self.chargedata[name] = {}
            self.chargedata[name]['q'] = self.chargeDict[name].q
            self.chargedata[name]['type'] = "charge"
            self.alldata[self.getMachineAreaString(name)].update({name: self.chargedata[name]})
        else:
            self.setAllDicts()
            self.getChargeData(name)

    def getScreenData(self, name):
        if self.dictsSet:
            self.screendata[name] = {}
            self.screendata[name]['state'] = str(self.screenDict[name].screenState)
            self.screendata[name]['type'] = "screen"
            self.alldata[self.getMachineAreaString(name)].update({name: self.screendata[name]})
        else:
            self.setAllDicts()
            self.getScreenData(name)

    def getMagnetData(self, name, energy):
        if self.dictsSet:
            self.magnetdata[name] = {}
            self.magnetdata[name]['READI'] = self.magDict[name].READI
            self.magnetdata[name]['SETI'] = self.magDict[name].getSETI()
            self.magnetdata[name]['type'] = self.type_alias[self.magFac.getMagnetType(name)]
            self.magnetdata[name]['psu_state'] = str(self.magDict[name].psu_state)
            # self.magnetdata[name]['field_integral_coefficients'] = []
            # self.magnetdata[name]['field_integral_coefficients'] = self.magDict[name].getFieldIntegralCoefficients()
            self.fic = self.magDict[name].getFieldIntegralCoefficients()
            self.seen = set()
            self.seen_add = self.seen.add
            self.ficmod =  [x for x in self.fic if not (x in self.seen or self.seen_add(x))]
            self.magnetdata[name]['field_integral_coefficients'] = self.ficmod
            self.magnetdata[name]['magnetic_length'] = self.magDict[name].magnetic_length * 1
            self.energy_at_magnet = 0
            if "GUN" in name or "LRG1" in name:
                self.energy_at_magnet = energy[self.gun_position]
            else:
                for key, value in energy.items():
                    if key < self.magDict[name].position:
                        self.energy_at_magnet += value
            if self.energy_at_magnet == 0:
                self.energy_at_magnet = energy[self.linac_position['L01']]
            self.unitConversion.currentToK(self.magnetdata[name]['type'],
                                           self.magDict[name].READI,
                                           self.magnetdata[name]['field_integral_coefficients'],
                                           self.magnetdata[name]['magnetic_length'],
                                           self.energy_at_magnet,
                                           self.magnetdata[name],
                                           psu_state=self.magnetdata[name]['psu_state'])
            self.magnetdata[name]['energy'] = self.energy_at_magnet
            self.magnetdata[name]['position'] = self.magDict[name].position
            self.alldata[self.getMachineAreaString(name)].update({name: self.magnetdata[name]})
        else:
            self.setAllDicts()
            self.getMagnetData(name)

    def setGunStartEndTime(self, start_time, end_time):
        self.gunStartTime = start_time
        self.gunEndTime = end_time
        for trace in self.guntraces:
            self.gunLLRFObj.setMeanStartEndTime(start_time, end_time, trace)

    def setLinacStartEndTime(self, name, start_time, end_time):
        for trace in self.linactraces:
            self.linacStartTimes[name] = start_time
            self.linacEndTimes[name] = end_time
            self.linacLLRFObj[name].setMeanStartEndTime(start_time, end_time, trace)

    def getGunLLRFData(self, crest=None):
        if self.dictsSet:
            if self.gunname in self.crest_phases.keys():
                if crest is not None:
                    self.gun_crest = crest
                else:
                    self.gun_crest = self.crest_phases[self.gunname]
            else:
                if crest is not None:
                    self.gun_crest = crest
                else:
                    self.gun_crest = self.crest_phases[aliases.alias_names[self.gunname]]
            if not self.epics_tools_types['llrf']:
                self.gunLLRFObj.updateTraceValues()
                # for trace in self.guntraces:
                    # self.gundata.update({trace: self.llrf_factory.getCavFwdPwr(self.gunname)})
                self.gundata.update({'crest': self.gun_crest})
                self.gundata.update({"phase_abs": self.gunLLRFObj.getPhi()})
                self.gundata.update({"phase": self.gundata['phase_abs'] - self.gun_crest})
                self.gundata.update({"amplitude_MW": max(self.llrf_factory.getCavFwdPwr(self.gunname))})
                self.gundata.update({"amplitude": self.gunLLRFObj.getAmp()})
                self.gunLLRFObj.stopTraceMonitoring()
            else:
                for key, value in aliases.llrf_epics_tools.items():
                    self.gundata[key] = float(
                        numpy.mean(self.epics_tools_monitors[self.llrf_names[0]][key].getBuffer()))
                self.gundata['amplitude_MW'] = self.gundata['klystron_amplitude_MW']
                self.gundata.update({'crest': self.gun_crest})
                self.gundata['phase_abs'] = self.gundata['phase_sp']
                self.gundata.update({"phase": self.gundata['phase_abs'] - self.gun_crest})
            self.pulse_length = 2.5
            self.getenergy = self.unitConversion.getEnergyGain(self.gunname,
                                                               self.gundata['amplitude_MW'],
                                                               self.gundata['phase'],
                                                               self.pulse_length,
                                                               self.gun_length,
                                                               calibrate=self.gun_calibration_data)
            self.gundata.update({"energy_gain": float(self.getenergy[0])})
            self.gundata.update({"field_amplitude": self.getenergy[1]})
            self.gundata.update({"type": 'cavity'})
            self.gundata.update({"length": self.gun_length})
            self.gundata.update({"pulse_length": self.pulse_length})
            self.gundata.update({"catap_alias": self.gunname})
            self.alldata[self.getMachineAreaString(self.gunname)].update({self.gunname: self.gundata})
            self.gunDataSet = True
        else:
            self.setAllDicts()
            self.getGunLLRFData()

    def getLinacLLRFData(self, linac_name, crest = None):
        if self.dictsSet:
            self.linacname = self.linacNameConvert(linac_name)
            if self.linacname in self.crest_phases.keys():
                if crest is not None:
                    self.linac_crest = crest
                else:
                    self.linac_crest = self.crest_phases[self.linacname]
            else:
                if crest is not None:
                    self.linac_crest = crest
                else:
                    self.linac_crest = self.crest_phases[aliases.alias_names[self.linacname]]
            if not self.epics_tools_types['llrf']:
                self.linacLLRFObj[self.linacname].updateTraceValues()
                for trace in self.linactraces:
                    self.linacdata[self.linacname].update({trace: self.llrf_factory.getCutMean(linac_name, trace)})
                # self.linacdata[self.linacname].update({trace: self.linacdata[self.linacname][trace]})
                self.linacdata[self.linacname].update({'crest': self.linac_crest})
                self.linacdata[self.linacname].update({"phase_abs": self.linacLLRFObj[self.linacname].getPhi()})
                self.linacdata[self.linacname].update(
                    {"phase": self.linacdata[self.linacname]['phase_abs'] - self.linac_crest})
                self.linacdata[self.linacname].update({"amplitude_MW": self.linacLLRFObj[self.linacname].getAmpMW()})
                self.linacdata[self.linacname].update({"amplitude": self.linacLLRFObj[self.linacname].getAmp()})
            else:
                for key, value in aliases.llrf_epics_tools.items():
                    self.linacdata[self.linacname][key] = float(numpy.mean(
                        self.epics_tools_monitors[linac_name][key].getBuffer()))
                self.linacdata[self.linacname]['amplitude_MW'] = self.linacdata[self.linacname]['klystron_amplitude_MW']
                self.linacdata[self.linacname].update({'crest': self.linac_crest})
                self.linacdata[self.linacname]['phase_abs'] = self.linacdata[self.linacname]['phase_sp']
                self.linacdata[self.linacname]['phase'] = self.linacdata[self.linacname]['phase_abs'] - \
                                                          self.linac_crest
            self.pulse_length = 0.75
            self.getenergy = self.unitConversion.getEnergyGain(linac_name,
                                                               self.linacdata[self.linacname]['amplitude_MW'],
                                                               self.linacdata[self.linacname]['phase'],
                                                               0.75,
                                                               self.linac_length[self.linacname],
                                                               calibrate=self.l01_calibration_data)
            # self.linacdata[linac_name].update({"phase":self.linacdata[linac_name]["CAVITY_FORWARD_PHASE"]})
            self.linacdata[self.linacname].update({"energy_gain": float(self.getenergy[0])})
            self.linacdata[self.linacname].update({"field_amplitude": self.getenergy[1]})
            self.linacdata[self.linacname].update({"type": 'cavity'})
            self.linacdata[self.linacname].update({"length": self.linac_length[self.linacname]})
            self.linacdata[self.linacname].update({"pulse_length": self.pulse_length})
            self.linacdata[self.linacname].update({"catap_alias": linac_name})
            self.alldata[self.getMachineAreaString(self.linacname)].update(
                {self.linacname: self.linacdata[self.linacname]})
            self.linacDataSet.update({self.linacname: True})

        else:
            self.setAllDicts()
            self.getLinacLLRFData(self.linacname)

    def setGunEnergyGain(self):
        if self.gunDataSet:
            self.gunEnergyGain = 1

    def setLinacEnergyGain(self, name):
        if self.linacDataSet[name]:
            self.linacEnergyGain[name] = 1

    def getEnergyDict(self):
        return self.energy

    def getAllData(self, crests=None):
        if self.dictsSet:
            if crests is not None:
                self.getGunLLRFData(crest=crests[aliases.alias_names[self.gunname]])
            else:
                self.getGunLLRFData()
            self.energy.update({self.gun_position: self.gundata['energy_gain']})
            for i in self.linacnames:
                self.linacname = self.linacNameConvert(i)
                if crests is not None:
                    self.getLinacLLRFData(i, crest=crests[aliases.alias_names[self.linacname]])
                else:
                    self.getLinacLLRFData(i)
                self.energy.update({self.linac_position[self.linacname]: self.linacdata[self.linacname]['energy_gain']})
            for i in self.bpmnames:
                self.getBPMData(i)
            for i in self.magnames:
                self.getMagnetData(i, self.energy)
            for i in self.chargenames:
                self.getChargeData(i)
            for i in self.screennames:
                self.getScreenData(i)
            for i in self.camnames:
                self.getCameraData(i)
            for i in self.alldata.keys():
                self.checkType(self.alldata[i])
                self.getSimFrameAlias(self.alldata[i])
        else:
            self.setAllDicts()
            self.getAllData()
        self.alldataset = True
        return self.alldata

    def getVCObject(self):
        if not self.alldataset:
            self.getAllData()
        else:
            if self.use_online_model_lattice:
                return self.alldata[aliases.lattice_to_online_model['VCA']]['CLA-VCA-DIA-CAM-01']
            else:
                print(self.alldata['VCA'])
                return self.alldata['VCA']['CLA-VCA-DIA-CAM-01']

    def getWCMObject(self):
        if not self.alldataset:
            self.getAllData()
        else:
            if self.use_online_model_lattice:
                return self.alldata[aliases.lattice_to_online_model['CLA-S01']]['CLA-S01-DIA-WCM-01']
            else:
                return self.alldata['CLA-S01']['CLA-S01-DIA-WCM-01']

    def checkType(self, datadict):
        for i in datadict.keys():
            for j in self.type_alias.keys():
                if isinstance(datadict[i], dict):
                    if 'type' in datadict[i].keys():
                        if datadict[i]['type'] == j:
                            datadict[i].update({'type': self.type_alias[j]})

    def getSimFrameAlias(self, datadict):
        for i in datadict.keys():
            if i in self.alias_names.keys():
                datadict[i]['simframe_alias'] = self.alias_names[i]

