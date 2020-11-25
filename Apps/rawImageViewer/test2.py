from bokeh.models import BoxZoomTool
import datashader as ds
import datashader.transfer_functions as tf
from bokeh.layouts import row, column
from bokeh.plotting import figure, output_file, show
import datashader as ds
import numpy
import numpy as np
from datashader.bokeh_ext import InteractiveImage
from functools import partial
from datashader.utils import export_image
from datashader.colors import colormap_select, Greys9, Hot, viridis, inferno
from IPython.core.display import HTML, display
from bokeh.models import Spacer

name = '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\Work\\2017\\CurrentCamera\\S02-CAM-03_001.bin'
#a = np.fromfile(f, dtype=np.uint16)
f = open(name, "r")
a = np.fromfile(f, dtype=np.uint16)
a = a.reshape((2160, 2560))

imarray =np.array(a)
sumX = np.sum(np.flipud(imarray),axis=0)
sumY = np.sum(np.flipud(imarray),axis=1)
hX = np.linspace(1,2560,2560)
vY = np.linspace(1,2160,2160)



TOOLS="pan,wheel_zoom,box_zoom,box_select,reset"
p = figure(tools=TOOLS, plot_width=700, plot_height=600, min_border=10, min_border_left=50,
           toolbar_location="above", #x_axis_location=None, y_axis_location=None,
           x_range=(0, 2560), y_range=(0, 2160), title=str(name).split('\\')[-1])

imagey = p.image(image=[np.flipud(imarray)],
                 x=0, y=0, dw=2560, dh=2160)#, palette="Spectral11")

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
        fill_alpha=0.8, fill_color="#3A5785", line_color=None)

vProfile = sumY
vzeros = np.zeros(len(sumY))
vmax = max(sumY) + 10
vmin = min(sumY) - 10

pv = figure(tools=TOOLS, toolbar_location=None, plot_width=200, plot_height=p.plot_height, x_range=(vmin, vmax),
            y_range=p.y_range, min_border=10, y_axis_location="right")
pv.ygrid.grid_line_color = None
pv.xaxis.major_label_orientation = np.pi/4
pv.background_fill_color = "#fafafa"

pv.hbar(y=vY, height=1, left=0, right=vProfile,
        fill_alpha=0.8, fill_color="#3A5785", line_color=None)

layout = column(row(p, pv), row(ph, Spacer(width=200, height=200)))

output_file("TEST2.html", title="T2")
show(layout)
