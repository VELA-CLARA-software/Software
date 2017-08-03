from ASTRAGeneral import *
import numpy as np
from operator import add
astra = ASTRAInjector('1')
if not os.name == 'nt':
    astra.defineASTRACommand(['mpiexec','-np','12','/opt/ASTRA/astra_MPICH2.sh'])
astra.loadSettings('short_240.def')
# print {k: v for k, v in astra.fileSettings['test.in.126'] if {'type': dipole} in k.values()]
# elements = astra.fileSettings['test.in.126']
# for l, e in elements.items():
#     if 'type' in e.keys() and 'dipole' in e['type']:
#         print e

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def sortByPositionFunction(element):
    return float(element[1]['position'][2])

def rotationMatrix(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.matrix([[c, 0, -s], [0, 1, 0], [s, 0, c]])

# def addDrift(d, length=0.1):
#     if not len(d) == 2:

def createDrifts(elements, startpos=None):
    positions = []
    elementno = 0
    for name, e in elements:
        pos = np.array(e['position'])
        positions.append(pos)
        length = np.array([0,0,e['length']])
        positions.append(pos+length)
    if not startpos == None:
        positions.prepend(startpos)
    else:
        positions = positions[1:]
        positions.append(positions[-1]+[0,0,0.1])
    driftdata = list(chunks(positions, 2))
    for d in driftdata:
        if len(d) > 1:
            elementno += 1
            length = d[1][2] - d[0][2]
            elements.append(['drift'+str(elementno),
                            {'length': length, 'type': 'drift',
                             'position': list(d[0])
                            }])
    return sorted(elements, key=sortByPositionFunction)

def getParameter(elem, param, default=0):
    return elem[param] if param in elem else default

def setDipoleAngle(dipole, angle=0):
    name, d = dipole
    d['angle'] = np.sign(d['angle'])*angle
    return [name, d]

def createASTRAChicane(group, dipoleangle=None):
    dipoles = astra.getGroup(group)
    if not dipoleangle == None:
        dipoles = [setDipoleAngle(d,dipoleangle) for d in dipoles]
    dipoles = createDrifts(dipoles)
    dipolepos, localXYZ = astra.elementPositions(dipoles)
    dipolepos = list(chunks(dipolepos,2))
    corners = [0,0,0,0]
    dipoleno = 0
    for elems in dipolepos:
        dipoleno += 1
        p1, psi1, nameelem1 = elems[0]
        p2, psi2, nameelem2 = elems[1]
        name, d = nameelem1
        angle1 = getParameter(nameelem1[1],'angle')
        angle2 = getParameter(nameelem2[1],'angle')
        length = getParameter(d,'length')
        e1 = getParameter(d,'e1')
        e2 = getParameter(d,'e2')
        rbend = 1 if d['type'] == 'rdipole' else 0
        rho = d['length']/angle1 if 'length' in d and angle1 > 1e-9 else 0
        print rho
        theta = -1*psi1+e1-rbend*rho*angle1/2.0
        corners[0] = np.array(map(add,np.transpose(p1),np.dot([0.2*length,0,0], rotationMatrix(theta))))[0,0]
        corners[3] = np.array(map(add,np.transpose(p1),np.dot([-0.2*length,0,0], rotationMatrix(theta))))[0,0]
        theta = -1*psi2-e2-rbend*rho*angle1/2.0
        corners[1] = np.array(map(add,np.transpose(p2),np.dot([0.2*length,0,0], rotationMatrix(theta))))[0,0]
        corners[2] = np.array(map(add,np.transpose(p2),np.dot([-0.2*length,0,0], rotationMatrix(theta))))[0,0]
        dipolenostr = str(dipoleno)
        diptext = "D_Type("+dipolenostr+")='horizontal'\n"+\
        "D_Gap(1,"+dipolenostr+")=0.02,\n"+\
        "D_Gap(2,"+dipolenostr+")=0.02,\n"+\
        "D1("+dipolenostr+")=("+str(corners[0][0])+","+str(corners[0][2])+"),\n"+\
        "D2("+dipolenostr+")=("+str(corners[1][0])+","+str(corners[1][2])+"),\n"+\
        "D3("+dipolenostr+")=("+str(corners[2][0])+","+str(corners[2][2])+"),\n"+\
        "D4("+dipolenostr+")=("+str(corners[3][0])+","+str(corners[3][2])+"),\n"+\
        "D_radius("+dipolenostr+")="+str(rho)+"\n"
        print diptext

createASTRAChicane('laser-heater',1)
