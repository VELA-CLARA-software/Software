from PyQt4.QtCore import QObject

# keys for ALL THE DATA we monitor
time_stamp = 'time_stamp'

# the mask
mask_x_rbv  = 'mask_x_rbv'
mask_y_rbv  = 'mask_y_rbv'
mask_x_rad_rbv  = 'mask_x_rad_rbv'
mask_y_rad_rbv  = 'mask_y_rad_rbv'
<<<<<<< HEAD





=======
mask_x_user  = 'mask_x_user'
mask_y_user  = 'mask_y_user'
mask_x_rad_user  = 'mask_x_rad_user'
mask_y_rad_user  = 'mask_y_rad_user'
mask_feedback = 'mask_feedback'

# imageCollection
num_images = 'num_images'
is_collecting_or_saving = 'is_collecting_or_saving'
last_filename = 'last_filename'

#imageview
is_acquiring = 'is_acquiring'
is_liverstream = 'is_liverstream'
min_level = 'min_level'
max_level = 'max_level'

# imageAnalysis
is_analysing = 'is_analysing'
use_background  = 'use_background'
use_npoint  = 'use_npoint'
ana_step_size = 'ana_step_size'
>>>>>>> 61a9e380278271c5f352948c5d3699d21e6b48d6

x_val = 'x_val'
y_val = 'y_val'
sx_val = 'sx_val'
sy_val = 'sy_val'
i_val = 'i_val'
cov_val = 'cov_val'

x_mean = 'x_mean'
y_mean = 'y_mean'
sx_mean = 'sx_mean'
sy_mean = 'sy_mean'
i_mean = 'i_mean'
cov_mean = 'cov_mean'

x_sd = 'x_sd'
y_sd = 'y_sd'
sx_sd = 'sx_sd'
sy_sd = 'sy_sd'
i_sd = 'i_sd'
cov_sd = 'cov_sd'

x_buf =  'x_buf'
y_buf = 'y_buf'
sx_buf= 'sx_buf'
sy_buf= 'sy_buf'
i_buf= 'i_buf'
cov_buf= 'cov_buf'

all_value_keys = [
time_stamp,
mask_x_rbv,
mask_y_rbv,
mask_x_rad_rbv,
mask_y_rad_rbv,
mask_x_user,
mask_y_user,
mask_x_rad_user,
mask_y_rad_user,
mask_feedback,
num_images,
is_collecting_or_saving,
last_filename,
is_acquiring,
is_liverstream,
min_level,
max_level,
is_analysing,
use_background,
use_npoint,
ana_step_size,
x_val,
y_val,
sx_val,
sy_val,
i_val,
cov_val,
x_mean,
y_mean,
sx_mean,
sy_mean,
i_mean,
cov_mean,
x_sd,
y_sd,
sx_sd,
sy_sd,
i_sd,
cov_sd,
x_buf,
y_buf,
sx_buf,
sy_buf,
i_buf,
cov_buf
] = 





class data(QObject):

    # dictionary of all data
    values = {}
    [values.update({x: 0}) for x in all_value_keys]
    #
    # values[time_stamp] =  0
    # values[mask_x_rbv] =  0
    # values[mask_y_rbv] =  0
    # values[mask_x_rad_rbv] =  0
    # values[mask_y_rad_rbv] =
    # values[mask_x_user] =
    # values[mask_y_user] =
    # values[mask_x_rad_user] =
    # values[mask_y_rad_user] =
    # values[mask_feedback] =
    # values[num_images] =
    # values[is_collecting_or_saving] =
    # values[last_filename] =
    # values[is_acquiring] =
    # values[is_liverstream] =
    # values[min_level] =
    # values[max_level] =
    # values[is_analysing] =
    # values[use_background] =  =
    # values[use_npoint] =
    # values[ana_step_size] =
    # values[x_val] =
    # values[y_val] =
    # values[sx_val] =
    # values[sy_val] =
    # values[i_val] =
    # values[cov_val] =
    # values[x_mean] =
    # values[y_mean] =
    # values[sx_mean] =
    # values[sy_mean] =
    # values[i_mean] =
    # values[cov_mean] =
    # values[x_sd] =
    # values[y_sd] =
    # values[sx_sd] =
    # values[sy_sd] =
    # values[i_sd] =
    # values[cov_sd] =
    # values[x_buf] =
    # values[y_buf] =
    # values[sx_buf] =
    # values[sy_buf] =
    # values[i_buf] =
    # values[cov_buf] =


    def __init__(self):
        QObject.__init__(self)
        pass

