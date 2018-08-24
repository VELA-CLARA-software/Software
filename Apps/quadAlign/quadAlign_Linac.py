import model as model
import sys, time
import numpy as np

timestr = time.strftime("%H%M%S")
dir = '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\'+time.strftime("%Y\\%m\\%d")+'\\'
filename = dir+timestr+'_'+'_QuadAlign.txt'

def setHCorrectors(h1):
	h2 = (0.0262516 - 1.25 * h1)
	print 'Setting S01-HCOR1 to ', h1, 'A'
	qa.machine.setCorr('S01-HCOR1', h1)
	print 'Setting S01-HCOR2 to ', h2, 'A'
	qa.machine.setCorr('S01-HCOR2', h2)
	while abs(qa.machine.getCorr('S01-HCOR1') - h1) > 0.05 or abs(qa.machine.getCorr('S01-HCOR2') - h2) > 0.05:
		time.sleep(0.1)
	return h2

def setVCorrectors(v1):
	v2 = (-0.962529 - 1.44488 * v1)
	print 'Setting S01-VCOR1 to ', v1, 'A'
	qa.machine.setCorr('S01-VCOR1', v1)
	print 'Setting S01-VCOR1 to ', v2, 'A'
	qa.machine.setCorr('S01-VCOR2', v2)
	while abs(qa.machine.getCorr('S01-VCOR1') - v1) > 0.05 or abs(qa.machine.getCorr('S01-VCOR2') - v2) > 0.05:
		time.sleep(0.1)
	return v2

def doQuadScan():
	global h1, h2, v1,v2
	for no in range(1,5):
		ans = qa.quadAligner(no=no, stepSize=2, nSamples=10, start=0.0, end=10, momentum=float(momentum))
		data.append([h1,h2,v1,v2,ans[0],ans[1],ans[2]])


qa = model.Model()
momentum = raw_input("What is your momentum in MeV/c? ")
# sys.stdout = open(filename, "w")
print 'Input momentum is ', momentum, 'MeV/c'

v1 = 0
v2 = setVCorrectors(v1)

data = [['hcorr1', 'hcorr2', 'vcorr1', 'vcorr2', 'quad', 'dx', 'dy']]
for h in np.arange(0,4.5,0.5):
	h1 = h
	h2 = setHCorrectors(h)
	# time.sleep(5)
	doQuadScan()

print data
with open(dir+timestr+'_'+'_QuadAlignX.dat', 'w') as file:
	file.writelines('\t'.join(str(j) for j in i) + '\n' for i in data)

h1 = 0
h2 = setHCorrectors(h1)

data = [['hcorr1', 'hcorr2', 'vcorr1', 'vcorr2', 'quad', 'dx', 'dy']]
for v in np.arange(-4.0,0.5,0.5):
	v1 = v
	v2 = setVCorrectors(v)
	# time.sleep(5)
	doQuadScan()

with open(dir+timestr+'_'+'_QuadAlignY.dat', 'w') as file:
	file.writelines('\t'.join(str(j) for j in i) + '\n' for i in data)
