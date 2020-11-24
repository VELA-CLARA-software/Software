#include <iostream>
#include <string>
#include <chrono>
#include <vector>
#include <numeric>
#include <thread>
//#include <qapplication.h>
//#include <qpushbutton.h>
#include "beamPositionMonitorController.h"
#include "chargeController.h"

int main()
{
    std::cout << " _____ _____ _____  " << std::endl;
    std::cout << "| __  |  _  |     | " << std::endl;
    std::cout << "| __ -|   __| | | | " << std::endl;
    std::cout << "|_____|__|  |_|_|_| " << std::endl;
    std::cout << "" << std::endl;
    std::cout << " _____             _ _ _           _        " << std::endl;
    std::cout << "| __  |___ ___ ___| |_| |_ ___ ___| |_ ___  " << std::endl;
    std::cout << "|    -| -_|  _| .'| | | . |  _| .'|  _| -_| " << std::endl;
    std::cout << "|__|__|___|___|__,|_|_|___|_| |__,|_| |___| " << std::endl;
    std::cout << "" << std::endl;
    std::cout << "" << std::endl;

    std::string machine_area_bpm, machine_area_charge;
    //std::string &bpmconf = UTL::APCLARA1_CONFIG_PATH + UTL::C2B_BPM_CONFIG;
    std::string &bpmconf = UTL::CLARANET_CONFIG_PATH + UTL::C2B_BPM_CONFIG;
//    if( machine_area_bpm == "1" )
//    {
//        const std::string &bpmconf = UTL::APCLARA1_CONFIG_PATH + UTL::CLARA_PH1_BPM_CONFIG;
//    }
//    else if( machine_area_bpm == "2" )
//    {
//        const std::string &bpmconf = UTL::APCLARA1_CONFIG_PATH + UTL::VELA_INJ_BPM_CONFIG;
//    }
//    else if( machine_area_bpm == "3" )
//    {
//        const std::string &bpmconf = UTL::APCLARA1_CONFIG_PATH + UTL::VELA_BA1_BPM_CONFIG;
//    }
//    else
//    {
//        std::cout << "invalid MACHINE_AREA parameter" << std::endl;
//        return 0;
//    }
    bool * message = new bool;
    bool * debugmessage = new bool;
    *message = false;
    *debugmessage = false;
    const bool withepics = true;
    const bool withvm = false;
    //const std::string &chargeconf = UTL::APCLARA1_CONFIG_PATH + UTL::CLARA_PH1_CHARGE_CONFIG;
    const std::string &chargeconf = UTL::CLARANET_CONFIG_PATH + UTL::CLARA_PH1_CHARGE_CONFIG;
    const HWC_ENUM::MACHINE_AREA mymachinearea = HWC_ENUM::MACHINE_AREA::CLARA_PH1;
    beamPositionMonitorController * bpmcont = new beamPositionMonitorController(bpmconf,
                                                                                *message,
                                                                                *debugmessage,
                                                                                withepics,
                                                                                withvm,
                                                                                mymachinearea);
    chargeController * chargecont = new chargeController(chargeconf,
                                                         *message,
                                                         *debugmessage,
                                                         withepics,
                                                         withvm,
                                                         mymachinearea);

    const std::vector< std::string > bpmnames = bpmcont->getBPMNames();
    std::this_thread::sleep_for(std::chrono::milliseconds(2000));
    const boost::circular_buffer< double > wcmchargebuffer = chargecont->getChargeBuffer(UTL::WCM);
    const double wcmchargemean = std::accumulate( wcmchargebuffer.begin(), wcmchargebuffer.end(), 0.0)/wcmchargebuffer.size();
    std::cout << std::endl;
    std::cout << "RUNNING" << std::endl;
    std::cout << std::endl;
    std::cout << "WCM charge = " << wcmchargemean << std::endl;
    if(wcmchargemean < 20.0 )
    {
        std::cout << "Measured WCM charge is too low to re-calibrate" << std::endl;
        std::cout << "A WCM charge above ~25pC **should** be fine to successfully run this procedure." << std::endl;
        std::cout << "Please try again." << std::endl;
    }
    else{

        for( auto && it : bpmnames )
        {
            bpmcont->reCalAttenuation(it,wcmchargemean);
            std::cout << "new ATT1 for " << it << " == " << bpmcont->getRA1(it) << std::endl;;
            std::cout << "new ATT2 for " << it << " == " << bpmcont->getRA2(it) << std::endl;;
        }
    }

    std::cout << std::endl;
    std::cout << "BPM recalibrate has finished, press some buttons to exit" << std::endl;
    std::cin.ignore();
    std::cin.get();

    delete bpmcont;
    delete chargecont;

    return 0;
}
