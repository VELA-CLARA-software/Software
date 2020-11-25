The package is *striptool2*, and there is an example of how to call it in the file examples/striptool_test.py (this is the file you should run).
Dependencies will mostly be met by default, but I need pyQtGraph and PyQt4 and numpy (I use anaconda and the only additional dependency was pyqtgraph I think)

This is a modification of the original striptool to better handle multiple axes, and for much faster plotting speed.
Major changes:
1. stripTool has actually been replaced by generalPlot - this instantiates the records (from signalRecord) and provides methods to create scrollingPlots, fftPlots and scatterPlots
2. scrollingPlot is now connected directly to the signalRecord update, so it draws only the latest value, and simply adds a QT linePath to the existing graphics
  1. This change means I no longer directly use the pyqtgraph plotting function setData, but instead directly draw a QPainterPath object onto the existing pyqtgraph viewBox
  2. It's no longer obvious how to add "old" data to the existing plot...
3. Each scrollingPlot can now use it's own or a more general axis, which is shared between multiple plots. Axis can be created and then assigned during the addSignal phase.
4. The old plotLegend has been replaced with a pyqtgraph ParameterTree. The headers now show the latest value of the signal (slugged to 1Hz), and clicking on the headers shows the correct axis for that signal (which may be a shared axis)
5. FFT plots and Scatter plots have now been separated from the scrollingPlot. For now they are connected and have their own controls to select plot different signals. At the moment this means that they can only show one plot at a time, although you can have multiple FFT or scatter plots.
  1. To keep the plots going at 1Hz only the last 1000 data points are plotted. This can be changed however.
6. Autoscroll is on permanently at the moment, and there is no pause!

Notes:
To change the scale use the mouse (http://www.pyqtgraph.org/documentation/mouse_interaction.html).
Us the legend to show the axes - click on a signal to show that axis, multiple select (hold shift or ctrl) to show multiple axes.
scrollingPlot keeps the current time at the right hand side, and scrolls the data relative to this point.
There is no way to add a new signal on-line inside the striptool, you have to do this in your own application.
If you delete a signal from the striptool it’s gone. Data deleted.

** Look at the example files for _examples_ - they demonstrate how to use most of the relevant features**
