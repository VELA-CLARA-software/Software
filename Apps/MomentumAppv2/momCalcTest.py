import numpy as np
import scipy.constants as physics
import VELA_CLARA_Magnet_Control as mag
magInit = mag.init()
Cmagnets = magInit.physical_CB1_Magnet_Controller()

#def calcMom(self, dctrl,dipole, I):
dipole = 'S02-DIP01'
D = Cmagnets.getMagObjConstRef(dipole)
I=8.5*8
#return (400.0033/D.magneticLength)*(np.polyval(D.fieldIntegralCoefficients, abs(I))*physics.c*180)/(45*physics.pi*1000000000)
for x in np.arange(0,len(D.fieldIntegralCoefficients)):
    print 'coeff ', x, ' = ', D.fieldIntegralCoefficients[x]
# print D.fieldIntegralCoefficients[1]
# print D.fieldIntegralCoefficients[2]
# print D.fieldIntegralCoefficients[3]
# print D.fieldIntegralCoefficients[4]
# print D.fieldIntegralCoefficients[5]

mom1 = (np.polyval(D.fieldIntegralCoefficients, abs(I))*physics.c*180)/(45*physics.pi*1000000000)
print mom1
#print (np.polyval(D.fieldIntegralCoefficients, abs(I))*physics.c/0.7853981634)/1e9


I2=(8.5*8)*1.08
mom2 = (np.polyval(D.fieldIntegralCoefficients, abs(I2))*physics.c*180)/(45*physics.pi*1000000000)
print mom2
print mom2/mom1

mom3 = (np.polyval(D.fieldIntegralCoefficients, abs(I))*physics.c*180)/(44*physics.pi*1000000000)
print mom3
print mom3/mom1
#print (np.polyval(D.fieldIntegralCoefficients, abs(I2))*physics.c/0.7853981634)/1e9
#print ((np.polyval(D.fieldIntegralCoefficients, abs(I2))*physics.c/0.7853981634)/1e9)/((np.polyval(D.fieldIntegralCoefficients, abs(I))*physics.c/0.7853981634)/1e9)

# for x in np.arange(0,3):
#     D.fieldIntegralCoefficients[x] = 0
#
# for x in np.arange(0,len(D.fieldIntegralCoefficients)):
#     print 'coeff ', x, ' = ', D.fieldIntegralCoefficients[x]
#
# print (np.polyval(D.fieldIntegralCoefficients, abs(I))*physics.c*180)/(45*physics.pi*1000000000)
