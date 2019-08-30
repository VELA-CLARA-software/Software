function f = gauss_min(p, arg1)

%	gauss_min(p) returns the error
%	between the data and the values computed by the current
%	function of p.  GAUSS_MIN assumes a function of the form
%
%	  y =  c(1) + c(2)*(1 - exp( -(x-p(1))^2/2*p(2)^2 ))/(x-p(1))
%
%	with 2 linear parameters and 2 nonlinear parameters (see also
%	GAUSS).

%===============================================================================
x  = arg1(:,1); 
y  = arg1(:,2);
dy = arg1(:,3);

A  = [ones(size(x)) gauss(x,p(1),p(2))];
c  = A\y;
z  = A*c;
f  = norm((z-y)./dy);

              
