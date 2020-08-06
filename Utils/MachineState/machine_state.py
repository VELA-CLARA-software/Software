import os, sys
import numpy
import ruamel.yaml as yaml
import get_data_from_catap
import get_data_from_simframe
import write_data_to_catap
import write_data_to_simframe
import unit_conversion
import aliases

# Main class for writing / reading the machine state from / to SimFrame / CATAP
class MachineState(object):

    def __init__(self):
        object.__init__(self)
        self.my_name="MachineState"
        self.getDataFromCATAP = get_data_from_catap.GetDataFromCATAP()
        self.getDataFromSimFrame = get_data_from_simframe.GetDataFromSimFrame()
        self.writeDataToCATAP = write_data_to_catap.WriteDataToCATAP()
        self.writeDataToSimFrame = write_data_to_simframe.WriteDataToSimFrame()
        self.unitConversion = unit_conversion.UnitConversion()
        self.screen_to_camera = aliases.screen_to_camera
        self.lattices = self.unitConversion.getLattices()
        self.pvAlias = {}
        self.CATAPInitialised = False
        self.SimFrameInitialised = False
        self.simulation_defaults_set = False

    # Initialises CATAP hardware factories
    def initialiseCATAP(self, mode):
        if not self.CATAPInitialised:
            self.getDataFromCATAP.initCATAP(mode)
            self.CATAPInitialised = True
        else:
            print("CATAP already initialised")

    # Reads the machine state from CATAP. See all functions below in GetDataFromCATAP class
    # Also sets defaults for the simulation
    def getMachineStateFromCATAP(self, mode):
        if not self.CATAPInitialised:
            self.getDataFromCATAP.initCATAP(mode)
            self.CATAPInitialised = True
        self.allDicts = self.getDataFromCATAP.setAllDicts()
        self.allData = self.getDataFromCATAP.getAllData()
        self.vc_object = self.getDataFromCATAP.getVCObject()
        self.wcm_object = self.getDataFromCATAP.getWCMObject()
        self.getDataFromSimFrame.setSimulationDictDefaults(self.allData,
                                                           vc_object=self.vc_object,
                                                           wcm_object=self.wcm_object)
        self.simulation_defaults_set = True
        return self.allData

    # Reads the machine state from SimFrame, given an input lattice
    # If there are already output files in 'directory', this function returns the beam distributions
    def getMachineStateFromSimFrame(self, directory, lattice):
        if not self.SimFrameInitialised:
            self.getDataFromSimFrame.loadFramework(directory)
            self.getDataFromSimFrame.loadLattice(lattice)
            self.SimFrameInitialised = True
        self.getDataFromSimFrame.getRunData()
        return self.getDataFromSimFrame.getAllBeamFiles(directory)

    # Returns the framework instance for running SimFrame
    def getFramework(self):
        return self.getDataFromSimFrame.getFramework()

    # Returns SimFrame beam distributions (if they exist)
    def getBeamDistributionsFromSimFrame(self, directory):
        return self.getDataFromSimFrame.getAllBeamFiles(directory)

    # Returns dictionary with all CATAP objects
    # Input: mode: CATAP STATE (physical / virtual)
    # Output: CATAP dictionary, keyed by type
    def getCATAPDict(self, mode):
        if not self.CATAPInitialised:
            self.getDataFromCATAP.initCATAP(mode)
            self.CATAPInitialised = True
        self.allDicts = self.getDataFromCATAP.setAllDicts()
        return self.allDicts

    def getEnergyGainFromCATAP(self):
        return self.getDataFromCATAP.getEnergyDict()

    # Writes the machine state to CATAP
    # Inputs: mode: CATAP STATE (physical / virtual)
    #         datadict: machine state file
    #         directory: location of simulated beam distributions
    def writeMachineStateToCATAP(self, mode, datadict, directory, sections=None):
        if not self.CATAPInitialised:
            self.getDataFromCATAP.initCATAP(mode)
            self.CATAPInitialised = True
        self.allDicts = self.getDataFromCATAP.setAllDicts()
        self.allbeamfiles = self.getDataFromSimFrame.getAllBeamFiles(directory)
        self.writeDataToSimFrame.getLLRFEnergyGain(datadict)
        self.energy = self.writeDataToSimFrame.getEnergyDict()
        if sections==None:
            self.sections_to_write = datadict.keys()
        else:
            self.sections_to_write = sections
        for i in self.sections_to_write:
            self.writeDataToCATAP.writeMachineStateToCATAP(mode, datadict[i], self.allbeamfiles, self.allDicts, self.energy)

    # Writes the machine state file to SimFrame. Requires the framework to be initialised, and a simulation lattice file
    # Inputs: directory: location of output beam distributions
    #         framework: SimFrame instance
    #         lattice: lattice to run
    #         datadict: machine state file to set simulation parameters
    #         type: get machine state from SimFrame or CATAP (if no file provided)
    #         mode: CATAP state (physical / virtual)
    #         run: do SimFrame tracking?
    # Output: returns the machine state file w/ average beam distributions and file locations
    def writeMachineStateToSimFrame(self, directory, framework, lattice, datadict=None,
                                    type=None, mode=None, run=False, sections=None):
        if sections==None:
            sections = self.lattices
        #self.getMachineStateFromSimFrame(directory, lattice)
        if datadict is not None:
            self.datadict = datadict
            self.writeDataToSimFrame.modifyFramework(framework, self.datadict, type=type)
        else:
            if type == "SimFrame":
                self.datadict = self.getSimFrameDataDict()
            elif type == "CATAP":
                self.datadict = self.getMachineStateFromCATAP(mode)
            self.writeDataToSimFrame.modifyFramework(framework, self.datadict, type=type)
        if run == True:
            if not os.path.isdir(directory):
                os.makedirs(directory)
            self.datadict['simulation']['directory'] = directory
            self.writeDataToSimFrame.runScript(framework, self.datadict, track=True)
            self.allbeamfiles = self.getDataFromSimFrame.getAllBeamFiles(directory)
            for i in self.allbeamfiles.keys():
                for j in sections:
                    if (self.allbeamfiles[i]['type'] == 'screen') and (i in self.datadict[j].keys()):
                        self.datadict[j][self.screen_to_camera[i]].update({'x_mm': self.allbeamfiles[i]['x']['mean']})
                        self.datadict[j][self.screen_to_camera[i]].update({'y_mm': self.allbeamfiles[i]['y']['mean']})
                        self.datadict[j][self.screen_to_camera[i]].update({'x_mm_sig': self.allbeamfiles[i]['x']['sigma']})
                        self.datadict[j][self.screen_to_camera[i]].update({'y_mm_sig': self.allbeamfiles[i]['y']['sigma']})
                        self.datadict[j][self.screen_to_camera[i]].update({'x_mean': self.allbeamfiles[i]['x']['mean']})
                        self.datadict[j][self.screen_to_camera[i]].update({'y_mean': self.allbeamfiles[i]['y']['mean']})
                        self.datadict[j][self.screen_to_camera[i]].update({'z_mean': self.allbeamfiles[i]['z']['mean']})
                        self.datadict[j][self.screen_to_camera[i]].update(
                            {'px_mean': self.allbeamfiles[i]['px']['mean']})
                        self.datadict[j][self.screen_to_camera[i]].update(
                            {'py_mean': self.allbeamfiles[i]['py']['mean']})
                        self.datadict[j][self.screen_to_camera[i]].update(
                            {'pz_mean': self.allbeamfiles[i]['pz']['mean']})
                        self.datadict[j][self.screen_to_camera[i]].update({'t_mean': self.allbeamfiles[i]['t']['mean']})
                        self.datadict[j][self.screen_to_camera[i]].update({'x_sigma': self.allbeamfiles[i]['x']['sigma']})
                        self.datadict[j][self.screen_to_camera[i]].update({'y_sigma': self.allbeamfiles[i]['y']['sigma']})
                        self.datadict[j][self.screen_to_camera[i]].update({'z_sigma': self.allbeamfiles[i]['z']['sigma']})
                        self.datadict[j][self.screen_to_camera[i]].update(
                            {'px_sigma': self.allbeamfiles[i]['px']['sigma']})
                        self.datadict[j][self.screen_to_camera[i]].update(
                            {'py_sigma': self.allbeamfiles[i]['py']['sigma']})
                        self.datadict[j][self.screen_to_camera[i]].update(
                            {'pz_sigma': self.allbeamfiles[i]['pz']['sigma']})
                        self.datadict[j][self.screen_to_camera[i]].update({'t_sigma': self.allbeamfiles[i]['t']['sigma']})
                        self.datadict[j][self.screen_to_camera[i]].update({'filename': self.allbeamfiles[i]['filename']})
                    elif (self.allbeamfiles[i]['type'] == 'bpm') and (i in self.datadict[j].keys()):
                        self.datadict[j][i].update({'x': self.allbeamfiles[i]['x']['mean']})
                        self.datadict[j][i].update({'y': self.allbeamfiles[i]['y']['mean']})
                        self.datadict[j][i].update({'filename': self.allbeamfiles[i]['filename']})
        return self.datadict

    # Returns the SimFrame machine state dict
    # Output: machine state dictionary
    def getSimFrameDataDict(self):
        return self.getDataFromSimFrame.getDataDict()

    # Initialises the SimFrame machine state data
    def initialiseSimFrameData(self):
        return self.getDataFromSimFrame.initialiseData()

    # Change the starting point for the simulation
    # Input: inputdict: machine state dictionary
    #        start: starting point string (there should be a check in here that it matches the lattice sections)
    def updateLatticeStart(self, inputdict, start):
        if (self.simulation_defaults_set) or (self.SimFrameInitialised):
            inputdict['simulation']['starting_lattice'] = start
            return True
        else:
            print("Simulation defaults not initialised!!!!")
            return False

    # Change the end point for the simulation
    # Input: inputdict: machine state dictionary
    #        end: end point string (there should be a check in here that it matches the lattice sections)
    def updateLatticeEnd(self, inputdict, end):
        if (self.simulation_defaults_set) or (self.SimFrameInitialised):
            inputdict['simulation']['final_lattice'] = end
            return True
        else:
            print("Simulation defaults not initialised!!!!")
            return False

    # Sets PV aliases for simframe. All names do not match up exactly between SimFrame & CATAP
    # Input: mode: CATAP STATE (physical / virtual)
    def setPVAliases(self, mode):
        if not self.CATAPInitialised:
            self.getMachineStateFromCATAP(mode)
        for key, value in self.allDicts.items():
            if value['simframe_alias'] is not None:
                self.pvAlias.update({key:value['simframe_alias']})

    # Write machine state to YAML file
    # Inputs: filename: name of file to write to
    #         data_dict: machine state data dictionary
    def exportParameterValuesToYAMLFile(self, filename, data_dict, auto=False):
        self.export_dict = {}
        if not filename == "":
            for n in data_dict:
                self.export_dict = self.convertDataTypes(self.export_dict, data_dict[n], n)
            self.writeParameterOutputFile(str(filename), self.export_dict)
        else:
            print('Failed to export, please provide a filename.')

    # Sorts everything out so that it can be made compatible w/ YAML output
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

    # Reads in a machine state file to a python dict
    # Input: filename: machine state yaml file
    def parseParameterInputFile(self, filename):
        with open(filename, 'r') as stream:
            yaml_parameter_dict = yaml.safe_load(stream)
            return yaml_parameter_dict

    # Writes machine state dictionary to yaml file
    # Input: filename: name to write to
    #        parameter_dict: machine state dictionary
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