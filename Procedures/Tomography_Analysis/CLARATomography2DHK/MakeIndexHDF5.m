clear

dirname    = '../Data 2019-03-04';
configfile = 'ImageFileInformation.mat';

load([dirname '/' configfile]);

dset = Image_and_background_filenames_at_observation_point;
dset_details.Location = '/BeamImageFilenames';
dset_details.Name = 'ObservationPoint';

attr = 0.0181;
attr_details.Name = 'Calibration factor';
attr_details.AttachedTo = '/BeamImageFilenames/ObservationPoint';
attr_details.AttachType = 'dataset';

hdf5write('QuadScanIndex.hdf5', dset_details, dset, attr_details, attr);

dset = Image_and_background_filenames_at_reconstruction_point;
dset_details.Location = '/BeamImageFilenames';
dset_details.Name = 'ReconstructionPoint';

attr = 0.0122;
attr_details.Name = 'Calibration factor';
attr_details.AttachedTo = '/BeamImageFilenames/ReconstructionPoint';
attr_details.AttachType = 'dataset';

hdf5write('QuadScanIndex.hdf5', dset_details, dset, attr_details, attr, 'WriteMode', 'append');

hdf5write('QuadScanIndex.hdf5', '/MachineSettings/QuadrupoleCurrents', QuadCurrents','WriteMode','append');

hdf5write('QuadScanIndex.hdf5', '/MachineSettings/BeamMomentum', 29.5,'WriteMode','append');

QuadCalibration = importdata('QuadCalibration.txt');

hdf5write('QuadScanIndex.hdf5', '/MachineSettings/QuadrupoleCalibration', QuadCalibration','WriteMode','append');
