#ifndef EDIT_H
#define EDIT_H

#include"ImageStructs.h"
#include "baseObject.h"

///------------------CLASS TO PUT EDITTING FUNCTIONS----------------------///
///------------Functions that will read in image data from----------------///
///------------image Analyser and output an editted version---------------///
class editor: public baseObject{
    public:
        //Constructor
        editor( const bool* show_messages_ptr, const  bool * show_debug_messages_ptr );
        //Destructor
        ~editor();


        ///Functions
        //APPLY MASK
        std::vector<double> applyMask(const imageDataStruct& ID);
        //CROP IMAGE
        imageDataStruct crop(const imageDataStruct& ID,const int& x,const int& y,const int& w,const int& h);
        //SUBTRACT BACKGROUND IMAGE
        std::vector<double> subtractBackground(const imageDataStruct& ID);
        //SUBTRACT IMAGES
        std::vector<double> subtractImages(const std::vector<double>& v1,const std::vector<double>& v2);
        //CHANGE INTENSITY OF IMAGE BY A FACTOR
        std::vector<double> scaleImage(const double& A, const std::vector<double>& v1);
        //SCALED MASK SUBTRACTION
        std::vector<double> scaledMaskSubtraction(const imageDataStruct& ID);
        //N POINT SCALING
        std::vector<double> nPointScaling(const imageDataStruct& ID);
        // APPLY FILTER MOVING AVERAGE (FOR PROJECTIONS) 5,10 or 20
        std::vector<double> applyFilter(const imageDataStruct& ID, const int& A, const projAxis& axis);
        //FILTER METHOD
        std::vector<double> filterMethod(const std::vector<double> &v, const int& A);
        //GET CORRECTIONS TO BEAM CENTROID
        std::vector<double> correctBeamPosition(const double& muX, const double& muY);
        //PIXTOMM
        double ptm(const double & ptmRatio, const double& valInPixels);
        //these keep track of how much the image has been cropped and used to rescale the centroid position later
        int croppedX=0,croppedY=0;
    protected:

    private:
};

#endif

