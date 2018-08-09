import numpy as np
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname( os.path.abspath(__file__)))))
from SimulationFramework.Framework import *
from SimulationFramework.Modules.constraints import *
import SimulationFramework.Modules.read_beam_file as rbf
import SimulationFramework.Modules.read_twiss_file as rtf
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

def eaSimple(population, toolbox, cxpb, mutpb, ngen, stats=None,
             halloffame=None, verbose=__debug__):

    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if halloffame is not None:
        halloffame.update(population)

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print logbook.stream

    # Begin the generational process
    for gen in range(1, ngen + 1):
        # Select the next generation individuals
        offspring = toolbox.select(population, len(population))

        # Vary the pool of individuals
        offspring = algorithms.varAnd(offspring, toolbox, cxpb, mutpb)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Update the hall of fame with the generated individuals
        if halloffame is not None:
            halloffame.update(offspring)
            with open('longitudinal_best_solutions_running.csv','wb') as out:
                csv_out=csv.writer(out)
                for row in halloffame:
                    csv_out.writerow(row)

        # Replace the current population by the offspring
        population[:] = offspring

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print logbook.stream

    return population, logbook


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

''' Run the injector part once if only optimising post-injector parameters'''
# framework = Framework('twiss_temp', overwrite=False)
# framework.loadSettings('clara400_v12.def')
# parameters = framework.getElementType('quadrupole','k1')
# best = parameters
# best = [0,0,0,0,0,0, 0,0,0,0,0,0,0,0, -0.595761, 0.665759, 0.606265, -0.378705, 1.,-0.917,-1.,-1.,0.921,0.122,-0.038,-0.396,0.872,-0.401,-0.043]
# basescaling=4
# # framework.astra.createInitialDistribution(npart=2**(3*basescaling), charge=250)
# if not os.name == 'nt':
#     framework.astra.defineASTRACommand(['mpiexec','-np',str(basescaling*3),'/opt/ASTRA/astra_MPICH2.sh'])
# else:
#     framework.astra.defineASTRACommand(['astra'])
# # framework.createInputFiles()
# # framework.runInputFiles(files=['injector400'])

