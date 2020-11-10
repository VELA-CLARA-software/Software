from CATAP.HardwareFactory import TYPE

alias_names = {"CLA-L01-LRF-CTRL-01": "CLA-L01-CAV",
               "L01": "CLA-L01-CAV",
               "LRRG_GUN": "CLA-LRG1-GUN-CAV",
               #"CLA-GUN-MAG-SOL-02": "CLA-LRG1-MAG-SOL-01",
               #"CLA-LRG1-MAG-SOL-01": "CLA-GUN-MAG-SOL-02",
               "CLA-L01-CAV": "L01",
               "CLA-LRG1-GUN-CAV": "LRRG_GUN"}
               #"CLA-LRG1-MAG-BSOL-01": "CLA-LRG1-MAG-SOL-01"}

screen_alias = {"S02-APER-01": "CLA-S02-APER-01",
                "S01-SCR-01": "CLA-S01-DIA-SCR-01",
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

screen_to_camera = {"CLA-S02-APER-01": "CLA-S02-APER-01",
                    "CLA-S01-DIA-SCR-01": "CLA-S01-DIA-CAM-01",
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
              TYPE.LLRF_TYPE: "cavity",
              TYPE.HORIZONTAL_CORRECTOR: "kicker",
              TYPE.VERTICAL_CORRECTOR: "kicker",
              TYPE.DIPOLE: "dipole",
              TYPE.BPM_TYPE: "bpm",
              TYPE.SCREEN: "screen",
              TYPE.CAMERA_TYPE: "camera",
              TYPE.VALVE: "valve",
              TYPE.CHARGE: "charge",
              TYPE.IMG_TYPE: "img"}

gun_kly_fwd_power_max = 9.9 * 10 ** 6