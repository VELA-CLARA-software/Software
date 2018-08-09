import numpy as np

a = np.array([1,2,3,4,5])
b = np.array([5,4,3,2,1])

print('-b', -b)


print(' np.dot(a,b) = ', np.dot(a,b))

print('a*b = ',a*b)

print('a*b / b = ',a*b /b)

print('a**b = ',a**b)

print('a+b = ',a+b)

print('np.multiply(a,b) = ', np.multiply(a,b))

print('np.multiply(a,b) * 2 = ', np.multiply(a,b) * 2)

print('np.divide(a,b) ', np.divide(a,b))

print('a / 2', a / 2, np.divide(a,2))

print('2 / a', 2. / a,np.divide(2.,a))

print('np.multiply(np.multiply(a,b),a) = ', np.multiply(a,np.multiply(a,b)))


raw_input()







