import os, sys
import time
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..', '..', 'SimFrame_fork', 'SimFrame')))
sys.path.append(
    (os.path.abspath(os.path.join(os.getcwd(), '..',  '..', 'VELA_CLARA_repository', 'Software', 'Utils',
                                  'MachineState'))))
sys.path.append(
    (os.path.abspath(os.path.join(os.getcwd(), '..', '..', 'VELA_CLARA_repository', 'catapillar-build',
                                  'PythonInterface', 'Release'))))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'QuadScan')))
from QuadScan.virtualclarabeamsizes import BeamSizeDetermination

a= BeamSizeDetermination()
a.charge = 10.0
a.screen = 'CLA-S02-DIA-CAM-03'

a.current_path = os.path.abspath(os.path.join(os.getcwd(), '..', '..', 'Emittance_matlab', 'CurrentList.txt'))
a.path_output = os.path.abspath(os.path.join(os.getcwd(), '..', '..', 'Emittance_matlab', 'quad_scan_beamsizes.png'))
a.fill_in_currents_from_file()
a.currents_to_quad_strengths()

a.sequence_to_prepare_machine_state_and_simframe()
print('+++++++++++++++++ Screen_data = {} +++++++++\n'.format(a.screen_data))
print('+++++++++++++++++ Beam_size = {} +++++++++\n'.format(a.beam_sizes))
#a.plot_quad_scan()
#a.finding_eigenvalues()
print('+++++++++++++++++ Transformation matrix = {} +++++++++\n'.format(a.emits_matrix))
print('+++++++++++++++++ Normalised Emittance values = {} +++++++++\n'.format(a.emits))
#time.sleep(20)