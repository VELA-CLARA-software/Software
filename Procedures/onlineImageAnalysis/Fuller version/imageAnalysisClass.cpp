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
//This is you main function!
std::vector<std::vector<double>> imageAnalysisClass::anaylseImage(std::vector<double> &arrayData){
    processedPixelData = arrayData;
    //1.Crop image based of mask parameters
    //auto t1 = Clock::now();
    //auto t8 = t1;
    crop(imageCenterXPixel-imageXMaskRadius,imageCenterXPixel+imageXMaskRadius,
         imageCenterYPixel-imageYMaskRadius,imageCenterYPixel+imageYMaskRadius);
    //auto t2 = Clock::now();
    //std::cout << "crop: " << double(std::chrono::duration_cast<std::chrono::nanoseconds>(t2 - t1).count())/1000000000<< " seconds" << std::endl;

    //2. Subtract background image
    //t1 = Clock::now();
    processedPixelData  =   subtractImages(processedPixelData,imageBkgrndPixelData);
    //t2 = Clock::now();
    //std::cout << "subtractImages: "<< double(std::chrono::duration_cast<std::chrono::nanoseconds>(t2 - t1).count())/1000000000<< " seconds" << std::endl;

    //3. Apply Mask
    //t1 = Clock::now();
    processedPixelData  =   overlayImages(processedPixelData,maskPixelData);
    //t2 = Clock::now();
    //std::cout << "overlayImages: "<< double(std::chrono::duration_cast<std::chrono::nanoseconds>(t2 - t1).count())/1000000000<< " seconds" << std::endl;

    //4.Update Projections
    //t1 = Clock::now();
    updateProjections();
    //t2 = Clock::now();
    //std::cout << "updateProjections: "<< double(std::chrono::duration_cast<std::chrono::nanoseconds>(t2 - t1).count())/1000000000<< " seconds" << std::endl;

    //5. nPointScaling
    //t1 = Clock::now();
    processedPixelData  =   nPointScaling();
    //t2 = Clock::now();
    //std::cout << "nPointScaling: "<< double(std::chrono::duration_cast<std::chrono::nanoseconds>(t2 - t1).count())/1000000000<< " seconds" << std::endl;

    //6.Update Projections
    //t1 = Clock::now();
    updateProjections();
    //t2 = Clock::now();
    //std::cout << "updateProjections: "<< double(std::chrono::duration_cast<std::chrono::nanoseconds>(t2 - t1).count())/1000000000<< " seconds" << std::endl;

    //7. Get Centroid Positions
    //t1 = Clock::now();
    double sumPixIntensity=0;
    for(auto i=0;i!=imageSize;++i){
        sumPixIntensity+=processedPixelData[i];
    }
    double muX          =   dotProduct(processedPixelData,
                                       processedPixelXPosition)/sumPixIntensity;
    double muY          =   dotProduct(processedPixelData,
                                       processedPixelYPosition)/sumPixIntensity;
    //t2 = Clock::now();
    //std::cout << "Centroid: "<< double(std::chrono::duration_cast<std::chrono::nanoseconds>(t2 - t1).count())/1000000000<< " seconds" << std::endl;

    //8. Get Beam width and Covariance Mixing
    //t1 = Clock::now();
    double sigmaX       =   calculateSigma(processedPixelData,
                                           processedPixelXPosition,
                                           muX)/sqrt(sumPixIntensity);
    double sigmaY       =   calculateSigma(processedPixelData,
                                           processedPixelYPosition,
                                           muY)/sqrt(sumPixIntensity);
    double covXY        =   calculateSigma(processedPixelData,
                                           processedPixelXPosition,
                                           processedPixelYPosition,
                                           muX,
                                           muY)/sqrt(sumPixIntensity);

    std::vector<double> pixelResults = {muX+runningXCropCounter,
                                        muY+runningYCropCounter,
                                        sigmaX,
                                        sigmaY,
                                        covXY};
    //t2 = Clock::now();
    //std::cout << "Sigma: "<< double(std::chrono::duration_cast<std::chrono::nanoseconds>(t2 - t1).count())/1000000000<< " seconds" << std::endl;

    //9. Convert
    //t1 = Clock::now();
    std::vector<double> mmReuslts = scaleImage(imagePix2mmRatio,pixelResults);          //scaleImage does the job
    //t2 = Clock::now();
    //std::cout << "Convert: " << double(std::chrono::duration_cast<std::chrono::nanoseconds>(t2 - t1).count())/1000000000<< " seconds" << std::endl;


    //auto t9=t2;
    //std::cout << "Overall: " << double(std::chrono::duration_cast<std::chrono::nanoseconds>(t9 - t8).count())/1000000000<< " seconds" << std::endl;

    std::vector<std::vector<double>> out = {pixelResults,mmReuslts};
    return out;
}
//Pass Data to Class
void                imageAnalysisClass::passInData(std::vector<double> &rawPixelData,
                                                   std::vector<double> &bkgrndPixelData,
                                                   const int &centerXPixel,
                                                   const int &centerYPixel,
                                                   const int &xMaskRadius,
                                                   const int &yMaskRadius,
                                                   const int &numberOfPixels,
                                                   const int &pixelWidth,
                                                   const int &pixelHeight,
                                                   const double &pix2mmRatio){
    processedPixelData       =   rawPixelData;
    imageBkgrndPixelData    =   bkgrndPixelData;
    imageCenterXPixel       =   centerXPixel;
    imageCenterYPixel       =   centerYPixel;
    imageXMaskRadius        =   xMaskRadius;
    imageYMaskRadius        =   yMaskRadius;
    imageSize               =   numberOfPixels;
    imageWidth              =   pixelWidth;
    imageHeight             =   pixelHeight;
    imagePix2mmRatio        =   pix2mmRatio;
    runningXCropCounter     =   0;
    runningYCropCounter     =   0;
    int c(0);
    for(auto i=imageHeight; i>0; --i){
        for(auto j=1; j<=imageWidth; ++j){
            processedPixelXPosition.push_back(j);
            processedPixelYPosition.push_back(i);
            c++;
        }
    }
    makeMask();
    updateProjections();
}
void                imageAnalysisClass::updateProjections(){
    xProjection     =   makeProjection(processedPixelData,imageWidth,
                                       imageHeight,imageWidth,false);
    yProjection     =   makeProjection(processedPixelData,imageHeight,
                                       imageWidth,imageWidth,true);
    xMaskProjection =   makeProjection(maskPixelData,imageWidth,
                                       imageHeight,imageWidth,false);
    yMaskProjection =   makeProjection(maskPixelData,imageHeight,
                                       imageWidth,imageWidth,true);
    std::reverse(yProjection.begin(),yProjection.end());
    std::reverse(yMaskProjection.begin(),yMaskProjection.end());
}
void                imageAnalysisClass::makeMask(){
    std::vector<double> out(imageSize);
    for(auto i=0;i<imageSize;i++){
        //distance of pixel from centre of an oval mask
        double x = abs(processedPixelXPosition[i]-imageCenterXPixel);
        double y = abs(processedPixelYPosition[i]-imageCenterYPixel);
        double r = pow(x/(imageXMaskRadius),2)+pow(y/(imageYMaskRadius),2);
        if (r>1){out[i]=0.;}
        else{out[i]=1.;}
    }
    maskPixelData=out;
}
std::vector<double> imageAnalysisClass::subtractImages(std::vector<double> &image1,
                                                       std::vector<double> &image2){
    std::vector<double> out(image1.size());
    for(auto i=0;i!=image1.size();++i){
        out[i]=image1[i]-image2[i];
    }
    return out;
}
std::vector<double> imageAnalysisClass::overlayImages(std::vector<double> &image1,
                                                      std::vector<double> &image2){
    std::vector<double> out(image1.size());
    for(auto i=0; i!=out.size();++i){
        out[i]=image1[i]*image2[i];
    }
    return out;
}
std::vector<double> imageAnalysisClass::scaleImage(const double &A,
                                                   std::vector<double> &image){
    std::vector<double> out(image.size());
    for(auto i=0;i!=image.size();++i){
        out[i]=A*image[i];
    }
    return out;
}
void                imageAnalysisClass::crop(const int &xMin, const int &xMax,
                                             const int &yMin, const int &yMax){
    if(imageHeight>yMax && imageWidth>xMax){
        double mark = -1;
        for(auto i=0;i<imageSize;++i){
            if(processedPixelXPosition[i]<xMin||processedPixelXPosition[i]>xMax||
               processedPixelYPosition[i]<yMin||processedPixelYPosition[i]>yMax){
                processedPixelData[i] = mark;
                maskPixelData[i] = mark;
                processedPixelXPosition[i] = mark;
                processedPixelYPosition[i] = mark;
                imageBkgrndPixelData[i] = mark;
            }
        }
        //remove highlighted data
        processedPixelData.erase(     std::remove(begin(processedPixelData),
                                                        end(processedPixelData),
                                                        mark),
                                                  end(processedPixelData));
        maskPixelData.erase(          std::remove(begin(maskPixelData),
                                                        end(maskPixelData),
                                                        mark),
                                                  end(maskPixelData));
        imageBkgrndPixelData.erase(   std::remove(begin(imageBkgrndPixelData),
                                                        end(imageBkgrndPixelData),
                                                        mark),
                                                  end(imageBkgrndPixelData));
        processedPixelXPosition.erase(std::remove(begin(processedPixelXPosition),
                                                        end(processedPixelXPosition),
                                                        mark),
                                                  end(processedPixelXPosition));
        processedPixelYPosition.erase(std::remove(begin(processedPixelYPosition),
                                                        end(processedPixelYPosition),
                                                        mark),
                                                  end(processedPixelYPosition));


        //Adjust size variable accordingly
        imageWidth=xMax-xMin+1;
        imageHeight=yMax-yMin+1;
        imageSize=processedPixelData.size();

        //Reset xy coordinates () so they start at 00
        for(auto j=0;j<imageSize;j++){
            processedPixelXPosition[j]-=xMin;
            processedPixelYPosition[j]-=yMin;
        }
        //take note of cutting
        runningXCropCounter+=xMin;
        runningYCropCounter+=yMin;

    }
}
std::vector<double> imageAnalysisClass::makeProjection(const std::vector<double> &v,
                                                       const int &lengthOfFirstSum,
                                                       const int &lengthOfSecondSum,
                                                       const int &width,
                                                       const bool &revIndices){
    std::vector<double> out;
    for(auto i=0; i<lengthOfFirstSum;i++){
        double dummy=0;
        for(auto j=0; j<lengthOfSecondSum;j++){
            if (!revIndices){ dummy+=v[i+(j*width)];}
            else {dummy+=v[j+(i*width)];}
        }
        out.push_back(dummy);
    }
    return out;
}
std::vector<double> imageAnalysisClass::nPointScaling(){

    std::vector<double> out(imageSize);

    // make vector conataining the first and last 10 point of x and y projections
    std::vector<double> xTopTail(xProjection.begin(),xProjection.begin()+10);
    double averageStartX = average(xTopTail);
    std::vector<double> yTopTail(yProjection.begin(),yProjection.begin()+10);
    double averageStartY = average(yTopTail);
    std::vector<double> endX(xProjection.end()-10,xProjection.end());
    double averageEndX = average(endX);
    std::vector<double> endY(yProjection.end()-10,yProjection.end());
    double averageEndY = average(endY);

    //add tail to topTail vectors
    xTopTail.insert(xTopTail.end(),endX.begin(),endX.end());
    yTopTail.insert(yTopTail.end(),endY.begin(),endY.end());
    //deteremine which lambda to use (x projection or y projection)
    //if top and tail of x proj. have sore similar mean intesities

    std::vector<double> topTailMask;
    std::vector<double> topTail;
    double Average;
    if(abs(averageStartX-averageEndX)<abs(averageStartY-averageEndY)){
        topTail=xTopTail;
        Average = average(xTopTail);
        topTailMask.insert(topTailMask.end(),
                           xMaskProjection.begin(),
                           xMaskProjection.begin()+10);
        topTailMask.insert(topTailMask.end(),
                           xMaskProjection.end()-10,
                           xMaskProjection.end());
    }
    else{
        topTail=yTopTail;
        Average = average(yTopTail);
        topTailMask.insert(topTailMask.end(),
                           yMaskProjection.begin(),
                           yMaskProjection.begin()+10);
        topTailMask.insert(topTailMask.end(),
                           yMaskProjection.end()-10,
                           yMaskProjection.end());
    }

    double scalingFactor[]={-100,100};
    double scaledMeanIntensity[]={0,0};
    //find Lambda in x axis where average intesity is zero
    scaledMeanIntensity[0]=average(subtractImages(topTail,
                                                  scaleImage(scalingFactor[0],
                                                             topTailMask)));
    scaledMeanIntensity[1]=average(subtractImages(topTail,
                                                  scaleImage(scalingFactor[1],
                                                             topTailMask)));
    //gradient of line
    double dy = scaledMeanIntensity[1]-scaledMeanIntensity[0];
    double dx = scalingFactor[1]-scalingFactor[0];
    double m = dy/dx;
    //L0: intersect where average intensity is zero
    double lambda = -Average/m;
    out=subtractImages(processedPixelData,scaleImage(lambda,maskPixelData));
    return out;
}
double              imageAnalysisClass::calculateSigma(const std::vector<double> &data,
                                                       const std::vector<double> &pos,
                                                       const double &mu){
    double out=0;
    for(auto i=0; i!=data.size();++i){
        out+=data[i]*pow(pos[i]-mu,2);
    }
    return sqrt(out);
}
double              imageAnalysisClass::calculateSigma(const std::vector<double> &data, //Overidden
                                                       const std::vector<double> &xData,
                                                       const std::vector<double> &yData,
                                                       const double &muX,
                                                       const double &muY){
    double out=0;
    for(auto i=0; i!=data.size();++i){
        out+=data[i]*(xData[i]-muX)*(yData[i]-muY);
    }
    return sqrt(out);
}
double              imageAnalysisClass::average(std::vector<double> &v){
    double sum(0);
    for(auto i=0;i!=v.size();++i){
        sum+=v[i];
    }
    return sum/(v.size());
}
double              imageAnalysisClass::dotProduct(std::vector<double> &v1,
                                                   std::vector<double> &v2){
    double out(0);
    for(auto i=0;i!=v1.size();++i){
        out+=v1[i]*v2[i];
    }
    return out;
}

