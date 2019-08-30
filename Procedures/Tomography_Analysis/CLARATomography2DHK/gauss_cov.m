function [covm] = gauss_cov(t,dy,b,c,d)
%
%       [covm] = gauss_cov (t,dy,b,c,d)
%
%       Calculates the covariance matrix from the nonlinear fit to
%
%         yfit = A+B*exp(-(t-C)^2/(2*D^2))
%
%       Naturally must be called AFTER a call to GAUSS_FIT, 
%       which is a 
%	non-linear fitting routine to fit an exponential curve
%	to the data in vectors "t" and "y", where "t" contains the
%	independent variable data and "y" contains the dependent data.
%
%
%    INPUTS:	t:	A vector (row or column) of independent variable
%			data.
%   		dy:	 A vector (row or	column)
%		        of the errors on the dependent variable
%			data.              
%               A       fit parameter
%               B       fit parameter
%               C       fit parameter
%               D       fit parameter
%
%    OUTPUTS:	covm    covariance matrix (4x4)
%                       containing the errors on each of the fit parameters

%===============================================================================
da = 1;
db = gauss_fun_dB(t,c,d);
dc = gauss_fun_dC(t,b,c,d);
dd = gauss_fun_dD(t,b,c,d);
h(1,1) = sum( 1./ dy .^2); 
h(2,2) = sum( db .^ 2 ./ dy .^2); 
h(3,3) = sum( dc .^ 2 ./ dy .^2); 
h(4,4) = sum( dd .^ 2 ./ dy .^2); 
h(1,2) = sum( da .* db ./ dy .^2);
h(1,3) = sum( da .* dc ./ dy .^2);
h(1,4) = sum( da .* dd ./ dy .^2);
h(2,3) = sum( db .* dc ./ dy .^2);
h(2,4) = sum( db .* dd ./ dy .^2);
h(3,4) = sum( dc .* dd ./ dy .^2);
h(2,1) = h(1,2);
h(3,1) = h(1,3);
h(4,1) = h(1,4);
h(3,2) = h(2,3);
h(4,2) = h(2,4);
h(4,3) = h(3,4);
covm = inv(h);
