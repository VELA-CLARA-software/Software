import subprocess
import time


run_start = time.time()

# vm flags and prefix
is_vm = True
vm_prefix = "VM-"

multi_pv_string_max_len = 32718


def get_multi_pv_string(pvs):
    multi_pv_string = ''
    # if the all pvs string is less than multi_pv_string_max_len just return it,
    if sum([len(x) for x in pvs]) < multi_pv_string_max_len:
        for pv in pvs:
            multi_pv_string += pv + ' '
        return (multi_pv_string, [])
    # else gokeep adding pvs until we reach the limit, adn return the unused pvs
    unused_pvs = pvs
    for i, pv in enumerate(pvs):
        multi_pv_string += pv + ' '
        if len(multi_pv_string + pvs[i + 1]) > multi_pv_string_max_len:
            # print("max string length reached get_multi_pv_string break")
            break
        unused_pvs.pop(0)
    # print("get_multi_pv_string result, ", len(multi_pv_string), len(unused_pvs))
    return (multi_pv_string, unused_pvs)

def check_pv_connection(pvs_in):
    pv_list = pvs_in # TODO i need to make a copy??
    start_time = time.time()
    r = []
    print("checking ", len(pvs_in), "pvs" )
    while len(pv_list) > 0:
        (multi_pv_string, pv_list) = get_multi_pv_string(pv_list)
        result = subprocess.run("cainfo " + multi_pv_string , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_put = result.stdout.decode('utf-8').split("\n")
        pvs = [x.rstrip() for x in out_put[0::7]]
        con = ["never" in x for x in out_put[1::7]]
        r += [pair for pair in zip(pvs,con)]
        print(len(pv_list),"/", len(pvs_in), str(int(time.time() - start_time)))
    return r

cam_pv_roots = ["CLA-C2V-DIA-CAM-01:", "CLA-S02-DIA-CAM-01:", "CLA-S01-DIA-CAM-01:", "CLA-S02-DIA-CAM-02:",
            "CLA-S02-DIA-CAM-03:", "CLA-VCA-DIA-CAM-01:", "EBT-INJ-DIA-CAM-01:", "EBT-INJ-DIA-CAM-02:",
            "EBT-INJ-DIA-CAM-03:", "EBT-INJ-DIA-CAM-04:", "EBT-INJ-DIA-CAM-05:", "EBT-INJ-DIA-CAM-06:",
            "EBT-INJ-DIA-CAM-07:", "EBT-INJ-DIA-CAM-08:", "EBT-INJ-DIA-CAM-09:", "EBT-INJ-DIA-CAM-10:",
            "EBT-INJ-DIA-CAM-11:", "EBT-INJ-DIA-CAM-12:", "EBT-INJ-DIA-CAM-13:", "EBT-INJ-DIA-CAM-18:",
            "EBT-INJ-DIA-CAM-14:", "EBT-INJ-DIA-CAM-16:", "EBT-INJ-DIA-CAM-17:", "EBT-INJ-DIA-CAM-19:",
            "EBT-INJ-DIA-CAM-20:"]

cam_pv_suffixes = ["HDF:WriteFile_RBV", "HDF:WriteStatus", "HDF:WriteMessage", "HDF:NumCaptured_RBV", "HDF:Capture_RBV",
    "CAM:Acquire_RBV", "HDF:NumCapture_RBV", "MAGICK:NumCaptured_RBV", "MAGICK:WriteFile_RBV", "MAGICK:WriteStatus",
    "MAGICK:WriteMessage", "MAGICK:Capture_RBV", "MAGICK:NumCapture_RBV", "ANA:StepSize_RBV", "ANA:EnableCallbacks_RBV",
    "ANA:UseBkgrnd", "ANA:UseNPoint", "ANA:X_RBV", "ANA:Y_RBV", "ANA:SigmaX_RBV", "ANA:SigmaY_RBV", "ANA:CovXY_RBV",
    "ANA:AvgIntensity_RBV", "ANA:Intensity_RBV", "ANA:XPix_RBV", "ANA:YPix_RBV", "ANA:SigmaXPix_RBV",
    "ANA:SigmaYPix_RBV", "ANA:CovXYPix_RBV", "ANA:PixelResults_RBV", "ANA:MaskXCenter_RBV", "ANA:MaskYCenter_RBV",
    "ANA:MaskXRad_RBV", "ANA:MaskYRad_RBV", "ANA:CenterX_RBV", "ANA:CenterY_RBV", "ANA:PixMM_RBV",
    "CAM:AcquireTime_RBV", "CAM:AcquirePeriod_RBV", "CAM:ArrayRate_RBV", "CAM:Temperature_RBV", "HDF:FilePath",
    "HDF:FileName", "HDF:FileNumber", "HDF:WriteFile", "CAM:Acquire", "CAM:Acquire", "HDF:Capture", "HDF:NumCapture",
    "MAGICK:FileName", "MAGICK:FilePath", "MAGICK:FileNumber", "MAGICK:Capture", "MAGICK:WriteFile",
    "MAGICK:NumCapture", "ANA:StepSize", "ANA:EnableCallbacks", "ANA:NewBkgrnd", "ANA:UseBkgrnd", "ANA:UseNPoint",
    "CAM2:ArrayData", "ANA:MaskXCenter", "ANA:MaskYCenter", "ANA:MaskXRad", "ANA:MaskYRad", "ANA:CenterX",
    "ANA:CenterY", "ANA:PixMM"]

bpm_pv_roots = ["EBT-INJ-DIA-BPM-01", "EBT-INJ-DIA-BPM-02", "EBT-INJ-DIA-BPM-03", "EBT-INJ-DIA-BPM-04",
                "EBT-INJ-DIA-BPM-05", "EBT-INJ-DIA-BPM-06", "CLA-S01-DIA-BPM-01", "CLA-S02-DIA-BPM-01",
                "CLA-S02-DIA-BPM-02", "CLA-C2V-DIA-BPM-01", "EBT-BA1-DIA-BPM-01", "EBT-BA1-DIA-BPM-02",
                "EBT-BA1-DIA-BPM-03", "EBT-BA1-DIA-BPM-04"]
bpm_pv_suffixes = ["SA1", "SA2", "SD1", "SD2", "RA1", "RA2", "RD1", "RD2", "X", "Y", "DATA:B2V.VALA", "RDY", "AWAK"]

charge_pv_roots = ["CLA-S01-DIA-WCM-01", "CLA-S02-DIA-FCUP-01"]
charge_pv_suffixes = ["V", "Q"]

img_pv_roots = ["EBT-INJ-VAC-IMG-01", "EBT-INJ-VAC-IMG-02", "EBT-INJ-VAC-IMG-03", "EBT-INJ-VAC-IMG-04", "EBT-INJ-VAC-IMG-05",
                "EBT-INJ-VAC-IMG-06", "EBT-INJ-VAC-IMG-07", "EBT-INJ-VAC-IMG-08", "EBT-INJ-VAC-IMG-09", "EBT-INJ-VAC-IMG-10",
                "EBT-INJ-VAC-IMG-11"]
img_pv_suffixes = ["P", "Sta"] # should this be STA??

llrf_gun_pv_roots = ["CLA-GUN-LRF-CTRL-01",]
llrf_gun_pv_suffixes = ["vm:dsp:ff_amp:amplitude", "tcm:trig:source", "vm:dsp:sp_amp:amplitude", "vm:dsp:ff_ph:phase", "vm:dsp:sp_ph:phase",
                    "app:interlock:state", "app:rf_ctrl", "vm:dsp:ff_ph:lock", "vm:dsp:ff_amp:lock", "app:time_vector", "vm:feed_fwd:offset",
                    "vm:feed_fwd:duration", "ff_pulse_shape:amp", "ff_pulse_shape:apply_tables", "ad1:interlock:ch1:status", "ad1:interlock:ch1:enable",
                    "ad1:interlock:ch1:U_level", "ad1:interlock:ch1:P_level", "ad1:interlock:ch1:Pdbm_level","ad1:interlock:ch2:status", "ad1:interlock:ch2:enable",
                    "ad1:interlock:ch2:U_level", "ad1:interlock:ch2:P_level", "ad1:interlock:ch2:Pdbm_level","ad1:interlock:ch3:status", "ad1:interlock:ch3:enable",
                    "ad1:interlock:ch3:U_level", "ad1:interlock:ch3:P_level", "ad1:interlock:ch3:Pdbm_level","ad1:interlock:ch4:status", "ad1:interlock:ch4:enable",
                    "ad1:interlock:ch4:U_level", "ad1:interlock:ch4:P_level", "ad1:interlock:ch4:Pdbm_level","ad1:interlock:ch5:status", "ad1:interlock:ch5:enable",
                    "ad1:interlock:ch5:U_level", "ad1:interlock:ch5:P_level", "ad1:interlock:ch5:Pdbm_level","ad1:interlock:ch6:status", "ad1:interlock:ch6:enable",
                    "ad1:interlock:ch6:U_level", "ad1:interlock:ch6:P_level", "ad1:interlock:ch6:Pdbm_level","ad1:interlock:ch7:status", "ad1:interlock:ch7:enable",
                    "ad1:interlock:ch7:U_level", "ad1:interlock:ch7:P_level", "ad1:interlock:ch7:Pdbm_level","ad1:interlock:ch8:status", "ad1:interlock:ch8:enable",
                    "ad1:interlock:ch8:U_level", "ad1:interlock:ch8:P_level", "ad1:interlock:ch8:Pdbm_level", "ad1:dod_demod_vec", "ad1:dod_demod_vec.SCAN",
                    "ad1:dod_demod_vec.ACQM", "ad1:ch1:power_local.SCAN", "ad1:ch1:power_remote.SCAN", "ad1:ch1:amp_phase.SCAN", "ad1:ch1:amp_derivative.SCAN",
                    "ad1:ch1:phase_derivative.SCAN", "ad1:ch2:power_local.SCAN", "ad1:ch2:power_remote.SCAN", "ad1:ch2:amp_phase.SCAN", "ad1:ch2:amp_derivative.SCAN",
                    "ad1:ch2:phase_derivative.SCAN", "ad1:ch3:power_local.SCAN", "ad1:ch3:power_remote.SCAN", "ad1:ch3:amp_phase.SCAN", "ad1:ch3:amp_derivative.SCAN",
                    "ad1:ch3:phase_derivative.SCAN", "ad1:ch4:power_local.SCAN", "ad1:ch4:power_remote.SCAN", "ad1:ch4:amp_phase.SCAN", "ad1:ch4:amp_derivative.SCAN",
                    "ad1:ch4:phase_derivative.SCAN", "ad1:ch5:power_local.SCAN", "ad1:ch5:power_remote.SCAN", "ad1:ch5:amp_phase.SCAN", "ad1:ch5:amp_derivative.SCAN",
                    "ad1:ch5:phase_derivative.SCAN", "ad1:ch6:power_local.SCAN", "ad1:ch6:power_remote.SCAN", "ad1:ch6:amp_phase.SCAN", "ad1:ch6:amp_derivative.SCAN",
                    "ad1:ch6:phase_derivative.SCAN", "ad1:ch7:power_local.SCAN", "ad1:ch7:power_remote.SCAN", "ad1:ch7:amp_phase.SCAN", "ad1:ch7:amp_derivative.SCAN",
                    "ad1:ch7:phase_derivative.SCAN", "ad1:ch8:power_local.SCAN", "ad1:ch8:power_remote.SCAN", "ad1:ch8:amp_phase.SCAN", "ad1:ch8:amp_derivative.SCAN",
                    "ad1:ch8:phase_derivative.SCAN"]

llrf_protection_pv_roots = ["CLA-GUN-RF-PROTG-01", "CLA-GUN-RF-PROTE-01", "CLA-GUN-RF-PROTT-01",
                            "CLA-GUN-RF-PROTCL-01", "CLA-GUN-RF-PROTCH-01", "CLA-GUN-RF-PROTVL-01",
                            "CLA-GUN-RF-PROTVH-01", "CLA-L01-RF-PROTG-01", "CLA-L01-RF-PROTE-01", 
                            "CLA-L01-RF-PROTT-01", "CLA-L01-RF-PROTL01-01"]
llrf_protection_pv_suffixes = ["Rst", "On", "Off", "Sta", "Cmi"]


llrf_linac_pv_roots = ["CLA-L01-LRF-CTRL-01"]
llrf_linac_pv_suffixes = ["vm:dsp:ff_amp:amplitude", "vm:dsp:sp_amp:amplitude", "vm:dsp:ff_ph:phase", "vm:dsp:ff_ph:phase", "vm:dsp:sp_ph:phase",
                          "ad1:ch3:power_remote.POWER", "ad1:ch4:power_remote.POWER", "ad1:ch1:power_remote.POWER", "ad1:ch1:power_remote.POWER",
                          "app:time_vector", "vm:feed_fwd:duration", "vm:feed_fwd:offset", "app:rf_ctrl", "app:interlock:state", "vm:dsp:ff_ph:lock",
                          "vm:dsp:ff_amp:lock", "tcm:trig:source", "CLA-C18-TIM-EVR-01:FrontUnivOut1-Ena-SP", "vm:dsp:ff_pulse_shape:amp",
                          "vm:dsp:ff_pulse_shape:apply_tables"]

llrf_hb_pv_roots = ["CLA-GUN-RF-SCR-01", "CLA-L01-LRF-CTRL-01"]
llrf_hb_pv_suffixes = ["HB"]

gun_mod_pv_roots = ["CLA-GUNS-HRF-MOD-01"]
gun_mod_pv_suffixes = ["Sys:StateSet", "Sys:StateRead", "Sys:ErrorRead.SVAL", "Sys:INTLK1",
                      "Sys:INTLK2", "Sys:INTLK3", "Sys:INTLK4", "Sys:INTLK5", "Sys:RemainingTime",
                      "Rf:MagPs1:CurrRead", "Rf:MagPs2:CurrRead", "Rf:MagPs3:CurrRead", "Rf:MagPs4:CurrRead",
                      "Rf:MagPs1:VoltRead", "Rf:MagPs2:VoltRead", "Rf:MagPs3:VoltRead", "Rf:MagPs4:VoltRead",
                      "HvPs:HvPs1:CurrRead", "HvPs:HvPs2:CurrRead", "HvPs:HvPs3:CurrRead", "HvPs:HvPs1:VoltRead",
                      "HvPs:HvPs2:VoltRead", "HvPs:HvPs3:VoltRead", "Pt:Diag:CtRead", "Pt:Diag:CvdRead", "Pt:Diag:PlswthRead",
                      "Pt:Diag:PlswthFwhmRead", "Rf:Ionp:PresRead1"]

l01_mod_pv_roots = ["CLA-L01-HRF-MOD-01"]
l01_mod_pv_suffixes = ["SYSMDE", "HVPS:VS:W", "HVPS:ALM:LO:W", "HVPS:ALM:HI:W", "RESET", "SYSST", "HVPS:VS:R", "HVPS:ALM:LO:R",
                       "HVPS:ALM:HI:R", "HVPS:V", "HVPS:I", "HEAT:V", "HEAT:I", "RESET:V", "RESET:I", "ION:V", "ION:I", "SUP:T",
                       "SUP:P", "RET:T", "RET:P", "BDY:FR", "COL:FR", "SOL:FR", "TNK:FR", "CR:T", "BR:T", "SOL:1:V", "SOL:1:I",
                       "SOL:2:V", "SOL:2:I", "SOL:3:V", "SOL:3:I", "FAULT", "F1DSTR.VALA", "F2DSTR.VALA", "F3DSTR.VALA", "F4DSTR.VALA",
                       "F6DSTR.VALA", "F7DSTR.VALA", "F8DSTR.VALA", "F9DSTR.VALA", "F10DSTR.VALA", "F11DSTR.VALA", "F13DSTR.VALA",
                       "F14DSTR.VALA", "F15DSTR.VALA", "F16DSTR.VALA", "F17DSTR.VALA", "F18DSTR.VALA", "F19DSTR.VALA", "F20DSTR.VALA",
                       "F1STR.VALA", "F2STR.VALA", "F3STR.VALA", "F4STR.VALA", "F5STR.VALA", "F6STR.VALA", "F7STR.VALA", "F8STR.VALA",
                       "F9STR.VALA", "F10STR.VALA", "F11STR.VALA", "F12STR.VALA", "F13STR.VALA", "F14STR.VALA", "F15STR.VALA", "F16STR.VALA",
                       "F17STR.VALA", "F18STR.VALA", "F19STR.VALA", "F20STR.VALA"]

# VM Laser transport mirror has different pv root: EBT-INJ-DIA-DUMMY-01 
laser_mirror_pv_roots = ["CLA-LAS-OPT-PICO-4C-PM-4"]
laser_mirror_pv_suffixes = ["H:MREL", "V:MREL", "hstep", "vstep",
                            "DDOUBLE8", "DDOUBLE9", "V:POS", "H:POS"]
pilaser_hwp_pv_roots = ["EBT-LAS-OPT-HWP-2:ROT", ]
pilaser_hwp_pv_suffixes = ["MABS", "stabilisation", "intensity", "status",
                           "RPOS"]
pilaser_em_pv_roots = ["CLA-LAS-DIA-EM-01"]
pilaser_em_pv_roots = ["E"]

magnet_pv_roots = ["CLA-LRG1-MAG-BSOL-01", "CLA-GUN-MAG-SOL-02", "CLA-L01-MAG-SOL-01", "CLA-L01-MAG-SOL-02", "CLA-S02-MAG-QUAD-01", "CLA-S02-MAG-QUAD-02",
                   "CLA-S02-MAG-QUAD-03", "CLA-S02-MAG-QUAD-04", "CLA-S02-MAG-QUAD-05", "CLA-C2V-MAG-QUAD-01", "CLA-C2V-MAG-QUAD-02", "CLA-C2V-MAG-QUAD-03",
                   "CLA-S01-MAG-HCOR-01", "CLA-S01-MAG-VCOR-01", "CLA-S01-MAG-HCOR-02", "CLA-S01-MAG-VCOR-02", "CLA-S02-MAG-HCOR-01", "CLA-S02-MAG-VCOR-01",
                   "CLA-S02-MAG-HCOR-02", "CLA-S02-MAG-VCOR-02", "CLA-S02-MAG-HCOR-03", "CLA-S02-MAG-VCOR-03", "CLA-C2V-MAG-HCOR-01", "CLA-C2V-MAG-VCOR-01",
                   "CLA-C2V-MAG-DIP-01", "EBT-INJ-MAG-HCOR-05", "EBT-INJ-MAG-HCOR-06", "EBT-INJ-MAG-HCOR-07", "EBT-INJ-MAG-HCOR-08", "EBT-INJ-MAG-HCOR-09",
                   "EBT-INJ-MAG-HCOR-10", "EBT-INJ-MAG-HCOR-11", "EBT-INJ-MAG-VCOR-05", "EBT-INJ-MAG-VCOR-06", "EBT-INJ-MAG-VCOR-07", "EBT-INJ-MAG-VCOR-08",
                   "EBT-INJ-MAG-VCOR-09", "EBT-INJ-MAG-VCOR-10", "EBT-INJ-MAG-VCOR-11", "EBT-INJ-MAG-QUAD-05", "EBT-INJ-MAG-QUAD-06", "EBT-INJ-MAG-QUAD-07",
                   "EBT-INJ-MAG-QUAD-08", "EBT-INJ-MAG-QUAD-09", "EBT-INJ-MAG-QUAD-10", "EBT-INJ-MAG-QUAD-11", "EBT-INJ-MAG-QUAD-12", "EBT-INJ-MAG-QUAD-13",
                   "EBT-INJ-MAG-QUAD-14", "EBT-INJ-MAG-QUAD-15", "CLA-C2V-MAG-DIP-02", "EBT-INJ-MAG-DIP-02", "EBT-INJ-MAG-DIP-03"]
magnet_pv_suffixes = ["RPOWER", "SPOWER", "SETI", "GETSETI", "READI", "RILK"]


screen_pv_roots = ["CLA-S01-DIA-SCR-01", "CLA-S02-DIA-SCR-01", "CLA-S02-DIA-SCR-02", "CLA-S02-DIA-SCR-03",
                   "CLA-C2V-DIA-SCR-01", "EBT-INJ-DIA-YAG-04", "EBT-INJ-DIA-YAG-05", "EBT-INJ-DIA-YAG-06",
                   "EBT-INJ-DIA-YAG-07", "EBT-INJ-DIA-YAG-08", "EBT-INJ-DIA-YAG-09", "EBT-INJ-DIA-YAG-10",
                   "EBT-BA1-DIA-YAG-01", "EBT-BA1-DIA-YAG-02", "EBT-BA1-DIA-YAG-03", "EBT-INJ-DIA-YAG-01",
                   "EBT-INJ-DIA-YAG-02", "EBT-INJ-DIA-YAG-03"]
screen_pv_suffixes = ["H:SDEV", "H:TRIGGER", "H:EX", "H:TGTPOS", "H:JOG", "H:JDIFF",
                      "V:SDEV", "V:TRIGGER", "V:EX", "V:TGTPOS", "V:JOG", "V:JDIFF",
                      "SDEV", "TRIGGER", "Sta", "On", "Off", "H:MOVING", "H:READY",
                      "H:GET_DEV", "H:DEV_STATE", "H:MAX_POS", "H:DEV_CENT", "H:ACTPOS",
                      "H:EN", "V:MOVING","V:READY", "V:GET_DEV", "V:DEV_STATE", "V:MAX_POS",
                      "V:DEV_CENT", "V:ACTPOS", "V:EN", "MOVING","READY", "GET_DEV", "DEV_STATE",
                      "MAX_POS", "DEV_CENT", "ACTPOS", "EN" ]

shutter_pv_roots = ["EBT-INJ-LSR-SHUT-01", "EBT-INJ-LSR-SHUT-02"]
shutter_pv_suffixes = ["On", "Off", "Sta"]

valve_pv_roots = ["CLA-S01-VAC-VALV-01", "CLA-S02-VAC-VALV-01", "CLA-C2V-VAC-VALV-01", "CLA-LAS-VAC-VALV-01", "CLA-LAS-VAC-VALV-02", "EBT-INJ-VAC-VALV-01",
                  "EBT-INJ-VAC-VALV-05", "EBT-INJ-VAC-VALV-06", "EBT-INJ-VAC-VALV-03", "EBT-INJ-VAC-VALV-07", "EBT-BA1-VAC-VALV-01", "EBT-BA1-VAC-VALV-02",
                  "EBT-BA1-VAC-VALV-03", "EBT-BA1-VAC-VALV-04", "EBT-BA1-VAC-VALV-05"]
valve_pv_suffixes = ["On", "Off", "Sta"]

## Get the PVs to check

def check_pvs(pv_roots, pv_suffixes):
    all_pvs = []
    for pv_root in pv_roots:
        for pv_suffix in pv_suffixes:
            if is_vm:
                all_pvs.append(vm_prefix + pv_root + pv_suffix)
            else:
                all_pvs.append(vm_prefix + pv_root + pv_suffix)
    all_pv_len = len(all_pvs)
    answer = check_pv_connection(all_pvs)
    print(len(answer),all_pv_len)
    print("Completed connection checking printing failed connections PVs ")
    fail_count = 0
    for item in answer:
        if item[1]:
            pass
        else:
            print(item[0])
            fail_count +=1
    print(fail_count, "/", all_pv_len, " failed to connect (see above list for PV strigns)")
    print("Fin, total time taken =  " + str(int(time.time() - run_start)) + ' seconds')
    
    
check_pvs(magnet_pv_roots, magnet_pv_suffixes)
input()

