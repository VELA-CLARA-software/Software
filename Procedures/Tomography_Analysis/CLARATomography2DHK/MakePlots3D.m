close all
clear

load PhaseSpaceDensity

relgamma   = 29.0/0.511;

dirname    = 'Data 2019-03-04';
configfile = 'ImageFileInformation_Iterated.mat';

load([dirname '/' configfile]);

imgfilename   = [dirname '/' Image_and_background_filenames_at_reconstruction_point{1,1}];
bgdfilename   = [dirname '/' Image_and_background_filenames_at_reconstruction_point{1,2}];

psresn        = size(rhox,1);
calibnrp      = 0.0122;  % calibration in millimetres/pixel of screen at reconstruction point

imagerp = GetH5Image(imgfilename, bgdfilename, imgrange/2, calibnrp);

set(gcf,'PaperUnits','inches')
set(gcf,'PaperPosition',[1 5 6 6])
% print('-dpng','BeamImage-Screen2-Observed','-r600')
print('-dpdf','BeamImage-Screen2-Observed.pdf')

%--------------------------------------------------------------------------

rhox1 = rhox;

for dindx1 = 1:psresn
    
    dindx0 = dindx1 - (psresn+1)/2;
    rhox1(:,:,dindx1) = ScaleImage(rhox1(:,:,dindx1),[1+dindx0*dispx/psresn, 1+dindx0*disppx/psresn]);
        
end

cropx    = 5;
croppx   = 5;
cropd    = 5;

zoomx    = (cropx +1):(size(rhox1,1)-cropx ); 
zoompx   = (croppx+1):(size(rhox1,2)-croppx);
zoomd    = (cropd +1):(size(rhox1,3)-cropd );

rhox1     = rhox1(zoomx,zoompx,zoomd);

% d0       = (psresn+1)/2;
rhox2    = sum(rhox1,3); % squeeze(rhox1(:,:,d0));

h        = fspecial('average',[1 1]);
rhox2f   = imfilter(rhox2,h);

rhox3    = permute(rhox1,[1 3 2]);
rhox3    = sum(rhox3,3);
rhox3f   = imfilter(rhox3,h);

% rhoxf    = rhoxf(zoomx,zoompx);

% rhoxf1   = rhoxf(:);
% ix       = find(rhoxf1<0);
% rhoxf1(ix) = 0;
% rhoxf    = reshape(rhoxf1,size(rhoxf));

% rhoxf    = imfilter(rhoxf,h);

rangex   = calibn1*(size(rhox2f,1)+1)/2;
rangepx  = calibn1*(size(rhox2f,2)+1)/2;

