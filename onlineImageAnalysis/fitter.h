#ifndef FIT_H
#define FIT_H


#include"ImageStructs.h"
#include "baseObject.h"


///------------------CLASS TO FIT EQUATIONS TO DATA----------------------///
///------------Functions that will read in image data from---------------///
///--------------image Analyser and fit function to them-----------------///
class fitter: public baseObject{
    public:
        //Constructor
        fitter( const bool* show_messages_ptr, const  bool * show_debug_messages_ptr );
        //Destructor
        ~fitter();


        ///Functions
        //1D ESTIMATES(GETS A,B MU, AND SIGAMA) CHOOSE PROJECTION AND WHETHER TO USE MOMENTS OR FWHM
        std::vector<double> get1DEstimates(const std::vector<double>& projection, const EstMethod& method);
        // COMPARE 1D MU AND SIGMA VALUES OF TWO ESTIMATES
        double compare1DEstimates(const double & mu1,const double & sigma1,const double & mu2,const double & sigma2);
        //FIT 1D GAUSSIAN
        std::vector<double> fit1DGaussianToProjection(const imageDataStruct& ID,const projAxis& axis, const std::vector<double>& estimates);
        //GENERAL 1D GUASSAIN FIT
        std::vector<double> fitGuassian(const std::vector<double> data, const std::vector<double> estimates);
        //USE 1D FITS TO DO A BVN FIT
        std::vector<double> fitBVN(const imageDataStruct& ID, const std::vector<double>& xEstimates, const std::vector<double>& yEstimates);
        //DIRECTLY CALCULATE THE MOMENT OF THE IMAGE DISTRIBUTION
        std::vector<double> covarianceValues(const imageDataStruct& ID,const double & cut);
        //CALC MU
        double calculateMu(const std::vector<double> &data,const std::vector<double> &position);
        //CALC SIGMA
        double calculateSigmaSquared(const std::vector<double> &data,const std::vector<double> &position, const double &mu);
        //CALC SIGMA SQUARED overidden
        double fitter::calculateSigmaSquared(const std::vector<double> &data,const std::vector<double> &position1, const std::vector<double> &position2,
                                                                                                                const double &mu1, const double &mu2);
        //GET R SQUARED OF 1d PROJECTIONS
        double rSquaredOf1DProjection(const imageDataStruct& ID, const std::vector<double>& parameters, const projAxis& axis);

    protected:
    private:
};

#endif

