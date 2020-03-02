import json
import requests
import numpy
import datetime
import epics
import time
import os
import shutil
import matplotlib.pyplot as plt
import VELA_CLARA_LLRF_Control as lrf
import VELA_CLARA_PILaser_Control as pil

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# MAKE SURE THAT THE LASER ENERGY IS READING BACK. YOU MAY NEED TO SET THE RANGE ON THE PHOEBUS SCREEN. 2uJ SHOULD DO IT
# ENSURE THAT THE BEAM IS IN RF CENTRE AND SOLENOID SETTINGS ARE NOMINAL

#Define the PV

wcm_pv_name = "CLA-S01-DIA-WCM-01:Q"
ophir_pv_name = "CLA-LAS-DIA-EM-06:E_RB"
hwp_pv_name = "EBT-LAS-OPT-HWP-2:ROT:MABS"
vc_x_pv_name = "CLA-VCA-DIA-CAM-01:ANA:X_RBV"
vc_y_pv_name = "CLA-VCA-DIA-CAM-01:ANA:Y_RBV"
vc_sig_x_pv_name = "CLA-VCA-DIA-CAM-01:ANA:SigmaX_RBV"
vc_sig_y_pv_name = "CLA-VCA-DIA-CAM-01:ANA:SigmaY_RBV"
gun_bsol_readi_pv_name = "CLA-LRG1-MAG-SOL-01:READI"
gun_sol_readi_pv_name = "CLA-GUN-MAG-SOL-02:READI"
laser_energy_overrange_pv = "CLA-LAS-DIA-EM-06:OverRange_RB"
laser_energy_start_stop_pv = "CLA-LAS-DIA-EM-06:Run_SP"
laser_energy_range_pv = "CLA-LAS-DIA-EM-06:Range_SP"

# Set up controllers
rf_init = lrf.init()
llrf_control = rf_init.physical_CLARA_LRRG_LLRF_Controller()
gun_obj = llrf_control.getLLRFObjConstRef()
gun_obj.kly_fwd_power_max


#Set HWP range
hwp_pv_range = numpy.linspace(-9,-1,16)
wcmvalues = {}
ophirvalues = {}
vcxvalues = {}
vcyvalues = {}
vcsigxvalues = {}
vcsigyvalues = {}
gunsolvalues = {}
gunbsolvalues = {}
epics.caput(laser_energy_start_stop_pv,0)
epics.caput(laser_energy_range_pv,3)
epics.caput(laser_energy_start_stop_pv,1)
for a in hwp_pv_range:
# SET HWP VALUES
	epics.caput(hwp_pv_name,a)
	if a-1 < epics.caget(hwp_pv_name) < a+1:
		time.sleep(10)
	if epics.caget(laser_energy_overrange_pv):
		epics.caput(laser_energy_start_stop_pv,0)
		epics.caput(laser_energy_range_pv,2)
		epics.caput(laser_energy_start_stop_pv,1)
	print("setting HWP = " + a)
	time_from = datetime.datetime.now().isoformat()+"Z"
	time.sleep(10)
	time_to = datetime.datetime.now().isoformat()+"Z"
