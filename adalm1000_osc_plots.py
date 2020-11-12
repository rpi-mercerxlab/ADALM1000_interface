from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import numpy as np
from collections import OrderedDict

matplotlib.use('Qt5Agg')

#import pdb; pdb.set_trace()
class MPLFrame(QtWidgets.QFrame):
    def __init__(self,parent=None,name=''):
        super(MPLFrame,self).__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.parent = parent
        self.graph = MPLGraph(name,self)
    
    def resizeEvent(self,event):
        self.graph.setGeometry(self.rect())
        
class MPLGraph(QtWidgets.QWidget):
    def __init__(self,name,parent=None):
        super(MPLGraph,self).__init__(parent)
        self.name = name
        self.parent = parent
        self.dpi = 60
        size = parent.rect()
        self.fig = Figure((20*size.width()/self.dpi, 40*size.height()/self.dpi),
                          dpi = self.dpi,
                          facecolor = (0,0,0),
                          edgecolor = (1,1,1))
        self.fig.set_tight_layout(True)
        self.ax = []    # list storing all axes present in figure
        self.hscale = 0
        self.hposition = 0
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        
        self.canvas.show()
        #self.timer = QtCore.QTimer()
        #self.timer.timeout.connect(self.resizeEvent)
        #self.timer.start(1000)
        QtCore.QTimer.singleShot(250,self.resize)
        
        self.traces = OrderedDict()
        self.cursor1 = []
        self.cursor2 = []
        self.connections = []
        
    def config(self,traces):
        for trace in traces:
            self.traces.update({trace[0]:Trace(self.newAxes(),*trace,parent=self)})
        self.cursor1 = PCursor(self.ax[0],self.traces,button=1)  # cursor associated with LMB
        self.cursor2 = PCursor(self.ax[0],self.traces,button=3)  # cursor associated with RMB
        self.connections.append(self.canvas.mpl_connect('button_press_event',self.cursor1.mouse_down))
        self.connections.append(self.canvas.mpl_connect('button_release_event',self.cursor1.mouse_up))
        self.connections.append(self.canvas.mpl_connect('motion_notify_event',self.cursor1.mouse_drag))
        self.connections.append(self.canvas.mpl_connect('button_press_event',self.cursor2.mouse_down))
        self.connections.append(self.canvas.mpl_connect('button_release_event',self.cursor2.mouse_up))
        self.connections.append(self.canvas.mpl_connect('motion_notify_event',self.cursor2.mouse_drag))
        self.ax[0].set_xlim(0,10)
        
    def newAxes(self):
        if not self.ax:
            self.ax.append(self.fig.add_subplot(111))
            self.ax[-1].locator_params(axis='x',nbins=10)
        else:
            self.ax.append(self.ax[0].twinx())
        self.ax[-1].set_yticklabels([])
        self.ax[-1].autoscale(False)
        self.ax[-1].set_facecolor((0,0,0))
        self.ax[-1].tick_params(colors='white')
        self.ax[-1].spines['bottom'].set_color('white')
        self.ax[-1].spines['left'].set_color('white')
        self.ax[-1].spines['right'].set_color('white')
        self.ax[-1].spines['top'].set_color('white')
        self.ax[-1].grid(color=(.5,.5,.5),which='major',linewidth=1)
        self.ax[-1].grid(color=(.25,.25,.25),which='minor',linewidth=1)
        self.ax[-1].locator_params(axis='y',nbins=10)
        return self.ax[-1]
        
    def resizeEvent(self,event):
        self.resize()
        
    def resize(self):
        size = self.parent.rect()
        self.fig.set_size_inches(w=size.width()/self.dpi,h=size.height()/self.dpi,forward=True)
        self.canvas.draw()
        
    def update(self,xdata,ydata,title=None):
        for tracename,data in zip(self.traces,ydata):
            self.traces[tracename].update(xdata,data)
            self.traces[tracename].enable()

        if title != None:
            self.axes.set_title(title)
            
        self.canvas.draw()
    
    def setHScale(self,scale):
        self.hscale = scale
        self.updateHScale()
    
    def setHPosition(self,position):
        self.hposition = position
        self.updateHScale()
    
    def updateHScale(self):
        xmin = self.hposition - self.hscale*5
        xmax = self.hposition + self.hscale*5
        self.ax[0].set_xlim(xmin,xmax)
        self.canvas.draw()
        
        
    

class Trace(object):
    def __init__(self,ax='',name='',unit='',scale='',color='',parent=''):
        self.ax = ax
        self.line, = self.ax.plot([0],[0],linestyle='None',color=color,label=name)
        self.name = name
        if self.name == 'ch1v':
            self.enabled = True
        else:
            self.enabled = False
        self.scale = scale
        self.offset = 0
        self.parent = parent
        
    def enable(self):
        self.line.set_linestyle('solid')
        self.enabled = True
        
    def diable(self):
        self.line.set_linestyle('None')
        self.enabled = False
    
    def update(self,x,y):
        self.line.set_data((x,y))
    
    def updateX(self,x):
        self.line.set_xdata(x)
        
    def updateY(self,y):
        self.line.set_ydata(y)
        
    def setScale(self,div):
        self.scale = div
        self.updateScale()
    
    def setOffset(self,offset):
        self.offset = offset
        self.updateScale()
        
    def updateScale(self):
        ymin = -self.scale*5+self.offset
        ymax = self.scale*5+self.offset
        self.ax.set_ylim(ymin,ymax)
        self.parent.canvas.draw()
        

class PCursor(object):
    def __init__(self,ax,traces=[],button=0):
        self.ax = ax
        self.button = button 
        self.ly = ax.axvline(color='r',alpha=0.5,label="cursor_{}".format(self.button))
        self.traces = traces
        #self.marker, = ax.plot([0],[0],marker="0",color="yellow",zorder=3,label="marker_{}".format(self.button))
        #self.x = []
        #self.y = []
        #self.txt = [ax.text(0.7,0.9,'')]
        self.markers = []
        self.drag = False
        for _,trace in self.traces.items():
            self.markers.append(Markers(ax,0,0,trace.line._label))
        
    def mouse_down(self,event):
        if not event.inaxes: return
        if event.button != self.button: return
    
        self.drag = True
        self.mouse_drag(event)
        
    def mouse_drag(self,event):
        if not self.drag: return
        if not event.inaxes: return
        x,y = event.xdata,event.ydata
        indx = []
        i = 0
        for ind,tracename in enumerate(self.traces):
            if not indx:
                indx = np.abs(np.array(self.traces[tracename].line.get_xdata())-x).argmin()
                x = self.traces[tracename].line.get_xdata()[indx]
            if self.traces[tracename].enabled:
                self.markers[ind].update(x,self.traces[tracename].line.get_ydata()[indx])
            else:
                self.markers[ind].hide()
        self.ly.set_xdata(x)
        self.ax.figure.canvas.draw_idle()
    
    def mouse_up(self,event):
        if event.button == self.button:
            self.drag = False

class Markers(object):
    def __init__(self,ax=[],x=[],y=[],name=''):
        self.name = ''
        self.x = 0
        if x:
            self.x = x
        if y:
            self.y = y            
        self.txt = ax.text(x,y,'x={0:1.2f},y={1:1.2f}'.format(x,y),color='white')
        self.marker, = ax.plot([x],[y],marker="x",color="red",zorder=2)
        
    def update(self,x,y):
        self.marker.set_marker='o'
        self.marker.set_data([x],[y])
        self.txt.set_text('y={1:1.2f}'.format(x,y))
        self.txt.set_position((x,y))
        
    def hide(self):
        self.marker.set_marker('None')
