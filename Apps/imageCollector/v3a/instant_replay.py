from epics import PV
from datetime import datetime
import numpy as np
import h5py
import sys
import os
import click
import ffmpeg  # ffmpeg-python
import colorcet
from collections import OrderedDict
from time import sleep
import msvcrt
sys.path.append(r'\\apclara1.dl.ac.uk\ControlRoomApps\Controllers\bin\Release')
# sys.path.append(r'..\..\..') # \Widgets\MachineSnapshot')
os.environ['PATH'] = os.environ['PATH'] + r';\\apclara1.dl.ac.uk\ControlRoomApps\Controllers\bin\stage\root_v5.34.34\bin'
import VELA_CLARA_Camera_Control
import VELA_CLARA_Screen_Control
cam_init = VELA_CLARA_Camera_Control.init()
scr_init = VELA_CLARA_Screen_Control.init()
cam_ctrl = cam_init.physical_Camera_Controller()
scr_ctrl = scr_init.physical_C2B_Screen_Controller()
camera_names = cam_ctrl.getCameraNames()
screen_names = cam_ctrl.getCameraScreenNames()
# Remove any that don't actually have a camera looking at them
screens_with_cameras = scr_ctrl.getNamesOfScreensWithCameras()
cam_dict = OrderedDict((scr, cam) for scr, cam in zip(screen_names, camera_names) if
                            scr in screens_with_cameras or scr.startswith('BA1-COFF'))
section_names = ['S01', 'S02', 'C2V', 'INJ', 'BA1']
cam_list = []
for section in section_names:
    for item in cam_dict.keys():
        if item.startswith(section):
            cam_list.append(item)

os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255"
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = str(2**26)

IMAGE_WIDTH = 2160 / 2  # for CLARA cameras
IMAGE_HEIGHT = 2560 / 2  # for CLARA cameras
IMAGE_DIMS = (IMAGE_HEIGHT, IMAGE_WIDTH)
IMAGE_WIDTH_VELA = 1392
IMAGE_HEIGHT_VELA = 1040
IMAGE_DIMS_VELA = (IMAGE_HEIGHT_VELA, IMAGE_WIDTH_VELA)
hdf5_image_folder = r'\\claraserv3\CameraImages'
fire = np.array([list(int(h[i:i + 2], 16) for i in (1, 3, 5)) for h in colorcet.fire], dtype='uint8')


def status_msg(timestamp):
    return '[{}] Acquiring images into rolling buffer. Press Ctrl-C to stop.'.format(timestamp.strftime('%H:%M:%S'))


