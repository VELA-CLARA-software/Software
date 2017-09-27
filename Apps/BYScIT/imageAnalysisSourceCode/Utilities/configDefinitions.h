#ifndef CONFIG_DEFINITIONS_H
#define CONFIG_DEFINITIONS_H

#include <string>

namespace UTL
{
    const double DUMMY_DOUBLE = -999.999;
    const long   DUMMY_LONG   = -999;

    const std::string END_OF_LINE = ";";
    const std::string EQUALS_SIGN = "=";
    const char EQUALS_SIGN_C      = '=';

    const std::string CONFIG_PATH = "C:\\Users\\wln24624\\Documents\\VELA\\Software\\Processing_Software\\IMAGE ANALYSIS\\imageAnalyser_v3\\Config\\";

    const std::string PIL_SHUTTER_CONFIG     = "pil_shutter.config";
    const std::string INJ_IMG_CONFIG         = "inj_img.config";
    const std::string VALVE_CONFIG           = "vac_valve.config";
    const std::string QBOX_CONFIG            = "qbox.config";
    const std::string BPM_CONFIG             = "bpm.config";
    const std::string SCOPE_CONFIG           = "scope.config";
    const std::string SCOPE_TRACE_CONFIG     = "scope_trace_new.config";
    const std::string RF_GUN_PWR_CONFIG      = "rf_gun_power.config";
    const std::string RF_GUN_MOD_CONFIG      = "rf_gun_modulator.config";
    const std::string RF_GUN_LLRF_CONFIG     = "rf_gun_LLRF.config";
    const std::string INJ_MAG_NR_PSU_CONFIG  = "inj_mag_NR_psu.config";
    const std::string INJ_MAG_CONFIG         = "inj_mag.config";
    const std::string INJ_MAG_DEGUASS_CONFIG = "inj_mag_degauss.config";
    const std::string COMPLEX_SCREENS_CONFIG = "complexScreens.config";
    const std::string SIMPLE_SCREENS_CONFIG  = "simpleScreens.config";
    const std::string YAG_MASK_CONFIG        = "YAG_masks.config";

    /// These are the keywords used in hardware config files

    /// General Keywords

    const std::string START_OF_DATA     = "START_OF_DATA";
    const std::string END_OF_DATA       = "END_OF_DATA";
    const std::string VERSION           = "VERSION";
    const std::string NAME              = "NAME";
    const std::string PV_ROOT           = "PV_ROOT";
    const std::string OBJECTS_START     = "OBJECTS_START";
    const std::string NUMBER_OF_OBJECTS = "NUMBER_OF_OBJECTS";
    const std::string PV_MONITORS_START = "PV_MONITORS_START";
    const std::string PV_COMMANDS_START = "PV_COMMANDS_START";
    const std::string PV_ARRAY_MONITORS_START = "PV_ARRAY_MONITORS_START";
    const std::string NUMBER_OF_ILOCKS  = "NUMBER_OF_ILOCKS";

    // PVs
    const std::string PV_SUFFIX_ON          = "PV_SUFFIX_ON";
    const std::string PV_SUFFIX_OFF         = "PV_SUFFIX_OFF";
    const std::string PV_SUFFIX_STA         = "PV_SUFFIX_STA";
    const std::string NUMBER_OF_INTERLOCKS  = "NUMBER_OF_INTERLOCKS";

    const std::string PV_COUNT  = "PV_COUNT" ;
    const std::string PV_CHTYPE = "PV_CHTYPE";
    const std::string PV_MASK   = "PV_MASK"  ;

    // RF POWER
    const std::string PV_SUFFIX_REV   = "PV_SUFFIX_REV";
    const std::string PV_SUFFIX_FWD   = "PV_SUFFIX_FWD";
    const std::string PV_SUFFIX_REVT  = "PV_SUFFIX_REVT";
    const std::string PV_SUFFIX_FWDT  = "PV_SUFFIX_FWDT";
    const std::string PV_SUFFIX_REVTM = "PV_SUFFIX_REVTM";
    const std::string PV_SUFFIX_FWDTM = "PV_SUFFIX_FWDTM";
    const std::string PV_SUFFIX_RATIO = "PV_SUFFIX_RATIO";

    // QBOX
    const std::string PV_QBOX_STATE    = "PV_QBOX_STATE";
    const std::string PV_QBOX_SETSTATE = "PV_QBOX_SETSTATE";

