function [y,dy,R,dR,chisq,V] = fit(Q,s,sig);

%FIT
%       [y,dy,R,dR,chisq,V] = fit(Q,s[,sig])
%
%       Function to fit the data in column vector "s" to the curve given by
%       the linear combination of the functions in "Q".  The matrix "Q" is
%       made up of n column vectors, each of which is a separate function.
%       There are n such funtions each of which is evaluated at N points,
%       and so the matrix "Q" is N rows by n columns.  The
%       column vector "s" has N rows.  The column vector "R" is output with
%       n rows, each of which is a coefficient of the fit.  The "chisq" is
%       a scalar as a measure of the goodness of fit ( ~1 is good, but this
%       scales with the inverse square of "sig", if "sig" is a constant).
%                        
%       (NOTE:    N       is the number of points to fit
%                 n       is the number of known functions)
%
%     e.g.      y1 = Q11*R1 + Q12*R2 + ... + Q1n*Rn
%               y2 = Q21*R1 + Q22*R2 + ... + Q2n*Rn
%               .       .       .               .
%               .       .       .               .
%               yN = QN1*R1 + QN2*R2 + ... + QNn*Rn,
%     or             
%               for yi = m*xi + b,      then Q = [x' ones(N,1)],
%                                            s = [y1 y2 ... yN]',
%                                          sig = (guess at s resolutions)
%                                            R = [m b]', 
%                                            
%
%     INPUTS:   Q:      Known functions matrix (N rows by n columns)
%               s:      Column vector of data to fit to (N rows)    
%               sig:    (Optional) Column vector of expected errors in fit
%                       with N rows, or a scalar which is assumed to 
%                       be the actual errors at each point.  If "sig" 
%                       is not given, all errors at each fit point are
%                       assumed the same, and the dR & dy errors are
%                       rescaled by renormalizing "chisq" to 1.
%     OUTPUTS:  y:      Fitted data (column vector of N rows)
%               dy:     Errors on fitted data (column vector on N rows)
%               R:      Fit coefficients (column vector of n rows)
%               dR:     Errors on fitted coefficients (vector of n rows)
%               chisq:  Goodness of fit scalar (normalized to the number
%                       of degrees of freedom (NDF = N - n)).
%               V:      Covariance matrix of the fit (n X n matrix)

%==========================================================================
        
s = s(:);

if exist('sig')==0,
  sig = 1;
  renorm = 1;
else
  sig = sig(:);
  renorm = 0;
end

[N,n] = size(Q);
if n==1 | N==1
  Q = Q(:);
  [N,n] = size(Q);
end

if n > N,
  error('Sorry, you don''t have enough points to fit to this curve')
end

n_sig = length(sig);

if n_sig == 1,
  sig = sig * ones(N,1);
elseif n_sig ~= N,
  disp(' ')
  disp('*** NUMBER OF SIGMAS MUST BE SAME AS NUMBER OF POINTS ***')
  disp(' ')
  return
end

sig2 = sig.^2;
e = sig2.^(-1);
E = e*ones(1,n);                        % symmetric matrix of 1/est^2 noises
G = Q.*E;
NDF = N - n;                            % number of degrees of freedom
if n == N,
  NDF = 1;
end

V = inv(Q'*G);
t = V*G';
dR = sqrt(diag(V));

T = Q*t;                                % use to calc errors
dy2 = (T.^2)*sig2;                      % square of errors
dy = sqrt(dy2);                         % vector of errors

R = t*s;                                % calculate n fit coefficients
y = Q*R;                                % calculate fitted curve
chi = (s - y)./sig;
chisq = chi'*chi/NDF;                   % calculate normalized chi squared

if renorm
  chi   = sqrt(chisq);
  dR    = dR*chi;
  dy    = dy*chi;
  V     = V*chisq;
  chisq = 1;
end
