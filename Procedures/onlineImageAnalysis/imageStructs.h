#ifndef _IMAGE_STRUCT_H_
#define _IMAGE_STRUCT_H_

#include<string>
#include<vector>

///----------------DATA STRUCT FOR IMAGE AND ITS MANIPULATIONS----------------///
//Holds data from Images and how to crop/ analyse it


///Enums
enum EstMethod {FWHM,moments};
enum projAxis {x,y,maskX,maskY};

typedef struct imageDataStruct
    {
        std::string imageName="UNKNOWN";
        std::string camName="UNKNOWN";
        std::string screenName="UNKNOWN";

        int dataSize=0;
        int imageWidth=0, imageHeight=0;
        double pixToMM=0;
        std::vector<double> pixIntensity;
        std::vector<double> X;
        std::vector<double> Y;
        std::vector<double> mask;
        //Projections of X and Y
        std::vector<double> xProjection;
        std::vector<double> yProjection;
        std::vector<double> maskXProjection;
        std::vector<double> maskYProjection;

        std::vector<double> background;//raw background data

        //cropping info(parameter for ellipse hole of mask)
        int x0=0, y0=0, xRad=0, yRad=0;

        void operator=(const imageDataStruct& ID){
            (*this).imageName=ID.imageName;
            (*this).camName=ID.camName;
            (*this).dataSize=ID.dataSize;
            (*this).imageWidth=ID.imageWidth;
            (*this).imageHeight=ID.imageHeight;
            (*this).pixIntensity=ID.pixIntensity;
            (*this).X=ID.X;
            (*this).Y=ID.Y;
            (*this).mask=ID.mask;
            (*this).xProjection=ID.xProjection;
            (*this).yProjection=ID.yProjection;
            (*this).maskXProjection=ID.maskXProjection;
            (*this).maskYProjection=ID.maskYProjection;
            (*this).background=ID.background;
            (*this).x0=ID.x0;
            (*this).y0=ID.y0;
            (*this).xRad=ID.xRad;
            (*this).yRad=ID.yRad;
            (*this).pixToMM=ID.pixToMM;
            return;
        }

        void clear(){
            imageDataStruct wipedData;
            (*this) = wipedData;
        }

    } imageDataStruct;

#endif
