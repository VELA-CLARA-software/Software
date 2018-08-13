import sys, os, time, math
from elegantWriter_objects import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pyqtgraph as pg
import subprocess
import sdds
import glob

class elegantGUI(QMainWindow):
    def __init__(self, parent = None):
        super(elegantGUI, self).__init__(parent)
        ''' Here we create an elegant environment '''
        ele = elegantInterpret()
        ''' now we read in a lattice file (can also be MAD format, but not all commands are equivalent (cavities are a problem!)) '''
        self.lattice = ele.readElegantFile('c2v.lte')
        self.lattice.writeLatticeFile('test.lte','cla-ebt')

        self.lattice.addCommand(type='global_settings',log_file="elegant.log",error_log_file="elegant.err")
        self.lattice.addCommand(type='run_setup',lattice="test.lte",use_beamline="CLA-EBT",p_central=70.31,centroid='%s.cen',always_change_p0 = 1)
        self.lattice.addCommand(type='run_control',n_steps=1, n_passes=1)
        self.lattice.addCommand(type='twiss_output',matched = 0,output_at_each_step=0,radiation_integrals=1,statistics=1,filename="%s.twi",beta_x  =  0.961326,
	alpha_x = -1.03701,
	beta_y  =  1.11184,
	alpha_y = -1.18067)
        self.lattice.addCommand(type='bunched_beam',n_particles_per_bunch=100,use_twiss_command_values=1,emit_nx=0.3e-6,emit_ny=0.3e-6)
        self.lattice.addCommand(type='track')
        # print lattice.global_settings.write()+lattice.run_setup.write()

        self.openElegantPipe()

        self.centralWidget = QWidget()
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.table = latticeTable(self.lattice)
        self.table.elementChanged.connect(self.runAndUpdate)
        self.table.updateTable('cla-ebt')
        self.layout.addWidget(self.table)

        self.tab = QTabWidget()
        self.sddsPlot = SDDSTwissPlotWidget()
        self.tab.addTab(self.sddsPlot,"Twiss Parameters")

        self.beamPlots = pg.GraphicsLayoutWidget()
        noplots = 0
        plotsperrow = int(math.sqrt(len(glob.glob('*SCR*.SDDS'))))
        for name in glob.glob('*SCR*.SDDS'):
            self.plot = SDDSBeamPlotWidget(name,xaxis='x',yaxis='y',pen='r').plot
            print self.plot
            self.beamPlots.addItem(self.plot)
            if noplots >= plotsperrow:
                self.beamPlots.nextRow()
            else:
                self.beamPlots.nextColumn()
        self.tab.addTab(self.beamPlots,"Beam Plots")

        self.layout.addWidget(self.tab)



        self.setCentralWidget(self.centralWidget)
        self.runAndUpdate()

    def runAndUpdate(self):
        self.lattice.writeLatticeFile('test.lte','cla-ebt')
        self.runElegant(self.lattice)
        self.sddsPlot.loadTwi()

    def openElegantPipe(self):
        self.proc = subprocess.Popen(['elegant','-pipe=in'],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        shell=False
                        )

    def runElegant(self, lattice):
        # try:
        #     modtimestart = os.stat('stdin.twi').st_mtime
        # except:
        #     modtimestart = 0
        # print modtimestart
        self.openElegantPipe()
        # self.proc.stdin.write(lattice.global_settings.write())
        # self.proc.stdin.write(lattice.run_setup.write())
        # self.proc.stdin.write(lattice.twiss_output.write())
        print lattice.writeCommandFile()
        stdout, stderr = self.proc.communicate(lattice.writeCommandFile())
        # self.proc.communicate(lattice.twiss_output.write())
        # time.sleep(1)
        # while os.stat('stdin.twi').st_mtime == modtimestart:
        #     print 'waiting'
        #     time.sleep(1)
        # self.lattice.writeCommandFile('test.ele')

