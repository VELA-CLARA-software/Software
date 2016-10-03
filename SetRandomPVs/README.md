Instructions for SetRandomPVs

Introduction

EPICS process variables (PVs) in the VELA/CLARA virtual machine will only change value when the user tells them to, 
unlike in the real machine, in which signals are sent from diagnostic devices to update the PVs. In order to help 
virtual machine users to write applications which will monitor changing parameters on the real machine, a package 
has been created in Python which will allow users to set random PV values within a given range, and at a given 
repetition rate.

randomPVs.py Package

This program is currently located in \\fed.cclrc.ac.uk\Org\NLab\ASTeC\Projects\VELA\Software\Python\SetRandomPVs\Package.
There is only one function which will be of use to users: "setPV". It takes the following as arguments:

- pvName (string): the name of the VM PV to which random values will be written.
- rangeSta and rangeEnd (double): the upper and lower bounds of values for the PV.
- numShots (int): number of shots to be written (a negative number will set the process running indefinitely)
- repRate (int): rate at which values will be written to the PV.
- pvType (string): a flag to indicate whether the EPICS PV will accept numbers or arrays (given as "num" or "array").
This program currently only supports the writing of single values to a PV, so RF or scope traces cannot be written, but
some PVs, such as BPM X and Y values, require an array to be sent to EPICS.

Any number of PVs can be set simultaneously in this way, with synchronisation down to ~1ms. An example program to demonstrate
the implementation of this package can be found in test.py in the Package folder. This method can be integrated into
any program which requires a changing PV to be monitored.

GUI

A GUI has also been created to help users to understand how this program is implemented. Most of the buttons, etc. should
be self-explanatory. If you have any further questions, ask me (Alex Brynes).