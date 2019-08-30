function [ imgBeam, sigmax, sigmay, sigmaxerr, sigmayerr ] = GetH5Image( fname, fnameb, range, calibration )
%GetH5Image Summary of this function goes here
%   Detailed explanation goes here

    info = h5info(fname);
    img  = h5read(fname,['/' info.Datasets(1).Name]);

    for n = 2:size(info.Datasets,1)
        img = img + h5read(fname,['/' info.Datasets(n).Name]);
    end
    
    infob  = h5info(fnameb);
    bgd    = h5read(fnameb,['/' infob.Datasets(1).Name]);

    img    = img/size(info.Datasets,1) - bgd;

    xcrop      = 100:size(img,1)-100;
    ycrop      = 100:size(img,2)-100;
    imgCropped = img(xcrop,ycrop);

    xvals      = 1:size(imgCropped,1);
    yvals      = 1:size(imgCropped,2);

    projx         = sum(imgCropped, 2);
    [xfit,qx,dqx] = gauss_fit(xvals', projx);
    sigmax        = qx(4);
    sigmaxerr     = dqx(4);

    projy         = sum(imgCropped, 1);
    [yfit,qy,dqy] = gauss_fit(yvals, projy);
    sigmay        = qy(4);
    sigmayerr     = dqy(4);
    
    figure(1)
    subplot(2,2,2)
    hold off
    imagesc(imgCropped')
    set(gca,'YDir','normal')
    hold on
    plot(xvals,ones(numel(xvals),1)*qy(3),'w');
    plot(ones(numel(yvals),1)*qx(3),yvals,'w');

    dx         = uint64(floor(range/2));
    dy         = uint64(floor(range/2));

    xmin       = qx(3) - dx;
    xmax       = qx(3) + dx;

    ymin       = qy(3) - dy;
    ymax       = qy(3) + dy;

    imgBeam    = imgCropped(xmin:xmax,ymin:ymax);

    xvals      = (1:size(imgBeam,1)) - (size(imgBeam,1)+1)/2;
    yvals      = (1:size(imgBeam,2)) - (size(imgBeam,2)+1)/2;

    subplot(2,2,3)
    hold off
    imagesc(calibration*xvals,calibration*yvals,imgBeam')
    set(gca,'YDir','normal')
    axis tight
    xlabel('x (mm)')
    ylabel('y (mm)')

    subplot(2,2,1)
    hold off
    plot(calibration*xvals,projx(xmin:xmax),'-k')
    hold on
    plot(calibration*xvals,xfit(xmin:xmax),'-r')
    axis tight

    subplot(2,2,4)
    hold off
    plot(projy(ymin:ymax),calibration*yvals,'-k')
    hold on
    plot(yfit(ymin:ymax),calibration*yvals,'-r')
    axis tight

end
