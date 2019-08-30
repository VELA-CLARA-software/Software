% Matlab script for specifying parameters for quad scan and tomography analysis
% Data 2019-03-04

configfile   = 'ImageFileInformation.mat';

%----------------------------------------------------------------------------
% Specify the screen calibration factors
%----------------------------------------------------------------------------
calibnop     = 0.0181;   % Screen 3 (observation point) calibration factor in millimeters/pixel
calibnrp     = 0.0122;  % calibration in millimetres/pixel of screen at reconstruction point

%----------------------------------------------------------------------------
% Specify which images to use in the analysis
%----------------------------------------------------------------------------
indxx        = setdiff(1:38,[3:5 26 31]); % images to use for the horizontal analysis
indxy        = setdiff(1:38,[33]);        % images to use for the vertical analysis

%----------------------------------------------------------------------------
% Set beam momentum (in MeV)
%----------------------------------------------------------------------------
BeamMomentum = 29.5; % 30.0 MeV nominal

%----------------------------------------------------------------------------
% Set nominal optics values for phase space normalisation
%----------------------------------------------------------------------------
betax        =  8.7047;
alphax       = -1.8511;
betay        =  2.1706;
alphay       = -2.2652;

%----------------------------------------------------------------------------
% Set magnification factors [x,y] for tomography analysis of images
%----------------------------------------------------------------------------
magnfcn      = [10,10];

%----------------------------------------------------------------------------
return