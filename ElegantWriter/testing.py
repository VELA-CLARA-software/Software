from elegantWriter import *

settings = command('global_settings',log_file="elegant.log",error_log_file="elegant.err")
runsetup = command('run_setup',lattice="doublering.lte",use_beamline="doublering",p_central_mev=700,centroid='%s.cen')
test = command('alter_elements',name="test",item='KQ1',value=10)

Q1 = element('kquad',l=0.5,k1=2.3)
D1 = element('drift',l=0.5)

lattice = elementLine(line=[D1,Q1,D1,Q1,D1,Q1,D1,Q1,D1,D1,Q1,D1,Q1,D1,Q1,D1,Q1,D1,D1,Q1,D1,Q1,D1,Q1,D1,Q1,D1,D1,Q1,D1,Q1,D1,Q1,D1,Q1,D1])

# print test
print settings.write()
print runsetup.write()
print test.write()
# print Q1.write()
# print D1.write()
lattice.writeElements()
print lattice.write()
