#ifndef IO_H
#define IO_H

#include"imageStructs.h"
#include"configReader_YAG_masks.h"
#include "baseObject.h"

///------------------CLASS TO SET IMAGE DATA AND OUTPUT DATA----------------------///
///---------------Holds reads in and holds original copy of data------------------///
class readAndWrite: public baseObject{
    public:
         //Constructor
        readAndWrite( const bool* show_messages_ptr, const  bool * show_debug_messages_ptr );
        //Destructor
        ~readAndWrite();

        ///Functions
        //READ IN DATA FROM EPICS (not made)

        //READ IN DATA FROM FILE
        void readFile(const std::string & imageName);
        //READ BACKGROUN FILE
        void readBackgroundFile(const std::string & imageName);
        //READ IN A PNG IMAGE
        std::vector<double> readPNG(const std::string & imageName);
        //READ IN A RAW FILE
        std::vector<double> readRAW(const std::string & imageName);
        //WRITE DATA TO FILES
        void writeToFile(const imageDataStruct& ID, const std::string & out);
        //MAKE A MASK
        std::vector<double> makeMask(const imageDataStruct& ID, const int& dataSize, const int& x0, const int& y0, const int& rX, const int& rY);
        //READ IN A MASK (not made)

        //MAKE PROJECTIONS X OR Y
        std::vector<double> getProjection(const imageDataStruct& ID, const projAxis &axis);
        //MAKE A PROJECTION (FUNCTION WITH STRUCTURE ON HOW ITS DONE)
        std::vector<double> makeProjection(const std::vector<double> &v, const int &lengthOfFirstSum, const int &lengthOfSecondSum, const int &width, const bool &revIndices);
        //GET FUNCTIONS
        imageDataStruct getOriginalImageData();
        std::vector<double> getOriginalPixIntensity();
        std::vector<double> getOriginalBackgroundImage();
        std::vector<double> getOriginalXProjection();
        std::vector<double> getOriginalYProjection();
        std::vector<double> getOriginalX();
        std::vector<double> getOriginalY();

    protected:
        //Orignal copy of image data that does NOT get editted
        imageDataStruct originalImageData;
        //config data;
        configReaderYAG configData;
    private:
};

#endif