    // Vac
    const std::string PV_VAC_PRESSURE = "PV_VAC_PRESSURE";

    // Scope
    const std::string PV_SUFFIX_P1    = "PV_SUFFIX_P1";
    const std::string PV_SUFFIX_P2    = "PV_SUFFIX_P2";
    const std::string PV_SUFFIX_P3    = "PV_SUFFIX_P3";
    const std::string PV_SUFFIX_P4    = "PV_SUFFIX_P4";
    const std::string PV_SUFFIX_TR1   = "PV_SUFFIX_TR1";
    const std::string PV_SUFFIX_TR2   = "PV_SUFFIX_TR2";
    const std::string PV_SUFFIX_TR3   = "PV_SUFFIX_TR3";
    const std::string PV_SUFFIX_TR4   = "PV_SUFFIX_TR4";
    const std::string PV_SCOPE_TYPE   = "PV_SCOPE_TYPE";
    const std::string TIMEBASE        = "TIMEBASE";
    const std::string NOISE_FLOOR     = "NOISE_FLOOR";
    const std::string DIAG_TYPE       = "DIAG_TYPE";
    const std::string WCM             = "WCM";
    const std::string ICT1            = "ICT1";
    const std::string ICT2            = "ICT2";
    const std::string FCUP            = "FCUP";
    const std::string ED_FCUP         = "ED_FCUP";

    // BPM
    const std::string PV_SUFFIX_BPM_SA1     = "PV_SUFFIX_BPM_SA1";
    const std::string PV_SUFFIX_BPM_SA2     = "PV_SUFFIX_BPM_SA2";
    const std::string PV_SUFFIX_BPM_SD1     = "PV_SUFFIX_BPM_SD1";
    const std::string PV_SUFFIX_BPM_SD2     = "PV_SUFFIX_BPM_SD2";
    const std::string PV_SUFFIX_BPM_RA1     = "PV_SUFFIX_BPM_RA1";
    const std::string PV_SUFFIX_BPM_RA2     = "PV_SUFFIX_BPM_RA2";
    const std::string PV_SUFFIX_BPM_RD1     = "PV_SUFFIX_BPM_RD1";
    const std::string PV_SUFFIX_BPM_RD2     = "PV_SUFFIX_BPM_RD2";
    const std::string PV_SUFFIX_BPM_X       = "PV_SUFFIX_BPM_X";
    const std::string PV_SUFFIX_BPM_Y       = "PV_SUFFIX_BPM_Y";
    const std::string PV_SUFFIX_BPM_DATA    = "PV_SUFFIX_BPM_DATA";
    const std::string ATT1CAL               = "ATT1CAL";
    const std::string ATT2CAL               = "ATT2CAL";
    const std::string V1CAL                 = "V1CAL";
    const std::string V2CAL                 = "V2CAL";
    const std::string QCAL                  = "QCAL";
    const std::string MN                    = "MN";
    const std::string XN                    = "XN";
    const std::string YN                    = "YN";

    // LLRF
    const std::string PV_SUFFIX_AMPR = "PV_SUFFIX_AMPR";
    const std::string PV_SUFFIX_PHI  = "PV_SUFFIX_PHI";
    const std::string PV_SUFFIX_AMPW = "PV_SUFFIX_AMPW";

    // Modulator
    const std::string PV_SUFFIX_RESET     = "PV_SUFFIX_RESET";
    const std::string PV_SUFFIX_STATESET  = "PV_SUFFIX_STATESET";
    const std::string PV_SUFFIX_STATEREAD = "PV_SUFFIX_STATEREAD";
    const std::string PV_SUFFIX_EXILOCK1  = "PV_SUFFIX_EXILOCK1";
    const std::string PV_SUFFIX_WARMUPT   = "PV_SUFFIX_WARMUPT";

    // NR-PSU
    const std::string PARENT_MAGNET = "PARENT_MAGNET";
    const std::string MAG_GANG_MEMBER = "MAG_GANG_MEMBER";
    const std::string PV_ROOT_N   = "PV_ROOT_N";
    const std::string PV_ROOT_R   = "PV_ROOT_R";
    // Magnet
    const std::string PV_SUFFIX_RI = "PV_SUFFIX_RI";
    const std::string PV_SUFFIX_SI = "PV_SUFFIX_SI";
    const std::string PV_PSU_ROOT  = "PV_PSU_ROOT";