class SDDSTwissPlotWidget(QWidget):

    def __init__(self, **kwargs):
        super(SDDSTwissPlotWidget, self).__init__(**kwargs)
        self.plotWidget = pg.PlotWidget()
        self.plot = self.plotWidget.plot()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.plotWidget)
        self.xAxisCombo = QComboBox()
        self.yAxisCombo = QComboBox()
        self.xAxisCombo.currentIndexChanged.connect(self.updatePlot)
        self.yAxisCombo.currentIndexChanged.connect(self.updatePlot)
        self.comboWidget = QWidget()
        self.comboLayout = QHBoxLayout()
        self.comboWidget.setLayout(self.comboLayout)
        self.comboLayout.addWidget(self.xAxisCombo)
        self.comboLayout.addWidget(self.yAxisCombo)
        self.layout.addWidget(self.comboWidget)
        self.layout.addWidget(self.plotWidget)

    def loadTwi(self):
        self.twi = sdds.SDDS(0)
        self.twi.load('stdin.twi')
        for col in range(len(self.twi.columnName)):
            if len(self.twi.columnData[col]) == 1:
                setattr(self.twi,self.twi.columnName[col],self.twi.columnData[col][0])
            else:
                setattr(self.twi,self.twi.columnName[col],self.twi.columnData[col])
        self.SDDSparameterNames = list()
        for param in self.twi.columnName:
            if isinstance(getattr(self.twi,param)[0], (float, long)):
                self.SDDSparameterNames.append(param)
        self.updateSelectionBar()
        self.updatePlot()

    def updateSelectionBar(self):
        xAxisCombotext = self.xAxisCombo.currentText()
        yAxisCombotext = self.yAxisCombo.currentText()
        self.xAxisCombo.currentIndexChanged.disconnect(self.updatePlot)
        self.yAxisCombo.currentIndexChanged.disconnect(self.updatePlot)
        allnames = []
        for name in self.SDDSparameterNames:
            allnames.append(name)
            if self.xAxisCombo.findText(name) == -1:
                self.xAxisCombo.addItem(name)
                self.yAxisCombo.addItem(name)
        for index in range(self.xAxisCombo.count()):
            if not self.xAxisCombo.itemText(index) in allnames:
                self.xAxisCombo.removeItem(index)
                self.yAxisCombo.removeItem(index)
            else:
                if self.xAxisCombo.itemText(index) == xAxisCombotext:
                    self.xAxisCombo.setCurrentIndex(index)
                if self.yAxisCombo.itemText(index) == yAxisCombotext:
                    self.yAxisCombo.setCurrentIndex(index)
        if xAxisCombotext == '':
            self.xAxisCombo.setCurrentIndex(0)
        if yAxisCombotext == '':
            self.yAxisCombo.setCurrentIndex(1)
        self.xAxisCombo.currentIndexChanged.connect(self.updatePlot)
        self.yAxisCombo.currentIndexChanged.connect(self.updatePlot)

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

class SDDSBeamPlotWidget(pg.PlotWidget):

    def __init__(self, filename, xaxis='x', yaxis='y', **kwargs):
        super(SDDSBeamPlotWidget, self).__init__(**kwargs)
        self.setLabels(left=yaxis, bottom=xaxis)
        self.sddsdata = sdds.SDDS(0)
        self.sddsdata.load(filename)
        for col in range(len(self.sddsdata.columnName)):
            if len(self.sddsdata.columnData[col]) == 1:
                setattr(self.sddsdata,self.sddsdata.columnName[col],self.sddsdata.columnData[col][0])
            else:
                setattr(self.sddsdata,self.sddsdata.columnName[col],self.sddsdata.columnData[col])
        self.SDDSparameterNames = list()
        for param in self.sddsdata.columnName:
            if isinstance(getattr(self.sddsdata,param)[0], (float, long)):
                self.SDDSparameterNames.append(param)
        self.plot = self.plot(x=getattr(self.sddsdata,xaxis), y=getattr(self.sddsdata,yaxis),pen=None,symbol='o')

