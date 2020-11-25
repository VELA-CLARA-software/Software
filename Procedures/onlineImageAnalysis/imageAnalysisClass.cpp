#include <fstream>
#include <iterator>
#include <vector>
#include <stdint.h>
#include<iostream>
#include<sstream>
#include <algorithm>
#include <cmath>
#include <chrono>
typedef std::chrono::high_resolution_clock Clock;
#include "imageAnalysisClass.h"

///-------------------------Functions of Image Analysis Class------------------------///

//Constructor
imageAnalysisClass::imageAnalysisClass(){}
//Destructor
imageAnalysisClass::~imageAnalysisClass(){}

////////////////////////////////////////////////////////////////////////////////////////
//This is your main function
typedef std::vector<double> dvec;
std::vector<dvec> imageAnalysisClass::anaylseImage(std::vector<double> &arrayData,
                                                   std::vector<double> &bkgrndData){
    //This is A speedy Version (no scaling)
    runningXCropCounter=0;
    runningYCropCounter=0;

    //1.Crop,Subtract Background and Apply Aask all in one loop.
    cropSubtractAndMask(arrayData,bkgrndData,imageCenterXPixel-imageXMaskRadius,
                        imageCenterXPixel+imageXMaskRadius,
                        imageCenterYPixel-imageYMaskRadius,
                        imageCenterYPixel+imageYMaskRadius);

    //2. Get Centroid Positions
    double sumPixIntensity=0;
    for(auto i=0;i!=imageSize;++i){
        sumPixIntensity+=processedPixelData[i];
    }

    double muX=dotProduct(processedPixelData,processedPixelXPosition)/sumPixIntensity;
    double muY=dotProduct(processedPixelData,processedPixelYPosition)/sumPixIntensity;

    //3. Get Beam width and Covariance Mixing
    //simgas=[sigmaX,sigmaY,covXY]
    std::vector<double> sigmas = calculateSigmas(processedPixelData,
                                           processedPixelXPosition,
                                           processedPixelYPosition,
                                           muX,
                                           muY);

    std::vector<double> pixelResults = {muX+runningXCropCounter-1,
                                        muY+runningYCropCounter-1,
                                        sigmas[0]/sqrt(sumPixIntensity),
                                        sigmas[1]/sqrt(sumPixIntensity),
                                        sigmas[2]/sumPixIntensity};
    //9. Convert
    std::vector<double> mmReuslts = scaleImage(imagePix2mmRatio,pixelResults);          //scaleImage does the job


    std::vector<std::vector<double>> out = {pixelResults,mmReuslts};
    return out;
}
////////////////////////////////////////////////////////////////////////////////////////
void imageAnalysisClass::passInData(std::vector<double> &dummyPixelData,
                                    const int &centerXPixel,
                                    const int &centerYPixel,
                                    const int &xMaskRadius,
                                    const int &yMaskRadius,
                                    const int &numberOfPixels,
                                    const int &pixelWidth,
                                    const int &pixelHeight,
                                    const double &pix2mmRatio,
                                    const int step){


    //set up raw image data
    jump=step;
    imageXMaskRadius        =   xMaskRadius;
    imageYMaskRadius        =   yMaskRadius;
    imageSize               =   numberOfPixels;
    //imageWidth              =   pixelWidth;
    //imageHeight             =   pixelHeight;
    rawImageWidth              =   pixelWidth;
    rawImageHeight             =   pixelHeight;
    rawImageSize                = rawImageWidth*rawImageHeight;
    imagePix2mmRatio        =   pix2mmRatio;
    runningXCropCounter     =   0;
    runningYCropCounter     =   0;
    int c(0);
    for(auto i=pixelHeight; i>0; --i){
        for(auto j=1; j<=pixelWidth; ++j){
            rawXPosition.push_back(j);
            rawYPosition.push_back(i);
            ++c;
        }
    }
    imageCenterXPixel       =   centerXPixel;
    imageCenterYPixel       =   centerYPixel;
    makeMask();

    //set up for cropped data
    processedPixelData      =   dummyPixelData;
    imageWidth              =2*imageXMaskRadius;
    imageHeight             =2*imageYMaskRadius;

    int A=(int)imageWidth/jump;
    int B=(int)imageHeight/jump;
    imageWidth = A;
    imageHeight = B;

    imageSize               =imageWidth*imageHeight;
    c=0;
    for(auto i=imageHeight; i>0; --i){
        for(auto j=1; j<=imageWidth; ++j){
            processedPixelXPosition.push_back(j);
            processedPixelYPosition.push_back(i);
            ++c;
        }
    }

}
void imageAnalysisClass::makeMask(){
    std::vector<double> out(imageSize);
    for(auto i=0;i<imageSize;i++){
        //distance of pixel from centre of an oval mask
        double x = abs(rawXPosition[i]-imageCenterXPixel);
        double y = abs(rawYPosition[i]-imageCenterYPixel);
        double r = pow(x/(imageXMaskRadius),2)+pow(y/(imageYMaskRadius),2);
        if (r>1){out[i]=0.;}
        else{out[i]=1.;}
    }
    maskPixelData=out;
}
std::vector<double> imageAnalysisClass::scaleImage(const double &A,
                                                   std::vector<double> &image){
    std::vector<double> out(image.size());
    for(auto i=0;i!=image.size();++i){
        out[i]=A*image[i];
    }
    return out;
}
void imageAnalysisClass::cropSubtractAndMask(std::vector<double> &image,
                                             std::vector<double> &bkgrnd,
                                             const int &xMin, const int &xMax,
                                             const int &yMin, const int &yMax){
    int c(0);
    for(auto j=rawImageHeight-yMax;j<rawImageHeight-yMin;j+=jump)
    {
        for(auto i=xMin;i<xMax;i+=jump)
        {
            processedPixelData[c] = (image[i+j*rawImageWidth]-bkgrnd[i+j*rawImageWidth])*maskPixelData[i+j*rawImageWidth];
            processedPixelXPosition[c] = rawXPosition[i+j*rawImageWidth];
            processedPixelYPosition[c] = rawYPosition[i+j*rawImageWidth];
            ++c;
        }
    }

    //runningXCropCounter+=xMin;
    //runningYCropCounter+=yMin;
}
std::vector<double> imageAnalysisClass::calculateSigmas(const std::vector<double> &data,
                                                       const std::vector<double> &xData,
                                                       const std::vector<double> &yData,
                                                       const double &muX,
                                                       const double &muY){
    std::vector<double> out(3,0);
    for(auto i=0; i!=data.size();++i){
        out[0]+=data[i]*pow(xData[i]-muX,2);
        out[1]+=data[i]*pow(yData[i]-muY,2);
        out[2]+=data[i]*(xData[i]-muX)*(yData[i]-muY);
    }
    out[0]=sqrt(out[0]);
    out[1]=sqrt(out[1]);
    return out;
}
double imageAnalysisClass::dotProduct(std::vector<double> &v1, std::vector<double> &v2){
    double out(0);
    for(auto i=0;i!=v2.size();++i){
        out+=v1[i]*v2[i];
    }
    return out;
}

