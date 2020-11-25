function [ m ] = TransferMatrixDrift( length )
%TransferMatrixDrift returns the transfer matrix for a drift
%   Detailed explanation goes here

    m = [1    length  0    0      ;...
         0    1       0    0      ;...
         0    0       1    length ;...
         0    0       0    1 ]    ;

end

