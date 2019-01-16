import sys
import argparse

# Prints differences between two BURT files
# run as python BURTcomparison.py filename1 filename2
# primarily it's to compare on/off setting and set values
# it can also compare read values but will print out loads...

parser = argparse.ArgumentParser(description='Prints differences between two BURT files')
parser.add_argument('file1')
parser.add_argument('file2')
parser.add_argument('-r','--readdiffs', default=0, type=int)

def readfile(file):
    dict = {}
    # read in entire file
    with open(file) as burt_file:
        content = burt_file.readlines()
    # look for the lines with required format and add to dict
    # [assumed to be those with 4 data points, when split by colon]
    for i, line in enumerate(content):
        content_split = line.split(':')
        if len(content_split) == 4:
            stripstring = '\n\r\w;'
            dict[content_split[0]] = [content_split[1].strip(stripstring), content_split[2].strip(stripstring), content_split[3].strip(stripstring)]
    return dict

def main():
    args = parser.parse_args()
    printreaddiffs = args.readdiffs # set !=0 to compare read diffs
    file1 = args.file1
    file2 = args.file2

    # read both BURT files into dicts
    burt1_dict = readfile(file1)
    burt2_dict = readfile(file2)

    # compare the two dictionaries and print any differences
    template = "{0:25}{1:17}{2:15}{3:15} --> {4:15}"
    for key, value in sorted(burt1_dict.items()):
        if burt1_dict[key][0] != burt2_dict[key][0]:
            # print 'ON/OFF DIFFERENCE:','\t', key,'\t', burt1_dict[key][0], '\t', burt2_dict[key][0]
            print template.format('ON/OFF DIFFERENCE:', key, burt1_dict[key][0], burt2_dict[key][0])
        if burt1_dict[key][1] != burt2_dict[key][1]:
            # print 'SET VALUE DIFFERENCE:','\t', key,'\t', burt1_dict[key][1], '\t', burt2_dict[key][1]
            print template.format('SET VALUE DIFFERENCE:', key, burt1_dict[key][1], burt2_dict[key][1], float(burt1_dict[key][1]) - float(burt2_dict[key][1]))
        if printreaddiffs and burt1_dict[key][2] != burt2_dict[key][2]:
            # print 'READ VALUE DIFFERENCE:', '\t', key,'\t', burt1_dict[key][2], '\t', burt2_dict[key][2]
            print template.format('READ VALUE DIFFERENCE:', key, burt1_dict[key][2], burt2_dict[key][2], float(burt1_dict[key][2]) - float(burt2_dict[key][2]))

if __name__ == '__main__':
   main()