    const std::string MAG_TYPE  = "MAG_TYPE";
    const std::string SOL   = "SOL";
    const std::string BSOL  = "BSOL";
    const std::string QUAD  = "QUAD";
    const std::string DIP   = "DIP";
    const std::string HCOR  = "HCOR";
    const std::string VCOR  = "VCOR";
    const std::string SEXT  = "SEXT";

    const std::string MAG_REV_TYPE  = "MAG_REV_TYPE";
    const std::string NR        = "NR";
    const std::string BIPOLAR   = "BIPOLAR";
    const std::string NR_GANGED = "NR_GANGED";
    const std::string POS       = "POS";
    // deguass
    const std::string NUM_DEGAUSS_STEPS = "NUM_DEGAUSS_STEPS";
    const std::string BSOL_DEGAUSS_VALUES = "BSOL_DEGAUSS_VALUES";
    const std::string DIP_DEGAUSS_VALUES = "DIP_DEGAUSS_VALUES";
    const std::string SOL_DEGAUSS_VALUES = "SOL_DEGAUSS_VALUES";
    const std::string QUAD_DEGAUSS_VALUES = "QUAD_DEGAUSS_VALUES";
    const std::string QUAD_DEGAUSS_TOLERANCE = "QUAD_DEGAUSS_TOLERANCE";
    const std::string BSOL_DEGAUSS_TOLERANCE = "BSOL_DEGAUSS_TOLERANCE";
    const std::string DIP_DEGAUSS_TOLERANCE = "DIP_DEGAUSS_TOLERANCE";
    const std::string SOL_DEGAUSS_TOLERANCE = "SOL_DEGAUSS_TOLERANCE";

    // chtypes

     const std::string DBR_STRING_STR = "DBR_STRING";
     const std::string DBR_INT_STR	  = "DBR_INT";
     const std::string DBR_SHORT_STR  = "DBR_SHORT";
     const std::string DBR_FLOAT_STR  = "DBR_FLOAT";
     const std::string DBR_ENUM_STR	  = "DBR_ENUM";
     const std::string DBR_CHAR_STR	  = "DBR_CHAR"  ;
     const std::string DBR_LONG_STR	  = "DBR_LONG"  ;
     const std::string DBR_DOUBLE_STR = "DBR_DOUBLE";
     const std::string DBR_TIME_STRING_STR ="DBR_TIME_STRING";
     const std::string DBR_TIME_INT_STR	   ="DBR_TIME_INT";
     const std::string DBR_TIME_SHORT_STR  ="DBR_TIME_SHORT";
     const std::string DBR_TIME_FLOAT_STR  ="DBR_TIME_FLOAT";
     const std::string DBR_TIME_ENUM_STR   ="DBR_TIME_ENUM";
     const std::string DBR_TIME_CHAR_STR	  ="DBR_TIME_CHAR"  ;
     const std::string DBR_TIME_LONG_STR	  ="DBR_TIME_LONG"  ;
     const std::string DBR_TIME_DOUBLE_STR ="DBR_TIME_DOUBLE";

     /// there are many others... e.g.
//    DBR_STS_ENUM	10	DBR_TIME_DOUBLE	20	DBR_CTRL_INT
//    DBR_STS_CHAR	11	DBR_GR_STRING	21	DBR_CTRL_FLOAT
//    DBR_STS_LONG	12	DBR_GR_SHORT	22	DBR_CTRL_ENUM
//    DBR_STS_DOUBLE	13	DBR_GR_INT	22	DBR_CTRL_CHAR	32
//    DBR_TIME_STRING	14	DBR_GR_FLOAT	23	DBR_CTRL_LONG
//    DBR_TIME_INT	15	DBR_GR_ENUM	24	DBR_CTRL_DOUBLE	34


