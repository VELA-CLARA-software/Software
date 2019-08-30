
clear

%datadir       = '../Data BuckingCoil/BCCurrent-1';
datadir      = 'Data 2019-03-04 10pC degaussing sol -125.0';
%--------------------------------------------------------------------------
% Set parameters for the analysis and specify directory for the results

run([datadir '/SetParameters.m']);

rsltdir      = [datadir '/Results/Tomography2D'];

load([datadir '/' configfile]);

load([rsltdir '/PhaseSpaceDensity.mat']);

relgamma      = BeamMomentum/0.511;
psresn        = size(rhox,1);

imgfilename   = [datadir '/' Image_and_background_filenames_at_reconstruction_point{1,1}];
bgdfilename   = [datadir '/' Image_and_background_filenames_at_reconstruction_point{1,2}];

imagerp       = GetH5Image(imgfilename, bgdfilename, imgrange/2, calibnrp);

%--------------------------------------------------------------------------

cropx    = 15;
croppx   = 15;

zoomx    = (cropx +1):(size(rhox,1)-cropx ); 
zoompx   = (croppx+1):(size(rhox,2)-croppx);

rhox1     = rhox(zoomx,zoompx);

h        = fspecial('average',[10 10]);
rhox1f   = imfilter(rhox1,h);

% rhoxf    = rhoxf(zoomx,zoompx);

% rhoxf1   = rhoxf(:);
% ix       = find(rhoxf1<0);
% rhoxf1(ix) = 0;
% rhoxf    = reshape(rhoxf1,size(rhoxf));

% rhoxf    = imfilter(rhoxf,h);

rangex   = calibn1(1)*(size(rhox1f,1)+1)/2;
rangepx  = calibn1(1)*(size(rhox1f,2)+1)/2;

