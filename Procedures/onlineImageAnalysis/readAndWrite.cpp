#include <fstream>
#include <iterator>
#include <vector>
#include <stdint.h>
#include<iostream>
#include<sstream>
//#include <algorithm>
#include <cmath>
/// For examples got to:
/// http://lodev.org/lodepng/
#include"lodepng.h"
#include"lodepng.cpp"
///
#include"readAndWrite.h"



///--------------------------------readAndWrite FUNCTIONS------------------------------------///
//CONSTRUCTOR
readAndWrite::readAndWrite( const bool* show_messages_ptr, const  bool * show_debug_messages_ptr )
: baseObject( show_messages_ptr, show_debug_messages_ptr ),configData( show_messages_ptr, show_debug_messages_ptr )
{}
//DESTRUCTOR
readAndWrite::~readAndWrite(){}
//READ FROM FILE
void readAndWrite::readFile(const std::string & imageName ){
    originalImageData.clear();
    std::string screenNumber;
    ///Reading file name to determine which YAG screen config data to use
    if (
        imageName.find("Virtual Cathode") != std::string::npos) {
        screenNumber = "VC";
    }
    else{
        std::size_t found = imageName.find_last_of( "YAG-" );
        screenNumber = imageName.substr( found + 1, 2 );

    }
    //Read config file and get relavent values
    bool dummy = configData.readYAGConfig(screenNumber);
    originalImageData=configData.getConfigData();
    std::string name = imageName;
    std::string::iterator last = name.end()-1;//last value is a space so the last character is the one before the end
    //Read in .raw or .png file identify using last character on image name
    if(*last=='w'){originalImageData.pixIntensity = readRAW(imageName);}
    else if(*last=='g'){originalImageData.pixIntensity = readPNG(imageName);}
    else{std::cout<<"Not valid file type"<<std::endl;}
    //set data size
    originalImageData.dataSize=originalImageData.pixIntensity.size();
    //set position of pixels
    for(auto i=originalImageData.imageHeight-1;i>=0;i--){
        for(auto j=0;j<originalImageData.imageWidth;j++){
            originalImageData.X.push_back((double)j);
            originalImageData.Y.push_back((double)i);
        }
    }
    //get projections
    originalImageData.xProjection = getProjection(originalImageData,x);
    originalImageData.yProjection = getProjection(originalImageData,y);


}
//READ BACKGROUND
void readAndWrite::readBackgroundFile(const std::string & imageName){
    originalImageData.background.clear();
    ///Similar method as reading in orignal image (above)
    std::string name = imageName;
    std::string::iterator last = name.end()-1;
    if(*last=='w'){
        originalImageData.background = readRAW(imageName);
    }
    else if(*last=='g'){
        originalImageData.background = readPNG(imageName);
    }
    else{std::cout<<"Not valid file type"<<std::endl;}

}
//READ PNG
std::vector<double> readAndWrite::readPNG(const std::string & imageName){
    std::cout<<"Importing .png file"<<std::endl;
    std::vector<unsigned char> buffer;
    std::vector<unsigned char> imageData;
    std::vector<double> out;
    unsigned w;
    unsigned h;
    unsigned error =lodepng::load_file(buffer, imageName.c_str()); //load the image file with given filename
    lodepng::State state;
    error = lodepng::decode(imageData, w,h,state,buffer);
    unsigned colortype = state.info_png.color.colortype;
    imageData.clear();
    if(colortype==6){
        std::cout<<"Importing RGBA 8-bit format..."<<std::endl;
        unsigned error = lodepng::decode(imageData, w,h,imageName.c_str(), LCT_RGBA, 8);///MAGIC NUMBER
    }
    else if (colortype==3){
        std::cout<<"Importing GREY 8-bit format..."<<std::endl;
        unsigned error = lodepng::decode(imageData, w,h,imageName.c_str(), LCT_GREY, 8);///MAGIC NUMBER
    }

    std::cout<<imageData.size()<<std::endl;
    if(colortype==6){
        int D = imageData.size();
        for(auto i=0;i<D;i+=4){
           // double dummy = (4095*(out[i]+out[i+1]+out[i+2]))/(3*255);
            out.push_back((4095*(imageData[i]+imageData[i+1]+imageData[i+2]))/(3*255));///MAGIC NUMBER (255 not 4095)
        }
    }
    else if(colortype==3){
        int D = imageData.size();
        for(auto i=0;i<D;i++){
            //double dummy = (4095*out[i])/255;
            out.push_back((4095*imageData[i])/255);
        }
    }

    return out;

}
//READ RAW
std::vector<double> readAndWrite::readRAW(const std::string & imageName){
    std::cout<<"Importing .raw file"<<std::endl;
    std::vector<double> out;
    std::ifstream file(imageName, std::ios::binary);
    char16_t pix;
    while (!file.eof()){
        file.read((char*)&pix, sizeof pix);
        out.push_back((double)pix);
    }
    file.clear();
    file.close();
    // !infile.eof() reads in last value twice therefore need to get rid of it!!!!!!
    out.pop_back();
    return out;
}
//RETURN BACKGROUND DATA
std::vector<double> readAndWrite::getOriginalBackgroundImage(){
    return originalImageData.background;
}
//WRITE TO FILE
void readAndWrite::writeToFile(const imageDataStruct& ID, const std::string & out){
    std::ofstream outfile(out+".txt");
    //output data in a nice way
    for(auto i=0; i<ID.dataSize; ++i){
        std::stringstream ss;
        ss << ID.X[i] << '\t'
           << ID.Y[i]  << '\t'
           << ID.pixIntensity[i];
        outfile << ss.str() << std::endl;
    }
    outfile.clear();
    outfile.close();

    std::ofstream projX("projections_x.txt");
    //output data in a nice way
    int xProjectionSize=ID.xProjection.size();
    for(auto i=0;i<xProjectionSize;++i){
        projX << ID.xProjection[i] << std::endl;
    }
    projX.clear();
    projX.close();

    std::ofstream projY("projections_y.txt");
    //output data in a nice way
     int yProjectionSize=ID.yProjection.size();
    for(auto i=0;i<yProjectionSize;++i){
        projY << ID.yProjection[i] << std::endl;
    }
    projY.clear();
    projY.close();
}
//MAKE MASK
std::vector<double> readAndWrite::makeMask(const imageDataStruct& ID, const int& dataSize, const int& x0, const int& y0, const int& rX, const int& rY){
    std::vector<double> out(dataSize);
    for(auto i=0;i<dataSize;i++){
        //distance of pixel from centre of oval mask
        double x = abs(ID.X[i]-x0);
        double y = abs(ID.Y[i]-y0);
        double r = pow(x/(rX),2)+pow(y/(rY),2);
        if (r>1){out[i]=0.;}
        else{out[i]=1.;}
    }
    return out;
}
//GET PROJECTIONS
std::vector<double> readAndWrite::getProjection(const imageDataStruct& ID, const projAxis &axis){
    ///This function is used to get projections and update them as analysis is ongoing
    std::vector<double> dummyProjection;
    switch(axis)
    {
        case x:
            {
                dummyProjection = makeProjection(ID.pixIntensity,ID.imageWidth,ID.imageHeight,ID.imageWidth,false);
                break;
            }
        case y:
            {
                dummyProjection = makeProjection(ID.pixIntensity,ID.imageHeight,ID.imageWidth,ID.imageWidth,true);
                //is read in reverese so have to change that
                std::reverse(dummyProjection.begin(),dummyProjection.end());
                break;
            }
        case maskX:
            {
                dummyProjection = makeProjection(ID.mask,ID.imageWidth,ID.imageHeight,ID.imageWidth,false);
                break;
            }
        case maskY:
            {
                dummyProjection = makeProjection(ID.mask,ID.imageHeight,ID.imageWidth,ID.imageWidth,true);
                //is read in reverese so have to change that
                std::reverse(dummyProjection.begin(),dummyProjection.end());
                break;
            }
    }
     return dummyProjection;
}

std::vector<double> readAndWrite::makeProjection(const std::vector<double> &v, const int &lengthOfFirstSum, const int &lengthOfSecondSum, const int &width, const bool &revIndices){
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
//GET ORIGINAL IMAGE DATA
imageDataStruct readAndWrite::getOriginalImageData(){
    return originalImageData;
}
//GET FUNCTIONS
///used to pass data up to image analyser class
std::vector<double> readAndWrite::getOriginalPixIntensity(){
    return originalImageData.pixIntensity;
}
std::vector<double> readAndWrite::getOriginalXProjection(){
    return originalImageData.xProjection;
}
std::vector<double> readAndWrite::getOriginalYProjection(){
     return originalImageData.yProjection;
}
std::vector<double> readAndWrite::getOriginalX(){
     return originalImageData.X;
}
std::vector<double> readAndWrite::getOriginalY(){
     return originalImageData.Y;
}














