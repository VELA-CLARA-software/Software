
close all
clear

%--------------------------------------------------------------------------
% Specify the data directory

% datadir      = '../Data 2019-03-04';
% datadir      = '../Data BuckingCoil/BCCurrent-1';
% datadir      = '../Data BuckingCoil/BCCurrent-4';
  datadir      = 'Data 2019-03-04 10pC degaussing sol -125.0';


%--------------------------------------------------------------------------
% Set parameters for the analysis and specify directory for the results

run([datadir '/SetParameters.m']);

psresn       =   201;        % Resolution (in pixels) of the phase space reconstruction
imgrange     =  1200;        % Range for cropping the raw camera image around the beam image

rsltdir      = [datadir '/Results/Tomography2D'];
mkdir(rsltdir);

%--------------------------------------------------------------------------

load([datadir '/' configfile]);

nx           = size(indxx,2);
ny           = size(indxy,2);


Beta_x_y_at_reconstruction_point  = [betax betay];
Alpha_x_y_at_reconstruction_point = [alphax alphay];

if exist('ScanQCurrents')
    QuadCurrents = ScanQCurrents;
end

if size(QuadCurrents,2) < 5
    QuadCurrents = [[-5.4853 0; 0 3.9678]*ones(2,size(QuadCurrents,1)); QuadCurrents']';
end

optics = CalculateOptics(betax, alphax, betay, alphay, QuadCurrents, BeamMomentum);

Beta_x_y_at_observation_point  = optics(:,[1, 3]);
Alpha_x_y_at_observation_point = optics(:,[2, 4]);
PhaseAdvance_x_y               = optics(:,[5, 6]);


% Load the images

disp('Loading the images...'); pause(0.01)

tic

nmax       = size(Image_and_background_filenames_at_observation_point,1);

imagearray = cell(1,nmax);
imagesigma = zeros(nmax,2);
sigmaerror = zeros(nmax,2);

dirlist    = dir(rsltdir);

if isempty(find(strcmp('BeamImages.mat',struct2cell(dirlist)),1))
    
    for n = 1:nmax

        imgfilename   = [datadir '/' Image_and_background_filenames_at_observation_point{n,1}];
        bgdfilename   = [datadir '/' Image_and_background_filenames_at_observation_point{n,2}];

        [imagearray{n}, imagesigma(n,1), imagesigma(n,2), sigmaerror(n,1), sigmaerror(n,2)] = ...
            GetH5Image(imgfilename, bgdfilename, imgrange, calibnop);

        pause(0.1)

    end

    save([rsltdir '/BeamImages.mat'],'imagearray','imagesigma','sigmaerror');
    
else

    load([rsltdir '/BeamImages.mat'])
    
end

toc

% return

% Scale and resize the images

disp('Processing images...'); pause(0.01)

close()

tic

% not used just saved?
calibn1     = calibnop*size(imagearray{1},1)/psresn./magnfcn; %2*calibration*floor(r1)/psresn;

for n = 1:nmax
    
    imgscaling    = magnfcn.*[1/sqrt(Beta_x_y_at_observation_point(n,1)) 1/sqrt(Beta_x_y_at_observation_point(n,2))];
    
    img           = ScaleImage(imagearray{n},imgscaling);
    img           = imresize(img,[psresn psresn]);
    
    imagearray{n} = img/sum(img(:));
    
    if ~isempty(union(intersect(n,indxx),intersect(n,indxy)))
        figure(1)
        imagesc(imagearray{n}')
        set(gca,'YDir','normal')
        title(['Image number ',num2str(n)])
        pause(0.01)
    end
    
end

hdf5write('C:\Users\djs56\GitHub\Software\Procedures\Tomography_Analysis\Image Scaling\matlab_imagearray.h5','/data',imagearray);

toc

% Set up variables for the tomography analysis

xprojection = zeros(nx*psresn,1);
yprojection = zeros(ny*psresn,1);

disp("size(xprojection) = ");
disp(size(xprojection));
disp("size(yprojection) = ");
disp(size(yprojection));


% disp("ny = ");
% disp(ny);
% disp("xprojection = ");
% disp(xprojection);
% disp("yprojection = ");
% disp(yprojection);



dfindxx     = zeros(2,nx*psresn^2);

disp('size(dfindxx) = ');
disp( size(dfindxx) );
disp('dfindxx[1] = ');
disp(dfindxx(1));

disp('size(dfindxx) = ')
disp(size(dfindxx))

dfcntrx     = 1;

dfindxy     = zeros(2,ny*psresn^2);
dfcntry     = 1;


ctroffset   = (psresn+1)/2;

% Scan over the quadrupole settings

disp('Setting up the equations...'); pause(0.01)

tic

disp("psresn = ");
disp(psresn);

disp("ctroffset = ");
disp(ctroffset);


disp("main loop x");
for n = 1:nx
    
%     disp("n = ");
%     disp(n);
    indx   = indxx(n);
%     disp("indx = ");
%     disp(indx);
    % Set the phase advance
    cosmux = cos(PhaseAdvance_x_y(indx,1));
    sinmux = sin(PhaseAdvance_x_y(indx,1));

    %disp("PhaseAdvance_x_y(indx,1) = ");
    %disp(PhaseAdvance_x_y(indx,1));
    %disp(cosmux);
    
    % Find the indices of the non-zero values of the matrix relating the
    % projected distribution at YAG02 to the phase space distribution at YAG01
    
    for xindx1 = 1:psresn
        for pxindx1 = 1:psresn
            xindx0  = round(cosmux*(xindx1 - ctroffset) - sinmux*(pxindx1 - ctroffset) + ctroffset);
            if xindx0>0 && xindx0<=psresn
                pxindx0 = round(sinmux*(xindx1 - ctroffset) + cosmux*(pxindx1 - ctroffset) + ctroffset);
                if pxindx0>0 && pxindx0<=psresn
                   
                    % set column dfcntrx in dfindxx
                    dfindxx(:,dfcntrx) = [(n-1)*psresn + xindx1; (xindx0-1)*psresn + pxindx0];
                    
                    %disp("n = ");
                    %disp(n);
                    %disp( "dfindxx(:,dfcntrx) = ")
                    %disp( dfindxx(:,dfcntrx) )
                    %disp("(n-1)*psresn + xindx1 = ");
                    %disp( (n-1)*psresn + xindx1 )
                    %disp("(xindx0-1)*psresn + pxindx0 = ");
                    %disp( (xindx0-1)*psresn + pxindx0 )
                    %disp( "[(n-1)*psresn + xindx1; (xindx0-1)*psresn + pxindx0] = " )
                    %disp( [(n-1)*psresn + xindx1; (xindx0-1)*psresn + pxindx0] )
                    %pause(121212);
                    
                    dfcntrx = dfcntrx + 1;
                end
            end
        end
    end
    % Construct the vector of image pixels
    % why not normalised?
%     nrm = sum(sum(imagearray{indx}));
    
    %disp((n-1)*psresn+1);
    disp(dfcntrx);
    % pause(12344);
    % sum(imagearray{indx},2);
    xprojection(((n-1)*psresn+1):n*psresn) = sum(imagearray{indx},2); %/nrm;

end




disp('xprojection() = ');
disp(xprojection(1));
disp(xprojection(1000));
disp('Final dfcntrx = ');
disp(dfcntrx);


for n = 1:ny
    
    indx   = indxy(n);
    
    % Set the phase advance
    
    cosmuy = cos(PhaseAdvance_x_y(indx,2));
    sinmuy = sin(PhaseAdvance_x_y(indx,2));
    
    % Find the indices of the non-zero values of the matrix relating the
    % projected distribution at YAG02 to the phase space distribution at YAG01
    
    for yindx1 = 1:psresn
        for pyindx1 = 1:psresn
            yindx0  = round(cosmuy*(yindx1 - ctroffset) - sinmuy*(pyindx1 - ctroffset) + ctroffset);
            if yindx0>0 && yindx0<=psresn
                pyindx0 = round(sinmuy*(yindx1 - ctroffset) + cosmuy*(pyindx1 - ctroffset) + ctroffset);
                if pyindx0>0 && pyindx0<=psresn

                    dfindxy(:,dfcntry) = [(n-1)*psresn + yindx1; (yindx0-1)*psresn + pyindx0];
                    dfcntry = dfcntry + 1;

                end
            end
        end
    end
    
    % Construct the vector of image pixels
    
%     nrm = sum(sum(imagearray{indx}));
    
    yprojection(((n-1)*psresn+1):n*psresn) = sum(imagearray{indx},1)'; %/nrm;
    
end

disp("yprojection() = ");
disp(yprojection(1));
disp(yprojection(1000));
%disp("pause(1233);");
%pause(1233);


% Finally, construct the (sparse) matrix relating the projected
% distribution at YAG02 to the phase space distribution at YAG01

disp(' size(dfindxx) = ');
disp(size(dfindxx));
disp('1 dfindxx() = ');

disp(dfindxx(1));
disp(dfindxx(2));
disp(dfindxx(1:10));

dfindxx = dfindxx(:,1:dfcntrx-1);
disp('2 dfindxx() = ');
disp(' size(dfindxx) = ');
disp(size(dfindxx));
disp(dfindxx(1:10));

%disp("dfindxx(1,:) = ")


disp("dfullx size = ");
disp(nx*psresn);
disp(psresn^2);
disp("size(dfindxx(1,:))");
disp(size(dfindxx(1,:)));
disp("size(dfindxx(2,:))");
disp(size(dfindxx(2,:)));
disp("size(ones(1,dfcntrx-1))");
disp(size(ones(1,dfcntrx-1)));
%pause(20);
%disp(ones(1,dfcntrx-1));

dfullx  = sparse(dfindxx(1,:),dfindxx(2,:),ones(1,dfcntrx-1),nx*psresn,psresn^2);
%pause(12344);


disp('dfullx() = ');
disp(size(dfullx));
disp(size(dfindxx(1,:)));
disp(size(dfindxx(2,:)));
disp(size(ones(1,dfcntrx-1)));
disp(nx*psresn);
disp(psresn^2);
disp(dfullx(1:10));
%save('dfullx_test.mat', 'dfullx');
%save('xprojection.mat', 'xprojection');


disp("rsltdir ");
disp(rsltdir);
save([rsltdir '/dfindxx.mat'],'dfindxx');

dfindxy = dfindxy(:,1:dfcntry-1);
disp('dfindxy() = ');
disp(dfindxy(1:10));
disp(dfindxy(1000:1010));
dfully  = sparse(dfindxy(1,:),dfindxy(2,:),ones(1,dfcntry-1),ny*psresn,psresn^2);



toc

% Find the phase space distribution at YAG01 that best fits the images
% observed on YAG02

disp('Solving the equations...'); pause(0.01)

tic

[rhovectorx ,flag] = lsqr(dfullx,xprojection,1e-6,400);

disp('flag = ')
disp(flag) 
%pause(12344)


rhovectory = lsqr(dfully,yprojection,1e-6,400);

toc

rhox  = reshape(rhovectorx,[psresn,psresn])';
rhoy  = reshape(rhovectory,[psresn,psresn])';

% Save the results

save([rsltdir '/PhaseSpaceDensity.mat'],...
    'rhox',...
    'rhoy',...
    'imgrange',...
    'calibn1',...
    'Beta_x_y_at_reconstruction_point',...
    'Alpha_x_y_at_reconstruction_point',...
    'BeamMomentum');

save([rsltdir '/TomographyMatrixX.mat'],'dfullx','rhovectorx','xprojection');
save([rsltdir '/TomographyMatrixY.mat'],'dfully','rhovectory','yprojection');

% Display a comparison of the fit to the date

h      = fspecial('average',[1 1]);

figure(2)
subplot(2,2,1)
hold off
plot(xprojection,'-k')
hold on
plot(dfullx*rhovectorx,'--r')
axis tight
xlabel('Data point')
ylabel('x projection')

subplot(2,2,2)
hold off
plot(xprojection - dfullx*rhovectorx,'-r')
hold on
axis tight
xlabel('Data point')
ylabel('x residual')

for n = 1:size(indxx,2)

    rho3     = imrotate(rhox,-optics(indxx(n),5)*180/pi,'nearest','crop');
    rho3f    = imfilter(rho3,h);

    rho3proj = sum(rho3f,2);

    xrnge    = ((n-1)*psresn+1):n*psresn;

    subplot(2,2,1)
    plot(xrnge,rho3proj,'.b')

    subplot(2,2,2)
    plot(xrnge,xprojection(xrnge)-rho3proj,'.b')

end

figure(2)
subplot(2,2,3)
hold off
plot(yprojection,'-k')
hold on
plot(dfully*rhovectory,'--r')
axis tight
xlabel('Data point')
ylabel('y projection')

subplot(2,2,4)
hold off
plot(yprojection - dfully*rhovectory,'-r')
hold on
axis tight
xlabel('Data point')
ylabel('y residual')

for n = 1:size(indxy,2)

    rho3     = imrotate(rhoy,-optics(indxy(n),6)*180/pi,'nearest','crop');
    rho3f    = imfilter(rho3,h);

    rho3proj = sum(rho3f,2);

    xrnge    = ((n-1)*psresn+1):n*psresn;

    subplot(2,2,3)
    plot(xrnge,rho3proj,'.b')

    subplot(2,2,4)
    plot(xrnge,yprojection(xrnge)-rho3proj,'.b')

end

% MakePlots