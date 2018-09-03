import model as model
import sys, time
import numpy as np

qa = model.Model()
momentum = raw_input("What is your momentum in MeV/c? ")
# sys.stdout = open(filename, "w")
print 'Input momentum is ', momentum, 'MeV/c'


with open(dir+timestr+'_'+'_QuadAlign.dat', 'a') as file:
	for no in range(1,5):
		quad = 'S02-QUAD'+str(no)
		result = qa.quadAligner(quad=quad, bpm='S02-BPM02', stepSize=1, nSamples=20, start=0.0, end=10, momentum=float(momentum))
		file.writelines('\t'.join(str(j) for j in i) + '\n' for i in [result])
