function g = gausin( prob )
%                     P
%
% clone of CERN's gausin function
%
c = 2.50662827 ;
%
if ( (prob<=0) | (prob>=1) )
  h = 0 ;
end
if (prob == 0.5)
  h=0 ;
end
if ( (prob>0) & (prob<1) & (prob~=0.5) )
  x = prob ;
  if (prob > 0.5)
    x = 1-prob; 
  end
  x=sqrt(-2*log(x)) ;
  x=x-((7.45551*x+450.636)*x+1271.059)/...
         (((x+110.4212)*x+750.365)*x+500.756) ;
  if (prob<0.5)
    x = -x ;
  end
  if (x<0)
    freqx = 0.5 * erfc(abs(x)/sqrt(2)) ;
  else
    freqx = 0.5 + 0.5 * erf(x/sqrt(2)) ;
  end
  h=c*(prob-freqx)*exp(0.5*x^2)+x ;
end
g = h ;