import sys, os, math
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname( os.path.abspath(__file__)))))
from SimulationFramework.Framework import *
import SimulationFramework.Modules.read_beam_file as rbf
beam = rbf.beam()
degree = 1./360.*2.*math.pi

scaling = 3

npart=2**(3*scaling)


''' ############# CLARA 400 to VELA #############'''

framework = Framework('C2V', overwrite=True, clean=True)

framework.loadSettings('Lattices/CLA400-C2V-INJ.def')
framework.astra.createInitialDistribution(npart=npart,charge=250)
framework.createRunProcessInputFiles()


''' ############# CLARA 400 #############'''

# framework = Framework('CLARA', overwrite=True, clean=False)
#
# ncpu = scaling*3
#
# if not os.name == 'nt':
#     framework.astra.defineASTRACommand(['mpiexec','-np',str(ncpu),'/opt/ASTRA/astra_MPICH2.sh'])
#     framework.CSRTrack.defineCSRTrackCommand(['/opt/OpenMPI-1.4.3/bin/mpiexec','-n',str(ncpu),'/opt/CSRTrack/csrtrack_openmpi.sh'])
# else:
#     framework.astra.defineASTRACommand(['astra'])
#     framework.CSRTrack.defineCSRTrackCommand(['CSRtrack_1.201.wic.exe'])
#
# framework.loadSettings('Lattices/clara400_v12_elegant.def')
# framework.astra.createInitialDistribution(npart=npart,charge=250)
# framework.modifyElement('CLA-L01-CAV-SOL-01','field_amplitude', 0)
# framework.modifyElement('CLA-L01-CAV-SOL-02','field_amplitude', 0)
# framework.createRunProcessInputFiles(run=True, files=['S02','L02'])
