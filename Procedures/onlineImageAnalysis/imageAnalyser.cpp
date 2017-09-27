#include <fstream>
#include <iterator>
#include <vector>
#include <stdint.h>
#include<iostream>
#include<sstream>
#include <algorithm>
#include <cmath>
#include <chrono>

#include"ImageStructs.h"
#include"imageAnalyser.h"

///--------------------------------IMAGE ANAYLSER FUNCTIONS------------------------------------///
//CONSTRUCTOR
imageAnalyser::imageAnalyser( const bool show_messages, const  bool show_debug_messages )
: baseObject( &show_messages, &show_debug_messages ), IO( &show_messages, &show_debug_messages ),fit( &show_messages, &show_debug_messages ), edit( &show_messages, &show_debug_messages )
{}
//DESTRUCTOR
imageAnalyser::~imageAnalyser(){}


//read data from file and load into image analyser class in 'imageData'
void imageAnalyser::loadImageFromFile(const std::string& file){
    IO.readFile(file);
    //imageData=IO.getOriginalImageData();

}
//LOAD BACKGROUND IMAGE
void imageAnalyser::loadBackgroundImageFromFile(const std::string& file){
    IO.readBackgroundFile(file);
    imageData.background.clear();
    imageData.background=IO.getOriginalBackgroundImage();
}
//WRITE DATA TO FILE
void imageAnalyser::writeDataToFiles(const std::string& file){
    IO.writeToFile(imageData, file);
    std::cout<<"Outputted to "+file+".txt"<<std::endl;
}
//BEAM ANALYSIS
std::vector<double> imageAnalyser::getBeamParameters(){

    imageData=IO.getOriginalImageData();

    //REMOVE BACKGROUND DATA
    if (bkgrnd==true){
        auto start = std::chrono::steady_clock::now();
        imageData.pixIntensity=edit.subtractBackground(imageData);
        auto finish = std::chrono::steady_clock::now();
        auto diff  = finish - start;
        std::cout<< "Finished subtracting background in "<< (double)std::chrono::duration_cast<std::chrono::nanoseconds>(diff).count()/1000000000<< std::endl;
    }
    else{std::cout<< "No background was removed"<< std::endl;}


    //MAKE THE MASK
    auto start = std::chrono::steady_clock::now();
    if(useMaskFromES==true){
        imageData.mask = IO.makeMask(imageData,imageData.dataSize,maskXES,maskYES,maskRXES,maskRYES);
    }
    else{
        imageData.mask = IO.makeMask(imageData,imageData.dataSize,imageData.x0,imageData.y0,imageData.xRad,imageData.yRad);
    }
    auto finish = std::chrono::steady_clock::now();
    auto diff  = finish - start;
    std::cout<<"Finished making mask in "<< (double)std::chrono::duration_cast<std::chrono::nanoseconds>(diff).count()/1000000000<< std::endl;

    //APPLY THE MASK
    start = std::chrono::steady_clock::now();
    imageData.pixIntensity = edit.applyMask(imageData);
    finish = std::chrono::steady_clock::now();
    diff  = finish - start;
    std::cout<<"finished applying mask in "<< (double)std::chrono::duration_cast<std::chrono::nanoseconds>(diff).count()/1000000000<< std::endl;

    //CROP IMAGE
    start = std::chrono::steady_clock::now();
    if(manualCrop==true){
        imageData = edit.crop(imageData,manualCropX,manualCropY,manualCropW+manualCropX,manualCropH+manualCropY);
    }
    else{
        imageData = edit.crop(imageData,(imageData.x0-imageData.xRad),(imageData.y0-imageData.yRad),(imageData.x0+imageData.xRad),(imageData.y0+imageData.yRad));
    }
    finish = std::chrono::steady_clock::now();
    diff  = finish - start;
    std::cout<<"Finished cropping in "<<(double)std::chrono::duration_cast<std::chrono::nanoseconds>(diff).count()/1000000000<<std::endl;

    //SET PROJECTIONS
    start = std::chrono::steady_clock::now();
    imageData.xProjection = IO.getProjection(imageData,x);
    imageData.yProjection = IO.getProjection(imageData,y);
    imageData.maskXProjection = IO.getProjection(imageData,maskX);
    imageData.maskYProjection = IO.getProjection(imageData,maskY);
    finish = std::chrono::steady_clock::now();
    diff  = finish - start;
    std::cout<<"Finished getting all projections in "<< (double)std::chrono::duration_cast<std::chrono::nanoseconds>(diff).count()/1000000000<<std::endl;

    // IMPROVE IMAGE USINF N POINT SCALING METHOD
    start = std::chrono::steady_clock::now();
    imageData.pixIntensity = edit.nPointScaling(imageData);
    //have to update projections
    imageData.xProjection = IO.getProjection(imageData,x);
    imageData.yProjection = IO.getProjection(imageData,y);
    finish = std::chrono::steady_clock::now();
    diff  = finish - start;
    std::cout<<"Finished N point scaling in "<< (double)std::chrono::duration_cast<std::chrono::nanoseconds>(diff).count()/1000000000<< std::endl;

    //GENERATE ESTIMATES FOR 1D PROJECTIONS
    start = std::chrono::steady_clock::now();
    std::vector<double>Estim;
    if(useFilterFromES==true){
        Estim = get1DParmaetersForXAndY(filterES);
    }
    else{
        Estim = getBest1DParmaetersForXAndY();
    }
    std::vector<double> x_estimation = {Estim[0],Estim[1],Estim[2],Estim[3]};
    std::vector<double> y_estimation = {Estim[4],Estim[5],Estim[6],Estim[7]};

    //USE ESTIMATES TO RUN GAUSSIAN FITS TO THE PROJECTIONS
    std::vector<double> fitY = fit.fit1DGaussianToProjection(imageData, y, y_estimation);
    std::vector<double> fitX = fit.fit1DGaussianToProjection(imageData, x, x_estimation);
    finish = std::chrono::steady_clock::now();
    diff  = finish - start;
    std::cout<<"Finished first 1D fit in "<< (double)std::chrono::duration_cast<std::chrono::nanoseconds>(diff).count()/1000000000<< std::endl;

    //FIND R^2 VALUES OF THE FITS (IF >0.4 USE PARAMETERS AS CUTTING VALUES)
    double RRx = fit.rSquaredOf1DProjection(imageData, fitX,x);
    double RRy = fit.rSquaredOf1DProjection(imageData, fitY,y);
    std::cout<<"R squared values of x and y fits respectively:"<< std::endl;
    std::cout<<RRx<<" "<<RRy<<std::endl;
    double cMuX,cMuY,cSigmaX,cSigmaY;
    // if fits are not good used FWHM estimates
    if(useRRThresholdFromES==true){
        if(RRx<RRThresholdES){cMuX=Estim[2];cSigmaX=Estim[3];}
        else{cMuX=fitX[2];cSigmaX=fitX[3];}

        if(RRy<RRThresholdES){cMuY=Estim[6];cSigmaY=Estim[7];}
        else{cMuY=fitY[2];cSigmaY=fitY[3];}
    }
    else{//default is 0.4
        if(RRx<0.4){cMuX=Estim[2];cSigmaX=Estim[3];}
        else{cMuX=fitX[2];cSigmaX=fitX[3];}

        if(RRy<0.4){cMuY=Estim[6];cSigmaY=Estim[7];}
        else{cMuY=fitY[2];cSigmaY=fitY[3];}
    }


    //CROP USING MU AND SIGMA
    int xC,yC,wC,hC;
    if(useSigmaCutFromES==true){
        xC = (int)round(cMuX-(sigmaCutES*cSigmaX));
        yC = (int)round(cMuY-(sigmaCutES*cSigmaY));
        wC = (int)round(cMuX+(sigmaCutES*cSigmaX));
        hC = (int)round(cMuY+(sigmaCutES*cSigmaY));
    }
    else{//default is three sigma
        xC = (int)round(cMuX-(3*cSigmaX));
        yC = (int)round(cMuY-(3*cSigmaY));
        wC = (int)round(cMuX+(3*cSigmaX));
        hC = (int)round(cMuY+(3*cSigmaY));
    }

    //CROP IMAGE DOWN FURTHER
    if(manualCrop==false){
        start = std::chrono::steady_clock::now();
        imageData = edit.crop(imageData,xC,yC,wC,hC);
        finish = std::chrono::steady_clock::now();
        diff  = finish - start;
        std::cout<<"Finished crop from fit estimates in "<< (double)std::chrono::duration_cast<std::chrono::nanoseconds>(diff).count()/1000000000<< std::endl;
    }

    //UPDATE PROJECTIONS
    imageData.xProjection = IO.getProjection(imageData,x);
    imageData.yProjection = IO.getProjection(imageData,y);

    //RECALCULATE ESTIMATES AND THEN FITS
    std::vector<double> Estim_ReCalc;
    if(useFilterFromES==true){
        Estim_ReCalc = get1DParmaetersForXAndY(filterES);
    }
    else{

        Estim_ReCalc = getBest1DParmaetersForXAndY();
    }
    std::vector<double> x_estimation_ReCalc = {Estim_ReCalc[0],Estim_ReCalc[1],Estim_ReCalc[2],Estim_ReCalc[3]};
    std::vector<double> y_estimation_ReCalc = {Estim_ReCalc[4],Estim_ReCalc[5],Estim_ReCalc[6],Estim_ReCalc[7]};


    //OVERIDING OLD FIT PARAMETERS
    std::vector<double> refitY = fit.fit1DGaussianToProjection(imageData, y, y_estimation_ReCalc);
    std::vector<double> refitX = fit.fit1DGaussianToProjection(imageData, x, x_estimation_ReCalc);
    std::cout<<"Finished re-calc of estimates and 1D re-fits"<< std::endl;


    //USING 1D FIT PARAMATERS FIT BVN TO IMAGE
    start = std::chrono::steady_clock::now();
    ///Curently not using this so just outputs 1s
    std::vector<double> fitImageBVN = {1,1,1,1,1,1,1};
    //std::vector<double> fitImageBVN = fit.fitBVN(imageData,refitX,refitY);
    finish = std::chrono::steady_clock::now();
    diff  = finish - start;
    std::cout<<"Finished BVN fit in "<< (double)std::chrono::duration_cast<std::chrono::nanoseconds>(diff).count()/1000000000<< std::endl;

    //CORRECT CENTROID POSITION (from the cropping)
    std::vector<double> corrections = edit.correctBeamPosition(fitImageBVN[2],fitImageBVN[3]);
    fitImageBVN[2] = corrections[0];
    fitImageBVN[3] = corrections[1];
    std::cout<<"Finished BVN corrections"<< std::endl;


    //DIRECTY FIT TO DATA WITHOUT ESTIMATES
    start = std::chrono::steady_clock::now();
    std::vector<double> fitImageCov= {1,1,1,1,1};
    if(useDirectCutLevelFromES==true){ fitImageCov = fit.covarianceValues(imageData,DirectCutLevelES);}
    else{ fitImageCov = fit.covarianceValues(imageData,0);}
    finish = std::chrono::steady_clock::now();
    diff  = finish - start;
    std::cout<<"Finished direct calc of parameters in "<< (double)std::chrono::duration_cast<std::chrono::nanoseconds>(diff).count()/1000000000<< std::endl;

    std::vector<double> correctionsCov = edit.correctBeamPosition(fitImageCov[0],fitImageCov[1]);
    fitImageCov[0] = correctionsCov[0];
    fitImageCov[1] = correctionsCov[1];
    std::cout<<"Finished corrections"<< std::endl;
    //clear up loose ends
    savedCroppedX = edit.croppedX;
    savedCroppedY = edit.croppedY;
    edit.croppedX=0;
    edit.croppedY=0;
    //imageData.clear();



    //OUTPUT IMAGE PARAMETERS in one string (BVN FIT,COVARIANCE FIT, 1D ESTIMATES FOR X, 1D ESTIMATES FOR Y)
    std::vector<double> output; //

    output.insert(output.end(),fitImageBVN.begin()+2,fitImageBVN.end());
    output.insert(output.end(),fitImageCov.begin(),fitImageCov.end());
    output.insert(output.end(),refitX.begin()+2,refitX.end());
    output.insert(output.end(),refitY.begin()+2,refitY.end());

    return output;

}
//GET THE BEST 1D PARAMETERS BY APPLYING DIFFERENT FILTERS (RETURNS FWHM ESTIMATES)
std::vector<double> imageAnalyser::getBest1DParmaetersForXAndY(){

    std::vector<double> wx(4,0),wy(4,0);
    std::vector<std::vector<double>> FWHMx(4,{0,0,0,0}),FWHMy(4,{0,0,0,0});

    std::vector<double> noFiltX = edit.applyFilter(imageData,1,x);
    std::vector<double> momx =  fit.get1DEstimates(noFiltX,moments);
    FWHMx[0]= fit.get1DEstimates(noFiltX,FWHM);
    wx[0] =  fit.compare1DEstimates(momx[2],momx[3],FWHMx[0][2],FWHMx[0][3]);


    std::vector<double> filt5x =  edit.applyFilter(imageData,5,x);
    std::vector<double> mom5x =  fit.get1DEstimates(filt5x,moments);
    FWHMx[1] =  fit.get1DEstimates(filt5x,FWHM);
    wx[1]=  fit.compare1DEstimates(mom5x[2],mom5x[3],FWHMx[1][2],FWHMx[1][3]);

    std::vector<double> filt10x = edit.applyFilter(imageData,10,x);
    std::vector<double> mom10x =  fit.get1DEstimates(filt10x,moments);
    FWHMx[2] =  fit.get1DEstimates(filt10x,FWHM);
    wx[2] =  fit.compare1DEstimates(mom10x[2],mom10x[3],FWHMx[2][2],FWHMx[2][3]);

    std::vector<double> filt20x = edit.applyFilter(imageData,20,x);
    std::vector<double> mom20x =  fit.get1DEstimates(filt20x,moments);
    FWHMx[3] =  fit.get1DEstimates(filt20x,FWHM);
    wx[3] =  fit.compare1DEstimates(mom20x[2],mom20x[3],FWHMx[3][2],FWHMx[3][3]);


    //Apply different filters and decid which is best FOR Y
    std::vector<double> noFiltY = edit.applyFilter(imageData,1,y);
    std::vector<double> momy =  fit.get1DEstimates(noFiltY,moments);
    FWHMy[0] =  fit.get1DEstimates(noFiltY,FWHM);
    wy[0] =  fit.compare1DEstimates(momy[2],momy[3],FWHMy[0][2],FWHMy[0][3]);

    std::vector<double> filt5y = edit.applyFilter(imageData,5,y);
    std::vector<double> mom5y =  fit.get1DEstimates(filt5y,moments);
    FWHMy[1] =  fit.get1DEstimates(filt5y,FWHM);
    wy[1] =  fit.compare1DEstimates(mom5y[2],mom5y[3],FWHMy[1][2],FWHMy[1][3]);

    std::vector<double> filt10y = edit.applyFilter(imageData,10,y);
    std::vector<double> mom10y =  fit.get1DEstimates(filt10y,moments);
    FWHMy[2] =  fit.get1DEstimates(filt10y,FWHM);
    wy[2] =  fit.compare1DEstimates(mom10y[2],mom10y[3],FWHMy[2][2],FWHMy[2][3]);

    std::vector<double> filt20y = edit.applyFilter(imageData,20,y);
    std::vector<double> mom20y =  fit.get1DEstimates(filt20y,moments);
    FWHMy[3] =  fit.get1DEstimates(filt20y,FWHM);
    wy[3] =  fit.compare1DEstimates(mom20y[2],mom20y[3],FWHMy[3][2],FWHMy[3][3]);

    //Find min w for x and y
    std::vector<double>::iterator wMinX = std::min_element(wx.begin(),wx.end());
    std::vector<double>::iterator wMinY = std::min_element(wy.begin(),wy.end());


    //Get the estimates that correspond to those minimum w values and output the corresponding estimates
    std::vector<double> output; //(xA,xB,xMu,xSigma,yA,yB,yMu,ySigma)

    output.insert(output.end(),FWHMx[std::distance(wx.begin(),wMinX)].begin(),FWHMx[std::distance(wx.begin(),wMinX)].end());

    output.insert(output.end(),FWHMy[std::distance(wy.begin(),wMinY)].begin(),FWHMy[std::distance(wy.begin(),wMinY)].end());

    return output;

}
//GET THE ESTIMATES USING A SPECIFIC FILTER
std::vector<double> imageAnalyser::get1DParmaetersForXAndY(const int& filter){

    std::vector<double> FWHMx={0,0,0,0},FWHMy={0,0,0,0};

    std::vector<double> FiltX = edit.applyFilter(imageData,filter,x);

    FWHMx= fit.get1DEstimates(FiltX,FWHM);

    std::vector<double> FiltY = edit.applyFilter(imageData,5,y);

    FWHMy =  fit.get1DEstimates(FiltY,FWHM);

    //Get the estimates that correspond to those minimum w values and output the corresponding estimates
    std::vector<double> output; //(xA,xB,xMu,xSigma,yA,yB,yMu,ySigma)
    output.insert(output.end(),FWHMx.begin(),FWHMx.end());
    output.insert(output.end(),FWHMy.begin(),FWHMy.end());

    return output;

}

