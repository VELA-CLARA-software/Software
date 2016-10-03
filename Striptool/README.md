Hi,

I have put my strip tool package on the server at \\fed.cclrc.ac.uk\Org\NLab\ASTeC\Projects\VELA\Software\Python\Striptool. The package is striptool.py, and there is an example of how to call it in the file striptool_test.py (this is the file you should run). Dependencies will mostly be met by default, but I need pyQtGraph and PyQt4 and numpy (I use anaconda and the only additional dependency was pyqtgraph I think)

Please try it out and let me know what you think, what you want changed, or (most importantly) any bugs. The package is not finished, I will be working on getting rid of an annoying graphical bug (see the top-left when you run the plot, caused by the custom axisItem that makes the time stamps…), and some other issues.

Notes:
To change the scale use the mouse (http://www.pyqtgraph.org/documentation/mouse_interaction.html). The plot filters the signal data to only show data inside the viewBox. For very long, fast data (hours at 100Hz) the drawing will slow down below 1Hz if you display all the data. There is some rudimentary decimation when this happens, but it needs improving.
Autoscroll keeps the current time at the right hand side, and scrolls the data relative to this point. Turn it off and the data will accumulate to the right, but the time stamps will stay in place.
The histogram and FFT plots *only* use data that matches what is shown in the line plot. This is because large data sets are slow to FFT, so this way you can FFT only over the relevant data. If you turn autoscroll OFF, and select some data that is not changing and then look at the histogram/FFT it won’t change, since the data in the linear plot is now fixed values. This makes sense.
Pause just pauses the plot updates, not the data acquisition.
There is no way to add a new signal on-line inside the striptool, you have to do this in your own application. If you delete a signal from the striptool it’s gone. Data deleted.
There is no way to save data yet. Working on it (should be easy using numpy to csv or hdf5).

I will make a pip installer at some point, and then it will be installed in your python “site-packages” so you don’t need to have the striptool.py in the same directory. Just need to work out how to specify package requirements correctly. Also, need to make the icon not external to the code. Can I do that??
