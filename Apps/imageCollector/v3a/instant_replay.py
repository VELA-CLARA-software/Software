from epics import PV
from datetime import datetime
import numpy as np
import h5py
import sys
import os
import click
import imageio
import colorcet

def status_msg(timestamp):
    return '[{}] Acquiring images into rolling buffer. Press ENTER to stop.'.format(timestamp.strftime('%H:%M:%S'))


def callback(pvname, value, *args, **kwargs):
    global buffer_pos, data_buffer, time_buffer
    data_buffer[buffer_pos] = value
    timestamp = datetime.now()
    time_buffer[buffer_pos] = timestamp
    buffer_pos = (buffer_pos + 1) % buffer_len
    if buffer_pos == 0:
        sys.stdout.write('\r' + status_msg(timestamp))
        sys.stdout.flush()


buffer_len = click.prompt('Enter size of buffer', type=int, default=100)

hdf5_image_folder = r'\\claraserv3\CameraImages'
# for CLARA cameras
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1280
data_buffer = np.zeros((buffer_len, IMAGE_WIDTH * IMAGE_HEIGHT), 'int32')
time_buffer = [None] * buffer_len
buffer_pos = 0

camdata = PV('CLA-C2V-DIA-CAM-01:CAM2:ArrayData', auto_monitor=True, callback=callback)

# Wait for ENTER to be pressed
raw_input(status_msg(datetime.now()))
camdata.clear_callbacks()

t0 = time_buffer[buffer_pos]
prev_pos = (buffer_pos - 1) % buffer_len
t1 = time_buffer[prev_pos]
dt = t1 - t0
print dt.total_seconds(), 'seconds of images captured'

save_it = click.confirm('Save as HDF5 stack?', default=True)

data_buffer = np.reshape(data_buffer, (buffer_len, IMAGE_HEIGHT, IMAGE_WIDTH))
folder = hdf5_image_folder + t1.strftime(r'\%Y\%#m\%#d')  # omit leading zeros from month and day
try:
    os.makedirs(folder)
except OSError as e:
    if e.errno != 17:  # dir already exists
        raise
save_filename = r'{}\{}_{}_{}images.hdf5'.format(folder, 'C2V-CAM-01', t1.strftime('%Y-%#m-%#d_%#H-%#M-%#S'), buffer_len)
print 'Saving to', save_filename
with h5py.File(save_filename, 'w') as hdf5_file:
    for i in range(buffer_len):
        hdf5_file.create_dataset('Capture%06d' % i, data=np.array(data_buffer[(i + buffer_pos) % buffer_len], dtype='uint16'))


# imageio.mimwrite(save_filename + '.mp4', np.array(data_buffer, dtype='uint16'), fps=int(buffer_len / dt.total_seconds()))

