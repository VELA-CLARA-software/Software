from CATAP.HardwareFactory import TYPE

alias_names = {"CLA-L01-LRF-CTRL-01": "CLA-L01-CAV",
               "L01": "CLA-L01-CAV",
               "LRRG_GUN": "CLA-LRG1-GUN-CAV",
               "CLA-GUN-LRF-CTRL-01": "CLA-LRG1-GUN-CAV",
               #"CLA-GUN-MAG-SOL-02": "CLA-LRG1-MAG-SOL-01",
               #"CLA-LRG1-MAG-SOL-01": "CLA-GUN-MAG-SOL-02",
               "CLA-L01-CAV": "L01",
               "CLA-LRG1-GUN-CAV": "LRRG_GUN"}
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
                    'phase_ff': 'vm:dsp:ff_ph:phase'}

