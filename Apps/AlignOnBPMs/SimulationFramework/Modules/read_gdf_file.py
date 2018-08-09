"""Reads in files from General Particle Tracer .gdf files
"""
from __future__ import division
# from pylab import *
import time
import struct
import os
import sys
import numpy as np

#Constants
GDFNAMELEN = 16;                 #Length of the ascii-names
GDFID  = 94325877;               #ID for GDF

#Data types
t_ascii  = int('0001', 16)       #ASCII character
t_s32    = int('0002', 16)       #Signed long
t_dbl    = int('0003', 16)       #Double
t_undef  = int('0000', 16)       #Data type not defined
t_null	 = int('0010', 16)       #No data
t_u8	 = int('0020', 16)       #Unsigned char
t_s8	 = int('0030', 16)       #Signed char
t_u16	 = int('0040', 16)       #Unsigned short
t_s16	 = int('0050', 16)       #Signed short
t_u32	 = int('0060', 16)       #Unsigned long
t_u64	 = int('0070', 16)       #Unsigned 64bit int
t_s64	 = int('0080', 16)       #Signed 64bit int
t_flt	 = int('0090', 16)       #Float

#Block types
t_dir    = 256      # Directory entry start
t_edir   = 512      # Directory entry end
t_sval   = 1024      # Single valued
t_arr    = 2048      # Array

class grab_group(object):

    def __init__(self, name):
        self.name = name
        self.attrs = {}
        self.groups = {}

    def create_group(self, name):
        self.groups[name] = self.group(name)
        return self.groups[name]

    class group(object):

        def __init__(self, name):
            self.name = name
            self.datasets = []

        def create_dataset(self, name, data=()):
            self.datasets.append(name)
            setattr(self,name, data)

