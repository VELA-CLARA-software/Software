from CATAP.HardwareFactory import TYPE, STATE
import scipy.interpolate

alias_names =  {"CLA-L01-LRF-CTRL-01": "CLA-L01-CAV",
               "L01": "CLA-L01-CAV",
               "LRRG_GUN": "CLA-LRG1-GUN-CAV",
               "CLA-GUN-LRF-CTRL-01": "CLA-LRG1-GUN-CAV",
               #"CLA-GUN-MAG-SOL-02": "CLA-LRG1-MAG-SOL-01",
               #"CLA-LRG1-MAG-SOL-01": "CLA-GUN-MAG-SOL-02",
               "CLA-L01-CAV": "L01",
               "CLA-LRG1-GUN-CAV": "Gun",
               "Gun": "CLA-LRG1-GUN-CAV",
               "Linac": "CLA-L01-CAV"}
               #"CLA-LRG1-MAG-BSOL-01": "CLA-LRG1-MAG-SOL-01"}

lattice_to_online_model = {'GUN': 'Gun',
                           'LRG1': 'Gun',
                           'CLA-S01': 'Gun',
                           'L01': 'Linac',
                           'CLA-S02': 'CLA-S02',
                           'CLA-C2V': 'CLA-C2V',
                           'EBT-INJ': 'EBT-INJ',
                           'EBT-BA1': 'EBT-BA1',
                           'VCA': 'Gun'}

screen_alias = {"S01-SCR-01": "CLA-S01-DIA-SCR-01",
                "S02-SCR-01": "CLA-S02-DIA-SCR-01",
                "S02-SCR-02": "CLA-S02-DIA-SCR-02",
                "S02-SCR-03": "CLA-S02-DIA-SCR-03",
                "C2V-SCR-01": "CLA-C2V-DIA-SCR-01",
                "INJ-SCR-04": "EBT-INJ-DIA-YAG-04",
                "INJ-SCR-05": "EBT-INJ-DIA-YAG-05",
                "INJ-SCR-06": "EBT-INJ-DIA-YAG-06",
                "INJ-SCR-07": "EBT-INJ-DIA-YAG-07",
                "INJ-SCR-08": "EBT-INJ-DIA-YAG-08",
                "INJ-SCR-09": "EBT-INJ-DIA-YAG-09"}

screen_to_camera = {"CLA-S01-DIA-SCR-01": "CLA-S01-DIA-CAM-01",
                    "CLA-S02-DIA-SCR-01": "CLA-S02-DIA-CAM-01",
                    "CLA-S02-DIA-SCR-02": "CLA-S02-DIA-CAM-02",
                    "CLA-S02-DIA-SCR-03": "CLA-S02-DIA-CAM-03",
                    "CLA-C2V-DIA-SCR-01": "CLA-C2V-DIA-CAM-01",
                    "EBT-INJ-DIA-YAG-04": "EBT-INJ-DIA-CAM-05",
                    "EBT-INJ-DIA-YAG-05": "EBT-INJ-DIA-CAM-06",
                    "EBT-INJ-DIA-YAG-06": "EBT-INJ-DIA-CAM-07",
                    "EBT-INJ-DIA-YAG-07": "EBT-INJ-DIA-CAM-08",
                    "EBT-INJ-DIA-YAG-08": "EBT-INJ-DIA-CAM-09"}

bsol_alias = {"CLA-LRG1-MAG-BSOL-01": "CLA-LRG1-MAG-SOL-01"}

type_alias = {TYPE.QUADRUPOLE: "quadrupole",
              TYPE.SOLENOID: "solenoid",
              TYPE.BUCKING_SOLENOID: "solenoid",
              TYPE.LRRG_GUN: "cavity",
              TYPE.L01: "cavity",
              TYPE.HORIZONTAL_CORRECTOR: "kicker",
              TYPE.VERTICAL_CORRECTOR: "kicker",
              TYPE.DIPOLE: "dipole",
              TYPE.BPM_TYPE: "bpm",
              TYPE.VELA_PNEUMATIC: "screen",
              TYPE.VELA_HV_MOVER: "screen",
              TYPE.CLARA_HV_MOVER: "screen",
              TYPE.CLARA_V_MOVER: "screen",
              TYPE.CLARA_PNEUMATIC: "screen",
              #TYPE.CAMERA_TYPE: "camera",
              TYPE.VALVE: "valve",
              TYPE.CHARGE: "charge",
              "DIP": 'dipole',
              "QUAD": 'quadrupole',
              "SOL": 'solenoid',
              "HCOR": 'kicker',
              "VCOR": 'kicker'}