class fitnessFunc():

    def __init__(self, args, tempdir, scaling=4, overwrite=True, verbose=False, summary=False):
        self.cons = constraintsClass()
        self.beam = rbf.beam()
        self.twiss = rtf.twiss()
        self.tmpdir = tempdir
        self.verbose = verbose
        self.summary = summary
        self.overwrite = overwrite
        ''' if only post-injector optimisation'''
        # post_injector = True
        self.post_injector = False
        if self.post_injector:
            linac2field, linac2phase, linac3field, linac3phase, fhcfield, fhcphase, linac4field, linac4phase, bcangle = args
            self.parameters = dict(zip(['linac2field', 'linac2phase', 'linac3field', 'linac3phase', 'fhcfield', 'fhcphase', 'linac4field', 'linac4phase', 'bcangle'], args))
        else:
            ''' including injector parameters '''
            gunphase, gunsol, linac1field, linac1phase, linac1sol1, linac1sol2, linac2field, linac2phase, linac3field, linac3phase, fhcfield, fhcphase, linac4field, linac4phase, bcangle = args
            self.parameters = dict(zip(['gunphase','gunsol','linac1field','linac1phase', 'linac1sol1', 'linac1sol2', 'linac2field', 'linac2phase', 'linac3field', 'linac3phase', 'fhcfield', 'fhcphase', 'linac4field', 'linac4phase', 'bcangle'], args))
        self.npart=2**(3*scaling)
        ncpu = scaling*3
        if self.post_injector:
            self.linacfields = np.array([linac2field, linac3field, linac4field])
        else:
            self.linacfields = np.array([linac1field, linac2field, linac3field, linac4field])
        self.dirname = os.path.basename(self.tmpdir)
        self.framework = Framework(self.dirname, overwrite=overwrite)
        if not os.name == 'nt':
            self.framework.astra.defineASTRACommand(['mpiexec','-np',str(ncpu),'/opt/ASTRA/astra_MPICH2.sh'])
            self.framework.CSRTrack.defineCSRTrackCommand(['/opt/OpenMPI-1.4.3/bin/mpiexec','-n',str(ncpu),'/opt/CSRTrack/csrtrack_openmpi.sh'])
        else:
            self.framework.astra.defineASTRACommand(['astra'])
            self.framework.CSRTrack.defineCSRTrackCommand(['CSRtrack_1.201.wic.exe'])
        self.framework.loadSettings('Lattices/clara400_v12.def')
        if self.post_injector:
            self.framework.fileSettings['S02']['input']['particle_definition'] = '../twiss_temp/'+'injector400.$output[\'start_element\']$.001'
            self.framework.modifyFile('S02',['ASTRA_Options','N_red'], int(np.floor( (2**(3*basescaling)) / (2**(3*scaling)) )))
        else:
            self.framework.modifyElement('CLA-HRG1-GUN-CAV', 'phase', gunphase)
            self.framework.modifyElement('CLA-HRG1-GUN-SOL', 'field_amplitude', gunsol)
            self.framework.modifyElement('CLA-L01-CAV', 'field_amplitude', abs(linac1field))
            self.framework.modifyElement('CLA-L01-CAV', 'phase', linac1phase)
            self.framework.modifyElement('CLA-L01-CAV-SOL-01', 'field_amplitude', linac1sol1)
            self.framework.modifyElement('CLA-L01-CAV-SOL-02', 'field_amplitude', linac1sol2)
        self.framework.modifyElement('CLA-L02-CAV', 'field_amplitude', abs(linac2field))
        self.framework.modifyElement('CLA-L02-CAV', 'phase', linac2phase)
        self.framework.modifyElement('CLA-L03-CAV', 'field_amplitude', abs(linac3field))
        self.framework.modifyElement('CLA-L03-CAV', 'phase', linac3phase)
        self.framework.modifyElement('CLA-L4H-CAV', 'field_amplitude', abs(fhcfield))
        self.framework.modifyElement('CLA-L4H-CAV', 'phase', fhcphase)
        self.framework.modifyElement('CLA-L04-CAV', 'field_amplitude', abs(linac4field))
        self.framework.modifyElement('CLA-L04-CAV', 'phase', linac4phase)
        self.framework.fileSettings['VBC']['groups']['VBC']['dipoleangle'] = abs(bcangle)


    def between(self, value, minvalue, maxvalue, absolute=True):
        if absolute:
            result = max([minvalue,min([maxvalue,abs(value)])])
        else:
            result = np.sign(value)*max([minvalue,min([maxvalue,abs(value)])])
        return result

    def calculateBeamParameters(self):
        bcangle = float(self.framework.fileSettings['VBC']['groups']['VBC']['dipoleangle'])
        try:
            if bcangle < 0.05 or bcangle > 0.125:
                raise ValueError
            if self.post_injector:
                del self.framework.fileSettings['injector400']
            else:
                self.framework.astra.createInitialDistribution(npart=self.npart, charge=250)
            if self.overwrite:
                self.framework.createRunProcessInputFiles()

            # self.beam.read_astra_beam_file(self.dirname+'/S07.4928.001')
            self.beam.read_HDF5_beam_file(self.dirname+'/CLA-S07-DIA-BPM-02.hdf5')
            self.beam.slices = 10
            self.beam.bin_time()
            sigmat = 1e12*np.std(self.beam.t)
            sigmap = np.std(self.beam.p)
            meanp = np.mean(self.beam.p)
            emitx = 1e6*self.beam.normalized_horizontal_emittance
            emity = 1e6*self.beam.normalized_vertical_emittance
            fitp = 100*sigmap/meanp
            fhcfield = self.parameters['fhcfield']
            peakI, peakIMomentumSpread, peakIEmittanceX, peakIEmittanceY, peakIMomentum = self.beam.sliceAnalysis()
            chirp = self.beam.chirp
            print 'momentum_spread = ', fitp
            constraintsList = {
                'peakI_min': {'type': 'greaterthan', 'value': abs(peakI), 'limit': 400, 'weight': 25},
                'peakI_max': {'type': 'lessthan', 'value': abs(peakI), 'limit': 600, 'weight': 100},
                'peakIMomentumSpread': {'type': 'lessthan', 'value': peakIMomentumSpread, 'limit': 0.2, 'weight': 10},
                'peakIEmittanceX': {'type': 'lessthan', 'value': 1e6*peakIEmittanceX, 'limit': 0.5, 'weight': 10},
                'peakIEmittanceY': {'type': 'lessthan', 'value': 1e6*peakIEmittanceY, 'limit': 0.5, 'weight': 10},
                'peakIMomentum': {'type': 'equalto','value': 1e-6*peakIMomentum, 'limit': 240, 'weight': 20},
                'linac fields': {'type': 'lessthan', 'value': 1e-6*self.linacfields, 'limit': 32, 'weight': 100},
                '4hc field': {'type': 'lessthan', 'value': 1e-6*fhcfield, 'limit': 35, 'weight': 100},
                'horizontal emittance': {'type': 'lessthan', 'value': emitx, 'limit': 0.75, 'weight': 10},
                'vertical emittance': {'type': 'lessthan', 'value': emity, 'limit': 0.75, 'weight': 10},
                'momentum_spread': {'type': 'lessthan', 'value': fitp, 'limit': 0.2, 'weight': 10},
                # 'chirp': {'type': 'lessthan', 'value': chirp, 'limit': 1, 'weight': 1}
            }
            # self.twiss.read_astra_emit_files(self.dirname+'/S07.Zemit.001')
            # constraintsList5 = {
            #     'last_exn_5': {'type': 'lessthan', 'value': 1e6*self.twiss['enx'], 'limit': 0.75, 'weight': 1},
            #     'last_eyn_5': {'type': 'lessthan', 'value': 1e6*self.twiss['eny'], 'limit': 0.75, 'weight': 1},
            # }
            # constraintsList = merge_two_dicts(constraintsList, constraintsList5)
            fitness = self.cons.constraints(constraintsList)
            if self.verbose:
                print self.cons.constraintsList(constraintsList)
            if self.summary:
                np.save('summary_constraints.txt', self.cons.constraintsList(constraintsList))
                # self.astra.createHDF5Summary(reference='Longitudinal_GA')
            return fitness
        except Exception as e:
            print(e)
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


