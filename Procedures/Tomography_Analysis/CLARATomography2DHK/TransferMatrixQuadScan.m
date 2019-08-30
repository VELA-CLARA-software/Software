function [ m ] = TransferMatrixQuadScan( qstrengths )
%TransferMatrixCLARA returns the transfer matrix for CLARA
%   Detailed explanation goes here

    qfringe = 0.0250;
    qlength = 0.1007 + qfringe;

    dlen1   = 0.165967 - qfringe/2;
    dlen2   = 0.299300 - qfringe;
    dlen3   = 0.712450 - qfringe;
    dlen4   = 0.181183 - qfringe/2;

    mq3 = TransferMatrixQuad(qstrengths(3),qlength);
    mq4 = TransferMatrixQuad(qstrengths(4),qlength);
    mq5 = TransferMatrixQuad(qstrengths(5),qlength);

    md1 = TransferMatrixDrift(dlen1);
    md2 = TransferMatrixDrift(dlen2);
    md3 = TransferMatrixDrift(dlen3);
    md4 = TransferMatrixDrift(dlen4);
    
    m   = md4*mq5*md3*mq4*md2*mq3*md1;
    
end

