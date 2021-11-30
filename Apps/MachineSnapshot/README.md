# Machine Snapshot

Simple GUI for saving a snapshot of the state of CLARA

Date created: 02/08/2021.

<!-- Procedure -->
## Procedure

This app uses the [MachineState](https://github.com/VELA-CLARA-software/Software/tree/master/Utils/MachineState) functions in Python to create a snapshot of CLARA using the [CATAP](https://gitlab.stfc.ac.uk/ujo48515/catapillar) libraries

The user only has to input the RF crest phases for the gun and linac and click the "Save Snapshot" button.

Files containing the machine settings will be written automatically to claraserv3: \\claraserv3\claranet\apps\dev\logs\machineSnapshot. Depending on the location from which the app is run, the snapshot files will appear in the 'dev', 'stage', etc... folder, with a timestamp.

<!-- App structure -->
## App structure

The app consists only of one Python file, containing some GUI buttons and a function which links to the MachineState scripts.

The only thing which may have to be updated are the file locations for the RF power -> momentum gain data. These measurements may be improved, and so we can update these files in due course. For now, the calibrations appear to agree well with the measurements.

<!-- CONTACT -->
## Contact

Alex Brynes - alexander.brynes@stfc.ac.uk