framework = Framework('longitudinal_best', overwrite=False)
framework.loadSettings('Lattices/clara400_v12.def')
parameters = []
''' if including injector'''
parameters.append(framework.getElement('CLA-HRG1-GUN-CAV', 'phase'))
parameters.append(framework.getElement('CLA-HRG1-GUN-SOL', 'field_amplitude'))
parameters.append(framework.getElement('CLA-L01-CAV', 'field_amplitude'))
parameters.append(framework.getElement('CLA-L01-CAV', 'phase'))
parameters.append(framework.getElement('CLA-L01-CAV-SOL-01', 'field_amplitude'))
parameters.append(framework.getElement('CLA-L01-CAV-SOL-02', 'field_amplitude'))
''' always '''
parameters.append(framework.getElement('CLA-L02-CAV', 'field_amplitude'))
parameters.append(framework.getElement('CLA-L02-CAV', 'phase'))
parameters.append(framework.getElement('CLA-L03-CAV', 'field_amplitude'))
parameters.append(framework.getElement('CLA-L03-CAV', 'phase'))
parameters.append(framework.getElement('CLA-L4H-CAV', 'field_amplitude'))
parameters.append(framework.getElement('CLA-L4H-CAV', 'phase'))
parameters.append(framework.getElement('CLA-L04-CAV', 'field_amplitude'))
parameters.append(framework.getElement('CLA-L04-CAV', 'phase'))
parameters.append(framework.fileSettings['VBC']['groups']['VBC']['dipoleangle'])
# parameters.append(0.106)
best = parameters

# results = []
# with open('longitudinal_best_solutions_running.csv', 'r') as csvfile:
#   reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
#   for row in reader:
#     results.append(row)
# best = results[0]

print 'starting values = ', best

# print optfunc(best, dir=os.getcwd()+'/best_longitudinal', scaling=6, overwrite=False, verbose=True, summary=True)
# exit()


# startranges = [[10, 32], [-40,40], [10, 32], [-40,40], [10, 32], [-40,40], [10, 32], [135,200], [10, 32], [-40,40], [0.8,0.15]]
startranges = [[0.9*i, 1.1*i] for i in best]
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
    toolbox.register("evaluate", optfunc, scaling=4)
else:
    toolbox.register("evaluate", optfunc, scaling=4)
toolbox.register("mate", tools.cxBlend, alpha=0.2)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=3, indpb=0.3)
toolbox.register("select", tools.selTournament, tournsize=3)


if __name__ == "__main__":
    global hof
    random.seed(64)

    # Process Pool of 4 workers
    if not os.name == 'nt':
        pool = multiprocessing.Pool(processes=3)
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

    pop, logbook = eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=50,
                            stats=stats, halloffame=hof, verbose=True)

    pool.close()
    # print 'pop = ', pop
    print logbook
    print hof

    try:
        print 'best fitness = ', optfunc(hof[0], dir=os.getcwd()+'/best_longitudinal', scaling=6, overwrite=True, verbose=True, summary=True)
        with open('best_longitudinal/longitudinal_best_solutions.csv','wb') as out:
            csv_out=csv.writer(out)
            for row in hof:
                csv_out.writerow(row)
        with open('best_longitudinal/longitudinal_best_stats.csv','wb') as out:
            csv_out=csv.writer(out)
            for row in stats:
                csv_out.writerow(row)
    except:
        with open('longitudinal_best_solutions.csv.tmp','wb') as out:
            csv_out=csv.writer(out)
            for row in hof:
                csv_out.writerow(row)
