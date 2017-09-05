from ASTRAInjector import *

''' initialise ASTRAFramework and set the base directory to '1'.
    If overwrite=False, nothing will be overwritten (useful for testing!) '''
astra = ASTRAInjector('1', overwrite=False)

''' Here we *can* set the base value of the ASTRA command
        - defaults to ['astra']
        - in linux we run multi-core using mpiexec
    This must be a list    '''
if not os.name == 'nt':
    astra.defineASTRACommand(['mpiexec','-np','12','/opt/ASTRA/astra_MPICH2.sh'])

''' Load a settings file '''
astra.loadSettings('short_240.settings')

''' Create an initial distribution
    - charge is in pC!
    '''
# astra.createInitialDistribution(npart=10000, charge=250)

''' Apply the new settings '''
# astra.applySettings()

''' Run ASTRA '''
# astra.runASTRAFiles()

''' Run this to create a summary file with all required input files, and the consequent output files'''
astra.createHDF5Summary(screens=[4929])

''' These commands convert the final bunch to SDDS and then compress it to an RMS value of <dt> '''
# ft = feltools('1')
# sddsfile = ft.convertToSDDS('test.in.128.4929.128')
# ft.sddsMatchTwiss(sddsfile, 'compressed.sdds', tstdev=5e-13)
