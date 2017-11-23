import pyqtgraph as pg
import pyqtgraph.opengl as gl

### something to graph ######
from numpy import *
pi=3.1415
X=linspace(-10,10,100)
Y1=2+sin(X)
Y2=-2+Y1*Y1
Y3=cos(1*Y1)/(X+0.0131415)
Y4=4+sin(X)*cos(2*X)
Z=exp(-0.1*X*X)*cos(0.3*(X.reshape(100,1)**2+X.reshape(1,100)**2))
#############################
# you need this call ONCE
app=pg.QtGui.QApplication([])
#############################

##### plot 3D surface data  ####
w = gl.GLViewWidget()
## Saddle example with x and y specified
p = gl.GLSurfacePlotItem(x=X, y=X, z=Z, shader='heightColor')
w.addItem(p)
# show
w.show()
pg.QtGui.QApplication.exec_()

#==============================================

##### plot 3D line data  ####
w = gl.GLViewWidget()
# first line
Z=zeros(size(X))
p=array([X,Y2,Z])
p=p.transpose()
C=pg.glColor('w')
###### SCATTER ######
plt = gl.GLScatterPlotItem(pos=p, color=C)
w.addItem(plt)
# second line
Z=zeros(size(X))
p=array([X,Z,Y3])
p=p.transpose()
C=pg.glColor('b')
######## LINE  ############
plt = gl.GLLinePlotItem(pos=p, connected=False,width=20.5,color=C)
w.addItem(plt)
# third line
Z=zeros(size(X))
p=array([Z,Y1,X])
p=p.transpose()
C=pg.glColor('g')
########### SCATTER #############
plt = gl.GLScatterPlotItem(pos=p, color=C, size=20)
w.addItem(plt)
############# GRID #################
g=gl.GLGridItem()
w.addItem(g)
# show
w.show()
pg.QtGui.QApplication.exec_()
