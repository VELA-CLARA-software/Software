from elegantWriter import *

# testlattice = elegantLattice()
#
# globalsettings = testlattice.addCommand('global_settings',log_file="elegant.log",error_log_file="elegant.err")
# runsetup = testlattice.addCommand('run_setup',lattice="doublering.lte",use_beamline="doublering",p_central_mev=700,centroid='%s.cen')
#
# Q1 = testlattice.addElement('kquad',l=0.5,k1=2.3)
# D1 = testlattice.addElement('drift',l=0.5)
# BEND1 = testlattice.addElement('ksbend',l=0.5,angle=0.36,E1=0.01,E2=0.022)
#
# # print D1*2
# latt1 = testlattice.addLine([2*D1,Q1*2])
# latt3 = testlattice.addLine([2*latt1,BEND1,latt1,D1])
# latt2 = testlattice.addLine([2*latt1,-latt3,D1])
#
# # testlattice.writeCommandFile('test.ele')
# testlattice.writeLatticeFile('test.lte')
class elegantInterpret(object):

    testlattice = elegantLattice()

    def readElegantFile(self,file):
        self.f = open(file,'r')
        line = self.readLine(self.f)
        while line != '':
            line = self.readLine(self.f)

    def readLine(self,f):
        element = ''
        tmpstring = f.readline()
        while '&' in tmpstring:
            element+= tmpstring
            tmpstring = f.readline()
        element+= tmpstring
        string = element.replace('&','').replace('\n','').replace(';','')
        if not 'line' in string.lower():
            try:
                pos = string.index(':')
                name = string[:pos]
                keywords = string[(pos+1):].split(',')
                commandtype = keywords[0].strip().lower()
                if commandtype in elementkeywords:
                    kwargs = {}
                    kwargs['type'] = commandtype
                    kwargs['name'] = name
                    for kw in keywords[1:]:
                        kwname = kw.split('=')[0].strip()
                        kwvalue = kw.split('=')[1].strip()
                        if kwname.lower() in elementkeywords[commandtype]:
                            kwargs[kwname.lower()] = kwvalue
                    # print self.testlattice.addElement(**kwargs)
                    setattr(name, self.testlattice.addElement(**kwargs))
                    # print name
            except:
                pass
        else:
            try:
                pos = string.index(':')
                name = string[:pos]
                pos1 = string.index('(')
                pos2 = string.index(')')
                lines = string[(pos1+1):pos2].split(',')
                setattr(name, self.testlattice.addLine(name=name,line=lines))
                print name
                    # kwargs = {}
                    # kwargs['type'] = commandtype
                    # kwargs['name'] = name
                    # for kw in keywords[1:]:
                    #     kwname = kw.split('=')[0].strip()
                    #     kwvalue = kw.split('=')[1].strip()
                    #     if kwname.lower() in elementkeywords[commandtype]:
                    #         kwargs[kwname.lower()] = kwvalue
                    # # print kwargs
                    # print testlattice.addElement(**kwargs)
            except:
                pass
        return element

ele = elegantInterpret()
ele.readElegantFile('alice.lte')
print ele.testlattice['lines']
ele.testlattice.writeLatticeFile('test.lte')