state_alias = {STATE.GOOD: "GOOD",
              STATE.BAD: "BAD",
              STATE.NONLINEAR: "NONLINEAR"}

vc_rf_centre = {'x_pix': 984,
                'y_pix': 1113,
                'x_mm': 5.898,
                'y_mm': 6.678}

vc_mechanical_centre = {'x_pix': 1080,
                'y_pix': 1000,
                'x_mm': 6.48,
                'y_mm': 6.0}

gun_kly_fwd_power_max = 9.9 * 10 ** 6

camera_epics_tools = {'x_pix': 'XPix_RBV',
                      'x_mm': 'X_RBV',
                      'y_pix': 'YPix_RBV',
                      'y_mm': 'Y_RBV',
                      'x_pix_sig': 'SigmaXPix_RBV',
                      'x_mm_sig': 'SigmaX_RBV',
                      'y_pix_sig': 'SigmaYPix_RBV',
                      'y_mm_sig': 'SigmaY_RBV',
                      # 'avg_intensity': 'AvgIntensity_RBV',
                      'sum_intensity': 'Intensity_RBV'}

llrf_epics_tools = {'klystron_amplitude_MW': 'ad1:ch1:Power:Wnd:Avg',
                    'cavity_amplitude_MW': 'ad1:ch3:Power:Wnd:Avg',
                    'phase_sp': 'vm:dsp:sp_ph:phase',
                    'phase_ff': 'vm:dsp:ff_ph:phase',
                    'amplitude_setpoint': 'vm:dsp:sp_amp:amplitude'}

# gun momentum measurements taken from \\fed.cclrc.ac.uk\Org\NLab\ASTeC\Projects\VELA\Work\2021\07\27\Gun_power_momentum_scan_cathode22.xls
power = [4.62*(10**6),5*(10**6),5.36*(10**6),5.81*(10**6),6.28*(10**6),6.74*(10**6),7.16*(10**6),7.62*(10**6),8.04*(10**6)]
momentum = [3.64,3.78,3.89,4.05,4.19,4.29,4.39,4.49,4.59]
gun_klystron_fwd_power_vs_momentum = [power, momentum]
gun_power_to_momentum = scipy.interpolate.interp1d(power,momentum,fill_value='extrapolate')
gun_momentum_to_power = scipy.interpolate.interp1d(momentum,power,fill_value='extrapolate')

# l01 momentum measurements taken from \\fed.cclrc.ac.uk\Org\NLab\ASTeC\Projects\VELA\Work\2021\07\28\Linac_power_momentum_scan_cathode22.xls
# NOTE: THESE MEASUREMENTS WERE TAKEN USING THE RF METRICS APP (AVG. KLYSTRON POWER BETWEEN THE CURSORS)
# CLA-GUN-LRF-CTRL-01:ad1:ch1:Power:Wnd:Hi IS THE PEAK IN THE RF TRACE
# CLA-GUN-LRF-CTRL-01:ad1:ch1:Power:Wnd:Avg IS THE AVERAGE BETWEEN THE CURSOR POSITIONS
# THE CURSOR POSITIONS WERE 74 AND 117
power = [7.49*(10**6),8.01*(10**6),8.66*(10**6),9.11*(10**6),9.61*(10**6),1.01*(10**7),1.04*(10**7),1.08*(10**7),1.11*(10**7),1.15*(10**7),1.18*(10**7),1.21*(10**7),1.23*(10**7),1.26*(10**7),1.27*(10**7),1.29*(10**7),1.31*(10**7),1.33*(10**7),1.34*(10**7),1.36*(10**7),1.38*(10**7)]
mom = [28.73,29.79,30.96,31.70,32.50,33.13,33.56,34.14,34.72,35.19,35.67,36.09,36.35,36.56,36.76,36.93,37.25,37.46,37.51,37.56,37.61]
momentum = [i - 4.45 for i in mom] #4.45 was gun momentum gain
l01_klystron_fwd_power_vs_momentum = [power, momentum]
l01_power_to_momentum = scipy.interpolate.interp1d(power,momentum,fill_value='extrapolate')
l01_momentum_to_power = scipy.interpolate.interp1d(momentum,power,fill_value='extrapolate')
