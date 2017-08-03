from ASTRAInjector import *

astra = ASTRAInjector('1')
if not os.name == 'nt':
    astra.defineASTRACommand(['mpiexec','-np','12','/opt/ASTRA/astra_MPICH2.sh'])
astra.loadSettings('short_240.settings')
astra.createInitialDistribution(npart=100, charge=10)
astra.applySettings()
