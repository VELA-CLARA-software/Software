from epics import PV
from datetime import datetime
import numpy as np
import h5py

def callback(pvname, value, *args, **kwargs):
    global buffer_pos, data_buffer, time_buffer
    data_buffer[buffer_pos] = value
    time_buffer[buffer_pos] = datetime.now()
    buffer_pos = (buffer_pos + 1) % buffer_len
    if buffer_pos == 0:
        print 'New buffer started. Press ENTER to stop acquiring.'

hdf5_image_folder = r'\\claraserv3\CameraImages'
buffer_len = 100
# for CLARA cameras
IMAGE_WIDTH = 1080
IMAGE_HEIGHT = 1280
data_buffer = np.zeros((buffer_len, IMAGE_WIDTH * IMAGE_HEIGHT), 'int32')
time_buffer = [None] * buffer_len
buffer_pos = 0

camdata = PV('CLA-C2V-DIA-CAM-01:CAM2:ArrayData', auto_monitor=True, callback=callback)

raw_input('Press ENTER to stop acquiring:\n')
camdata.clear_callbacks()

t0 = time_buffer[buffer_pos]
prev_pos = (buffer_pos - 1) % buffer_len
t1 = time_buffer[prev_pos]
dt = t1 - t0
print dt.total_seconds(), 'seconds of images captured'

# data_buffer = np.reshape(data_buffer, (buffer_len, IMAGE_HEIGHT, IMAGE_WIDTH))
timestamp = datetime.now()
folder = hdf5_image_folder + timestamp.strftime(r'\%Y\%#m\%#d')  # omit leading zeros from month and day
save_filename = r'{}\{}_{}_{}images.hdf5'.format(folder, 'C2V-CAM-01', timestamp.strftime('%Y-%#m-%#d_%#H-%#M-%#S'), buffer_len)
print 'Saving to', save_filename
with h5py.File(save_filename, 'w') as hdf5_file:
    for i in range(buffer_len):
        hdf5_file.create_dataset('Capture%06d' % i, data=np.array(data_buffer[(i + buffer_pos) % buffer_len], dtype='uint16'))