figure(3)
hold off
subplot(2,2,1)
imagesc([-rangex rangex],[-rangepx rangepx],rhox1f');
set(gca,'YDir','normal')
xlabel('x_N (mm/\surdm)')
ylabel('p_{xN} (mm/\surdm)')

rhoxproj = sum(rhox1f,2);
xvals1   = calibn1(1)*sqrt(Beta_x_y_at_reconstruction_point(1))*((1:size(rhoxproj,1))-size(rhoxproj,1)/2)/2;
nrm      = max(rhoxproj); %sum(rhoxproj)*(xvals(2)-xvals(1));
subplot(2,2,3)
hold off
plot(xvals1,rhoxproj/nrm,'-k')
sigx1    = sqrt(sum(rhoxproj'.*xvals1.^2)/sum(rhoxproj));

obsxproj = sum(imagerp,2);
xvals2   = calibnrp*((1:size(obsxproj,1))-size(obsxproj,1)/2)/2;
indx     = find(abs(xvals2)<max(xvals1));
xvals2   = xvals2(indx);
obsxproj = obsxproj(indx);
nrm      = max(obsxproj); %sum(obsxproj)*(xvals(2)-xvals(1));
hold on
plot(xvals2,obsxproj/nrm,'-r')
axis tight
xlabel('x (mm)')
ylabel('Intensity (arb. units)')
sigx2    = sqrt(sum(obsxproj'.*xvals2.^2)/sum(obsxproj));
% title(['\sigma_x = ' num2str(sigx1,'%5.3f') 'mm (fit ' num2str(sigx2,'%5.3f') 'mm)']);

%--------------------------------------------------------------------------

dx     = 2*rangex /(size(rhox1f,1)-1);
dpx    = 2*rangepx/(size(rhox1f,2)-1);

valsx  = -rangex :dx :rangex;
valspx = -rangepx:dpx:rangepx;

[gridx, gridpx] = meshgrid(valsx,valspx);

iint     = sum(sum(rhox1f));

xavg     = sum(sum(gridx .*rhox1f',1))/iint;
pxavg    = sum(sum(gridpx.*rhox1f',1))/iint;

x2avg    = sum(sum(gridx .*gridx .*rhox1f',1))/iint - xavg^2;
xpxavg   = sum(sum(gridx .*gridpx.*rhox1f',1))/iint - xavg*pxavg;
px2avg   = sum(sum(gridpx.*gridpx.*rhox1f',1))/iint - pxavg^2;

emitx    = sqrt(x2avg*px2avg - xpxavg^2);
gemitx   = relgamma*emitx;

bn       = x2avg  / emitx;
an       =-xpxavg / emitx;

phi      = 0:2*pi/100:2*pi;
ellipsx  = sqrt(bn*emitx)*cos(phi);
ellipsy  =-sqrt(emitx/bn)*(sin(phi) + an*cos(phi));

figure(3)
hold off
subplot(2,2,1)
hold on
plot(ellipsx,ellipsy,'-k');

betx     = bn*Beta_x_y_at_reconstruction_point(1);
alfx     = an + betx*Alpha_x_y_at_reconstruction_point(1)/Beta_x_y_at_reconstruction_point(1);

titlestr = ['\gamma\epsilon_x=' num2str(gemitx,'%4.3f') '\mum, '...
            '\beta_x=' num2str(betx,'%4.4f') 'm, '...
            '\alpha_x=' num2str(alfx,'%4.4f')];

title(titlestr);

%--------------------------------------------------------------------------

cropy    = 15; %cropx;
croppy   = 15; %croppx;

zoomy    = (cropy +1):(size(rhoy,1)-cropy ); 
zoompy   = (croppy+1):(size(rhoy,2)-croppy);

rhoy1    = rhoy(zoomy,zoompy);

h        = fspecial('average',[6 6]);
rhoy1f    = imfilter(rhoy1,h);

% rhoyf    = rhoyf(zoomy,zoompy);

% rhoy1    = rhoyf(:);
% ix       = find(rhoy1<300);
% rhoy1(ix) = 0;
% rhoyf    = reshape(rhoy1,size(rhoyf));

rangey   = calibn1(2)*(size(rhoy1f,1)+1)/2;
rangepy  = calibn1(2)*(size(rhoy1f,2)+1)/2;

figure(3)
hold off
subplot(2,2,2)
imagesc([-rangey rangey],[-rangepy rangepy],rhoy1f');
set(gca,'YDir','normal')
xlabel('y_N (mm/\surdm)')
ylabel('p_{yN} (mm/\surdm)')

rhoyproj = sum(rhoy1f,2);
yvals1   = calibn1(2)*sqrt(Beta_x_y_at_reconstruction_point(2))*((1:size(rhoyproj,1))-size(rhoyproj,1)/2)/2;
nrm      = max(rhoyproj); %sum(rhoyproj)*(yvals(2)-yvals(1));
subplot(2,2,4)
hold off
plot(yvals1,rhoyproj/nrm,'-k')
axis tight
sigy1    = sqrt(sum(rhoyproj'.*yvals1.^2)/sum(rhoyproj));

obsyproj = sum(imagerp,1)';
% cutoff   = 0.03*max(obsyproj);
% indx     = find(obsyproj<cutoff);
% obsyproj(indx) = 0;
yvals2   = calibnrp*((1:size(obsyproj,1))-size(obsyproj,1)/2)/2;
indx     = find(abs(yvals2)<max(yvals1));
yvals2   = yvals2(indx);
obsyproj = obsyproj(indx);
nrm      = max(obsyproj); %sum(obsyproj)*(yvals(2)-yvals(1));
hold on
plot(yvals2,obsyproj/nrm,'-r')
axis tight
xlabel('y (mm)')
ylabel('Intensity (arb. units)')
sigy2    = sqrt(sum(obsyproj'.*yvals2.^2)/sum(obsyproj));
% title(['\sigma_y = ' num2str(sigy1,'%5.3f') 'mm (fit ' num2str(sigy2,'%5.3f') 'mm)']);

%--------------------------------------------------------------------------

dy     = 2*rangey /(size(rhoy1f,1)-1);
dpy    = 2*rangepy/(size(rhoy1f,2)-1);

valsy  = -rangey :dy :rangey;
valspy = -rangepy:dpy:rangepy;

[gridy, gridpy] = meshgrid(valsy,valspy);

iint     = sum(sum(rhoy1f));

yavg     = sum(sum(gridy .*rhoy1f',1))/iint;
pyavg    = sum(sum(gridpy.*rhoy1f',1))/iint;

y2avg    = sum(sum(gridy .*gridy .*rhoy1f',1))/iint - yavg^2;
ypyavg   = sum(sum(gridy .*gridpy.*rhoy1f',1))/iint - yavg*pyavg;
py2avg   = sum(sum(gridpy.*gridpy.*rhoy1f',1))/iint - pyavg^2;

emity    = sqrt(y2avg*py2avg - ypyavg^2);
gemity   = relgamma*emity;

bn       = y2avg  / emity;
an       =-ypyavg / emity;

phi      = 0:2*pi/100:2*pi;
ellipsx  = sqrt(bn*emity)*cos(phi);
ellipsy  =-sqrt(emity/bn)*(sin(phi) + an*cos(phi));

figure(3)
hold off
subplot(2,2,2)
hold on
plot(ellipsx,ellipsy,'-k');

bety     = bn*Beta_x_y_at_reconstruction_point(2);
alfy     = an + bety*Alpha_x_y_at_reconstruction_point(2)/Beta_x_y_at_reconstruction_point(2);

titlestr = ['\gamma\epsilon_y=' num2str(gemity,'%4.3f') '\mum, '...
            '\beta_y=' num2str(bety,'%4.4f') 'm, '...
            '\alpha_y=' num2str(alfy,'%4.4f')];

title(titlestr);
        
%--------------------------------------------------------------------------

set(gcf,'PaperUnits','inches')
set(gcf,'PaperPosition',[1 5 6 6])
% print('-dpng',[rsltdir '/Tomography2DPhaseSpace.png'],'-r600')
print('-dpdf',[rsltdir '/Tomography2DPhaseSpace.pdf'])

%--------------------------------------------------------------------------