figure(3)
subplot(3,2,1)
imagesc([-rangex rangex],[-rangepx rangepx],rhox2f');
set(gca,'YDir','normal')
xlabel('x_N (mm/\surdm)')
ylabel('p_{xN} (mm/\surdm)')

subplot(3,2,3)
imagesc([-rangex rangex],[-rangepx rangepx],rhox3f');
set(gca,'YDir','normal')
xlabel('x_N (mm/\surdm)')
ylabel('\delta (arb units)')

rhoxproj = sum(rhox2f,2);
xvals    = calibn1*sqrt(Beta_x_y_at_reconstruction_point(1))*((1:size(rhoxproj,1))-size(rhoxproj,1)/2)/2;
subplot(3,2,5)
hold off
plot(xvals,rhoxproj/max(rhoxproj),'-k')

obsxproj = sum(imagerp,2);
xvals    = calibnrp*((1:size(obsxproj,1))-size(obsxproj,1)/2)/2;
hold on
plot(xvals,obsxproj/max(obsxproj),'-r')
axis tight
xlabel('x (mm)')
ylabel('Intensity (arb. units)')

%--------------------------------------------------------------------------

dx     = 2*rangex /(size(rhox2f,1)-1);
dpx    = 2*rangepx/(size(rhox2f,2)-1);

valsx  = -rangex :dx :rangex;
valspx = -rangepx:dpx:rangepx;

[gridx, gridpx] = meshgrid(valsx,valspx);

iint     = sum(sum(rhox2f));

xavg     = sum(sum(gridx .*rhox2f',1))/iint;
pxavg    = sum(sum(gridpx.*rhox2f',1))/iint;

x2avg    = sum(sum(gridx .*gridx .*rhox2f',1))/iint - xavg^2;
xpxavg   = sum(sum(gridx .*gridpx.*rhox2f',1))/iint - xavg*pxavg;
px2avg   = sum(sum(gridpx.*gridpx.*rhox2f',1))/iint - pxavg^2;

emitx    = sqrt(x2avg*px2avg - xpxavg^2);
gemitx   = relgamma*emitx;

bn       = x2avg  / emitx;
an       =-xpxavg / emitx;

phi      = 0:2*pi/100:2*pi;
ellipsx  = sqrt(bn*emitx)*cos(phi);
ellipsy  =-sqrt(emitx/bn)*(sin(phi) + an*cos(phi));

figure(3)
subplot(3,2,1)
hold on
plot(ellipsx,ellipsy,'-k');

betx     = bn*Beta_x_y_at_reconstruction_point(1);
alfx     = an + betx*Alpha_x_y_at_reconstruction_point(1)/Beta_x_y_at_reconstruction_point(1);

titlestr = ['\gamma\epsilon_x=' num2str(gemitx,'%4.2f') '\mum, '...
            '\beta_x=' num2str(betx,'%4.2f') 'm, '...
            '\alpha_x=' num2str(alfx,'%4.2f')];

title(titlestr);
        
%--------------------------------------------------------------------------

rhoy1 = rhoy;

for dindx1 = 1:psresn
    
    dindx0 = dindx1 - (psresn+1)/2;
    rhoy1(:,:,dindx1) = ScaleImage(rhoy1(:,:,dindx1),[1+dindx0*dispy/psresn, 1+dindx0*disppy/psresn]);
        
end

cropy    = 5;
croppy   = 5;
cropd    = 5;

zoomy    = (cropy +1):(size(rhoy1,1)-cropy ); 
zoompy   = (croppy+1):(size(rhoy1,2)-croppy);
zoomd    = (cropd +1):(size(rhoy1,3)-cropd );

rhoy1     = permute(rhoy1(zoomy,zoompy,zoomd),[1 2 3]);

% d0       = (psresn+1)/2;
rhoy2    = sum(rhoy1,3); % squeeze(rhoy1(:,:,1));

h        = fspecial('average',[3 3]);
rhoy2f    = imfilter(rhoy2,h);

rhoy3    = permute(rhoy1,[1 3 2]);
rhoy3    = sum(rhoy3,3);
rhoy3f   = imfilter(rhoy3,h);

% rhoyf    = rhoyf(zoomy,zoompy);

% rhoy1    = rhoyf(:);
% ix       = find(rhoy1<300);
% rhoy1(ix) = 0;
% rhoyf    = reshape(rhoy1,size(rhoyf));

rangey   = calibn1*(size(rhoy2f,1)+1)/2;
rangepy  = calibn1*(size(rhoy2f,2)+1)/2;

figure(3)
subplot(3,2,2)
imagesc([-rangey rangey],[-rangepy rangepy],rhoy2f');
set(gca,'YDir','normal')
xlabel('y_N (mm/\surdm)')
ylabel('p_{yN} (mm/\surdm)')

subplot(3,2,4)
imagesc([-rangey rangey],[-rangepy rangepy],rhoy3f');
set(gca,'YDir','normal')
xlabel('y_N (mm/\surdm)')
ylabel('\delta (arb units)')

rhoyproj = sum(rhoy2f,2);
yvals    = calibn1*sqrt(Beta_x_y_at_reconstruction_point(2))*((1:size(rhoyproj,1))-size(rhoyproj,1)/2)/2;
subplot(3,2,6)
hold off
plot(yvals,rhoyproj/max(rhoyproj),'-k')
axis tight

obsyproj = sum(imagerp,1)';
yvals    = calibnrp*((1:size(obsyproj,1))-size(obsyproj,1)/2)/2;
hold on
plot(yvals,obsyproj/max(obsyproj),'-r')
axis tight
xlabel('y (mm)')
ylabel('Intensity (arb. units)')

%--------------------------------------------------------------------------

dy     = 2*rangey /(size(rhoy2f,1)-1);
dpy    = 2*rangepy/(size(rhoy2f,2)-1);

valsy  = -rangey :dy :rangey;
valspy = -rangepy:dpy:rangepy;

[gridy, gridpy] = meshgrid(valsy,valspy);

iint     = sum(sum(rhoy2f));

yavg     = sum(sum(gridy .*rhoy2f',1))/iint;
pyavg    = sum(sum(gridpy.*rhoy2f',1))/iint;

y2avg    = sum(sum(gridy .*gridy .*rhoy2f',1))/iint - yavg^2;
ypyavg   = sum(sum(gridy .*gridpy.*rhoy2f',1))/iint - yavg*pyavg;
py2avg   = sum(sum(gridpy.*gridpy.*rhoy2f',1))/iint - pyavg^2;

emity    = sqrt(y2avg*py2avg - ypyavg^2);
gemity   = relgamma*emity;

bn       = y2avg  / emity;
an       =-ypyavg / emity;

phi      = 0:2*pi/100:2*pi;
ellipsx  = sqrt(bn*emity)*cos(phi);
ellipsy  =-sqrt(emity/bn)*(sin(phi) + an*cos(phi));

figure(3)
subplot(3,2,2)
hold on
plot(ellipsx,ellipsy,'-k');

bety     = bn*Beta_x_y_at_reconstruction_point(2);
alfy     = an + bety*Alpha_x_y_at_reconstruction_point(2)/Beta_x_y_at_reconstruction_point(2);

titlestr = ['\gamma\epsilon_y=' num2str(gemity,'%4.2f') '\mum, '...
            '\beta_y=' num2str(bety,'%4.2f') 'm, '...
            '\alpha_y=' num2str(alfy,'%4.2f')];

title(titlestr);
        
%--------------------------------------------------------------------------

set(gcf,'PaperUnits','inches')
set(gcf,'PaperPosition',[1 5 6 6])
% print('-dpng','BeamImage-Screen2-Reconstructed.png','-r600')
print('-dpdf','BeamImage-Screen2-Reconstructed.pdf')

%--------------------------------------------------------------------------

% figure(4)
% subplot(1,2,1)
% surf(rhoxf)
% 
% subplot(1,2,2)
% surf(rhoyf)
