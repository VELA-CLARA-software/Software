import model as model
import sys, time
import numpy as np

qa = model.Model()
momentum = raw_input("What is your momentum in MeV/c? ")
# sys.stdout = open(filename, "w")
print 'Input momentum is ', momentum, 'MeV/c'

for no in range(1,5):
	qa.quadAligner(no=no, stepSize=1, nSamples=20, start=0.0, end=10, momentum=float(momentum))