//GET FUNCTIONS
std::vector<double> imageAnalyser::getPixIntensity(){
    return imageData.pixIntensity;
}
std::vector<double> imageAnalyser::getBackgroundImage(){
    std::cout<<imageData.background.size()<<std::endl;
    return IO.getOriginalBackgroundImage();
}
std::vector<double> imageAnalyser::getOriginalPixIntensity(){
    return IO.getOriginalPixIntensity();
}
std::vector<double> imageAnalyser::getXProjection(){
    return imageData.xProjection;
}
std::vector<double> imageAnalyser::getOriginalXProjection(){
    return IO.getOriginalXProjection();
}
std::vector<double> imageAnalyser::getYProjection(){
    return imageData.yProjection;
}
std::vector<double> imageAnalyser::getOriginalYProjection(){
     return IO.getOriginalYProjection();
}
std::vector<double> imageAnalyser::getX(){
        return imageData.X;
}
std::vector<double> imageAnalyser::getY(){
     return imageData.Y;
}
std::vector<double> imageAnalyser::getOriginalX(){
     return IO.getOriginalX();
}
std::vector<double> imageAnalyser::getOriginalY(){
     return IO.getOriginalY();
}
int imageAnalyser::getImageHeight(){
    return imageData.imageHeight;
}
int imageAnalyser::getImageWidth(){
    return imageData.imageWidth;
}
int imageAnalyser::getImageDataSize(){
    return imageData.dataSize;
}
int imageAnalyser::getCroppedX(){
    return savedCroppedX;
}
int imageAnalyser::getCroppedY(){
    return savedCroppedY;
}
void imageAnalyser::crop(const int& x,const int& y,const int& w,const int& h){
    //CROP IMAGE
    imageData = edit.crop(imageData,x,y,w,h);
    std::cout<<"Finished cropping"<<std::endl;

}

