from elegantWriter_objects import *

class application(object):

    def __init__(self, parent=None):

        testlattice = elegantLattice(self)

        testlattice.addCommand(name='global',type='global_settings',log_file="elegant.log",error_log_file="elegant.err")
        testlattice.addCommand(name='runsetup',type='run_setup',lattice="doublering.lte",use_beamline="doublering",p_central_mev=700,centroid='%s.cen')

        testlattice.addElement(name='Q1',type='kquad',l=0.5,k1=2.3)
        testlattice.addElement(name='D1',type='drift',l=0.5)
        testlattice.addElement(name='BEND1',type='ksbend',l=0.5,angle=0.36,E1=0.01,E2=0.022)
        #
        # print D1*2
        latt1 = testlattice.addLine(name='latt1',line=[2*self.D1,self.Q1*2])
        latt3 = testlattice.addLine(name='latt3',line=[2*self.latt1,-self.BEND1,self.latt1,self.D1])
        latt2 = testlattice.addLine(name='latt2',line=[2*self.latt1,self.latt3,self.D1])

        print testlattice.latt3.write()
        # testlattice.writeCommandFile('test.ele')
        # testlattice.writeLatticeFile('test.lte')



ele = elegantInterpret()
lattice = ele.readElegantFile('lattice8.5.mff')
# print lattice.elements
# print lattice.drift97
print lattice.begarc1
lattice.writeLatticeFile('test.lte','arc1')

# application()
