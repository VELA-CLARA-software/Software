from CATAP.HardwareFactory import TYPE

alias_names = {"CLA-L01-LRF-CTRL-01": "CLA-L01-CAV",
               "L01": "CLA-L01-CAV",
               "LRRG_GUN": "CLA-LRG1-GUN-CAV",
               "CLA-GUN-MAG-SOL-02": "CLA-LRG1-MAG-SOL-01",
               "CLA-LRG1-MAG-SOL-01": "CLA-GUN-MAG-SOL-02",
               "CLA-L01-CAV": "L01",
               "CLA-LRG1-GUN-CAV": "LRRG_GUN",
               "CLA-LRG1-MAG-BSOL-01": "CLA-LRG1-MAG-SOL-01"}

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