# Use Miniconda to install various packages required for Python
# (pip can't install PyQt4 or scipy, so this is the most pain-free way to do it!)
# Note: matplotlib 1.5.3 or higher requires PyQt5, so keep below that for now
conda install pyqt=4 scipy xlrd "matplotlib<1.5.3" functools32 git -y

# Now use pip to install the hardware controllers:
#    magnets, BPMs, screens, ...
pip install -e "\\fed.cclrc.ac.uk\Org\NLab\ASTeC\Projects\VELA\Software\VELA_CLARA_PYDs\bin\Release"

