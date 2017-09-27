//tjp
#include "configReader_YAG_masks.h"

//stl
#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <time.h>
#include <algorithm>
#include <ctype.h>
//______________________________________________________________________________
configReaderYAG::configReaderYAG( const bool* show_messages_ptr, const  bool * show_debug_messages_ptr  ): configReader( UTL::CONFIG_PATH, show_messages_ptr, show_debug_messages_ptr )
{}
//______________________________________________________________________________
configReaderYAG::~configReaderYAG(){}
//______________________________________________________________________________
bool configReaderYAG::readYAGConfig(const std::string& yag)
{
    std::string line, trimmedLine;
    bool success = false;
    std::ifstream inputFile;
    inputFile.open(configFile_Path+UTL::YAG_MASK_CONFIG.c_str(), std::ios::in );
    if( inputFile )
    {
        bool readingData         = false;
        bool desiredYAGInfo = false;

        debugMessage( UTL::YAG_MASK_CONFIG, " opened from ", configFile_Path );
        while( std::getline( inputFile, line ) ) /// Go through, reading file line by line
        {
            trimmedLine = trimAllWhiteSpace( trimToDelimiter( line, UTL::END_OF_LINE ) );
            if( trimmedLine.size() > 0 )
            {
                if( stringIsSubString( line, UTL::END_OF_DATA ) )
                {
                    readingData = false;
                    break;
                }
                if( stringIsSubString( line, UTL::START_OF_DATA ) )
                {
                    readingData = true;
                }

                if(readingData)
                {
                    if( stringIsSubString( trimmedLine, yag ) )
                    {
                        desiredYAGInfo = true;

                    }
                    if(stringIsSubString( trimmedLine, UTL::SCREEN_INFO_END ))
                    {
                        desiredYAGInfo = false;
                    }

                    if(desiredYAGInfo)
                    {
                        //GET SCREEN NAME
                        if(stringIsSubString( trimmedLine, UTL::SCREEN_NAME ))
                        {
                            dataFromConfig.screenName=getAfterEqualsSign(trimmedLine);
                            std::cout<<"Reading config data for "+dataFromConfig.screenName<<std::endl;
                        }
                        //GET CAMERA NAME
                        if(stringIsSubString( trimmedLine, UTL::CAMERA_NAME ))
                        {
                            dataFromConfig.camName=getAfterEqualsSign(trimmedLine);
                        }
                        //GET GET HEIGHT OF IMAGE
                        if(stringIsSubString( trimmedLine, UTL::HEIGHT_OF_IMAGE ))
                        {
                            dataFromConfig.imageHeight=getNum(trimmedLine);
                        }
                       //GET GET WIDTH OF IMAGE
                        if(stringIsSubString( trimmedLine, UTL::WIDTH_OF_IMAGE ))
                        {
                            dataFromConfig.imageWidth=getNum(trimmedLine);
                        }
                       //GET GET CENTRE X VALUE OF MASK
                        if(stringIsSubString( trimmedLine, UTL::MASK_X ))
                        {
                            dataFromConfig.x0=getNum(trimmedLine);
                        }
                       //GET GET CENTRE Y VALUE OF MASK
                        if(stringIsSubString( trimmedLine, UTL::MASK_Y ))
                        {
                            dataFromConfig.y0=getNum(trimmedLine);

                        }
                       //GET GET X RAD VALUE OF MASK
                        if(stringIsSubString( trimmedLine, UTL::MASK_RX ))
                        {
                            dataFromConfig.xRad=getNum(trimmedLine);
                        }
                       //GET GET Y RAD VALUE OF MASK
                        if(stringIsSubString( trimmedLine, UTL::MASK_RY ))
                        {
                            dataFromConfig.yRad=getNum(trimmedLine);
                        }
                       //GET GET PIXTOMM VALUE OF MASK
                        if(stringIsSubString( trimmedLine, UTL::PIXELS_TO_MILLIMETER_RATIO ))
                        {
                            dataFromConfig.pixToMM=getNumD(trimmedLine);

                        }
                        //Read in file with mask already calulated (will not make theis funcition now... later)
                    }
                }
            }


        }
        inputFile.close( );


        success = true;
    }
    else{
        //message( "!!!! Error Can't Open Shutter Config File after searching in:  ", configFile_Path, " !!!!"  );
    }
    return success;
}
//______________________________________________________________________________
imageDataStruct configReaderYAG::getConfigData(){
    return dataFromConfig;
}