//Set bools
void imageAnalyser::useBackground(const bool& tf){
    bkgrnd=tf;
}
void imageAnalyser::useManualCrop(const bool& tf){
    manualCrop=tf;
}
void imageAnalyser::useESMask(const bool& tf){
    useMaskFromES=tf;
}
void imageAnalyser::useESPixToMm(const bool& tf){
    usePixToMmFromES=tf;
}
void imageAnalyser::useESRRThreshold(const bool& tf){
    useRRThresholdFromES=tf;
}
void imageAnalyser::useESSigmaCut(const bool& tf){
    useSigmaCutFromES=tf;
}
void imageAnalyser::useESFilter(const bool& tf){
    useFilterFromES=tf;
}
void imageAnalyser::useESDirectCut(const bool& tf){
    useDirectCutLevelFromES=tf;
}
// Functions to set ES data
void imageAnalyser::setManualCrop(const int& x,const int& y,const int& w,const int& h){
    manualCropX=x;
    manualCropY=y;
    manualCropW=w;
    manualCropH=h;
}
void imageAnalyser::setESMask(const int& x,const int& y,const int& rx,const int& ry){
    maskXES=x;
    maskYES=y;
    maskRXES=rx;
    maskRYES=ry;
}
void imageAnalyser::setESPixToMm(const double& ptm){
    pixToMmES=ptm;
}
void imageAnalyser::setESRRThreshold(const double& rrt){
    RRThresholdES=rrt;
}
void imageAnalyser::setESSigmaCut(const double& sc){
    sigmaCutES=sc;
}
void imageAnalyser::setESFilter(const int& f){
    filterES=f;
}
void imageAnalyser::setESDirectCut(const double& dc){
    DirectCutLevelES=dc;
}

double imageAnalyser::getPTMRatio(){
    return imageData.pixToMM;
}

