import numpy as np
import scipy.constants as physics
import pyqtgraph as pg
import VELA_CLARA_Magnet_Control as mag
magInit = mag.init()
Cmagnets = magInit.physical_CB1_Magnet_Controller()

#def calcMom(self, dctrl,dipole, I):
dipole = 'S02-DIP01'
D = Cmagnets.getMagObjConstRef(dipole)
#I=8.5*8
#return (400.0033/D.magneticLength)*(np.polyval(D.fieldIntegralCoefficients, abs(I))*physics.c*180)/(45*physics.pi*1000000000)
for x in np.arange(0,len(D.fieldIntegralCoefficients)):
    print 'coeff ', x, ' = ', D.fieldIntegralCoefficients[x]
# print D.fieldIntegralCoefficients[1]
# print D.fieldIntegralCoefficients[2]
# print D.fieldIntegralCoefficients[3]
# print D.fieldIntegralCoefficients[4]
# print D.fieldIntegralCoefficients[5]

#mom1 = (np.polyval(D.fieldIntegralCoefficients, abs(I))*physics.c*180)/(45*physics.pi*1000000000)
#print mom1
#print (np.polyval(D.fieldIntegralCoefficients, abs(I))*physics.c/0.7853981634)/1e9

I = 7
mom_centre = float(np.polyval(D.fieldIntegralCoefficients, abs(I))*physics.c*180)/((45)*physics.pi*1000000000)
angle_misaligned = []
mom = []

for theta in np.arange(-20,20.2,0.2):
    print theta
    mom.append(float(np.polyval(D.fieldIntegralCoefficients, abs(I))*physics.c*180)/((45+theta)*physics.pi*1000000000))
    angle_misaligned.append(45 + theta)

print mom
print angle_misaligned
mom_rel = [100*((y-mom_centre)/mom_centre) for y in mom]
print mom_rel


plotWidget = pg.plot(title = "Test", labels = {'left': '&Delta;p/p [%]', 'bottom': '&Theta;'})#-45&deg;'})
#plotWidget.addLegend()
#l = pg.LegendItem((100,60), offset=(70,30)) # args are size, offset
#l.setParentItem(plotWidget.graphicsItem())

#plotWidget.plot(awd_z,awd, pen = (2,3))
p1 = plotWidget.plot(angle_misaligned, mom_rel, pen = 'r')
plotWidget.showGrid(x = True, y = True)
#p2 = plotWidget.plot(awd_z, awd, pen = pg.mkPen('b', style=QtCore.Qt.DotLine))
#p3 = plotWidget.plot(qf_z,qf, pen = pg.mkPen('r', style=QtCore.Qt.DashLine))

#l.addItem(p1, 'line')
pg.QtGui.QApplication.processEvents()
raw_input('press enter')

offset = [100*(1.531*np.tan((2*physics.pi)*(z-45)/360)) for z in angle_misaligned]
print offset

plotWidget = pg.plot(title = "Test", labels = {'left': '(&Delta;p-p)/p [%]', 'bottom': 'Offset [cm]'})
p1 = plotWidget.plot(offset, mom_rel, pen = 'g')
plotWidget.showGrid(x = True, y = True)
pg.QtGui.QApplication.processEvents()
raw_input('press enter')

#I2=(8.5*8)*1.08
#mom2 = (np.polyval(D.fieldIntegralCoefficients, abs(I2))*physics.c*180)/(45*physics.pi*1000000000)
#print mom2
#print mom2/mom1

#mom3 = (np.polyval(D.fieldIntegralCoefficients, abs(I))*physics.c*180)/(44*physics.pi*1000000000)
#print mom3
#print mom3/mom1
#print (np.polyval(D.fieldIntegralCoefficients, abs(I2))*physics.c/0.7853981634)/1e9
#print ((np.polyval(D.fieldIntegralCoefficients, abs(I2))*physics.c/0.7853981634)/1e9)/((np.polyval(D.fieldIntegralCoefficients, abs(I))*physics.c/0.7853981634)/1e9)

# for x in np.arange(0,3):
#     D.fieldIntegralCoefficients[x] = 0
#
# for x in np.arange(0,len(D.fieldIntegralCoefficients)):
#     print 'coeff ', x, ' = ', D.fieldIntegralCoefficients[x]
#
# print (np.polyval(D.fieldIntegralCoefficients, abs(I))*physics.c*180)/(45*physics.pi*1000000000)