class RollingBuffer(object):

    def __init__(self):
        default = None
        for i, name in enumerate(cam_list):
            print '{:2d}. {}'.format(i, name)
            if cam_ctrl.isAcquiring(name):
                default = i
        index = click.prompt('Which screen to watch', type=click.IntRange(0, len(cam_list)), default=default)
        self.screen_name = cam_list[index]
        camera_name = cam_dict[self.screen_name]
        cam_ctrl.startAcquiring(camera_name)  # this will automatically stop all the other ones
        self.img_height, self.img_width = IMAGE_DIMS_VELA if cam_ctrl.isVelaCam(camera_name) else IMAGE_DIMS
        self.buffer_len = click.prompt('Enter size of buffer', type=int, default=100)
        while self.buffer_len > 1:
            try:
                self.data_buffer = np.zeros((self.buffer_len, self.img_width * self.img_height), 'int32')
                break
            except (MemoryError, ValueError):
                self.buffer_len -= 1
                print "Out of memory. Retrying with buffer size", self.buffer_len
        self.time_buffer = [None] * self.buffer_len
        self.buffer_pos = 0
        self.process = None

    def callback(self, **kwargs):
        self.data_buffer[self.buffer_pos] = kwargs['value']
        timestamp = datetime.now()
        self.time_buffer[self.buffer_pos] = timestamp
        self.buffer_pos = (self.buffer_pos + 1) % self.buffer_len
        if self.buffer_pos % 10 == 0:
            sys.stdout.write('\r' + status_msg(timestamp))
            sys.stdout.flush()

    def start(self):
        suffix = 'CAM1:ArrayData' if cam_ctrl.isVelaCam(self.screen_name) else 'CAM2:ArrayData'
        pv_name = cam_ctrl.getCameraObj(self.screen_name).pvRoot + suffix
        camdata = PV(pv_name)  # , auto_monitor=True, callback=self.callback)

        # Wait for Ctrl-C to be pressed
        sys.stdout.write('\r' + status_msg(datetime.now()))
        while True:
            t0 = datetime.now()
            try:
                self.callback(value=camdata.get())
                sleep(max(0.0, 0.1 - (datetime.now() - t0).total_seconds()))  # try to maintain 10 Hz
            except KeyboardInterrupt:
                break
        # camdata.clear_callbacks()  # stop updating buffer

        t0 = self.time_buffer[self.buffer_pos]
        prev_pos = (self.buffer_pos - 1) % self.buffer_len
        if t0 is None:  # haven't looped around yet - less than target number of frames captured
            self.buffer_len = self.buffer_pos
            self.buffer_pos = 0
            t0 = self.time_buffer[self.buffer_pos]
        t1 = self.time_buffer[prev_pos]
        dt = t1 - t0
        print '\n', dt.total_seconds(), 'seconds of images captured,', self.buffer_len, 'frames'

        while msvcrt.kbhit():
            msvcrt.getch()
        prompt = 'Save as [h]df5, [m]ovie, [b]oth, or [n]either'
        save_type = click.prompt(prompt, type=click.Choice(['h', 'm', 'b', 'n']), default='m')
        if save_type != 'n':
            data_buffer = np.reshape(self.data_buffer[:self.buffer_len], (self.buffer_len, self.img_height, self.img_width))
            folder = hdf5_image_folder + t1.strftime(r'\%Y\%#m\%#d')  # omit leading zeros from month and day
            try:
                os.makedirs(folder)
            except OSError as e:
                if e.errno != 17:  # dir already exists
                    raise
            time_str = t1.strftime('%Y-%#m-%#d_%#H-%#M-%#S')
            save_filename = r'{}\{}_{}_{}images'.format(folder, self.screen_name, time_str, self.buffer_len)

            if save_type in ('h', 'b'):
                hdf5_filename = save_filename + '.hdf5'
                print 'Saving to', hdf5_filename
                with h5py.File(hdf5_filename, 'w') as hdf5_file:
                    for i in range(self.buffer_len):
                        frame = np.array(data_buffer[(i + self.buffer_pos) % self.buffer_len], dtype='uint16')
                        hdf5_file.create_dataset('Capture%06d' % (i + 1), data=frame)

            if save_type in ('m', 'b'):
                movie_filename = save_filename + '.mp4'
                print 'Saving to', movie_filename
                # Find largest 95th-percentile value in frames. This is likely to be the brightest frame.
                # We can't do it on all the frames at once - this is prone to memory errors.
                p95 = 0
                for frame in data_buffer:
                    p95 = max(p95, np.percentile(frame, 95))
                factor = p95 / 256  # 5% of pixels are saturated
                dims = '{}x{}'.format(self.img_width, self.img_height)
                if self.process:
                    self.process.wait()  # might need to wait for a previous instance
                self.process = (ffmpeg
                                .input('pipe:', format='rawvideo', pix_fmt='rgb24', s=dims)
                                .filter('fps', fps=self.buffer_len / (dt.total_seconds()))
                                .output(movie_filename, pix_fmt='yuv420p')
                                .overwrite_output()
                                .run_async(pipe_stdin=True, quiet=True)
                                )
                with click.progressbar(length=self.buffer_len) as bar:
                    for i in range(self.buffer_len):
                        frame = data_buffer[(i + self.buffer_pos) % self.buffer_len]
                        data_uint8 = np.asarray(np.clip(frame / factor, 0, 255), 'uint8')
                        data_mapped = fire[data_uint8]
                        self.process.stdin.write(data_mapped.tobytes())
                        bar.update(i)
                self.process.stdin.close()

    def close(self):
        if self.process:
            self.process.wait()


if __name__ == '__main__':
    while True:
        image_buffer = RollingBuffer()
        try:
            image_buffer.start()
        except click.exceptions.Abort:
            image_buffer.close()


