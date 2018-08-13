import yaml, collections, subprocess, os, sys
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\..\\SAMM3.0\\Python\\')
from SAMMcore.Components import Drift as d
from SAMMcore.Components import Dipole as D
from SAMMcore.Components import Quadrupole as Q
from SAMMcore.Components import Screen as S
from SAMMcore.Components import OrbitCorrector as C
from SAMMcore.Components import BeamPositionMonitor as BPM
from SAMMcore.SAMMlab import Beamline
from SAMMcore.SAMMlab import Beam
from SAMMcore.Particles import Electron
from SAMMcore.SAMMlab import PhysicalUnits
import numpy as np


stream = file("VELA.yaml", 'r')
settings = yaml.load(stream)
elements = settings['elements']
groups = settings['groups']


"""1. Make a Beam"""
beam1 = Beam.Beam(species=Electron.Electron, energy=4.5 * PhysicalUnits.MeV)
ptcle1 = [0.001, 0, 0, 0, 0, 0]
ptcle2 = [0, 0, 0.001, 0, 0, 0]
ptcle3 = [0, 0, 0, 0, 0, 0]
beam1.particles = np.array([ptcle1, ptcle2, ptcle3])
"""2. Make a Beamline"""
V1_SP1 = Beamline.Beamline(componentlist=[])
driftCounter = 0
for index, name in enumerate(groups['VELA-SP1']):
    element = elements[name]
    component = None
    # Check element type and add accordingly
    if element['type'] == 'dipole':
        angle = element['angle']
        field = beam1.rigidity * angle * (np.pi / 180) / element['length']
        print field
        print angle * (np.pi / 180)
        component = D.Dipole(name=name, length=element['length'],
                             theta=angle * (np.pi / 180), field=field)
    elif element['type'] == 'quadrupole':
        component = Q.Quadrupole(name=name,
                                 length=element['length'],
                                 gradient=0.0)
    elif element['type'] == 'kicker':
        component = C.OrbitCorrector(name=name,
                                     field=[0, 0],
                                     length=element['length'])
    elif element['type'] == 'bpm':
        component = BPM.BeamPositionMonitor(name=name, length=element['length'])
    elif element['type'] == 'screen':
        component = S.Screen(name=name)
    elif element['type'] == 'wcm':
        component = d.Drift(name=name, length=element['length'])
    elif element['type'] == 'tdc':
        component = d.Drift(name=name, length=element['length'])
    else:
        print ('ERROR: This reader doesn\'t recognise element type of ', name)

    if index != 0:
        lastElement = elements[groups['VELA-SP1'][index - 1]]
        backOfLast = lastElement['global_position'][-1]
        frontOfCurrent = element['global_position'][-1]
        #if element['global_rotation'][-1] == 45:
        if element['type'] == 'dipole':
            print 'LALALALALAL'
            frontOfCurrent = element['global_front'][-1]
        else:
            frontOfCurrent = (frontOfCurrent -
                              element['length'] * np.cos(element['global_rotation'][-1]*np.pi / 180))
        #elif element['global_rotation'][-1] == 0:
        #    frontOfCurrent = (frontOfCurrent - element['length'])
        #else:
        #    print('Unknown rotation read')
        if frontOfCurrent < backOfLast:
            print ('Elements ', groups['VELA-SP1'][index - 1],
                   ' and ', name, ' overlap!!')
        elif frontOfCurrent > backOfLast:
            # Add a drift before adding component
            b = frontOfCurrent
            a = backOfLast
            print 'drift: ', (b - a)/np.cos(element['global_rotation'][-1]*np.pi / 180)
            driftCounter = driftCounter + 1
            driftComponent = d.Drift(name='drift' + str(driftCounter),
                                     length=(b - a)/np.cos(element['global_rotation'][-1]*np.pi / 180))
            V1_SP1.componentlist.append(driftComponent)
        else:
            print 'No drift required', index

    # Append component
    V1_SP1.componentlist.append(component)

len(V1_SP1.componentlist)
a=40 # len(V1_SP1.componentlist)-1
print V1_SP1.componentlist[a].name
print V1_SP1.componentlist[a].length
#for c in V1_SP1.componentlist:
#    print c.name
beam2 = V1_SP1.TrackMatlab([0, a], beam1)
print "beam2 particle1 = ", beam1.particles[0]
print "beam2 particle2 = ", beam1.particles[1]
print "beam2 particle3 = ", beam1.particles[2]
