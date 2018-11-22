function [deconvolutionFilter] = DeconvolutionFilter(folder,noiseFile,singlePhotonFile,blackmanSize)
    % Read in data
    noiseData = importdata([folder noiseFile]);
    singlePhotonData = importdata([folder singlePhotonFile]);

    % Format data
    numberOfDataPoints = length(noiseData);
    noiseIntensity = noiseData(:,2);
    singlePhotonIntensity = singlePhotonData(:,2);

    % Fourier transform
    noiseFT = fft(noiseIntensity);
    singlePhotonFT = fft(singlePhotonIntensity);

    % Wiener filter
    wienerFilter = (abs(singlePhotonFT).^2) ./ ( abs(singlePhotonFT).^2 + abs(noiseFT).^2 );

    % Blackman window
    blackmanWindow = blackman(blackmanSize);
    blackmanWindow(numberOfDataPoints) = 0;
    blackmanWindowFT = fft(blackmanWindow);

    % Deconvolution Filter
    deconvolutionFilter = ifft( (blackmanWindowFT./singlePhotonFT).* wienerFilter );
end