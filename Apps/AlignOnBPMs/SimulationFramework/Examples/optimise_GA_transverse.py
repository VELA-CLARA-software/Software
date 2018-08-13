from Framework import *
import numpy as np
from constraints import *
import os
import read_twiss_file as rtf
import read_beam_file as rbf
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
import operator
import random
import multiprocessing
from scoop import futures
import csv

import shutil
import uuid

def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z

class TemporaryDirectory(object):
    """Context manager for tempfile.mkdtemp() so it's usable with "with" statement."""

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def tempname(self):
        return 'tmp'+str(uuid.uuid4())

    def __enter__(self, dir=os.getcwd()):
        exists = True
        while exists:
            self.name = dir + '/' + self.tempname()
            if not os.path.exists(self.name):
                exists=False
                os.makedirs(self.name)
        return self.name

    def __exit__(self, exc_type, exc_value, traceback):
        shutil.rmtree(self.name)

framework = Framework('twiss_temp', overwrite=False)
framework.loadSettings('clara400_v12.def')
parameters = framework.getElementType('quadrupole','k1')
best = parameters
# best = [0,0,0,0,0,0, 0,0,0,0,0,0,0,0, -0.595761, 0.665759, 0.606265, -0.378705, 1.,-0.917,-1.,-1.,0.921,0.122,-0.038,-0.396,0.872,-0.401,-0.043]
basescaling=4
# framework.astra.createInitialDistribution(npart=2**(3*basescaling), charge=250)
if not os.name == 'nt':
    framework.astra.defineASTRACommand(['mpiexec','-np',str(basescaling*3),'/opt/ASTRA/astra_MPICH2.sh'])
else:
    framework.astra.defineASTRACommand(['astra'])
# framework.createInputFiles()
# framework.runInputFiles(files=['injector400'])

class fitnessFunc():

    def __init__(self, args, tempdir, scaling=4, overwrite=True, verbose=False, summary=False):
        self.cons = constraintsClass()
        self.beam = rbf.beam()
        self.twiss = rtf.twiss()
        self.tmpdir = tempdir
        self.verbose = verbose
        self.summary = summary
        self.parameters = list(args)
        self.npart=2**(3*scaling)
        ncpu = scaling*3
        self.dirname = os.path.basename(self.tmpdir)
        self.framework = Framework(self.dirname, overwrite=overwrite)
        if not os.name == 'nt':
            self.framework.astra.defineASTRACommand(['mpiexec','-np',str(ncpu),'/opt/ASTRA/astra_MPICH2.sh'])
            self.framework.CSRTrack.defineCSRTrackCommand(['/opt/OpenMPI-1.4.3/bin/mpiexec','-n',str(ncpu),'/opt/CSRTrack/csrtrack_openmpi.sh'])
        else:
            self.framework.astra.defineASTRACommand(['astra'])
            self.framework.CSRTrack.defineCSRTrackCommand(['CSRtrack_1.201.wic.exe'])
        self.framework.loadSettings('clara400_v12.def')
        self.framework.setElementType('quadrupole','k1', self.parameters)
        self.framework.fileSettings['S02']['input']['particle_definition'] = '../twiss_temp/'+'injector400.$output[\'start_element\']$.001'
        self.framework.modifyFile('S02',['ASTRA_Options','N_red'], int(np.floor( (2**(3*basescaling)) / (2**(3*scaling)) )))

    def between(self, value, minvalue, maxvalue, absolute=True):
        if absolute:
            result = max([minvalue,min([maxvalue,abs(value)])])
        else:
            result = np.sign(value)*max([minvalue,min([maxvalue,abs(value)])])
        return result

    def calculateBeamParameters(self):
        twiss = self.twiss
        try:
            del self.framework.fileSettings['injector400']
            # self.framework.astra.createInitialDistribution(npart=self.npart, charge=250)
            self.framework.createInputFiles()
            self.framework.runInputFiles()

            constraintsList = {}
            constraintsListQuads = {
                'max_k': {'type': 'lessthan', 'value': [abs(p) for p in self.parameters], 'limit': 0.25, 'weight': 10},

            }
            constraintsList = merge_two_dicts(constraintsList, constraintsListQuads)
            twiss.read_astra_emit_files( [ self.dirname+'/'+n+'.Zemit.001' for n in self.framework.fileSettings.keys() if self.framework.fileSettings[n]['code'].upper() == 'ASTRA'] )
            constraintsListSigmas = {
                'max_xrms': {'type': 'lessthan', 'value': 1e3*twiss['sigma_x'], 'limit': 1, 'weight': 10},
                'max_yrms': {'type': 'lessthan', 'value': 1e3*twiss['sigma_y'], 'limit': 1, 'weight': 10},
                'min_xrms': {'type': 'greaterthan', 'value': 1e3*twiss['sigma_x'], 'limit': 0.1, 'weight': 10},
                'min_yrms': {'type': 'greaterthan', 'value': 1e3*twiss['sigma_y'], 'limit': 0.1, 'weight': 10},
                'last_exn': {'type': 'lessthan', 'value': 1e6*twiss['enx'][-1], 'limit': 0.6, 'weight': 1},
                'last_eyn': {'type': 'lessthan', 'value': 1e6*twiss['eny'][-1], 'limit': 0.6, 'weight': 1},
            }
            constraintsList = merge_two_dicts(constraintsList, constraintsListSigmas)
            twiss.read_astra_emit_files(self.dirname+'/S07.Zemit.001')
            tdc_position = self.framework.getElement('CLA-S07-TDC-01-R','position_start')[2]
            tdc_screen_position = self.framework.getElement('CLA-S07-DIA-SCR-03-W','position_start')[2]
            dechirper_position = self.framework.getElement('CLA-S07-DCP-01','position_start')[2]
            constraintsListS07 = {
                'tdc_phase_advance': {'type': 'equalto', 'value': twiss.interpolate(tdc_screen_position,'muy') - twiss.interpolate(tdc_position,'muy'), 'limit': 0.25, 'weight': 1},
                'tdc_screen_beta_y': {'type': 'greaterthan', 'value': twiss.extract_values('beta_y', tdc_position, tdc_screen_position), 'limit': 5, 'weight': 1},
                'dechirper_sigma_x': {'type': 'lessthan', 'value': 1e3*twiss.interpolate(dechirper_position, 'sigma_x'), 'limit': 0.1, 'weight': 1},
                'dechirper_sigma_y': {'type': 'lessthan', 'value': 1e3*twiss.interpolate(dechirper_position, 'sigma_y'), 'limit': 0.1, 'weight': 1},
            }
            constraintsList = merge_two_dicts(constraintsList, constraintsListS07)
            fitness = self.cons.constraints(constraintsList)
            if self.verbose:
                print self.cons.constraintsList(constraintsList)
            if self.summary:
                self.astra.createHDF5Summary(reference='Transverse_GA')
            return fitness
        except:
            return 1e6

