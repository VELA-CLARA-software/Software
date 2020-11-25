function FieldVals = I2K_CLARA(Ilist, p0_MeVc)

% Mimics MagnetTable.exe : goes from currents to K values, for given ref
 % momentum (in MeV/c).  Inverse of K2I_CLARA

if nargin<2
    p0_MeVc = 30;  % Momentum in MeV/c
%     disp('Default momentum: 30MeV/c');
end

c = 2.99792458e8;
% Data for 'S02-QUAD1' - 'S02-QUAD5' from C2BMagnets.txt%%%%%%%%%%%%%%%%%%%
lengths = [128.68478212775, 126.817287248819, ...
    127.241994829126, 127.421664936758, 127.162566301558]/1000;
field_integral_coeffs_PosI = ...
    [-2.23133410405682E-10, 4.5196171252132E-08, -3.46208258004659E-06, ...
    1.11195870210961E-04, 2.38129337415767E-02, 9.81229429460256E-03;... %1
     -4.69068497199892E-10, 7.81236692669882E-08, -4.99557108021749E-06,...
     1.39687166906618E-04, 2.32819099224878E-02, 9.77695097574923E-03;... %2
    -4.01132756980213E-10, 7.04774652367448E-08, -4.7303680012511E-06,...
    1.37571730391246E-04, 2.33327839789932E-02, 9.49568371388574E-03; ...%3
    -3.12868198002574E-10, 5.87771428279647E-08, -4.18748562338666E-06,...
    1.27524427731924E-04, 2.34218216296292E-02, 9.38588316008555E-03; ...%4
    -3.12232013228657E-10, 5.86576256524889E-08, -4.17897080912429E-06,...
    1.27265120139323E-04, 2.33741958038237E-02, 9.36679794786415E-03]; %5

% For negative I, orig python script inverted the polynomial coefficients,
% apart from the zero order one.  This is treated here as the offset.
Offsets = squeeze(field_integral_coeffs_PosI(:,end));
field_integral_coeffs_noOffset = field_integral_coeffs_PosI;
field_integral_coeffs_noOffset(:,end) = 0;


% Divide current up into arrays of negative and positive values (with zeros
% corresponding to "wrong" sign)
[Ineg, Ipos] = deal(Ilist);
Ineg(Ineg>0)=0;
Ipos(Ipos<0)=0;

% generate field integral data from polynomial coefficients: start with
% offsets

FieldVals = ones(size(Ilist,1),1)*Offsets';  % n * 5 table, start with zero order vals

% return
for n = 1:5  % For each quadrupole...
    
    p0loverc = p0_MeVc*1e6*lengths(n)/c; % ref mom(MeV/c) * length(m) / c 
    

    FieldVals(:,n) = (FieldVals(:,n) + ...
        polyval(-field_integral_coeffs_noOffset(n,:),abs(Ineg(:,n))) + ...
        polyval(field_integral_coeffs_noOffset(n,:),Ipos(:,n)))/p0loverc; 
    
    
end

end

