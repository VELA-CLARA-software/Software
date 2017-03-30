import sys
from elegantWriter_objects import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pyqtgraph as pg
import subprocess
import sdds

class elegantGUI(QMainWindow):
    def __init__(self, parent = None):
        super(elegantGUI, self).__init__(parent)
        ''' Here we create an elegant environment '''
        ele = elegantInterpret()
        ''' now we read in a lattice file (can also be MAD format, but not all commands are equivalent (cavities are a problem!)) '''
        lattice = ele.readElegantFile('diamond.lte')
        lattice.writeLatticeFile('test.lte','diamond')

        lattice.addCommand(type='global_settings',log_file="elegant.log",error_log_file="elegant.err")
        lattice.addCommand(type='run_setup',lattice="test.lte",use_beamline="diamond",p_central_mev=3000,centroid='%s.cen')
        lattice.addCommand(type='twiss_output',matched = 1,output_at_each_step=0,radiation_integrals=1,statistics=1,filename="%s.twi")
        # print lattice.global_settings.write()+lattice.run_setup.write()
        proc = subprocess.Popen(['elegant','-pipe=in'],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        shell=True
                        )
        proc.stdin.write(lattice.global_settings.write())
        proc.stdin.write(lattice.run_setup.write())
        proc.stdin.write(lattice.twiss_output.write())
        self.twi = sdds.SDDS(0)
        self.twi.load('stdin.twi')
        for col in range(len(self.twi.columnName)):
            if len(self.twi.columnData[col]) == 1:
                setattr(self.twi,self.twi.columnName[col],self.twi.columnData[col][0])
            else:
                setattr(self.twi,self.twi.columnName[col],self.twi.columnData[col])
        self.plotWidget = pg.PlotWidget()
        self.plot = self.plotWidget.plot()
        self.centralWidget = QWidget()
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.layout.addWidget(self.plotWidget)
        self.xAxisCombo = QComboBox()
        self.yAxisCombo = QComboBox()
        for param in self.twi.columnName:
            if isinstance(getattr(self.twi,param)[0], (float, long)):
                self.xAxisCombo.addItem(param)
                self.yAxisCombo.addItem(param)
        self.yAxisCombo.setCurrentIndex(1)
        self.updatePlot()
        self.comboWidget = QWidget()
        self.comboLayout = QHBoxLayout()
        self.xAxisCombo.currentIndexChanged.connect(self.updatePlot)
        self.yAxisCombo.currentIndexChanged.connect(self.updatePlot)
        self.comboWidget.setLayout(self.comboLayout)
        self.comboLayout.addWidget(self.xAxisCombo)
        self.comboLayout.addWidget(self.yAxisCombo)

        self.layout.addWidget(self.plotWidget)
        self.layout.addWidget(self.comboWidget)
        self.setCentralWidget(self.centralWidget)
        # self.plotData(self.twi.s,self.twi.betax)

    def updatePlot(self):
        self.plotData(getattr(self.twi,str(self.xAxisCombo.currentText())),getattr(self.twi,str(self.yAxisCombo.currentText())))

    def plotData(self, x, y,pen='r'):
        self.plot.clear()
        self.plot.setData(x,y,pen='r')
        # exit()
        # proc.kill()
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
