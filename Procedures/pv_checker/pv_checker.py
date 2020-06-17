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

pv_roots = ["CLA-C2V-DIA-CAM-01:", "CLA-S02-DIA-CAM-01:", "CLA-S01-DIA-CAM-01:", "CLA-S02-DIA-CAM-02:",
            "CLA-S02-DIA-CAM-03:", "CLA-VCA-DIA-CAM-01:", "EBT-INJ-DIA-CAM-01:", "EBT-INJ-DIA-CAM-02:",
            "EBT-INJ-DIA-CAM-03:", "EBT-INJ-DIA-CAM-04:", "EBT-INJ-DIA-CAM-05:", "EBT-INJ-DIA-CAM-06:",
            "EBT-INJ-DIA-CAM-07:", "EBT-INJ-DIA-CAM-08:", "EBT-INJ-DIA-CAM-09:", "EBT-INJ-DIA-CAM-10:",
            "EBT-INJ-DIA-CAM-11:", "EBT-INJ-DIA-CAM-12:", "EBT-INJ-DIA-CAM-13:", "EBT-INJ-DIA-CAM-18:",
            "EBT-INJ-DIA-CAM-14:", "EBT-INJ-DIA-CAM-16:", "EBT-INJ-DIA-CAM-17:", "EBT-INJ-DIA-CAM-19:",
            "EBT-INJ-DIA-CAM-20:"]

pv_suffxes = ["HDF:WriteFile_RBV", "HDF:WriteStatus", "HDF:WriteMessage", "HDF:NumCaptured_RBV", "HDF:Capture_RBV",
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

## Get the PVs to check
all_pvs = []
for pv_root in pv_roots:
    for pv_suffx in pv_suffxes:
        if is_vm:
            all_pvs.append(vm_prefix + pv_root + pv_suffx)
        else:
            all_pvs.append(vm_prefix + pv_root + pv_suffx)

all_pvs = all_pvs[:2000]
all_pv_len = len(all_pvs)
print("all_pv_len = ", all_pv_len)

# check the PVs
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

input()