class read_gdf_file(object):
###############################################################################

    def create_grab_group(self, name):
        self.grab_groups[name] = grab_group(name)
        return self.grab_groups[name]

    @property
    def positions(self):
        positions = []
        for datagrab in self.grab_groups.values():
            if hasattr(datagrab.groups['param'],'position'):
                positions.append(datagrab.groups['param'].position)
        return positions

    def get_position(self, position):
        for datagrab in self.grab_groups.values():
            if hasattr(datagrab.groups['param'],'position'):
                if str(datagrab.groups['param'].position) == str(position):
                    return datagrab.groups['data']
    @property
    def times(self):
        times = []
        for datagrab in self.grab_groups.values():
            if hasattr(datagrab.groups['param'],'time'):
                times.append(datagrab.groups['param'].time)
        return times

    def get_time(self, time):
        for datagrab in self.grab_groups.values():
            if hasattr(datagrab.groups['param'],'time'):
                if str(datagrab.groups['param'].time) == str(time):
                    return datagrab.groups['data']
    def get_grab(self, grab_group_number=0):
        for name, datagrab in self.grab_groups.items():
            if name == 'datagrab_' + str(grab_group_number):
                return datagrab.groups['data']

    def __init__(self, filename):
        self.attrs = {}
        self.grab_groups = {}
        self.filename = filename

        with open(self.filename, 'rb') as f:   #Important to open in binary mode 'b' to work cross platform

            #Read the GDF main header

            gdf_id_check = struct.unpack('i', f.read(4))[0]
            if gdf_id_check != GDFID:
                raise RuntimeWarning('File is not a .gdf file')

            self.attrs['time_created'] = struct.unpack('i', f.read(4))[0]

            #get creator name and use string part upto zero-character
            creator = list(f.read(GDFNAMELEN))
            creator = [struct.unpack('B', element)[0] for element in creator]
            creator_name = []
            for element in creator:
                if element is 0:
                    break
                else:
                    creator_name.append(chr(element))
            self.attrs['creator_name'] = creator_name
           #get destination and use string part upto zero-character
            dest = f.read(GDFNAMELEN)
            dest = [struct.unpack('B', element)[0] for element in dest]
            destination = []
            for element in dest:
                if element is 0:
                    break
                else:
                    destination.append(chr(element))
            self.attrs['destination'] = ''.join(destination)

            #get other metadata about the GDF file
            major = struct.unpack('B', f.read(1))[0]
            minor = struct.unpack('B', f.read(1))[0]
            self.attrs['gdf_version'] = str(major) + '.' + str(minor)

            major = struct.unpack('B', f.read(1))[0]
            minor = struct.unpack('B', f.read(1))[0]
            self.attrs['creator_version'] = str(major) + '.' + str(minor)

            major = struct.unpack('B', f.read(1))[0]
            minor = struct.unpack('B', f.read(1))[0]
            self.attrs['destination_version'] = str(major) + '.' + str(minor)

            f.seek(2, 1)   # skip to next block

            #Create first hdf group and sub groups for data to be put into
            #First group is called "datagrab" because it could be output at a particular time, or the projection at a particular position
            grab_group_number = 0
            grab_group = self.create_grab_group('datagrab_' + str(grab_group_number))
            grab_group.attrs['grab_number'] = grab_group_number
            data_group = grab_group.create_group('data')
            param_group = grab_group.create_group('param')

            #Read GDF data blocks
            lastarr = False
            while True:
                if f.read(1) == '':
                    break
                f.seek(-1, 1)

                #Read GDF block header
                name = f.read(16)
                typee = struct.unpack('i', f.read(4))[0]
                size = struct.unpack('i', f.read(4))[0]

                #Get name
                import string
                printable = set(string.printable)

                def find_name(name):
                    found_str = ""
                    for char in name:
                        if char in printable:
                            found_str += char
                        elif len(found_str) >= 1:
                            return found_str
                        else:
                            found_str = ""
                name = str(find_name(name))
                name = name

                #Get block type
                dir  = int(typee & t_dir > 0)
                edir = int(typee & t_edir > 0)
                sval = int(typee & t_sval > 0)
                arr  = int(typee & t_arr > 0)

                #Get data type
                dattype = typee & 255

                #Check if array block is finished
                if lastarr and not arr:
                    #We save the stuff as we go rather than storing it in local dictionaries and creating all the groups at the end. Here we make the groups for next time step, as this code only runs when all data current block has been extracted
                    grab_group_number += 1
                    grab_group = self.create_grab_group('datagrab_' + str(grab_group_number))
                    grab_group.attrs['grab_number'] = grab_group_number
                    data_group = grab_group.create_group('data')
                    param_group = grab_group.create_group('param')

                #Read single value
                if sval:
                    if dattype == t_dbl:
                        # print 'new dbl = ', name
                        value = struct.unpack('d', f.read(8))[0]
                        # print '    dbl = ', value
                        param_group.create_dataset(name, data=value)
                    elif dattype == t_null:
                        # print 'new null = ', name
                        pass
                    elif dattype == t_ascii:
                        # print 'new ascii = ', name
                        value = str(f.read(size))
                        value = value.strip(' \t\r\n\0')
                        # print '    ascii = ', value
                        try:
                            param_group.create_dataset(name, data=value)
                        except RuntimeError:
                            del param_group[name]
                            param_group.create_dataset(name, data=value)
                    elif dattype == t_s32:
                        # print 'new s32 = ', name
                        value = struct.unpack('i', f.read(4))[0]
                        param_group.create_dataset(name, data=value)
                    else:
                        print 'unknown datatype of value!!!'
                        print 'name=', name
                        print 'type=', typee
                        print 'size=', size
                        value = f.read(size)

                #Read data array
                if arr:
                    if dattype == t_dbl:
                        if (size % 8) != 0:
                            raise RuntimeWarning('Tried to save an array of doubles, but the array size is not consistant with that of doubles.')
                        value = np.fromfile(f, dtype=np.dtype('f8'), count=int(size/8))
                        data_group.create_dataset(name, data=value)
                        # print 'new dataset = ', name
                    else:
                        print 'unknown datatype of value!!!'
                        print 'name=', name
                        print 'type=', typee
                        print 'size=', size
                        value = f.read(size)

                lastarr = arr;
        f.close()
