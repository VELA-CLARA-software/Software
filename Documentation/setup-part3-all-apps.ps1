# This script installs all the apps in the VELA-CLARA repository that have a setup.py.
# Not automatically updated - if you add a setup.py to your app, please also update this file.

pip install git+https://github.com/VELA-CLARA-software/Software.git#subdirectory=Striptool
pip install git+https://github.com/VELA-CLARA-software/Software.git#subdirectory=magnet-table
pip install git+https://github.com/VELA-CLARA-software/Software.git#subdirectory=loggerWidget

