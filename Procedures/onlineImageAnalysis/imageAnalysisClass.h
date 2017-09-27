#ifndef IMAGE_ANALYSIS_CLASS_H
#define IMAGE_ANALYSIS_CLASS_H


class imageAnalysisClass{
    public:
        //Constructor
        imageAnalysisClass();
        //Destructor
        ~imageAnalysisClass();

        //Functions
        std::vector<std::vector<double>>  anaylseImage(std::vector<double> &arrayData,
                                                       std::vector<double> &bkgrndData);
        void                passInData(std::vector<double> &arrayData,
                                       const int &centerX,
                                       const int &centerY,
                                       const int &xMaskRadius,
                                       const int &yMaskRadius,
                                       const int &numberOfPixels,
                                       const int &pixelWidth,
                                       const int &pixelHeight,
                                       const double &p2mRatio,
                                       const int step);
        std::vector<double> scaleImage(const double &A,
                                       std::vector<double> &image);
        std::vector<double> pixelPositions2mm(const int &x,
                                              const int &y);
        std::vector<double>calculateSigmas(const std::vector<double> &data,
                                           const std::vector<double> &xData,
                                           const std::vector<double> &yData,
                                           const double &muX,
                                           const double &muY);
        void                makeMask();
        double              dotProduct(std::vector<double> &v1,
                                       std::vector<double> &v2);
        void                cropSubtractAndMask(std::vector<double> &image,
                                                std::vector<double> &bkgrnd,
                                             const int &xMin, const int &xMax,
                                             const int &yMin, const int &yMax);
    protected:

    private:
        //Objects in Class
        std::vector<double> processedPixelData;
        std::vector<double> processedPixelXPosition;
        std::vector<double> processedPixelYPosition;
        std::vector<double> rawXPosition;
        std::vector<double> rawYPosition;
        int runningXCropCounter, runningYCropCounter;
        int imageSize, imageWidth, imageHeight,jump;
        int rawImageSize, rawImageWidth, rawImageHeight;
        std::vector<double> maskPixelData;
        std::vector<double> xProjection;
        std::vector<double> yProjection;
        std::vector<double> xMaskProjection;
        std::vector<double> yMaskProjection;
        int imageCenterXPixel, imageCenterYPixel, imageXMaskRadius, imageYMaskRadius;
        double imagePix2mmRatio;



};

#endif