     //MASK
     const std::string DBE_VALUE_STR = "DBE_VALUE";
     const std::string DBE_LOG_STR	 = "DBE_LOG";
     const std::string DBE_ALARM_STR = "DBE_ALARM";

//
//    /// RF_GUN Keywords
//
//    const std::string RF_GUN_PyOW_OBJ_START  = "RF_GUN_PyOW_OBJ_START";
//    const std::string RF_GUN_MOD_OBJ_START  = "RF_GUN_MOD_OBJ_START";
//    const std::string RF_GUN_OBJ_START      = "RF_GUN_OBJ_START";
//    const std::string PV_PyOW_MONITORS_START = "PV_PyOW_MONITORS_START";
//
//    const std::string RF_GUN_PyOW_PyV_SUFFIX_REV   = "RF_GUN_PyOW_PyV_SUFFIX_REV";
//    const std::string RF_GUN_PyOW_PyV_SUFFIX_FWD   = "RF_GUN_PyOW_PyV_SUFFIX_FWD";
//    const std::string RF_GUN_PyOW_PyV_SUFFIX_REVT  = "RF_GUN_PyOW_PyV_SUFFIX_REVT";
//    const std::string RF_GUN_PyOW_PyV_SUFFIX_FWDT  = "RF_GUN_PyOW_PyV_SUFFIX_FWDT";
//    const std::string RF_GUN_PyOW_PyV_SUFFIX_REVTM = "RF_GUN_PyOW_PyV_SUFFIX_REVTM";
//    const std::string RF_GUN_PyOW_PyV_SUFFIX_FWDTM = "RF_GUN_PyOW_PyV_SUFFIX_FWDTM";
//    const std::string RF_GUN_PyOW_PyV_SUFFIX_RATIO = "RF_GUN_PyOW_PyV_SUFFIX_RATIO";
//
//    const std::string RFGUNPWR    = "RFGUNPWR";
//    const std::string RFGUNKLYPWR = "RFGUNKLYPWR";
//
//    const std::string PV_RF_GUN_MOD_STATESET  = "PV_RF_GUN_MOD_STATESET";
//    const std::string PV_RF_GUN_MOD_STATEREAD = "PV_RF_GUN_MOD_STATEREAD";
//    const std::string PV_RF_GUN_MOD_EXILOCK1  = "PV_RF_GUN_MOD_EXILOCK1";
//    const std::string PV_RF_GUN_MOD_WARMUPT   = "PV_RF_GUN_MOD_WARMUPT";
//    const std::string PV_RF_GUN_MOD_RESET     = "PV_RF_GUN_MOD_RESET";
//
//    const std::string REV_TRACE_SIZE = "REV_TRACE_SIZE";
//    const std::string FWD_TRACE_SIZE = "FWD_TRACE_SIZE";
//
//    const std::string PV_RF_GUN_FWD       = "PV_RF_GUN_FWD";
//    const std::string PV_RF_GUN_REV       = "PV_RF_GUN_REV";
//    const std::string PV_RF_GUN_KLY_FWD   = "PV_RF_GUN_KLY_FWD";
//    const std::string PV_RF_GUN_KLY_REV   = "PV_RF_GUN_KLY_REV";
//    const std::string PV_RF_GUN_PyHI       = "PV_RF_GUN_PyHI";
//    const std::string PV_RF_GUN_AMP_WRITE = "PV_RF_GUN_AMP_WRITE";
//    const std::string PV_RF_GUN_AMP_READ  = "PV_RF_GUN_AMP_READ";
//    const std::string PV_RF_GUN_RATIO     = "PV_RF_GUN_RATIO";
//    const std::string RF_GUN_SAFE_AMP     = "RF_GUN_SAFE_AMP";
//
//    /// MAGNETS
//
//    const std::string INJ_MAG_MONITORS_PyV_START = "INJ_MAG_MONITORS_PyV_START";
//    const std::string INJ_MAG_PyV_START          = "INJ_MAG_PyV_START";
//    const std::string NR_PyV_MONITORS_START      = "NR_PyV_MONITORS_START";
//    const std::string NR_PyV_START               = "NR_PyV_START";
//    const std::string INJ_MAG_PyV_SUFFIX_SI      = "INJ_MAG_PyV_SUFFIX_SI";
//    const std::string INJ_MAG_PyV_SUFFIX_RI      = "INJ_MAG_PyV_SUFFIX_RI";
//
//    const std::string MAG_TYPE   = "MAG_TYPE";
//

//
//    const std::string MAG_REV_TYPE            = "MAG_REV_TYPE";
//    const std::string MAG_REV_TYPE_NR         = "NR";
//    const std::string MAG_REV_TYPE_NR_BIPOLAR = "BIPOLAR";
//    const std::string MAG_REV_TYPE_NR_GANGED  = "NR_GANGED";
//    const std::string MAG_REV_TYPE_PyOS        = "POS";
//    const std::string PARENT_MAGNET           = "PARENT_MAGNET";
//    const std::string MAG_PySU_ROOT            = "MAG_PySU_ROOT";
//    const std::string MAG_GANG_MEMBER         = "MAG_GANG_MEMBER";
//
//    const std::string BSOL_DEGAUSS_VALUES  = "BSOL_DEGAUSS_VALUES";
//    const std::string DIP_DEGAUSS_VALUES   = "DIP_DEGAUSS_VALUES";
//    const std::string SOL_DEGAUSS_VALUES   = "SOL_DEGAUSS_VALUES";
//    const std::string QUAD_DEGAUSS_VALUES  = "QUAD_DEGAUSS_VALUES";
//
//    const std::string QUAD_DEGAUSS_TOLERANCE = "QUAD_DEGAUSS_TOLERANCE";
//    const std::string BSOL_DEGAUSS_TOLERANCE = "BSOL_DEGAUSS_TOLERANCE";
//    const std::string DIP_DEGAUSS_TOLERANCE  = "DIP_DEGAUSS_TOLERANCE";
//    const std::string SOL_DEGAUSS_TOLERANCE  = "SOL_DEGAUSS_TOLERANCE";

