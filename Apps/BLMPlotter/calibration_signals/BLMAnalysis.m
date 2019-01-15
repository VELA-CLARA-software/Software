c = 299792458;
n = 1.46;
vFibre = c/n;
vElectron = c;
% Input upstream data
folderUpstream = 'D:\VELA-CLARA_software\Software\Apps\BLMPlotter\calibration_signals';
noiseUpstreamFile = '\C18 december noise00000.dat';
singlePhotonUpstreamFile = '\C18 december 1 photon00000.dat';
peaksUpstreamFile = '\C2blmfromthebeam00005 S02 YAG02.dat';
blackmanUpstreamSize = 100;
peakThresholdUpstream = 0.01;
peakMinSeparationUpstream = 5e-9;

% Input downstream data
folderDownstream = 'D:\VELA-CLARA_software\Software\Apps\BLMPlotter\calibration_signals';
noiseDownstreamFile = '\C18 december noise00000.dat';
singlePhotonDownstreamFile = '\C18 december 1 photon00000.dat';
peaksDownstreamFile = '\C3blmfromthebeam00006 S02 YAG02.dat';
blackmanDownstreamSize = 100;
peakThresholdDownstream = 0.01;
peakMinSeparationDownstream = 5e-9;

% Format upstream data
peaksUpstreamData = importdata([folderUpstream peaksUpstreamFile]);
peaksUpstreamIntensity = peaksUpstreamData(:,2);
peaksUpstreamTime = peaksUpstreamData(:,1);
peaksUpstreamTime = peaksUpstreamTime - abs(min(peaksUpstreamTime));

% Format downstream data
peaksDownstreamData = importdata([folderDownstream peaksDownstreamFile]);
peaksDownstreamIntensity = peaksDownstreamData(:,2);
peaksDownstreamTime = peaksDownstreamData(:,1);
peaksDownstreamTime = peaksDownstreamTime - abs(min(peaksDownstreamTime));

% Filter upstream data
%deconvolutionUpstreamFilter = DeconvolutionFilter(folderUpstream,noiseUpstreamFile,singlePhotonUpstreamFile,blackmanUpstreamSize);
filteredUpstreamData = peaksUpstreamIntensity.*1;

% Filter downstream data
%deconvolutionDownstreamFilter = DeconvolutionFilter(folderDownstream,noiseDownstreamFile,singlePhotonDownstreamFile,blackmanDownstreamSize);
filteredDownstreamData = peaksDownstreamIntensity.*1;

% Plot
figure();
hold on;
plot(peaksUpstreamTime,filteredUpstreamData,peaksUpstreamTime,filteredDownstreamData);
grid on;
grid minor;
xlim([0,2e-6]);

% Peak locations
% [peaksUpstreamValues,peaksUpstreamLocations] = findpeaks(filteredUpstreamData,peaksUpstreamTime,'MinPeakHeight',peakThresholdUpstream,'MinPeakDistance',peakMinSeparationUpstream);
% [peaksDownstreamValues,peaksDownstreamLocations] = findpeaks(filteredDownstreamData,peaksDownstreamTime,'MinPeakHeight',peakThresholdDownstream,'MinPeakDistance',peakMinSeparationDownstream);
[peaksUpstreamValues, peaksUpstreamLocations] = max(filteredUpstreamData);
[peaksDownstreamValues, peaksDownstreamLocations] = max(filteredDownstreamData);

% Time delay calculation !!!Assuming length(peaksUpstreamValues) = length(peaksDownstreamValues)
deltaT = zeros(length(peaksUpstreamValues),1);

for i=1:length(peaksUpstreamValues)
    deltaT(i) = peaksUpstreamTime(peaksUpstreamLocations(i)) - peaksDownstreamTime(peaksDownstreamLocations(i));
end

% Position calculation
deltaX = deltaT.*vFibre;
calibrationTime = deltaX./vElectron;
display(deltaT);
display(deltaX);
display(calibrationTime);