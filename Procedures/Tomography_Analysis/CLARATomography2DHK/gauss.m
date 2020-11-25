        function y = gauss(x,x_bar,sig)
              
%       y = gauss(x[,x_bar,sig]);
%
%       Gaussian function to create a "bell" curve of width "sig" centered
%       around "x_bar" from the independent variable "x".  It is normalized
%       already so that the area under the full curve will be 1.
%
%                                             2      2
%               y = (1/sqrt(2pi)) exp(-(x-<x>) /2 sig )
%
%     INPUTS:   x:      The independent variable in the exponential of the
%                       gaussian (column or row vector)
%               sig:    (Optional,DEF=1) The gaussian standard deviation 
%                       ("width") which defaults to 1 if not given (scalar)
%               x_bar:  (Optional,DEF=0) The center of the gaussian on the 
%                       "x" axis (mean) which defaults to 0 if not given
%                       (scalar)
%
%     OUTPUTS:  y:      The values of the gaussian at each "x" (vector the
%                       same size as "x").
%
%     EXAMPLE:  >>x = [-2.5   -2.0   -1.5   -1.0   -0.5   0 
%                       0.5    1.0    1.5    2.0    2.5];
%               >>y = gauss(x);
%                 y =  
%                      0.0175 0.0540 0.1295 0.2420 0.3521 0.3990 
%                      0.3521 0.2420 0.1295 0.0540 0.0175

%===============================================================================

if nargin == 1
  sig = 1;
  x_bar = 0;
elseif nargin == 2
  x_bar = 0;
end
if(sig~=0),
y = (1/(sqrt(2*pi)*sig))*exp(-( (x-x_bar).^2)/(2*sig^2));
else
y = (1/(sqrt(2*pi)*1e-3))*exp(-( (x-x_bar).^2)/(2*1e-3^2));           
end
