import epics        

class l01_modultor_monitor:

    fault_status = 0
    fault_PV = "CLA-L01-HRF-MOD-01:FAULT"
    reset_PV = "CLA-L01-HRF-MOD-01:RESET"
    faults_str_PV = []
    faults_dstr_PV = []
    

    def ___init___:
    
        for i in range (1,21):
            self.faults_str_PV.append("CLA-L01-HRF-MOD-01:F" + str(i) + "STR.VALA")
            self.faults_dstr_PV.append("CLA-L01-HRF-MOD-01:F" + str(i) + "DSTR.VALA")