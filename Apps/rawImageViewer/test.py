''' Present a scatter plot with linked histograms on both axes.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve selection_histogram.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/selection_histogram
in your browser.
'''

import numpy as np

from bokeh.layouts import row, column
from bokeh.models import BoxSelectTool, LassoSelectTool, Spacer
from bokeh.plotting import figure, curdoc, output_file,show
from PIL import Image
from bokeh.models import ColumnDataSource
name = 'C:\\Users\\wln24624\\Documents\\SOFTWARE\\Camera image plotting\\sol-100.tif'
name1 = '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\Work\\2017\\CurrentCamera\\C2V-CAM-01_001.bin'
#a = np.fromfile(f, dtype=np.uint16)
im = Image.open(name1)


f = open(name, "r")
a = np.fromfile(f, dtype=np.uint16)
a = a.reshape((2160, 2560))
imarray = np.array(im)
#a = a.reshape((2160, 2560))
#p.append(figure(x_range=(0, 2560), y_range=(0, 2160), title=str(name).split('\\')[-1]))
#p.image(image=[np.flipud(imarray)], x=0, y=0, dw=2560, dh=2160, palette="Spectral11")


import pandas as pd


df = pd.DataFrame()
#print len(imarray)
x=numpy.zeros(2560*2160)
y=numpy.zeros(2560*2160)
c=0
for i in range(len(imarray)):
    for j in range(len(imarray[0])):
        x[c]=j
        y[c]=i
        c+=1
df['x']=x
df['y']=y

df['data']=imarray.flatten()
import datashader as ds
import datashader.transfer_functions as tf

TOOLS="pan,wheel_zoom,box_zoom,box_select,reset"

# create the scatter plot
p = figure(tools=TOOLS, plot_width=700, plot_height=600, min_border=10, min_border_left=50,
           toolbar_location="above", #x_axis_location=None, y_axis_location=None,
           x_range=(0, 2560), y_range=(0, 2160), title=str(name).split('\\')[-1])

#p.background_fill_color = "#fafafa"
p.select(BoxSelectTool).select_every_mousemove = False

#r = p.scatter(x, y, size=3, color="#3A5785", alpha=0.6)
sumX = np.sum(np.flipud(imarray),axis=0)
#print sumX.size()
sumY = np.sum(np.flipud(imarray),axis=1)
# create the horizontal histogram
hX = np.linspace(1,2560,2560)
vY = np.linspace(1,2160,2160)
#data = {'sumY': sumY,
#        'imageDat': np.flipud(imarray)()}

#source = ColumnDataSource(data)

imagey = p.image(image=[np.flipud(imarray)],
                 x=0, y=0, dw=2560, dh=2160, palette="Spectral11")


hProfile = sumX
hzeros = np.zeros(len(sumX))
hmax = max(sumX) + 10
hmin = min(sumX) - 10

LINE_ARGS = dict(color="#3A5785", line_color=None)

ph = figure(tools=TOOLS,toolbar_location=None, plot_width=p.plot_width, plot_height=200, x_range=p.x_range,
            y_range=(hmin, hmax), min_border=10, min_border_left=50, y_axis_location="right")
ph.xgrid.grid_line_color = None
ph.yaxis.major_label_orientation = np.pi/4
ph.background_fill_color = "#fafafa"
ph.vbar(x=hX, width=1, bottom=0, top=hProfile,
        fill_alpha=0.3, fill_color="#3A5785", line_color=None)
hb1 = ph.vbar(x=hX, width=1, bottom=0, top=sumX,
        fill_alpha=0.5, fill_color="#3A5785", line_color=None)

# create the vertical histogram
vProfile = sumY

vzeros = np.zeros(len(sumY))
vmax = max(sumY) + 10
vmin = min(sumY) - 10
#vhist, vedges = np.histogram(sumY, bins=20)
#vzeros = np.zeros(len(vedges)-1)
#vmax = max(vhist)*1.1

pv = figure(tools=TOOLS, toolbar_location=None, plot_width=200, plot_height=p.plot_height, x_range=(vmin, vmax),
            y_range=p.y_range, min_border=10, y_axis_location="right")
pv.ygrid.grid_line_color = None
pv.xaxis.major_label_orientation = np.pi/4
pv.background_fill_color = "#fafafa"

pv.hbar(y=vY, height=1, left=0, right=vProfile,
        fill_alpha=0.3, fill_color="#3A5785", line_color=None)
vb1 = ph.hbar(y=vY, height=1, left=0, right=vzeros,
        fill_alpha=0.5, fill_color="#3A5785", line_color=None)

layout = column(row(p, pv), row(ph, Spacer(width=200, height=200)))
'''
curdoc().add_root(layout)
curdoc().title = " Raw Image Viewer"
'''
'''
def update(attr, old, new):
    create_figure()
#    inds = np.array(new['1d']['indices'])
##
#    if len(inds) == 0 or len(inds) == len(newX):
#        newX = hzeros
#        newY = vzeros
#    else:
#        newX = sumX[inds]
#        newY = sumY[inds]
#
#    hb1.data_source.data["top"]   =  newX
#    vb1.data_source.data["right"] =  newY

#imagey.data_source.on_change('selected', update)



curdoc().add_root(layout)
curdoc().title = "Crossfilter"
'''
output_file("TEST.html", title="TT")

show(layout)
