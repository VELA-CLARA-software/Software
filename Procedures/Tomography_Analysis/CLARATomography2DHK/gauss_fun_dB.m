        function y = gauss_fun_dB(x,C,D)
              
%       y = gauss_fun_dB(x,C,D);
%                                             
%               y = exp(-(x-C)^2/(2*D^2))
%
%       is the derivative wrt B of Gaussian function 
%               y = A + B *  exp(-(x-C)^2/(2*D^2))
%
%     INPUTS:   x:      The independent variable in the exponential
%                       (column or row vector)
%              ( A:      Vertical offset)
%              ( B:      Max amplitude)
%               C:      Horizontal offset
%               D:      Standard deviation
%
%     OUTPUTS:  y:      The values of the exponential at each "x" (vector the
%                       same size as "x").

%===============================================================================

y = exp(-(x-C).^2/(2*D.^2));
