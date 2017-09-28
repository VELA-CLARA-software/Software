# Written by Michael Sullivan (Ogden Trust Internship)
# July-August 2017

# This class takes in a txt file of instructions (variables) which will be used to run simulations on either the virtual
# or physical machine.  The Reader stores the raw data of the text file into a dictionary, which can be searched for
# certain keywords to extract relevant data
# Functions also exist to verify the information in the txt file for consistency
# A Reader object will be passed to the Master Controller to set the variables via the various controllers in the system

# This is the reader class for the txt file in the format of "Instructions2.txt"

class worker(object):

    def __init__(self):
        print "An empty worker object has been created!"
