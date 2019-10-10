
dirname    = 'Data 2019-03-04';
configfile = 'ImageFileInformation.mat';

load([dirname '/' configfile]);

n = 1;
psresn = 41;

imgfilename   = [dirname '/' Image_and_background_filenames_at_reconstruction_point{n,1}];
bgdfilename   = [dirname '/' Image_and_background_filenames_at_reconstruction_point{n,2}];

calibration   = 0.0122; % Screen 2 millimeters/pixel

% GetH5Image(imgfilename, 3.0*psresn, psresn, [sqrt(Beta_x_y_at_observation_point(n,1)) sqrt(Beta_x_y_at_observation_point(n,2))]);
[~, imgBeam] = GetH5Image(imgfilename, bgdfilename, 12.0*psresn, psresn, [1, 1], calibration);

% set(gcf,'PaperUnits','inches')
% set(gcf,'PaperPosition',[1 1 6 6])
% print('-dpng','BeamImageReconstructionPoint.png','-r600')
% print('-dpdf','BeamImageReconstructionPoint.pdf')

figure(3)
imagesc([-1 1]*psresn*calibration,[-1 1]*psresn*calibration,imgBeam');
set(gca,'YDir','normal')
xlabel('x (mm)')
ylabel('y (mm)')
title('Observed image at Screen 2')

set(gcf,'PaperUnits','inches')
set(gcf,'PaperPosition',[1 1 6 6])
% print('-dpng','BeamImageReconstructionPoint.png','-r600')
print('-dpdf','BeamImageScrn2-Observed.pdf')

