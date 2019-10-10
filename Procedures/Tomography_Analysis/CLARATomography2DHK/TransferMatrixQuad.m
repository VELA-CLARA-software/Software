function [ m ] = TransferMatrixQuad( k1, length )
%TransferMatrixQuad returns the transfer matrix for a quadrupole
%   Detailed explanation goes here

    m = TransferMatrixDrift(length);

    if k1 > 0
        
        omega = sqrt(k1);
    
        m = [ cos(omega*length)         sin(omega*length)/omega  0                          0 ;...
             -sin(omega*length)*omega   cos(omega*length)        0                          0 ;...
              0                         0                        cosh(omega*length)         sinh(omega*length)/omega ;...
              0                         0                        sinh(omega*length)*omega   cosh(omega*length) ];

    end
    
    if k1 < 0
        
        omega = sqrt(-k1);
    
        m = [ cosh(omega*length)         sinh(omega*length)/omega  0                          0 ;...
              sinh(omega*length)*omega   cosh(omega*length)        0                          0 ;...
              0                         0                        cos(omega*length)         sin(omega*length)/omega ;...
              0                         0                       -sin(omega*length)*omega   cos(omega*length) ];

    end
end

