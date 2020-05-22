25th March 2019
-Submit around 1940
A version with colour scale and message window. NOT SURE if it works in practice, but uses signals slots to separate gui from procedure. i.e. scanner.py should be able to run/import independently. 

25th March 2019. Submit around 2000
THIS IS NOT AN EVOLUTION OF THE PREVIOUS VERSION.
This is the exact set of files used for doing the laser virtual cathode scans  which were performed on the Thu 14-Mar-19 08:41 log #846. The script was modified on the day to take averages of quantities rather than instantaneous values. The GUI is simply with no logging message window and very little information.    

26th March 2019, 11:30
!!!!PLEASE NOTE:  UNTESTED!!!!!.
Added monitoring of second photodiode at cathode position CLA-LAS-DIA-EM-02:E for laser/mirror/cathode studies. 

26th March 2019, 12:00
!!!!PLEASE NOTE:  UNTESTED!!!!!.
Trivial modification to previous version to save VC images at each grid point in the scan.

26th March 2019, ~13:00
!!!!PLEASE NOTE:  UNTESTED and likely needs debugging!!!!.
Added saving of an addition CLARA camera image at each VC gridpoint. This camera will be placed at the cathode position. It is highly likely that this version will need debugging. 

26th March 2019, ~18:00
!!!!PLEASE NOTE:  UNTESTED and likely needs debugging!!!!.
Added mathematica notebook to plot scan data. But did not update this README file

26th March 2019, ~18:05
!!!!PLEASE NOTE:  UNTESTED and likely needs debugging!!!!.
Updated the README file. 

27th March 2019, ~1500
First time used succesfully. Tested the changes of the previous versions by doing a scan with cathode removed and photodiode in place. Seemed to work OK  

28th March 2019, ~0030
Just saving a version of the code used at the end of the day on 27th March, also added the MMA notebook used to plot results.  

28th March 2019, ~2150
Saving a version of the code + MMA used at the end of the day on 28th March. Changes from 27th March included different way of reading the laser photodiode signals and thus different PVs for these. Also change to get means/stdevs within same loop to speed up. And scan ranges changed slightly.   

4th April 2019, ~1530
After 28th March, there were more scans on 29th March. On this day, the photodiode at the cathode was moved to allow a large scan range to all fit on the photodiode (on previous days we'd fallen off the edge of the photodiode). In the morning of 29th there were two scans with this new photodiode position at 1051 and 1153. THEN THE NEW light box mirror put in place. Everything was still at air pressure. One scan was completed at 1404 with the new light box mirror. 

13th May 2020
code from previous version semi-upgraded to python3/pqt5 and placed in directory \pre2020code. 
main app files/functions now from from 25th March 2019 - more advanced GUI, with color legend and message box   
Contains syntax for getting LLRF traces getting.
Writes results to workfolder.
No data/app history from 2019/20 gun upgrade is saved to the github repo. They stay on sever at \\apclara1.dl.ac.uk\ControlRoomApps\Stage\Software\Apps\qscan. 

13th May 2020
added code (courtesy of Duncan) to get scan information all through PI laser controller.

15th May 2020
Scan parameters inputs added to GUI as spin boxes. 