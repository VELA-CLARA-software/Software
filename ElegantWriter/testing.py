from elegantWriter import *

settings = command('global_settings',log_file="elegant.log",error_log_file="elegant.err")
runsetup = command('run_setup',lattice="doublering.lte",use_beamline="doublering",p_central_mev=700,centroid='%s.cen')
test = command('alter_elements',name="test",item='KQ1',value=10)

# print test
print settings.write()
print runsetup.write()
print test.write()
