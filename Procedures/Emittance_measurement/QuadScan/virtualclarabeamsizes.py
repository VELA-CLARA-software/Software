import os
import sys
import numpy as np
from copy import deepcopy
from collections import OrderedDict
import scipy.constants
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..', '..', '..', 'SimFrame_fork', 'SimFrame')))
sys.path.append(
    (os.path.abspath(os.path.join(os.getcwd(), '..', '..', '..', 'VELA_CLARA_repository', 'Software', 'Utils',
                                  'MachineState'))))
sys.path.append(
    (os.path.abspath(os.path.join(os.getcwd(), '..', '..', '..', 'VELA_CLARA_repository', 'catapillar-build',
                                  'PythonInterface', 'Release'))))
import machine_state
import SimulationFramework.Modules.read_beam_file as read_beam_file
from unit_conversion import *
import CATAP.HardwareFactory
import time
from QuadScanclass import GeneralQuadScan


class BeamSizeDetermination(GeneralQuadScan):
    """

    Daughter class of py:class GeneralQuadScan containing all methods to
    calculate the quad strengths from experimental data and use the interface
    between CATAP and SimFrame to obtain the beam sizes.

    :ivar BeamMomentum: Beam Momentum: 29.5 MeV
    :ivar beam_sizes: Dictionary to save the beam sizes: OrderedDict()
    :ivar current_path: Path of Current file: []
    :ivar currents_optimised: Array of optimised currents : []
    :ivar machinestate: Machine State object built from the interface between SIMFRAME and CATAP: 'machinestate'
    :ivar mode: Mode in which CATAP is to work (PHYSICAL or VIRTUAL): VIRTUAL
    :ivar simframedata: SimFrameDictionary for the simulation
    :ivar framework: SimFrame object
    :ivar lattice_start: Beginning of lattice (SimFrame run)
    :ivar lattice_end: End of lattice (Simframe run)
    :ivar camera_data: camera data along S02: dictionary
    :ivar screen: screen to look at: ''


    """
    m_e_MeV = scipy.constants.physical_constants['natural unit of energy in MeV'][0]
    speed_of_light=scipy.constants.c
    BeamMomentum = 29.5  #: Beam momentum 30.0 MeV nominal
    unitconversion = UnitConversion()
    lattice = 'Lattices/CLA10-BA1_OM_emittance.def'
    beam = read_beam_file.beam()
    def _init__(self):
        """

        Initialisation of the object

        """
        super(BeamSizeDetermination, self).__init__()
        self.current_path = ''  #: Path of the file with the experimental currents
        self.currents_optimised = np.array([])  #: Numpy Matrix with the values of the currents from the file
        try:
            self.machinestate = machine_state.MachineState()  #: machine_state object initialised
            print('machinestate attribute correct')
        except AttributeError:
            print('no machinestate attribute correct')
        self.mode = CATAP.HardwareFactory.STATE.VIRTUAL  #: Mode in which CATAP is to be used (VIRTUAL or PHYSICAL)
        self.simframedata = self.machinestate.getSimFrameDataDict()  #: SimFrameDictionary for the simulation
        self.framework = self.machinestate.getFramework()  #: SimFrame Object
        self.__lattice_start = ''  #: Lattice start
        self.__lattice_end = ''  #: Lattice end
        self.camera_data = OrderedDict() #: Camera data dictionary


    @property
    def lattice_start(self):
        """
            The unique name of the lattice_start property.

            :getter: Returns lattice_start's name
            :setter: Sets lattice_start's name
            :type: string
            """
        return self.__lattice_start

    @lattice_start.setter
    def lattice_start(self, lat_start):
        self.__lattice_start = deepcopy(lat_start)

    @property
    def lattice_end(self):
        """
            The unique name of the lattice_end property.

            :getter: Returns lattice_end's name
            :setter: Sets lattice_end's name
            :type: string
        """
        return self.__lattice_end

    @lattice_end.setter
    def lattice_end(self, lat_end):
        self.__lattice_end = deepcopy(lat_end)

    @staticmethod
    def extract_beamsize_dict_one_quad(camera_dictionary):
        """

        Method to fill in the beam size dictionary for a set of optimised quads

        :parameter camera_dictionary: Dictionary with all the information from the Observation point camera

        :return beam_size: Dictionary with beam sizes and coupling terms
        """

        # Update dictionary of beam size

        return deepcopy(camera_dictionary['x_var']), deepcopy(camera_dictionary['y_var']), \
               deepcopy(camera_dictionary['x_y_mean'])

    def calculation_cov_matrix(self, distribution):
        """

        :param distribution: Distribution obtained at the end of LINAC

        :return: self.cov_m_linac: Covariant matrix at the end of LINAC

        """
        matrix = np.zeros((4, 4))
        velocity_conversion = (scipy.constants.m_e * (self.BeamMomentum/(1.0e-6*self.m_e_MeV)))
        matrix[0, 0] = np.mean(distribution['x_var'])
        matrix[0, 1] = velocity_conversion*np.mean(distribution['x_px_mean'])
        matrix[0, 2] = np.mean(distribution['x_y_mean'])
        matrix[0, 3] = velocity_conversion*np.mean(distribution['x_py_mean'])
        matrix[1, 0] = velocity_conversion*np.mean(distribution['y_px_mean'])
        matrix[1, 1] = np.square(velocity_conversion)*np.mean(distribution['px_var'])
        matrix[1, 2] = velocity_conversion*np.mean(distribution['y_px_mean'])
        matrix[1, 3] = np.square(velocity_conversion)*np.mean(distribution['px_py_mean'])
        matrix[2, 0] = np.mean(distribution['x_y_mean'])
        matrix[2, 1] = velocity_conversion*np.mean(distribution['y_px_mean'])
        matrix[2, 2] = np.mean(distribution['y_var'])
        matrix[2, 3] = velocity_conversion*np.mean(distribution['y_py_mean'])
        matrix[3, 0] = velocity_conversion*np.mean(distribution['x_py_mean'])
        matrix[3, 1] = np.square(velocity_conversion)*np.mean(distribution['px_py_mean'])
        matrix[3, 2] = velocity_conversion*np.mean(distribution['y_py_mean'])
        matrix[3, 3] = np.square(velocity_conversion)*np.mean(distribution['py_var'])
        np.savetxt(os.path.join(os.getcwd(), 'cov_matrix_end_linac.txt'), matrix)
        return matrix

    def currents_to_quad_strengths(self):
        """

        Calculate the quad strengths from array of currents

        :return self.quad_strengths: array of optimised quad strengths


        """
        for i_c, currents in enumerate(self.currents_optimised):
            self.quad_settings[i_c, :] = deepcopy(
                super(BeamSizeDetermination, self).I2K_CLARA_simple(currents, self.BeamMomentum))
        setattr(self, 'qstrengths', getattr(self, 'quad_settings'))
        super(BeamSizeDetermination, self).plot_quad_scan_strengths()

    def fill_in_currents_from_file(self):
        """

        Fill in the currents array (self.currents_optimised) by reading the Current file

        :return self.currents_optimised: array of optimised currents for sets of quads


        """
        self.currents_optimised = np.array(super(BeamSizeDetermination, self).FileOpen(self.current_path))
        self.currents_optimised = deepcopy(self.currents_optimised)
        self.nsteps = self.currents_optimised.shape[0]
        self.quad_settings = np.zeros((self.nsteps, 5))

    def read_hdf5_file(self, directory):
        dictionary_aperture = {}
        allbeamfiles = self.machinestate.getDataFromSimFrame.getAllBeamFiles(directory)
        for i in allbeamfiles.keys():
            if allbeamfiles[i]['type'] == 'aperture':
                dictionary_aperture.update({'x_mm': allbeamfiles[i]['x']['mean']})
                dictionary_aperture.update({'y_mm': allbeamfiles[i]['y']['mean']})
                dictionary_aperture.update({'x_mm_sig': allbeamfiles[i]['x']['sigma']})
                dictionary_aperture.update({'y_mm_sig': allbeamfiles[i]['y']['sigma']})
                dictionary_aperture.update({'x_mean': allbeamfiles[i]['x']['mean']})
                dictionary_aperture.update({'y_mean': allbeamfiles[i]['y']['mean']})
                dictionary_aperture.update({'x_var': allbeamfiles[i]['x']['var']})
                dictionary_aperture.update({'y_var': allbeamfiles[i]['y']['var']})
                dictionary_aperture.update({'x_y_mean': np.mean(np.multiply(
                    np.multiply(1.0, allbeamfiles[i]['x']['dist']), allbeamfiles[i]['y']['dist']))})
                dictionary_aperture.update({'px_py_mean': np.mean(np.multiply(
                    np.multiply(1.0, allbeamfiles[i]['px']['dist']),
                    allbeamfiles[i]['py']['dist']))})
                dictionary_aperture.update({'x_px_mean': np.mean(np.multiply(
                    np.multiply(1.0, allbeamfiles[i]['x']['dist']),
                    allbeamfiles[i]['px']['dist']))})
                dictionary_aperture.update({'y_py_mean': np.mean(np.multiply(
                    np.multiply(1.0, allbeamfiles[i]['y']['dist']),
                    allbeamfiles[i]['py']['dist']))})
                dictionary_aperture.update({'x_py_mean': np.mean(np.multiply(
                    np.multiply(1.0, allbeamfiles[i]['x']['dist']),
                    allbeamfiles[i]['py']['dist']))})
                dictionary_aperture.update({'y_px_mean': np.mean(np.multiply(
                    np.multiply(1.0, allbeamfiles[i]['y']['dist']),
                    allbeamfiles[i]['px']['dist']))})
                dictionary_aperture.update({'z_mean': allbeamfiles[i]['z']['mean']})
                dictionary_aperture.update(
                    {'px_mean': allbeamfiles[i]['px']['mean']})
                dictionary_aperture.update(
                    {'py_mean': allbeamfiles[i]['py']['mean']})
                dictionary_aperture.update(
                    {'pz_mean': allbeamfiles[i]['pz']['mean']})
                dictionary_aperture.update({'t_mean': allbeamfiles[i]['t']['mean']})
                dictionary_aperture.update({'x_sigma': allbeamfiles[i]['x']['sigma']})
                dictionary_aperture.update({'y_sigma': allbeamfiles[i]['y']['sigma']})
                dictionary_aperture.update({'z_sigma': allbeamfiles[i]['z']['sigma']})
                dictionary_aperture.update(
                    {'px_sigma': allbeamfiles[i]['px']['sigma']})
                dictionary_aperture.update(
                    {'py_sigma': allbeamfiles[i]['py']['sigma']})
                dictionary_aperture.update(
                    {'pz_sigma': allbeamfiles[i]['pz']['sigma']})
                dictionary_aperture.update({'px_var': allbeamfiles[i]['px']['var']})
                dictionary_aperture.update({'py_var': allbeamfiles[i]['py']['var']})
                dictionary_aperture.update({'pz_var': allbeamfiles[i]['pz']['var']})
                dictionary_aperture.update({'t_sigma': allbeamfiles[i]['t']['sigma']})
                dictionary_aperture.update({'filename': allbeamfiles[i]['filename']})
            else:
                continue
        return dictionary_aperture


    def preparing_catap_data(self):
        """

        Method with the sequence for getting the CATAP Dictionary and interact with SimFrame

        :return  catapdict : Dictionary with all the PVs

        """
        setattr(self, 'machinestate', machine_state.MachineState())
        setattr(self, 'mode', CATAP.HardwareFactory.STATE.VIRTUAL)
        self.machinestate.initialiseCATAP(self.mode)
        # Get the dictionary containing all CATAP hardware objects
        catapdict = self.machinestate.getCATAPDict(self.mode)

        # Switch on magnets in VM
        for name in catapdict['Magnet'].keys():
            catapdict['Magnet'][name].switchOn()
            if name == 'CLA-LRG1-MAG-BSOL-01':
                catapdict['Magnet'][name].SETI(-2.20)
            elif name == 'CLA-LRG1-MAG-SOL-01':
                catapdict['Magnet'][name].SETI(-150.0)
            time.sleep(0.5)

        catapdict['L01'].setAmpMW(10.0e6)
        catapdict['LRRG_GUN'].setAmpMW(8.630e6)
        catapdict['L01'].setPhiDEG(0)
        catapdict['LRRG_GUN'].setPhiDEG(0)

        print('LLRG Energy ',
              self.unitconversion.getEnergyFromRF(catapdict['LRRG_GUN'].getAmpMW(), catapdict['LRRG_GUN'].getPhiDEG(),
                                                  2.5,
                                                  "LRRG_GUN"), ' MeV',
              ' Linac Energy ',
              self.unitconversion.getEnergyFromRF(catapdict['L01'].getAmpMW(), catapdict['L01'].getPhiDEG(), 0.7,
                                                  "L01"),
              ' MeV',
              ' Total Energy = ',
              self.unitconversion.getEnergyFromRF(catapdict['LRRG_GUN'].getAmpMW(), catapdict['LRRG_GUN'].getPhiDEG(),
                                                  2.5,
                                                  "LRRG_GUN") + self.unitconversion.getEnergyFromRF(
                  catapdict['L01'].getAmpMW(),
                  catapdict['L01'].getPhiDEG(), 0.7,
                  "L01"), ' MeV')
        time.sleep(5)
        self.machinestate.exportParameterValuesToYAMLFile(
            os.path.abspath(os.path.join(os.getcwd(), "test", "catap-test.yaml")),
            self.machinestate.getMachineStateFromCATAP(self.mode))
        return catapdict

    def quad_set_sequence(self, rows, catapdict):
        """

                Method to extract the camera info from each set of quad sequence

                :parameter rows: Number of quad scan (from 1 up to the number of scans: int(self.nsteps)

                :parameter catapdict: CATAP dictionary  with all the PVs obtained from CATAP:

                :parameter self.currents_optimised: Set of currents for the optimised quad strengths:

                :return self.beam_sizes: beam sizes array obtained from quad scans:

                """
        cam_data = OrderedDict()
        print('+++++++++++++++++++++++ Before ', catapdict['Magnet']['CLA-S02-MAG-QUAD-01'].READI,
              catapdict['Magnet']['CLA-S02-MAG-QUAD-02'].READI,
              catapdict['Magnet']['CLA-S02-MAG-QUAD-03'].READI, catapdict['Magnet']['CLA-S02-MAG-QUAD-04'].READI,
              catapdict['Magnet']['CLA-S02-MAG-QUAD-05'].READI)
        for i_currents, currents in enumerate(self.currents_optimised[rows, :]):
            catapdict['Magnet']['CLA-S02-MAG-QUAD-0' + str(i_currents + 1)].SETI(currents)
            if catapdict['Magnet']['CLA-S02-MAG-QUAD-0' + str(i_currents + 1)].psu_state == 'OFF':
                catapdict['Magnet']['CLA-S02-MAG-QUAD-0' + str(i_currents + 1)].SetPSUState('ON')
            time.sleep(1.5)
            # ri_tol = catapdict['Magnet']['CLA-S02-MAG-QUAD-03'].getREADITolerance()
            # while (currents - ri_tol) < catapdict['Magnet']['CLA-S02-MAG-QUAD-03'].getREADI() < (currents + ri_tol):
            #    time.sleep(5)
        print('+++++++++++++++++++++++ After ', catapdict['Magnet']['CLA-S02-MAG-QUAD-01'].READI,
              catapdict['Magnet']['CLA-S02-MAG-QUAD-02'].READI,
              catapdict['Magnet']['CLA-S02-MAG-QUAD-03'].READI,
              catapdict['Magnet']['CLA-S02-MAG-QUAD-04'].READI,
              catapdict['Magnet']['CLA-S02-MAG-QUAD-05'].READI)
        # Get updated machine state from CATAP
        catapdata = self.machinestate.getMachineStateFromCATAP(self.mode, start_lattice=self.lattice_start,
                                                               final_lattice=self.lattice_end)
        # Write machine state dictionary to simframe and runs simulation
        catapdata['generator']['number_of_particles']['value'] = np.power(2, 6)
        catapdata['generator']['charge'].update({'value': self.charge})
        simframe_file_update = self.machinestate.writeMachineStateToSimFrame(
            directory= 'quad_scan_setup_' + str(rows),
            framework=self.framework, lattice=self.lattice,
            datadict=catapdata, run=True, type='CATAP', sections=['CLA-S02'])
        # Exports machine state from simframe (hardware settings and simulated data @ screens / bpms)
        self.machinestate.exportParameterValuesToYAMLFile(
            os.path.abspath(os.path.join(os.getcwd(), "test", "simframe-test" + str(rows) + ".yaml")),
            simframe_file_update)
        [catapdict['Magnet']['CLA-S02-MAG-QUAD-0' + str(i_c)].SETI(0.0) for i_c in np.arange(1, 6)]
        time.sleep(0.5)
        for key in ['01', '02', '03']:
            cam_data.update({'CLA-S02-DIA-CAM-'+key: simframe_file_update['CLA-S02']['CLA-S02-DIA-CAM-'+key]})
        #return simframe_file_update['CLA-S02']['CLA-S02-DIA-CAM-03']
        return cam_data

    def fill_in_beam_size_dictionary(self, x_sig, y_sig, x_y_sig):
        """

         Fill in the beam size dictionary

        :param x_sig: Array with x rms from the camera:

        :param y_sig: Array with y rms from the camera:

        :param x_y_sig: Array with x-y coupling terms from the camera:

        :return self.beam_sizes: Dictionary with info from the camera:

        """
        setattr(self,'screen_data', [])
        setattr(self, 'beam_sizes', OrderedDict())

        [self.beam_sizes.update({key: values}) for key, values in zip(['x_var', 'y_var', 'x_y_mean'],
                                                                      [np.array(x_sig), np.array(y_sig),
                                                                       np.array(x_y_sig)])]
        for x_s, x_y_s, y_s in zip(self.beam_sizes['x_var'], self.beam_sizes['x_y_mean'], self.beam_sizes['y_var']):
            self.screen_data.append(x_s)
            self.screen_data.append(x_y_s)
            self.screen_data.append(y_s)
        self.screen_data = deepcopy(np.array(self.screen_data))
        # self.machinestate.exportParameterValuesToYAMLFile(
        #    os.path.abspath(os.path.join(os.getcwd(), "test", "catap-test_quad_" + str(rows) + ".yaml")),
        #    self.machinestate.getMachineStateFromCATAP(self.mode))

    def quad_scan(self, catapdict):
        """

        Method to perform the quad scan from the optimised currents

        :parameter catapdict: CATAP dictionary  with all the PVs obtained from CATAP:

        :return self.beam_sizes: beam sizes array obtained from quad scans

        """
        self.camera_data = OrderedDict()
        x_sigma = []
        y_sigma = []
        x_y_mean = []

        setattr(self, 'lattice_start', 'CLA-S02')
        setattr(self, 'lattice_end', getattr(self, 'lattice_start'))
        setattr(self, 'beam_sizes', OrderedDict)
        for key, magnet in catapdict['Magnet'].items():
            if key.startswith('CLA-S02-MAG-QUAD'):
                catapdict['Magnet'][key].switchOff()
                catapdict['Magnet'][key].switchOn()
                catapdict['Magnet'][key].SETI(0.0)
                catapdict['Magnet'][key].debugMessagesOff()
        time.sleep(1.5)
        for rows in np.arange(len(self.currents_optimised)):
            simframe_dictionary = deepcopy(self.quad_set_sequence(rows, catapdict))
            x_sig, y_sig, x_y_sig = self.extract_beamsize_dict_one_quad(simframe_dictionary[self.screen])
            x_sigma.append(x_sig)
            y_sigma.append(y_sig)
            x_y_mean.append(x_y_sig)

        self.fill_in_beam_size_dictionary(x_sigma, y_sigma, x_y_mean)

    def setting_up_simframe(self, catapdict):
        """

        Method to set up the simframe object (machine state)

        :parameter catapdict: CATAP dictionary

        :return simframedata: SimFrame dict

        """
        # Set up Simframe
        self.machinestate.getMachineStateFromSimFrame('test', self.lattice)
        self.machinestate.initialiseSimFrameData()
        setattr(self, 'simframedata', self.machinestate.getSimFrameDataDict())
        setattr(self, 'framework', self.machinestate.getFramework())

        # Set up lattice end point (default is to start at generator, at the moment we have to do it this way)
        machinestatefile = self.machinestate.parseParameterInputFile(
            os.path.abspath(os.path.join(os.getcwd(), "test", "catap-test.yaml")))
        self.machinestate.updateLatticeEnd(machinestatefile, 'CLA-S02')
        catapdata = self.machinestate.getMachineStateFromCATAP(self.mode)
        # We have to fudge this for now as the conversion between current and solenoid strength doesn't work
        get_data_from_catap = self.machinestate.getDataFromCATAP
        for suffix in ['SOL', 'BSOL']:
            name = 'CLA-LRG1-MAG-' + suffix + '-01'
            self.unitconversion.currentToK('SOL', catapdict['Magnet'][name].READI,
                                                        get_data_from_catap.magnetdata[name][
                                                            'field_integral_coefficients'],
                                                        get_data_from_catap.magnetdata[name]['magnetic_length'],
                                                        self.BeamMomentum, get_data_from_catap.magnetdata[name])
            catapdata['INJ'][name].update({'field_amplitude': get_data_from_catap.magnetdata[name]['field_amplitude'] })


        #catapdata['INJ']['CLA-LRG1-MAG-SOL-01'].update({'field_amplitude': 0.255})
        #catapdata['INJ']['CLA-LRG1-MAG-BSOL-01'].update({'field_amplitude': 0.0})
        # # Write machine state dictionary to simframe and runs simulation
        simframefileupdate = self.machinestate.writeMachineStateToSimFrame('injector',
                                                                           self.framework,
                                                                           self.lattice,
                                                                           datadict=catapdata,
                                                                           run=True, type='CATAP',
                                                                           sections=['INJ', 'CLA-S01', 'L01'])
        dictionary_aperture = self.read_hdf5_file('injector')
        matrix=self.calculation_cov_matrix(dictionary_aperture)

        file_path = os.path.join(os.getcwd(), 'test')
        self.framework['CLA-S02'].prefix = os.path.join('..', 'injector/')
        #self.quad_scan(catapdict)

    def sequence_to_prepare_machine_state_and_simframe(self):
        """
        Sequence to set up the catap and simframe dictionaries

        :return self.beam_sizes: Set beam_sizes

        """
        catapdict = self.preparing_catap_data()
        self.setting_up_simframe(catapdict)
