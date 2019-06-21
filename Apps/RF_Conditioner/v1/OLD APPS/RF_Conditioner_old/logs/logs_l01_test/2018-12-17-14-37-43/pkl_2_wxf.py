import re
import os
import cPickle as pkl
import wolframclient.serializers as wxf
import random
	
def pkl2wxf(path):
	file = open(path, 'rb')
	objs = []
	while True:
		try: 
			objs.append(pkl.load(file))
		except EOFError: break
	file.close()
	#print(objs)
	path2 = path.replace(".pkl","")
	wxf.export(objs, path2 + '.wxf', target_format='wxf')
			
			
files = [f for f in os.listdir('.') if os.path.isfile(f)]

for f in files:
	if re.search('.pkl', f):
		pkl2wxf(f)