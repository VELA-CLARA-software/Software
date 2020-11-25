function [yfit,q,dq,chisq_ndf] = gauss_fit(x,y,dy,y_off)   

%	[yfit,q,dq,chisq_ndf] = gauss_fit(x,y[,dy,y_off]);
%
%	Non-linear fitting routine to fit a gaussian "bell" curve
%	to the data in vectors "x" and "y", where "x" contains the
%	independent variable data and "y" contains the dependent data.
%	The fit form is as follows:
%
%    	  yfit =  q(1) + q(2)*exp( -(x-q(3))^2/2*q(4)^2 )
%
%	When "y_off" = 0 then q(1) is returned as exactly zero.
%
%    INPUTS:	x:	A vector (row or column) of independent variable
%			data.
%		y:	A vector (row or column) of dependent data.
%		dy:	(Optional,DEF=no errors) A vector (row or
%			column) of the errors on the dependent variable
%			data.
%		y_off:  (Optional,DEF=1) If "y_off" .NE. 0, then the gaussian
%			fit includes a "y" offset parameter in the fit.
%			If "y_off" = 0, this forces the fit to include no
%			"y" offset and therefore q(1) is set exactly to zero.
%
%    OUTPUTS:	yfit:	A vector of fitted bell curve data from which the
%			difference to the original data "y" has been
%			minimized.
%		q:	A vector of the 4 scalars which are fitted:
%			q(1) => DC offset in the gaussian data (if "y_off"=0
%				then q(1) = 0).
%			q(2) => Amplitude scaling factor of gaussian curve.
%			q(3) => Horizontal offset (X0).     
%                       q(4) => Standard deviation of the gaussian.
%               dq:     A vector of the 4 errors on each of the above q's.
%		chisq_ndf:	Chi_squared per degree of freedom (~1 =>
%				good fit when "dy" is given)

%===============================================================================
if length(y) < 5
  error('Need at least 5 data points to fit a gaussian')
end

x = x(:);
y = y(:);
if ~exist('dy'),     dy = ones(size(y));  end
if isempty(dy),      dy = ones(size(y));  end
dy = dy(:);
if ~exist('y_off'),  y_off = 1;           end

arg1(:,3) = dy;
arg1(:,1) = x;
arg1(:,2) = y;

% sort data to find the pedistal (the 5% population level)
% and the peak.  Use this data to identify data points 
% 1/e above pedistal

[tmp,indx]=sort(y);
npnts=length(y);
ymin=y(indx(round(npnts*0.05+1)));  % the 5% point
ymax=y(indx(round(npnts*0.98)));    % the 98% point

% Using prior ymin,ymax, find indicies for y>ymin + 1/e (ymax-ymin)

th=find(y > ymin + (ymax-ymin)/2.7);

% guess that the x0 is at the mean of the above threshold
% points

x_ymax=mean(x(th));

% and that the varience is somehow related to to distribution
% of x with y>threshold

xstd=1.3*std(x(th));
p = [x_ymax xstd];

[p,opt] = fminsearch('gauss_min',p,[],arg1);
z = sqrt(2*pi)*p(2)*gauss(x,p(1),p(2));
if y_off
  Q = [ones(size(z)) z];
  [yfit,dyfit,c] = fit(Q,y,dy);
  q = [c(1) c(2) p(1) p(2)];
else
  Q = z;
  [yfit,dyfit,c] = fit(Q,y,dy);
  q = [0 c(1) p(1) p(2)];
end
chisq_ndf = norm( (y-yfit)./dy )/sqrt(length(y) - length(q));        
chisq_ndf = chisq_ndf^2;
covm = gauss_cov(x,dy,q(2),q(3),q(4));
da = sqrt(abs(covm(1,1)));
db = sqrt(abs(covm(2,2)));
dc = sqrt(abs(covm(3,3)));
dd = sqrt(abs(covm(4,4)));
dq = [da db dc dd];

% returning [yfit,q,dq,chisq_ndf]                                                          