# READ FROM ARCHIVER OVER 1s 
	wcm_url="http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv="+wcm_pv_name+"&from="+time_from+"&to="+time_to
	ophir_url="http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv="+ophir_pv_name+"&from="+time_from+"&to="+time_to
	vc_x_url="http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv="+vc_x_pv_name+"&from="+time_from+"&to="+time_to
	vc_y_url="http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv="+vc_y_pv_name+"&from="+time_from+"&to="+time_to
	vc_sig_x_url="http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv="+vc_sig_x_pv_name+"&from="+time_from+"&to="+time_to
	vc_sig_y_url="http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv="+vc_sig_y_pv_name+"&from="+time_from+"&to="+time_to
	gun_bsol_readi_url="http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv="+gun_bsol_readi_pv_name+"&from="+time_from+"&to="+time_to
	gun_sol_readi_url="http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv="+gun_sol_readi_pv_name+"&from="+time_from+"&to="+time_to
	wcmr = requests.get(wcm_url)
	wcmdata=wcmr.json()
	wcmevent = []
	for i in range(len(wcmdata[0]["data"])):
		wcmevent.append(wcmdata[0]["data"][i]["val"])
	ophirr = requests.get(ophir_url)
	ophirdata=ophirr.json()
	ophirevent = []
	for i in range(0,len(ophirdata[0]["data"])):
		ophirevent.append(ophirdata[0]["data"][i]["val"])
	vcxr = requests.get(vc_x_url)
	vcxdata=vcxr.json()
	vcxevent = []
	for i in range(0,len(vcxdata[0]["data"])):
		vcxevent.append(vcxdata[0]["data"][i]["val"])
	vcyr = requests.get(vc_y_url)
	vcydata=vcyr.json()
	vcyevent = []
	for i in range(0,len(vcydata[0]["data"])):
		vcyevent.append(vcydata[0]["data"][i]["val"])
	vcsigxr = requests.get(vc_sig_x_url)
	vcsigxdata=vcsigxr.json()
	vcsigxevent = []
	for i in range(0,len(vcsigxdata[0]["data"])):
		vcsigxevent.append(vcsigxdata[0]["data"][i]["val"])
	vcsigyr = requests.get(vc_sig_y_url)
	vcsigydata=vcsigyr.json()
	vcsigyevent = []
	for i in range(0,len(vcsigydata[0]["data"])):
		vcsigyevent.append(vcsigydata[0]["data"][i]["val"])
	gunbsolr = requests.get(gun_bsol_readi_url)
	gunbsoldata=gunbsolr.json()
	gunbsolevent = []
	for i in range(0,len(gunbsoldata[0]["data"])):
		gunbsolevent.append(gunbsoldata[0]["data"][i]["val"])
	gunsolr = requests.get(gun_sol_readi_url)
	gunsoldata=gunsolr.json()
	gunsolevent = []
	for i in range(0,len(gunsoldata[0]["data"])):
		gunsolevent.append(gunsoldata[0]["data"][i]["val"])
	wcmvalues[a] = wcmevent
	ophirvalues[a] = ophirevent
	vcxvalues[a] = vcxevent
	vcyvalues[a] = vcyevent
	vcsigxvalues[a] = vcsigxevent
	vcsigyvalues[a] = vcsigyevent
	gunsolvalues[a] = gunsolevent
	gunbsolvalues[a] = gunbsolevent
	print("wcm mean (pC) = " + numpy.mean(wcmevent))
	print("ophir mean (uJ) = " + numpy.mean(ophirevent))


json_data = {"hwp" : hwp_pv_range.tolist(),
			 "wcmdata" : wcmvalues,
			 "ophirdata" : ophirvalues,
			 "vcxdata" : vcxvalues,
			 "vcydata" : vcyvalues,
			 "vcsigxdata" : vcsigxvalues,
			 "vcsigydata" : vcsigyvalues,
			 "gunsoldata" : gunsolvalues,
			 "gunbsoldata" : gunbsolvalues}
#WRITE TO FILE
with open("wcm_vs_ophir"+datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".json", 'w') as outfile:
	outfile.write(json.dumps(json_data,indent=4, sort_keys=True))
	file = outfile
if os.path.split(os.getcwd())[1] != "Charge_Measurements":
	shutil.copyfile(file.name, "\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\Measurements\\Charge_Measurements\\"+file.name)
	
wcmmean = []
ophirmean = []
wcmstddev = []
ophirstddev = []
wcmmeanall = []
ophirmeanall = []
wcmstddevall = []
ophirstddevall = []
for j, k in zip(json_data["ophirdata"],json_data["wcmdata"]):
    ophirmean.append(numpy.mean(json_data["ophirdata"][j]))
    wcmmean.append(numpy.mean(json_data["wcmdata"][k]))
    ophirstddev.append(numpy.std(json_data["ophirdata"][j]))
    wcmstddev.append(numpy.std(json_data["wcmdata"][k]))
wcmmeanall.append(wcmmean)
ophirmeanall.append(ophirmean)
wcmstddevall.append(wcmstddev)
ophirstddevall.append(ophirstddev)
plt.errorbar(ophirmeanall[0],wcmmeanall[0],yerr=wcmstddevall[0],xerr=ophirstddevall[0])
plt.ylabel("WCM (pC)")
plt.xlabel("Ophir (uJ)")
plt.savefig("charge_"+datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".png")
plt.show()
year = str(datetime.datetime.now().year)
month = datetime.datetime.now().strftime('%m')
day = datetime.datetime.now().strftime('%d')
scandir =  "\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\"+self.year+"\\"+self.month+"\\"+self.day
if not os.path.isdir(self.scandir):
	os.makedirs(scandir)
plt.savefig(scandir+"\\charge_"+datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".png")
