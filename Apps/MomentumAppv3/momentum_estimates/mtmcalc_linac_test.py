import math

class calc():

	def __init__(self):
		#self.pulselength = None
		self.c = 299792458
		self.freq = 2998.5 										#C3: Frequency [MHz]
		self.n_cells = 61. 										#C6: Number of cells
		self.length_cell = 1./3*self.c/(self.freq*1e6) 			#C7: Length of cell [m]
		self.length_acc = self.n_cells*self.length_cell			#C8: Acceleration length [m]
		#print(self.length_acc)
		self.R_sh_MOhmperm = 5.4e7 								#C9: [MOhm/m]
		self.R_sh_MOhm = self.length_acc*self.R_sh_MOhmperm		#C11: [MOhm]
		#print(self.R_sh_MOhm)
		self.E_acc = 25. 										#C23: Accelerating gradient [MV/m]
		self.V_acc = self.length_acc*self.E_acc 				#C24: [MeV]
		self.attenuation = 0.42 								#C25: Attenuation factor
		self.P_diss = (self.V_acc*1e6)**2/self.R_sh_MOhm/1e6 	#C27: [MW]
		self.P_RF = self.P_diss/(1-math.exp(-2*self.attenuation)) 	#C29: [MW]
		#print(self.P_RF)
		self.waveguide_loss = 17 								#C31: [%]
		self.klypower = self.P_RF*(1.+self.waveguide_loss/100.) #C32: Klystron peak power [MW]

		self.test = math.sqrt(((self.klypower / (1.+self.waveguide_loss/100.)) * (1.-math.exp(-2.*self.attenuation))) * 1e6*self.R_sh_MOhm)/1e6
		#self.test = math.sqrt((1e6*self.n_cells*self.length_cell*self.R_sh_MOhm)*((self.klypower/(1. + self.waveguide_loss/100.)) * (1. - math.exp(-2.*self.attenuation))))/1e6
		print(self.test)
		#print(self.klypower)

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