class latticeTable(pg.TableWidget):

    elementChanged = pyqtSignal()

    def __init__(self, lattice, headings=None):
        super(latticeTable, self).__init__()
        if headings == None:
            self.headings = ['name','type','l','k1']
        else:
            self.headings = headings
        self.lattice = lattice
        # self.itemChanged.connect(self.propertyChanged)

    def updateTable(self,line):
        # self.itemChanged.disconnect(self.propertyChanged)
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
        # self.itemChanged.connect(self.propertyChanged)

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
                        if isinstance(val[h],(float)):
                            widget = QDoubleSpinBox()
                            widget.setContextMenuPolicy(Qt.CustomContextMenu)
                            widget.customContextMenuRequested.connect(self.spinBoxMenu)
                            widget.setDecimals(5)
                            widget.setSingleStep(0.001)
                            widget.setMinimum(-20)
                            widget.setMaximum(20)
                            widget.setValue(val[h])
                            widget.editingFinished.connect(self.spinboxChanged)
                            self.setCellWidget(row,col,widget)
                        elif isinstance(val[h],(long, int)):
                            widget = QSpinBox()
                            widget.setSingleStep(1)
                            widget.editingFinished.connect(self.spinboxChanged)
                            widget.setValue(val[h])
                            self.setCellWidget(row,col,widget)
                        elif val[h] == None:
                            item = QLabel('')
                            # item.setFlags(Qt.ItemIsEnabled)
                            self.setCellWidget(row,col,item)
                        else:
                            item = QLabel(str(val[h]))
                            self.setCellWidget(row,col,item)
                    col += 1
            row += 1

    def spinBoxMenu(self, position):
        spinbox = self.sender()
        menu = QMenu()
        w = QWidget()
        wl = QGridLayout()
        w.setLayout(wl)
        minlabel = QLabel('Step:')
        minbox = QSpinBox()
        minbox.setValue(spinbox.singleStep())
        minbox.setRange(-100,100)
        minbox.editingFinished.connect(spinbox.setMinimum)
        # maxlabel = QLabel('Max:')
        # maxbox = QSpinBox()
        # maxbox.setValue(spinbox.maximum())
        # maxbox.setRange(-100,100)
        # maxbox.editingFinished.connect(spinbox.setMaximum)
        wl.addWidget(minlabel,0,0)
        wl.addWidget(minbox,0,1)
        wl.addWidget(maxlabel,1,0)
        wl.addWidget(maxbox,1,1)
        a = QWidgetAction(self)
        a.setDefaultWidget(w)
        menu.addAction(a)
        # quitAction = menu.addAction("Quit")
        action = menu.exec_(spinbox.mapToGlobal(position))
        # if action == quitAction:
        #     qApp.quit()

    def propertyChanged(self, widget):
        self.lattice[str(self.verticalHeaderItem(widget.row()).text())][str(self.horizontalHeaderItem(widget.column()).text())] = widget.text()
        self.elementChanged.emit()

    def typeChanged(self):
        combobox = self.sender()
        widget = self.indexAt(combobox.pos())
        self.lattice[str(self.verticalHeaderItem(widget.row()).text())][str(self.horizontalHeaderItem(widget.column()).text())] = combobox.currentText()
        self.elementChanged.emit()

    def spinboxChanged(self):
        spinbox = self.sender()
        widget = self.indexAt(spinbox.pos())
        self.lattice[str(self.verticalHeaderItem(widget.row()).text())][str(self.horizontalHeaderItem(widget.column()).text())] = spinbox.value()
        self.elementChanged.emit()

def main():
   app = QApplication(sys.argv)
   pg.setConfigOptions(antialias=True)
   pg.setConfigOption('background', 'w')
   pg.setConfigOption('foreground', 'k')
   # app.setStyle(QStyleFactory.create("plastique"))
   ex = elegantGUI()
   ex.show()
   ex.lattice.screensToWatch()
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
