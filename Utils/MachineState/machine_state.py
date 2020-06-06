import os, sys
import numpy
import ruamel.yaml as yaml
import get_data_from_catap
import get_data_from_simframe
import write_data_to_catap
import write_data_to_simframe
import unit_conversion

class MachineState(object):

    def __init__(self):
        object.__init__(self)
        self.my_name="MachineState"
        self.getDataFromCATAP = get_data_from_catap.GetDataFromCATAP()
        self.getDataFromSimFrame = get_data_from_simframe.GetDataFromSimFrame()
        self.writeDataToCATAP = write_data_to_catap.WriteDataToCATAP()
        self.writeDataToSimFrame = write_data_to_simframe.WriteDataToSimFrame()
        self.unitConversion = unit_conversion.UnitConversion()
        self.pvAlias = {}
        self.CATAPInitialised = False
        self.SimFrameInitialised = False

    def initialiseCATAP(self, mode):
        if not self.CATAPInitialised:
            self.getDataFromCATAP.initCATAP(mode)
            self.CATAPInitialised = True
        else:
            print("CATAP already initialised")

    def getMachineStateFromCATAP(self, mode):
        if not self.CATAPInitialised:
            self.getDataFromCATAP.initCATAP(mode)
            self.CATAPInitialised = True
        self.allDicts = self.getDataFromCATAP.setAllDicts()
        self.allData = self.getDataFromCATAP.getAllData()
        self.getDataFromSimFrame.setSimulationDictDefaults(self.allData)
        return self.allData

    def getMachineStateFromSimFrame(self, directory, lattice):
        if not self.SimFrameInitialised:
            self.getDataFromSimFrame.loadFramework(directory)
            self.getDataFromSimFrame.loadLattice(lattice)
            self.SimFrameInitialised = True
        self.getDataFromSimFrame.getRunData()

    def getFramework(self):
        return self.getDataFromSimFrame.getFramework()

    def getBeamDistributionsFromSimFrame(self, directory):
        return self.getDataFromSimFrame.getAllBeamFiles(directory)

    def writeMachineStateToCATAP(self, mode, datadict, directory):
        if not self.CATAPInitialised:
            self.getDataFromCATAP.initCATAP(mode)
            self.CATAPInitialised = True
        self.allDicts = self.getDataFromCATAP.setAllDicts()
        self.allbeamfiles = self.getDataFromSimFrame.getAllBeamFiles(directory)
        self.writeDataToSimFrame.getLLRFEnergyGain(datadict)
        self.energy = self.writeDataToSimFrame.getEnergyDict()
        for i in datadict.keys():
            self.writeDataToCATAP.writeMachineStateToCATAP(mode, datadict[i], self.allbeamfiles, self.allDicts, self.energy)

    def writeMachineStateToSimFrame(self, directory, framework, lattice, datadict=None, type=None, mode=None, run=False):
        self.getMachineStateFromSimFrame(directory, lattice)
        if datadict is not None:
            self.datadict = datadict
            self.writeDataToSimFrame.modifyFramework(framework, self.datadict)
        else:
            if type == "SimFrame":
                self.datadict = self.getSimFrameDataDict()
            elif type == "CATAP":
                self.datadict = self.getMachineStateFromCATAP(mode)
            self.writeDataToSimFrame.modifyFramework(framework, self.datadict)
        if run == True:
            self.writeDataToSimFrame.runScript(framework, self.datadict, track=True)

    def getSimFrameDataDict(self):
        return self.getDataFromSimFrame.getDataDict()

    def initialiseSimFrameData(self):
        return self.getDataFromSimFrame.initialiseData()

    def setPVAliases(self, mode):
        if not self.CATAPInitialised:
            self.getMachineStateFromCATAP(mode)
        for key, value in self.allDicts.items():
            if value['simframe_alias'] is not None:
                self.pvAlias.update({key:value['simframe_alias']})

    def exportParameterValuesToYAMLFile(self, filename, data_dict, auto=False):
        self.export_dict = {}
        if not filename == "":
            for n in data_dict:
                self.export_dict = self.convertDataTypes(self.export_dict, data_dict[n], n)
            self.writeParameterOutputFile(str(filename), self.export_dict)
        else:
            print('Failed to export, please provide a filename.')

    def convertDataTypes(self, export_dict={}, data_dict={}, keyname=None):
        if keyname is not None:
            export_dict[keyname] = dict()
            edict = export_dict[keyname]
        else:
            edict = export_dict
        for key, value in data_dict.items():
            if isinstance(value, dict) and not key == 'sub_elements':
                subdict = self.convertDataTypes({}, value)
                edict.update({key:subdict})
            else:
                if not key == 'sub_elements':
                    # value = self.model.data.Framework.convert_numpy_types(value)
                    edict.update({key:value})
        return export_dict

    def parseParameterInputFile(self, filename):
        with open(filename, 'r') as stream:
            yaml_parameter_dict = yaml.safe_load(stream)
            return yaml_parameter_dict

    def writeParameterOutputFile(self, filename, parameter_dict):
        with open(filename, 'w') as output_file:
            # default flow-style = FALSE allows us to write our python dict out
            # in the key-value mapping that is standard in YAML. If this is set
            # to true; the output looks more like JSON, so best to leave it.
            yaml.dump(parameter_dict, output_file, default_flow_style=False)
            # currently the values that are output for each key will be surrounding with ''
            # which does not matter for this purpose as everything gets put into a string
            # format anyway. It may just introduce inconsistencies between hand-written and
            # computer-generated YAML files, but we can deal with that when a problem arises.