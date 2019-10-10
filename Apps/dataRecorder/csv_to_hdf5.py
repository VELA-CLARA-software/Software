import sys
import os
import csv
import h5py
sys.path.append("../../../")
import Software.Utils.dict_to_h5 as dict_to_h5
import argparse
from glob import glob
import split_file as splitfile

parser = argparse.ArgumentParser(description='Convert a dataRecorder CSV file to HDF5')
parser.add_argument('inputfile', metavar='CSV input file',
                   help='CSV file containing the data')
parser.add_argument('-c', '--chunksize', default=5*10**6, help='Set chunk file size', type=int)


def add_data_to_dict(data, dict):
    if len(data) == 3:
        name, x, y = data
        x = float(x)
        y = float(y)
        if name not in dict:
            dict[name] = []
        dict[name].append([x,y])

def read_data_into_dict(reader):
    datadict = {}
    for row in reader:
        if isinstance(row,(str)):
            subreader = csv.reader(row.split('\n'), delimiter=',')
            for subrow in subreader:
                add_data_to_dict(subrow, datadict)
        else:
            add_data_to_dict(row, datadict)
    return datadict

def load_csv_file(filename):
    data = {}
    with open(filename,"r") as csv_file:
        csv_reader = csv.reader(csv_file, csv.QUOTE_NONE, delimiter=',')
        return read_data_into_dict(csv_reader)

def convert_csv_to_hdf5(filename):
    datadict = load_csv_file(filename)
    pre, ext = os.path.splitext(filename)
    dict_to_h5.save_dict_to_hdf5(datadict, pre + '.hdf5')

def convert_csv_to_hdf5_chunks(filename, chunksize=5*10**6):
    print '\tChunking data!'
    pre, ext = os.path.splitext(filename)
    with open(filename) as bigfile:
        for i, lines in enumerate(splitfile.chunks(bigfile, chunksize)):
            file_split = '{}.{}'.format(pre, i)+'.hdf5'
            datadict = read_data_into_dict(lines)
            print '\t\tSaving HDF5 file: ', file_split
            dict_to_h5.save_dict_to_hdf5(datadict, file_split)

if __name__ == '__main__':
    args = parser.parse_args()
    for filename in glob(args.inputfile):
        print 'Converting ', filename, ' to HDF5'
        if os.path.getsize(filename) > 1024*1024*500:
            convert_csv_to_hdf5_chunks(filename, args.chunksize)
        else:
            convert_csv_to_hdf5(filename)
