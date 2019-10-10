function imscaled = ScaleImage(im0,scale)

    tform    = affine2d([scale(2) 0 0; 0 scale(1) 0; 0 0 1]);
    
%     tic
    im1      = imwarp(im0,tform,'linear');
%     toc
    
    imscaled = zeros(size(im0));

    x1       = floor( (size(im1,1)+1)/2 );
    y1       = floor( (size(im1,2)+1)/2 );

    x2       = floor( (size(imscaled,1)+1)/2 );
    y2       = floor( (size(imscaled,2)+1)/2 );

    rangex   = min(x1,x2)-1;
    rangey   = min(y1,y2)-1;

    imscaled(x2+(-rangex:rangex),y2+(-rangey:rangey)) = im1(x1+(-rangex:rangex),y1+(-rangey:rangey));

return


% testimage = zeros(101,101);
% 
% theta = 0:2*pi/100:2*pi;
% 
% for n = 1:size(theta,2)
%    
%     testimage(51+round(24*cos(theta(n))),51+round(24*sin(theta(n)))) = 1;
%     
% end
% 
% figure(1)
% imagesc(testimage)
% axis equal
% axis tight
% 
% tform   = affine2d([2 0 0; 0 0.5 0; 0 0 1]);
% image1  = imwarp(testimage,tform);
% 
% figure(2)
% imagesc(image1)
% axis equal
% axis tight
% 
% image2 = zeros(size(testimage));
% 
% x1 = floor( (size(image1,1)+1)/2 );
% y1 = floor( (size(image1,2)+1)/2 );
% 
% x2 = floor( (size(image2,1)+1)/2 );
% y2 = floor( (size(image2,2)+1)/2 );
% 
% rangex = min(x1,x2)-1;
% rangey = min(y1,y2)-1;
% 
% image2(x2+(-rangex:rangex),y2+(-rangey:rangey)) = image1(x1+(-rangex:rangex),y1+(-rangey:rangey));
% 
% figure(3)
% imagesc(image2)
% axis equal
% axis tight
