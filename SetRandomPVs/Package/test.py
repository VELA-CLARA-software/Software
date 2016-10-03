import randomPVs
import sys,os
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"


def main():
	srPV = randomPVs.setRandomPV()
	pv1 = 'VM-EBT-INJ-SCOPE-01:P1'
	pv2 = 'VM-EBT-INJ-SCOPE-01:P2'
	pv3 = 'VM-EBT-INJ-DIA-BPMC-02:X'
	srPV.setPV(pv1,1,10,10,1, "num")
	srPV.setPV(pv2,1,10,10,1, "num")
	srPV.setPV(pv3,1,10,10,1, "array")
	
if __name__ == "__main__":
	main()