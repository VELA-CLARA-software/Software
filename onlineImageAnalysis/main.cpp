
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

int main (int argc, const char * argv[]) {
    // insert code here...

    //Parameters of image

    int     pixelWidth = 2560;
    int     pixelHeight = 2160/2;
    int     centerXPixel(2560/2);
    int     centerYPixel(pixelHeight/2);
    int     xMaskRadius(pixelWidth/2-10);
    int     yMaskRadius(pixelHeight/2-10);
    int     numberOfPixels(pixelWidth*pixelHeight);
    double pix2mmRatio(20.2);

    std::vector<double>     rawPixelData(numberOfPixels,0.0);
    std::vector<double>  bkgrndPixelData(numberOfPixels,0.0);
    //Fill array Data
    double  muX      = 1200;
    double  sigmaX   = 80;
    double  muY      = 500;
    double  sigmaY   = 20;
    int c(0);


    std::vector<double>croppedDummy(((2*xMaskRadius)*(2*yMaskRadius)),0);

    for(auto i=pixelHeight-1; i>=0; --i){
        for(auto j=0; j!=pixelWidth; ++j){
            rawPixelData[c]=exp(-0.5*(pow((j-muX)/sigmaX,2)+pow((i-muY)/sigmaY,2)));
            bkgrndPixelData[c]=0;
            c++;
        }
    }

    imageAnalysisClass test = imageAnalysisClass();
    auto t0 = Clock::now();
    test.passInData(croppedDummy,
                    centerXPixel,
                    centerYPixel,
                    xMaskRadius,
                    yMaskRadius,
                    numberOfPixels,
                    pixelWidth,
                    pixelHeight,
                    pix2mmRatio);
    std::vector<std::vector<double>> results={{0,0,0,0,0},{0,0,0,0,0}};
    auto t1 = Clock::now();

    for(auto i =0;i!=500;++i) {
        results=test.anaylseImage(rawPixelData,bkgrndPixelData);
    }
    auto t2 = Clock::now();
    std::cout << "Time to Anaylse Image:        "
              << double(std::chrono::duration_cast<std::chrono::nanoseconds>(t2 - t1).count())/500000000000
              << " seconds" << std::endl;
    std::cout <<"RESULT"<<std::endl;
    std::cout << results[0][0]<<std::endl;
    std::cout << results[0][1]<<std::endl;
    std::cout << results[0][2]<<std::endl;
    std::cout << results[0][3]<<std::endl;
    std::cout << results[0][4]<<std::endl;
    return 0;
}
