# Charge Measurement

App for scanning wall current monitor charge as a function of photoinjector laser pulse energy.

Date created: 03/12/2020.

<!-- Procedure -->
## Procedure

This app uses the [CATAP](https://gitlab.stfc.ac.uk/ujo48515/catapillar) library to control and monitor the CLARA photoinjector. The user sets a range to scan the photoinjector laser half-wave plate, and the app will monitor the wall current monitor and the laser pulse energy.

Once the measurement is complete, the charge extracted as a function of pulse energy (in pC/uJ) is calculated by means of a linear fit, and using this value with some calibration factors for the laser, a calculation of the effective quantum efficiency (QE) is made. For more details on the procedure, see [this report](https://stfc365.sharepoint.com/:w:/r/sites/CLARAWorkflow/_layouts/15/Doc.aspx?sourcedoc=%7B23751CA9-A99F-4536-B58B-6C14719687EC%7D&file=VELA-EN-20200312%20-%20Charge%20measurements.docx&action=default&mobileredirect=true).

The user should set the range of half-wave plate values such that the initial bunch charge is not lower than 20pC. It is expected that at some point (beyond a bunch charge of ~250pC), the linear relationship between laser pulse energy and bunch charge will not hold due to space-charge blowout. This has not yet been observed experimentally with this app.

In order to keep a consistent record of all photoinjector parameters that could potentially impact the bunch charge, the app also records the RF phase and forward power, magnet settings, and laser position and intensity on the virtual cathode.

The data recorded by the app is saved in three different file types:
* Log data. This provides a record of what happened while the app was running.
* Measurement data. This stores all of the raw data recorded during the measurement in a .json file for post-processing.
* Summary data. The main results of every QE measurement (if the user chooses to save it) is stored in an excel spreadsheet for quick comparisons of changes in the QE over time.

<!-- App structure -->
## App structure

The app roughly follows the model-view-controller structure.

### base

This is the base class to which all hardware objects and monitors have access. 

### controllers

All of the hardware types which are monitored use a separate file, which can be accessed through the file ```controller_base.py```.
Monitors and controllers are linked through the ```main_controller.py``` file. This file links together the GUI, monitors and controllers, and contains the procedure for controlling and monitoring the photoinjector laser.

### data

All of the data that is recorded by the app is stored in a dictionary -- via ```charge_measurement_data_base.py``` that can be accessed by all of the classes within the app.
This folder also contains classes for reading the config file, and for saving data to log files.

### data_monitors

The classes within this folder are used for monitoring hardware objects via CATAP.

### gui

This contains the GUI, and handles the plots.

### config

This file contains the PV names to be monitored, along with locations for the log, data and summary files. 

<!-- CONTACT -->
## Contact

Alex Brynes - alexander.brynes@stfc.ac.uk

Project Link: [https://gitlab.stfc.ac.uk/clara-control-room-applications/charge-measurement](https://gitlab.stfc.ac.uk/clara-control-room-applications/charge-measurement)