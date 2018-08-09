ASTRARules = {}

ASTRARules["NEWRUN"] = ["NLoop", "ion_mass", "N_red", \
"Xoff", "Yoff", "xp", "yp", "Zoff", "Toff", "Xrms", "Yrms", "XYrms", \
"Zrms", "Trms", "Tau", "cor_px", "cor_py", \
"SRT_Q_Schottky", "Q_Schottky", "debunch", "Track_All", \
"Track_On_Axis", "Auto_Phase", "Phase_Scan", "check_ref_part", \
"L_rm_back", "Z_min", "Z_Cathode", "H_max", "H_min", "Max_step", \
"Lmonitor"]

ASTRARules["OUTPUT"] = ["ZSTART", "ZSTOP", "ZEMIT", "ZPHASE",
  "SCREEN", "SCR_XROT", "SCR_YROT", "STEP_WIDTH", "STEP_MAX",
  "LPROJECT_EMIT", "LOCAL_EMIT", "LMAGNETIZED", "LSUB_ROT",
  "LSUB_LARMOR", "LSUB_COUP", "ROT_ANG", "LSUB_COR", "REFS", "EMITS",
  "C_EMITS", "c99_EMITS", "TR_EMITS", "SUB_EMITS", "CROSS_START",
  "CROSS_END", "PHASES", "T_PHASES", "HIGH_RES", "BINARY", "TRACKS",
  "TCHECKS", "SIGMAS", "CATHODES", "LANDFS", "LARMORS"]

ASTRARules["CHARGE"] = ["L2D_3D",
   "LMIRROR", "L_CURVED_CATHODE", "CATHODE_CONTOUR", "R_ZERO",
    "CELL_VAR", "N_MIN", "MIN_GRID", "MERGE_1", "MERGE_2",
    "MERGE_3", "MERGE_4", "MERGE_5", "MERGE_6", "MERGE_7", "MERGE_8",
   "MERGE_9", "MERGE_10", "Z_TRANS", "MIN_GIRD_TRANS", "NX0",
   "NY0", "NZF", "SMOOTH_X", "SMOOTH_Y", "SMOOTH_Z",
   "MAX_SCALE", "MAX_COUNT", "EXP_CONTROL"]

ASTRARules["SCAN"] = ["LEXTEND", "SCAN_PARA",
   "S_MIN", "S_MAX", "S_NUMB", "O_MIN", "O_MAX", "O_MATCH",
   "MATCH_VALUE", "O_DEPTH", "L_MIN", "L_MAX", "S_ZMIN", "S_ZMAX",
   "S_DZ", "FOM"]

ASTRARules["APERTURE"] = ["FILE_APERTURE", "AP_Z1",
   "AP_Z2", "AP_R", "AP_GR", "A_POS", "A_XOFF", "A_YOFF", "A_XROT",
   "A_YROT", "A_ZROT", "SE_D0", "SE_EPM", "SE_FS", "SE_TAU", "SE_ESC",
    "SE_FF1", "SE_FF2", "MAX_SECONDARY", "LCLEAN_STACK"]

ASTRARules["CAVITY"] = ["C_NOSCALE",
    "COM_GRID", "C_HIGHER_ORDER", "K_WAVE",
   "EX_STAT", "EY_STAT", "BX_STAT", "BY_STAT", "BZ_STAT",
   "FLATNESS", "T_DEPENDENCE", "T_NULL",
   "C_TAU", "E_STORED", "C_XROT", "C_YROT",
   "C_ZROT", "C_ZKICKMIN", "C_ZKICKMAX", "C_XKICK", "C_YKICK",
   "FILE_A0", "P_Z1", "P_R1", "P_Z2", "P_R2", "P_N", "E_A0", "E_Z0",
   "E_SIG", "E_SIGZ", "E_ZR", "E_EPS", "E_LAM", "ZETA"]

ASTRARules["SOLENOID"] = ["LOOP", "LBFIELD",
   "S_NOSCALE", "S_HIGHER_ORDER", "S_XROT", "S_YROT"]