def optfunc(args, dir=None, **kwargs):
    if dir == None:
        with TemporaryDirectory(dir=os.getcwd()) as tmpdir:
            fit = fitnessFunc(args, tmpdir, **kwargs)
            fitvalue = fit.calculateBeamParameters()
    else:
            fit = fitnessFunc(args, dir, **kwargs)
            fitvalue = fit.calculateBeamParameters()
    return (fitvalue,)


# print 'starting values = ', best

# framework.setElementType('quadrupole','k1', [0.8*i for i in best])
# parameters = framework.getElementType('quadrupole','k1')
# print 'after setting values = ', parameters

# twiss = rtf.twiss()

# emitfiles = framework.fileSettings.keys()
# twiss.read_astra_emit_files( [ '2/'+n+'.Zemit.001' for n in framework.fileSettings.keys() if framework.fileSettings[n]['code'].upper() == 'ASTRA'] )
# print twiss['sigma_x']
#twiss.read_astra_emit_files(self.dirname+'/test.2.Zemit.001')
print optfunc(best, dir=os.getcwd()+'/test_transverse', scaling=3, overwrite=True, verbose=True, summary=False)
exit()


# startranges = [[10, 32], [-40,40], [10, 32], [-40,40], [10, 32], [-40,40], [10, 32], [135,200], [10, 32], [-40,40], [0.8,0.15]]
startranges = [[0.8*i, 1.2*i] if abs(i) > 0 else [-0.1,0.1] for i in best]
generateHasBeenCalled = False
def generate():
    global generateHasBeenCalled
    if not generateHasBeenCalled:
        generateHasBeenCalled = True
        return creator.Individual(list(best))
    else:
        return creator.Individual(random.uniform(a,b) for a,b in startranges)

# print generate()

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("attr_bool", generate)

# Structure initializers
toolbox.register("Individual", generate)
toolbox.register("population", tools.initRepeat, list, toolbox.Individual)

if os.name == 'nt':
    toolbox.register("evaluate", optfunc, scaling=3)
else:
    toolbox.register("evaluate", optfunc, scaling=3)
toolbox.register("mate", tools.cxBlend, alpha=0.2)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=3, indpb=0.3)
toolbox.register("select", tools.selTournament, tournsize=3)


if __name__ == "__main__":
    random.seed(64)

    # Process Pool of 4 workers
    if not os.name == 'nt':
        pool = multiprocessing.Pool(processes=12)
    else:
        pool = multiprocessing.Pool(processes=3)
    toolbox.register("map", pool.map)
    # toolbox.register("map", futures.map)

    if not os.name == 'nt':
        pop = toolbox.population(n=48)
    else:
        pop = toolbox.population(n=6)
    hof = tools.HallOfFame(10)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)

    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=50,
                            stats=stats, halloffame=hof)

    # print 'pop = ', pop
    print logbook
    print hof

    try:
        print 'best fitness = ', optfunc(hof[0], dir=os.getcwd()+'/longitudinal_best_Short_240', npart=50000, ncpu=40, overwrite=True, verbose=True, summary=True)
        with open('longitudinal_best_Short_240/longitudinal_best_solutions.csv','wb') as out:
            csv_out=csv.writer(out)
            for row in hof:
                csv_out.writerow(row)
    except:
        with open('longitudinal_best_Short_240_solutions.csv.tmp','wb') as out:
            csv_out=csv.writer(out)
            for row in hof:
                csv_out.writerow(row)
    pool.close()