 /// SCREEN YAG 1/2/3 COMMAND PVs

    const std::string PV_SUFFIX_H_MABS      = "PV_SUFFIX_H_MABS";
    const std::string PV_SUFFIX_V_MABS      = "PV_SUFFIX_V_MABS";
    const std::string PV_SUFFIX_H_RPOS      = "PV_SUFFIX_H_RPOS";
    const std::string PV_SUFFIX_V_RPOS      = "PV_SUFFIX_V_RPOS";
    const std::string PV_SUFFIX_STOP        = "PV_SUFFIX_STOP";

    ///SCREEN YAG 1/2/3 MONITOR PVs

    const std::string PV_SUFFIX_H_PROT01    = "PV_SUFFIX_H_PROT01";
    const std::string PV_SUFFIX_V_PROT01    = "PV_SUFFIX_V_PROT01";
    const std::string PV_SUFFIX_PROT03      = "PV_SUFFIX_PROT03";
    const std::string PV_SUFFIX_PROT05      = "PV_SUFFIX_PROT05";
    const std::string PV_SUFFIX_H_RPWRLOSS  = "PV_SUFFIX_H_RPWRLOSS";
    const std::string PV_SUFFIX_V_RPWRLOSS  = "PV_SUFFIX_V_RPWRLOSS";


    /// SCREEN YAG 1/2/3 POSITIONS

    const std::string H_MIRROR      = "H_MIRROR";
    const std::string H_50U_SLIT    = "H_50U_SLIT";
    const std::string H_25U_SLIT    = "H_25U_SLIT";
    const std::string H_63MM_HOLE    = "H_63MM_HOLE";
    const std::string H_10MM_HOLE   = "H_10MM_HOLE";
    const std::string V_YAG         = "V_YAG";
    const std::string V_SLIT        = "V_SLIT";
    const std::string H_SLIT        = "H_SLIT";
    const std::string H_OUT         = "H_OUT";
    const std::string V_OUT         = "V_OUT";
    const std::string OUT           = "OUT";
    const std::string IN            = "IN";

    /// YAG MASKS DATA FOR IMAGE ANAYLSIS
    const std::string SCREEN_INFO_END      = "SCREEN_INFO_END";
    const std::string SCREEN               = "SCREEN";
    const std::string CAMERA_NAME          = "CAMERA_NAME";
    const std::string SCREEN_NAME          = "SCREEN_NAME";
    const std::string HEIGHT_OF_IMAGE      = "HEIGHT_OF_IMAGE";
    const std::string WIDTH_OF_IMAGE       = "WIDTH_OF_IMAGE";
    const std::string MASK_X               = "MASK_X";
    const std::string MASK_Y               = "MASK_Y";
    const std::string MASK_RX              = "MASK_RX";
    const std::string MASK_RY              = "MASK_RY";
    const std::string MASK_FILE            = "MASK_FILE";
    const std::string PIXELS_TO_MILLIMETER_RATIO = "PIXELS_TO_MILLIMETER_RATIO";


}
#endif //CONFIG_DEFINITIONS_H

