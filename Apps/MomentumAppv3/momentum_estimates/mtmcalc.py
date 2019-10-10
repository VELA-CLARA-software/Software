import math

class calc():

	def __init__(self):
		self.pulselength = None
		self.klypower = None
	def bestcase(self):
		return 0.407615 + 1.94185* ((1 - math.exp((-1.54427*10**6 * self.pulselength*10**-6))) *(0.0331869 + 6.05422*10**-7 *self.klypower*10**6))**0.5
		
	def worstcase(self):
		return 0.377 + 1.81689* ((1 - math.exp((-1.54427*10**6 * self.pulselength*10**-6))) *(0.0331869 + 6.05422*10**-7 *self.klypower*10**6))**0.5

		
#pulselength= input("Input the pulse length in microseconds ")*10**-6
#klypower= input("Input the klystron power in megaWatts ")*10**6
#bestcase = 0.407615 + 1.94185* ((1 - math.exp((-1.54427*10**6 * pulselength))) *(0.0331869 + 6.05422*10**-7 *klypower))**0.5
#worstcase = 0.377 + 1.81689* ((1 - math.exp((-1.54427*10**6 * pulselength))) *(0.0331869 + 6.05422*10**-7 *klypower))**0.5

#print("the pulse length is "+ str(pulselength*10**6)+ " micro s")
#print("the klystron power is " +str(klypower*10**-6) + " MW")
#print("the best case momentum is " +str(bestcase)+ "MeV/c")
#print("the worst case momentum is " +str(worstcase)+ "MeV/c")


