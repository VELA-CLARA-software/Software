import os
import sys
import numpy as np
from copy import deepcopy
from collections import OrderedDict
import scipy.constants
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..', '..', '..', 'SimFrame_fork', 'simframe')))
sys.path.append(
    (os.path.abspath(os.path.join(os.getcwd(), '..', '..', '..', 'VELA_CLARA_repository', 'Software', 'Utils',
                                  'MachineState',"Version 1"))))
sys.path.append(
    (os.path.abspath(os.path.join(os.getcwd(), '..', '..', '..', 'VELA_CLARA_repository', 'catapillar-build',
                                  'PythonInterface', 'Release'))))
import machine_state as machine_state
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
    :ivar screen: screen to look at: ''
    """
    m_e_MeV = scipy.constants.physical_constants['natural unit of energy in MeV'][0]
    q_e_c = scipy.constants.e / scipy.constants.c
    speed_of_light = scipy.constants.c
    unitconversion = UnitConversion()
    lattice = os.path.join('Lattices', 'CLA10-BA1_OM_emitt.def')
    lattice_injector = os.path.join('Lattices', 'CLA10-BA1_OM_emitt_inj.def')
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
            :getter: Returns lattice_end's name:
            :setter: Sets lattice_end's name:
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
            :param camera_dictionary: Dictionary with all the information from the Observation point camera:
            :return beam_size: Dictionary with beam sizes and coupling terms:
        """

        # Update dictionary of beam size

        return deepcopy(camera_dictionary['x_var']), deepcopy(camera_dictionary['y_var']), \
               deepcopy(camera_dictionary['x_y_mean'])

    def calculation_cov_matrix(self):
        """
            Calculation of the covariance matrix at any point for any distribution
            :param distribution: Distribution obtained at a particular point:
            :return: matrix: Covariance matrix at the point of analysis:
        """
        gamma = self.BeamMomentum / self.m_e_MeV
        factor = scipy.constants.e / (self.q_e_c * gamma * scipy.constants.m_e * np.square(self.speed_of_light))
        matrix = np.zeros((4, 4))
        matrix[0, 0] = np.mean(np.square(getattr(self.beam, 'x')))
        matrix[0, 1] = np.multiply(factor, np.mean(np.multiply(getattr(self.beam, 'x'), getattr(self.beam, 'px'))))
        matrix[0, 2] = np.mean(np.multiply(getattr(self.beam, 'x'), getattr(self.beam, 'y')))
        matrix[0, 3] = np.multiply(factor, np.mean(np.multiply(getattr(self.beam, 'x'), getattr(self.beam, 'py'))))
        matrix[1, 0] = np.multiply(factor, np.mean(np.multiply(getattr(self.beam, 'x'), getattr(self.beam, 'px'))))
        matrix[1, 1] = np.mean(np.square(np.multiply(factor, getattr(self.beam, 'px'))))
        matrix[1, 2] = np.multiply(factor, np.mean(np.multiply(getattr(self.beam, 'px'), getattr(self.beam, 'y'))))
        matrix[1, 3] = np.multiply(np.square(factor),
                                   np.mean(np.multiply(getattr(self.beam, 'px'), getattr(self.beam, 'py'))))
        matrix[2, 0] = np.mean(np.multiply(getattr(self.beam, 'x'), getattr(self.beam, 'y')))
        matrix[2, 1] = np.multiply(factor, np.mean(np.multiply(getattr(self.beam, 'px'), getattr(self.beam, 'y'))))
        matrix[2, 2] = np.mean(np.square(getattr(self.beam, 'y')))
        matrix[2, 3] = np.multiply(factor, np.mean(np.multiply(getattr(self.beam, 'y'), getattr(self.beam, 'py'))))
        matrix[3, 0] = np.multiply(factor, np.mean(np.multiply(getattr(self.beam, 'x'), getattr(self.beam, 'py'))))
        matrix[3, 1] = np.multiply(np.square(factor),
                                   np.mean(np.multiply(getattr(self.beam, 'px'), getattr(self.beam, 'py'))))
        matrix[3, 2] = np.multiply(factor, np.mean(np.multiply(getattr(self.beam, 'y'), getattr(self.beam, 'py'))))
        matrix[3, 3] = np.mean(np.square(np.multiply(factor, getattr(self.beam, 'py'))))
        np.savetxt(os.path.join(os.getcwd(), 'cov_matrix_end_linac_new.txt'), matrix)
        return matrix

    def fill_in_currents_from_file(self):
        """
            Fill in the currents array (self.currents_optimised) by reading the Current file
            :return self.currents_optimised: array of optimised currents for sets of quads:
        """
        self.currents_optimised = np.loadtxt(self.current_path, delimiter=',')
        self.nsteps = self.currents_optimised.shape[0]
        self.quad_settings = np.zeros((self.nsteps, 5))

    def currents_to_quad_strengths(self):
        """
            Calculate the quad strengths from array of currents
            :return self.quad_strengths: array of optimised quad strengths:
        """
        quad_settings = np.zeros_like(self.quad_settings)
        for i_c, currents in enumerate(self.currents_optimised):
            quad_settings[i_c, :] = deepcopy(
                super(BeamSizeDetermination, self).I2K_CLARA_simple(currents, self.BeamMomentum))
        setattr(self, 'quad_settings', quad_settings)
        setattr(self, 'qstrengths', getattr(self, 'quad_settings'))
        np.savetxt(os.path.abspath(os.path.join(os.getcwd(), 'quad_settings_from_VM_interpolation.txt')),
                   self.qstrengths)
        super(BeamSizeDetermination, self).plot_quad_scan_strengths()

    def setting_up_simframe(self):
        """
            Method to set up the simframe object (machine state)
            :param catapdict: CATAP dictionary:
            :return simframedata: SimFrame dict:
        """
        # Set up Simframe
        self.machinestate.getMachineStateFromSimFrame('test', self.lattice_injector)
        time.sleep(1)
        self.machinestate.initialiseSimFrameData()
        setattr(self, 'simframedata', self.machinestate.getSimFrameDataDict())
        setattr(self, 'framework', self.machinestate.getFramework())

        # Set up lattice end point (default is to start at generator, at the moment we have to do it this way)
        machinestatefile = self.machinestate.parseParameterInputFile(os.path.join("test", "catap-test.yaml"))
        self.machinestate.updateLatticeEnd(machinestatefile, 'CLA-S02')
        catapdata = self.machinestate.getMachineStateFromCATAP(self.mode, start_lattice='Generator',
                                                               final_lattice='INJ')
        # We have to fudge this for now as the conversion between current and solenoid strength doesn't work
        get_data_from_catap = self.machinestate.getDataFromCATAP
        catapdata['generator']['charge'].update({'value': self.charge})
        catapdata['generator']['number_of_particles']['value'] = np.power(2, 14)
        catapdata['L01']['CLA-L01-MAG-SOL-01'].update({'field_amplitude': 0.0})
        catapdata['L01']['CLA-L01-MAG-SOL-02'].update({'field_amplitude': 0.0})
        catapdata['INJ']['CLA-LRG1-MAG-SOL-01'].update({'field_amplitude': 0.216})
        catapdata['INJ']['CLA-LRG1-MAG-BSOL-01'].update({'field_amplitude': -0.06730128})
        print(catapdata.keys())
        time.sleep(40)
        energy_beam = self.machinestate.getEnergyGainFromCATAP()
        setattr(self, 'BeamMomentum', float(energy_beam[0.17] + energy_beam[3.2269]))
        print(self.BeamMomentum)
        time.sleep(40)
        # Write machine state dictionary to simframe and runs simulation
        simframefileupdate = self.machinestate.writeMachineStateToSimFrame('injector',
                                                                           framework=self.framework,
                                                                           lattice=self.lattice_injector,
                                                                           datadict=catapdata,
                                                                           run=True, type='CATAP',
                                                                           sections=['INJ', 'CLA-S01', 'L01'])
        ######################## Chromaticity: Setting the beam energy to be the same for all particles #############
        self.beam.read_HDF5_beam_file(os.path.join('injector', 'CLA-S02-APER-01.hdf5'))
        a_p_sq = np.square(np.multiply(1.e-6 / self.q_e_c, getattr(self.beam, 'px'))) + np.square(
            np.multiply(1.e-6 / self.q_e_c, getattr(self.beam, 'py')))
        a_pz = np.sqrt(np.multiply(np.square(1. / self.speed_of_light),
                                   np.array(
                                       [np.square(self.BeamMomentum) - t - np.square(self.m_e_MeV) for t in a_p_sq])))
        self.beam.beam.update({'code': 'ASTRA'})
        self.beam.beam.update({'pz': np.multiply(1.e6 * scipy.constants.e, a_pz)})
        self.beam.write_HDF5_beam_file(os.path.join('injector', 'CLA-S02-APER-01.hdf5'))
        ############################################################################
        matrix = self.calculation_cov_matrix()
        file_path = os.path.join(os.getcwd(), 'test')

    def preparing_catap_data_and_simframe(self):
        """
            Method with the sequence for getting the CATAP Dictionary and interact with SimFrame
            :return  catapdict: Dictionary with all the PVs:
        """
        setattr(self, 'machinestate', machine_state.MachineState())
        setattr(self, 'mode', CATAP.HardwareFactory.STATE.VIRTUAL)
        self.machinestate.initialiseCATAP(self.mode)
        # Get the dictionary containing all CATAP hardware objects
        catapdict = self.machinestate.getCATAPDict(self.mode)

        # Switch on magnets in VM
        for name in catapdict['Magnet'].keys():
            catapdict['Magnet'][name].switchOn()

        catapdict['L01'].setAmpMW(21.2*10**6)
        catapdict['LRRG_GUN'].setAmpMW(58.8*10**6)
        catapdict['L01'].setPhiDEG(0)
        catapdict['LRRG_GUN'].setPhiDEG(0)
        catapdict['Charge']['CLA-S01-DIA-WCM-01'].q = self.charge

        if not os.path.isdir(os.path.abspath(os.path.join(os.getcwd(), "test"))):
            os.makedirs(os.path.abspath(os.path.join(os.getcwd(), "test")))

        catapdata=self.machinestate.getMachineStateFromCATAP(self.mode)
        self.machinestate.exportParameterValuesToYAMLFile(
            os.path.abspath(os.path.join(os.getcwd(), "test", "catap-test.yaml")),catapdata)
        self.setting_up_simframe()
        return catapdict

    def quad_set_sequence(self, rows, currents_optimised, catapdict):
        """
                Method to extract the camera info from each set of quad sequence
                :param rows: Number of quad scan (from 1 up to the number of scans: int(self.nsteps):
                :param catapdict: CATAP dictionary  with all the PVs obtained from CATAP:
                :param self.currents_optimised: Set of currents for the optimised quad strengths:
                :return self.beam_sizes: beam sizes array obtained from quad scans:
                """
        cam_data = OrderedDict()
        self.framework.set_lattice_prefix('CLA-S02', os.path.join('..', 'injector/'))
        setattr(self, 'lattice_start', 'CLA-S02')
        setattr(self, 'lattice_end', getattr(self, 'lattice_start'))
        print('+++++++++++++++++++++++ Before ', catapdict['Magnet']['CLA-S02-MAG-QUAD-01'].READI,
              catapdict['Magnet']['CLA-S02-MAG-QUAD-02'].READI,
              catapdict['Magnet']['CLA-S02-MAG-QUAD-03'].READI, catapdict['Magnet']['CLA-S02-MAG-QUAD-04'].READI,
              catapdict['Magnet']['CLA-S02-MAG-QUAD-05'].READI)
        for i_currents, currents in enumerate(currents_optimised[rows, :]):
            if catapdict['Magnet']['CLA-S02-MAG-QUAD-0' + str(i_currents + 1)].psu_state == 'OFF':
                catapdict['Magnet']['CLA-S02-MAG-QUAD-0' + str(i_currents + 1)].SetPSUState('ON')
                catapdict['Magnet']['CLA-S02-MAG-QUAD-0' + str(i_currents + 1)].SETI(0)
        catapdict['Magnet']['CLA-S02-MAG-QUAD-01'].SETI(currents_optimised[rows, 0])
        time.sleep(0.25)
        catapdict['Magnet']['CLA-S02-MAG-QUAD-02'].SETI(currents_optimised[rows, 1])
        time.sleep(0.25)
        catapdict['Magnet']['CLA-S02-MAG-QUAD-03'].SETI(currents_optimised[rows, 2])
        time.sleep(0.25)
        catapdict['Magnet']['CLA-S02-MAG-QUAD-04'].SETI(currents_optimised[rows, 3])
        time.sleep(0.25)
        catapdict['Magnet']['CLA-S02-MAG-QUAD-05'].SETI(currents_optimised[rows, 4])
        time.sleep(0.25)
        print('+++++++++++++++++++++++ After ', catapdict['Magnet']['CLA-S02-MAG-QUAD-01'].READI,
              catapdict['Magnet']['CLA-S02-MAG-QUAD-02'].READI,
              catapdict['Magnet']['CLA-S02-MAG-QUAD-03'].READI,
              catapdict['Magnet']['CLA-S02-MAG-QUAD-04'].READI,
              catapdict['Magnet']['CLA-S02-MAG-QUAD-05'].READI)
        #  Get updated machine state from CATAP
        catapdata = self.machinestate.getMachineStateFromCATAP(self.mode, start_lattice=self.lattice_start,
                                                               final_lattice=self.lattice_end)
        simframe_file_update = self.machinestate.writeMachineStateToSimFrame(
            directory='quad_scan_setup_' + str(rows),
            framework=self.framework, lattice=self.lattice,
            datadict=catapdata, run=True, type='CATAP', sections=['CLA-S02'])
        # Exports machine state from simframe (hardware settings and simulated data @ screens / bpms)
        self.machinestate.exportParameterValuesToYAMLFile(
            os.path.abspath(os.path.join(os.getcwd(), "test", "simframe-test" + str(rows) + ".yaml")),
            simframe_file_update)
        [catapdict['Magnet']['CLA-S02-MAG-QUAD-0' + str(i_c)].switchOn() for i_c in np.arange(1, 6)]
        [catapdict['Magnet']['CLA-S02-MAG-QUAD-0' + str(i_c)].SETI(0.0) for i_c in np.arange(1, 6)]
        time.sleep(1)
        for key in ['01', '02', '03']:
            cam_data.update({'CLA-S02-DIA-CAM-' + key: simframe_file_update['CLA-S02']['CLA-S02-DIA-CAM-' + key]})
        return cam_data

    def fill_in_beam_size_dictionary(self, x_sig, y_sig, x_y_sig):
        """
             Fill in the beam size dictionary
            :param x_sig: Array with x rms from the camera:
            :param y_sig: Array with y rms from the camera:
            :param x_y_sig: Array with x-y coupling terms from the camera:
            :return self.beam_sizes: Dictionary with info from the camera:
        """
        setattr(self, 'beam_sizes', OrderedDict())
        screen_data = np.zeros(3 * self.nsteps)
        [self.beam_sizes.update({key: values}) for key, values in zip(['x_var', 'x_y_mean', 'y_var'],
                                                                      [np.sqrt(np.array(x_sig)),
                                                                       np.array(x_y_sig),
                                                                       np.sqrt(np.array(y_sig))])]
        for i_beamsize in np.arange(self.nsteps):
            screen_data[(3 * i_beamsize)] = deepcopy(np.square(self.beam_sizes['x_var'])[i_beamsize])
            screen_data[(3 * i_beamsize) + 1] = deepcopy(self.beam_sizes['x_y_mean'][i_beamsize])
            screen_data[(3 * i_beamsize) + 2] = deepcopy(np.square(self.beam_sizes['y_var'])[i_beamsize])
        setattr(self, 'screen_data', screen_data)

    def quad_scan(self, catapdict):
        """

            Method to perform the quad scan from the optimised currents

            :param catapdict: CATAP dictionary  with all the PVs obtained from CATAP:

            :return self.beam_sizes: beam sizes array obtained from quad scans:

        """
        x_sigma = []
        y_sigma = []
        x_y_mean = []
        cam_data = OrderedDict()
        self.framework.set_lattice_prefix('CLA-S02', os.path.join('..', 'injector/'))
        setattr(self, 'lattice_start', 'CLA-S02')
        setattr(self, 'lattice_end', getattr(self, 'lattice_start'))
        setattr(self, 'beam_sizes', OrderedDict)
        self.fill_in_currents_from_file()
        currents_optimised = np.loadtxt(self.current_path, delimiter=',')
        self.currents_to_quad_strengths()
        for key, magnet in catapdict['Magnet'].items():
            if key.startswith('CLA-S02-MAG-QUAD'):
                catapdict['Magnet'][key].switchOff()
                catapdict['Magnet'][key].switchOn()
                catapdict['Magnet'][key].SETI(0.0)
                catapdict['Magnet'][key].debugMessagesOff()
        time.sleep(1)

        for rows in np.arange(currents_optimised.shape[0]):
            print('+++++++++++++++++++++++ Before ', catapdict['Magnet']['CLA-S02-MAG-QUAD-01'].READI,
                  catapdict['Magnet']['CLA-S02-MAG-QUAD-02'].READI,
                  catapdict['Magnet']['CLA-S02-MAG-QUAD-03'].READI, catapdict['Magnet']['CLA-S02-MAG-QUAD-04'].READI,
                  catapdict['Magnet']['CLA-S02-MAG-QUAD-05'].READI)
            for i_currents in np.arange(currents_optimised.shape[1]):
                # simframe_dictionary = deepcopy(self.quad_set_sequence(rows, currents_optimised, catapdict))
                if catapdict['Magnet']['CLA-S02-MAG-QUAD-0' + str(i_currents + 1)].psu_state == 'OFF':
                    catapdict['Magnet']['CLA-S02-MAG-QUAD-0' + str(i_currents + 1)].SetPSUState('ON')
                    catapdict['Magnet']['CLA-S02-MAG-QUAD-0' + str(i_currents + 1)].SETI(0.0)

                while catapdict['Magnet']['CLA-S02-MAG-QUAD-0' + str(i_currents + 1)].READI != float(
                        currents_optimised[rows, i_currents]):
                    catapdict['Magnet']['CLA-S02-MAG-QUAD-0' + str(i_currents + 1)].SETI(
                        float(currents_optimised[rows, i_currents]))

            # ri_tol = catapdict['Magnet']['CLA-S02-MAG-QUAD-03'].READITolerance()
            # while (currents - ri_tol) < catapdict['Magnet']['CLA-S02-MAG-QUAD-0' + str(i_currents + 1)].READI() < (currents + ri_tol):
            #    time.sleep(1.55)
            print('+++++++++++++++++++++++ After ',
                  catapdict['Magnet']['CLA-S02-MAG-QUAD-01'].READI == currents_optimised[rows, 0],
                  catapdict['Magnet']['CLA-S02-MAG-QUAD-02'].READI == currents_optimised[rows, 1],
                  catapdict['Magnet']['CLA-S02-MAG-QUAD-03'].READI == currents_optimised[rows, 2],
                  catapdict['Magnet']['CLA-S02-MAG-QUAD-04'].READI == currents_optimised[rows, 3],
                  catapdict['Magnet']['CLA-S02-MAG-QUAD-05'].READI == currents_optimised[rows, 4])

            # Exports machine state from simframe (hardware settings and simulated data @ screens / bpms)
            self.machinestate.exportParameterValuesToYAMLFile(
                os.path.abspath(os.path.join(os.getcwd(), "test", "simframe-test" + str(rows) + ".yaml")),
                self.machinestate.getMachineStateFromCATAP(self.mode))

            machinestatefile = self.machinestate.parseParameterInputFile(
                os.path.join("test", "simframe-test" + str(rows) + ".yaml"))
            self.machinestate.updateLatticeEnd(machinestatefile, 'CLA-S02')
            #  Get updated machine state from CATAP
            catapdata = self.machinestate.getMachineStateFromCATAP(self.mode, start_lattice=self.lattice_start,
                                                                   final_lattice=self.lattice_end)
            for i_currents in np.arange(currents_optimised.shape[1]):
                catapdata['CLA-S02']['CLA-S02-MAG-QUAD-0' + str(i_currents + 1)]['k1'] = self.qstrengths[
                    rows, i_currents]
            # Write machine state dictionary to simframe and runs simulation
            # catapdata['generator']['charge'].update({'value': self.charge})
            # catapdata['generator']['number_of_particles']['value'] = np.power(2, 9)
            # catapdata['simulation'].update({'starting_lattice': self.lattice_start})
            # catapdata['simulation'].update({'final_lattice': self.lattice_end})

            simframe_file_update = self.machinestate.writeMachineStateToSimFrame(
                directory='quad_scan_setup_' + str(rows),
                framework=self.framework, lattice=self.lattice,
                datadict=catapdata, run=True, type='CATAP', sections=['CLA-S02'])

            [catapdict['Magnet']['CLA-S02-MAG-QUAD-0' + str(i_c)].switchOn() for i_c in np.arange(1, 6)]
            [catapdict['Magnet']['CLA-S02-MAG-QUAD-0' + str(i_c)].SETI(0.0) for i_c in np.arange(1, 6)]
            time.sleep(1)
            for key in ['01', '02', '03']:
                cam_data.update({'CLA-S02-DIA-CAM-' + key: simframe_file_update['CLA-S02']['CLA-S02-DIA-CAM-' + key]})
            x_sig, y_sig, x_y_sig = self.extract_beamsize_dict_one_quad(cam_data[self.screen])
            x_sigma.append(x_sig)
            y_sigma.append(y_sig)
            x_y_mean.append(x_y_sig)

        self.fill_in_beam_size_dictionary(x_sigma, y_sigma, x_y_mean)

    def sequence_to_prepare_machine_state_and_simframe(self):
        """
            Sequence to set up the catap and simframe dictionaries
            :return self.beam_sizes: Set beam_sizes:
        """
        catapdict = self.preparing_catap_data_and_simframe()
        self.quad_scan(catapdict)
