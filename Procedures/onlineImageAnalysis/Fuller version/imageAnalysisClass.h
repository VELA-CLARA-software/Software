#ifndef IMAGE_ANALYSIS_CLASS_H
#define IMAGE_ANALYSIS_CLASS_H


class imageAnalysisClass{
    public:
        //Constructor
        imageAnalysisClass();
        //Destructor
        ~imageAnalysisClass();

        //Functions
        void                passInData(std::vector<double> &arrayData,
                                       std::vector<double> &bkgrndArrayData,
                                       const int &centerX,
                                       const int &centerY,
                                       const int &xMaskRadius,
                                       const int &yMaskRadius,
                                       const int &numberOfPixels,
                                       const int &pixelWidth,
                                       const int &pixelHeight,
                                       const double &p2mRatio);
        std::vector<std::vector<double>>  anaylseImage(std::vector<double> &arrayData);
        std::vector<double> subtractImages(std::vector<double> &image1,
                                           std::vector<double> &image2);
        std::vector<double> overlayImages(std::vector<double> &image1,
                                          std::vector<double> &image2);
        void                crop(const int &xMin, const int &xMax,
                                 const int &yMin, const int &yMax);
        std::vector<double> scaleImage(const double &A,
                                       std::vector<double> &image);
        std::vector<double> updateProjections(std::vector<double> &image);
        std::vector<int>    correctedPixelPositions(const int &x,
                                                 const int &y);
        std::vector<double> pixelPositions2mm(const int &x,
                                              const int &y);
        std::vector<double> nPointScaling();
        double              calculateSigma(const std::vector<double> &data,
                                           const std::vector<double> &pos,
                                           const double &mu);
        double              calculateSigma(const std::vector<double> &data,
                                           const std::vector<double> &xData,
                                           const std::vector<double> &yData,
                                           const double &muX,
                                           const double &muY);
        double              average(std::vector<double> &v);
        std::vector<double> makeProjection(const std::vector<double> &v,
                                           const int &lengthOfFirstSum,
                                           const int &lengthOfSecondSum,
                                           const int &width,
                                           const bool &revIndices);
        void                makeMask();
        double              dotProduct(std::vector<double> &v1,
                                       std::vector<double> &v2);
        void                updateProjections();
    protected:

    private:
        //Objects in Class
        //Change during analysis
        std::vector<double> processedPixelData;
        std::vector<double> processedPixelXPosition;
        std::vector<double> processedPixelYPosition;
        std::vector<double> imageBkgrndPixelData;
        int runningXCropCounter, runningYCropCounter;
        int imageSize, imageWidth, imageHeight;
        std::vector<double> maskPixelData;
        std::vector<double> xProjection;
        std::vector<double> yProjection;
        std::vector<double> xMaskProjection;
        std::vector<double> yMaskProjection;
        //Constant during analysis
        int imageCenterXPixel, imageCenterYPixel, imageXMaskRadius, imageYMaskRadius;
        double imagePix2mmRatio;



};

#endif
