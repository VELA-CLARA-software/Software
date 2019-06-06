import os
from itertools import chain, islice
import argparse

parser = argparse.ArgumentParser(description='Split a large file into smaller chunks')
parser.add_argument('inputfile', metavar='Large input file',
                   help='CSV file containing the data')
parser.add_argument('-c', '--chunksize', default=5*10**6, help='Set chunk file size', type=int)

def chunks(iterable, n):
   "chunks(ABCDE,2) => AB CD E"
   iterable = iter(iterable)
   while True:
       # store one line in memory,
       # chain it to an iterator on the rest of the chunk
       yield chain([next(iterable)], islice(iterable, n-1))

def split_file(filename, chunksize=5*10**6):
    l = chunksize
    file_large = filename
    outputfilenames = []
    print 'Splitting file:'
    with open(file_large) as bigfile:
        for i, lines in enumerate(chunks(bigfile, l)):
            pre, ext = os.path.splitext(filename)
            file_split = '{}.{}'.format(pre, i)+ext
            with open(file_split, 'w') as f:
                print '\tCreating file: ', file_split
                f.writelines(lines)
                outputfilenames.append(file_split)
    return outputfilenames

if __name__ == '__main__':
    args = parser.parse_args()
    split_file(args.inputfile, args.chunksize)
