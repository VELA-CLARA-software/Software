import sys
from elegantWriter_objects import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pyqtgraph as pg
import subprocess

class elegantGUI(QMainWindow):
    def __init__(self, parent = None):
        super(elegantGUI, self).__init__(parent)
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

        lattice.addCommand(type='global_settings',log_file="elegant.log",error_log_file="elegant.err")
        print lattice.global_settings.write()
        proc = subprocess.Popen(['elegant','-pipe=in'],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        )
        stdout_value, stderr_value = proc.communicate(lattice.global_settings.write())
        print 'stdout = ', repr(stdout_value)
        print 'stderr = ', repr(stderr_value)
        # self.table = latticeTable(lattice)
        # self.table.updateTable('lin2wig')
        # self.setCentralWidget(self.table)

class latticeTable(QTableWidget):

    def __init__(self, lattice, headings=None):
        super(latticeTable, self).__init__()
        if headings == None:
            self.headings = ['name','type','l','k1']
        else:
            self.headings = headings
        self.lattice = lattice
        self.itemChanged.connect(self.someFunc)

    def updateTable(self,line):
        self.itemChanged.disconnect(self.someFunc)
        self.lattprops = self.lattice.getLatticeDefinitions(line, self.headings)
        self.elementNames = self.lattprops.keys()
        self.setRowCount(len(self.lattprops))
        shortenedHeadings = self.headings
        shortenedHeadings.remove('name')
        columncount = len(shortenedHeadings)
        self.setColumnCount(columncount)
        self.setVerticalHeaderLabels(self.elementNames)
        self.setHorizontalHeaderLabels(shortenedHeadings)
        self.tableSetData()
        self.itemChanged.connect(self.someFunc)

    def tableSetData(self):
        row = 0
        for key,val in self.lattprops.items():
            col = 0
            for h in self.headings:
                if not h == 'name':
                    if h == 'type':
                        widget = QComboBox()
                        i = 0
                        for elemtype in sorted(elementkeywords):
                            widget.addItem(elemtype)
                            if val[h] == elemtype:
                                widget.setCurrentIndex(i)
                            i += 1
                        widget.currentIndexChanged.connect(self.typeChanged)
                        self.setCellWidget(row,col,widget)
                    else:

                        if val[h] == None:
                            item = QTableWidgetItem('')
                            item.setFlags(Qt.ItemIsEnabled)
                        else:
                            item = QTableWidgetItem(str(val[h]))
                        self.setItem(row,col,item)
                    col += 1
            row += 1

    def someFunc(self, widget):
        self.lattice[str(self.verticalHeaderItem(widget.row()).text())][str(self.horizontalHeaderItem(widget.column()).text())] = widget.text()
        # widget.setText(str(self.lattice[str(self.verticalHeaderItem(widget.row()).text())][str(self.horizontalHeaderItem(widget.column()).text())]))

    def typeChanged(self, index):
        combobox = self.sender()
        widget = self.indexAt(combobox.pos())
        self.lattice[str(self.verticalHeaderItem(widget.row()).text())][str(self.horizontalHeaderItem(widget.column()).text())] = combobox.currentText()

def main():
   app = QApplication(sys.argv)
   # app.setStyle(QStyleFactory.create("plastique"))
   ex = elegantGUI()
   ex.show()
   # ex.pausePlots(ex.tab)
   # ex.testSleep()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()

#
# ''' Ok. Lets create a new lattice from scratch '''
# a = elegantLattice()
# ''' Here we create a command, but do not assign a name - it defaults to the type '''
# a.addCommand(type='global_settings',log_file="elegant.log",error_log_file="elegant.err")
# ''' here we assign a name - Why? We may want multiple 'run_setup' commands in the same command file... '''
# a.addCommand(name='runsetup',type='run_setup',lattice="doublering.lte",use_beamline="doublering",p_central_mev=700,centroid='%s.cen')
# ''' this will print out all commands in the 'testlattice' environment '''
# print 'testlattice commands = ', a.commands
#
# ''' add some elements '''
# a.addElement(name='Q1',type='kquad',l=0.5,k1=2.3)
# a.addElement(name='D1',type='drift',l=0.5)
# a.addElement(name='BEND1',type='ksbend',l=0.5,angle=0.36,E1=0.01,E2=0.022)
#
# ''' We can do some arithmetic on elements'''
# print '2*D1 = ', [getattr(x,'name') for x in (2*a.D1)]
# ''' and it "reverses" dipoles (correctly I think!)
#     NB. the brackets are so we get the properties of the reversed element, not the negative of properties of the normal element'''
# print 'Negative BEND1 = ', (-a.BEND1).properties
# ''' lets define some lines '''
# latt1 = a.addLine(name='latt1',line=[2*a.D1,a.Q1*2])
# ''' we can use elements in the environment (testlattice.<elementname>) or strings '''
#
# ''' this has a reversed element in it...'''
# latt3 = a.addLine(name='latt3',line=[2*a.latt1,-a.BEND1,a.latt1,a.D1])
# latt2 = a.addLine(name='latt2',line=[2*a.latt1,a.latt3,a.D1])
#
# ''' now we can print out what the elegant lattice line definition would look like - it should have a - in front of the bend! '''
# print 'line definition for latt3 = ', a.latt3.write()
