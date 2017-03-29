from elegantWriter_objects import *

''' Here we create an elegant environment '''
ele = elegantInterpret()
''' now we read in a lattice file (can also be MAD format, but not all commands are equivalent (cavities are a problem!)) '''
lattice = ele.readElegantFile('lattice8.5.mff')
''' lets modify the 'k1' parameter of the element 'st1dip01high' '''
lattice.st1dip01high['k1'] = 1.2
''' print the output '''
print 'st1dip01high k1 = ', lattice['st1dip01high']['k1']
''' or we could do this! '''
lattice['st1dip01high']['k1'] = 1.8
''' print the output using a different mechanism - isn't python great! '''
print 'st1dip01high k1 = ', lattice.st1dip01high.k1
''' let's write out the lattice to a .lte file - we have to give the line name '''
lattice.writeLatticeFile('test.lte','lin2wig')


''' Ok. Lets create a new lattice from scratch '''
testlattice = elegantLattice()
''' Here we create a command, but do not assign a name - it defaults to the type '''
testlattice.addCommand(type='global_settings',log_file="elegant.log",error_log_file="elegant.err")
''' here we assign a name - Why? We may want multiple 'run_setup' commands in the same command file... '''
testlattice.addCommand(name='runsetup',type='run_setup',lattice="doublering.lte",use_beamline="doublering",p_central_mev=700,centroid='%s.cen')
''' this will print out all commands in the 'testlattice' environment '''
print 'testlattice commands = ', testlattice.commands

''' add some elements '''
testlattice.addElement(name='Q1',type='kquad',l=0.5,k1=2.3)
testlattice.addElement(name='D1',type='drift',l=0.5)
testlattice.addElement(name='BEND1',type='ksbend',l=0.5,angle=0.36,E1=0.01,E2=0.022)

''' We can do some arithmetic on elements'''
print '2*D1 = ', [getattr(x,'name') for x in (2*testlattice.D1)]
''' and it "reverses" dipoles (correctly I think!)
    NB. the brackets are so we get the properties of the reversed element, not the negative of properties of the normal element'''
print 'Negative BEND1 = ', (-testlattice.BEND1).properties
''' lets define some lines '''
latt1 = testlattice.addLine(name='latt1',line=[2*testlattice.D1,'Q1*2'])
''' we can use elements in the environment (testlattice.<elementname>) or strings '''

''' this has a reversed element in it...'''
latt3 = testlattice.addLine(name='latt3',line=[2*testlattice.latt1,-testlattice.BEND1,testlattice.latt1,testlattice.D1])
latt2 = testlattice.addLine(name='latt2',line=[2*testlattice.latt1,testlattice.latt3,testlattice.D1])

''' now we can print out what the elegant lattice line definition would look like - it should have a - in front of the bend! '''
print 'line definition for latt3 = ', testlattice.latt3.write()
