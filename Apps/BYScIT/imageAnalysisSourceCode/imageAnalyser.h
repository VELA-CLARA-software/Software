#ifndef IMAGE_ANALYSER_H
#define IMAGE_ANALYSER_H


#include<string>
#include<vector>


#include"imagestructs.h"
#include"readAndWrite.h"
#include"editor.h"
#include"fitter.h"
#include "baseObject.h"



//FOR PYTHON DLL
#ifdef BUILD_DLL
#include <boost/python/detail/wrap_python.hpp>
#define BOOST_PYTHON_STATIC_LIB /// !!! This should come before  #include <boost/python.hpp>
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>
#include <boost/python/suite/indexing/map_indexing_suite.hpp>
#endif



///---------------------------CLASS TO ANALYSE IMAGE------------------------------///
///------------Holds data of image high level imageAnalysis functions-------------///
class imageAnalyser: public baseObject{
    public:
        //Constructor
        imageAnalyser( const bool show_messages = true, const  bool show_debug_messages = true);
        //Destructor
        ~imageAnalyser();

        //get access to loats of functions
        readAndWrite IO;
        editor edit;
        fitter fit;


        ///Functions
        //read data from file and load into image analyser class in 'imageData'
        void loadImageFromFile(const std::string& file);

        void loadBackgroundImageFromFile(const std::string& file);

        void writeDataToFiles(const std::string& file);

        void crop(const int& x,const int& y,const int& w,const int& h);

        std::vector<double> getBeamParameters();

        std::vector<double> getBest1DParmaetersForXAndY();
        //for use with a specific filter
        std::vector<double> get1DParmaetersForXAndY(const int& filter);

        ///Function to be sent up access data in python
        std::vector<double> getPixIntensity();
        std::vector<double> getBackgroundImage();
        std::vector<double> getOriginalPixIntensity();
        std::vector<double> getXProjection();
        std::vector<double> getOriginalXProjection();
        std::vector<double> getYProjection();
        std::vector<double> getOriginalYProjection();
        std::vector<double> getX();
        std::vector<double> getY();
        std::vector<double> getOriginalX();
        std::vector<double> getOriginalY();
        int getImageHeight();
        int getImageWidth();
        int getImageDataSize();
        int getCroppedX();
        int getCroppedY();

        void useBackground(const bool& tf);
        void useManualCrop(const bool& tf);
        void setManualCrop(const int& x,const int& y,const int& w,const int& h);
        void useESMask(const bool& tf);
        void setESMask(const int& x,const int& y,const int& rx,const int& ry);
        void useESPixToMm(const bool& tf);
        void setESPixToMm(const double& ptm);
        double getPTMRatio();
        void useESRRThreshold(const bool& tf);
        void setESRRThreshold(const double& rrt);
        void useESSigmaCut(const bool& tf);
        void setESSigmaCut(const double& sc);
        void useESFilter(const bool& tf);
        void setESFilter(const int& f);
        void useESDirectCut(const bool& tf);
        void setESDirectCut(const double& dc);


    protected:
        ///Data of uploaded image that can be editted
        imageDataStruct imageData;
        bool bkgrnd=false;
        bool manualCrop=false;
        bool useBVN=false;

        ///Expret Settings (ES) Options
        bool useMaskFromES=false;
        int maskXES=0,maskYES=0,maskRXES=0,maskRYES=0;
        bool usePixToMmFromES=false;
        double pixToMmES=0.;
        bool useRRThresholdFromES=false;
        double RRThresholdES=0.;
        bool useSigmaCutFromES=false;
        double sigmaCutES=0.;
        bool useFilterFromES=false;
        int filterES=0;
        bool useDirectCutLevelFromES=false;
        double DirectCutLevelES=0.;

        int manualCropX=0,manualCropY=0,manualCropW=0,manualCropH=0;
        int savedCroppedX=0,savedCroppedY=0;

    private:
};

//PYTHON DLL STUFF
#ifdef BUILD_DLL

#define BOOST_LIB_DIAGNOSTIC
using namespace boost::python;

///PYTHON MODULE CONTAINING ACCESSABLE FUNCTIONS
BOOST_PYTHON_MODULE(imageAnalyser)
{
    //this lest python know what a vector of doubles it
    class_<std::vector< double > >("std_vector_double")
		.def( vector_indexing_suite< std::vector< double >>() )
    ;


/// Expose base classes

    boost::python::class_<baseObject, boost::noncopyable>("baseObject", boost::python::no_init)
            ;

    /// member functions to expose to python, remmeber to include enum definitions as boost::python::dict <int, string>
    /// as well as boost::python::dict <int, int>

    class_<imageAnalyser,bases<baseObject>, boost::noncopyable>("imageAnalyser")
        .def(init< optional< const bool, const bool> >())
        .def("loadImageFromFile", &imageAnalyser::loadImageFromFile)
        .def("loadBackgroundImageFromFile", &imageAnalyser::loadBackgroundImageFromFile)
        .def("writeDataToFiles", &imageAnalyser::writeDataToFiles)
        .def("getBeamParameters", &imageAnalyser::getBeamParameters)

        .def("getPixIntensity", &imageAnalyser::getPixIntensity)
        .def("getOriginalPixIntensity", &imageAnalyser::getOriginalPixIntensity)
        .def("getXProjection", &imageAnalyser::getXProjection)
        .def("getOriginalXProjection", &imageAnalyser::getOriginalXProjection)
        .def("getYProjection", &imageAnalyser::getYProjection)
        .def("getOriginalYProjection", &imageAnalyser::getOriginalYProjection)
        .def("getX", &imageAnalyser::getX)
        .def("getY", &imageAnalyser::getY)
        .def("getOriginalX", &imageAnalyser::getOriginalX)
        .def("getOriginalY", &imageAnalyser::getOriginalY)
        .def("useBackground", &imageAnalyser::useBackground)
        .def("getBackgroundImage", &imageAnalyser::getBackgroundImage)

        .def("getImageHeight", &imageAnalyser::getImageHeight)
        .def("getImageWidth", &imageAnalyser::getImageWidth)
        .def("getImageDataSize", &imageAnalyser::getImageDataSize)
        .def("getCroppedX", &imageAnalyser::getCroppedX)
        .def("getCroppedY", &imageAnalyser::getCroppedY)
        .def("useManualCrop", &imageAnalyser::useManualCrop)
        .def("setManualCrop", &imageAnalyser::setManualCrop)

        .def("useESMask", &imageAnalyser::useESMask)
        .def("setESMask", &imageAnalyser::setESMask)
        .def("useESPixToMm", &imageAnalyser::useESPixToMm)
        .def("setESPixToMm", &imageAnalyser::setESPixToMm)
        .def("useESRRThreshold", &imageAnalyser::useESRRThreshold)
        .def("setESRRThreshold", &imageAnalyser::setESRRThreshold)
        .def("useESSigmaCut", &imageAnalyser::useESSigmaCut)
        .def("setESSigmaCut", &imageAnalyser::setESSigmaCut)
        .def("useESFilter", &imageAnalyser::useESFilter)
        .def("setESFilter", &imageAnalyser::setESFilter)
        .def("useESDirectCut", &imageAnalyser::useESDirectCut)
        .def("setESDirectCut", &imageAnalyser::setESDirectCut)
        .def("getPTMRatio", &imageAnalyser::getPTMRatio)
    ;
};//BOOST_PYTHON_MODULE

#endif // BUILD_DLL




#endif

