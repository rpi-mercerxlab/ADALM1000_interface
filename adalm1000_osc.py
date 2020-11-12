from PyQt5 import QtWidgets
from adalm1000_interface import Ui_MainWindow
import sys
from adalm1000_osc_plots import MPLFrame
import numpy as np
import faulthandler

traces = (('chAV','V','1','blue'),
          ('chBV','V','1','red'),
          ('math1','V','1','green'),
          ('math2','V','1','yellow'))



class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.controls = self.ui.allcfg
        self.graph = self.ui.plotframe.graph
        self.config()
        
        self.controls.samp.hscale.valueChanged.connect(self.graph.setHScale)
        self.controls.samp.position.valueChanged.connect(self.graph.setHPosition)
        self.controls.chAV.scale.valueChanged.connect(self.graph.traces['chAV'].setScale)
        self.controls.chAV.voff.valueChanged.connect(self.graph.traces['chAV'].setOffset)
        self.controls.chBV.scale.valueChanged.connect(self.graph.traces['chBV'].setScale)
        self.controls.chBV.voff.valueChanged.connect(self.graph.traces['chBV'].setOffset)
        
    
    def config(self):
        self.ui.plotframe.graph.config(traces)
        #self.mplframe = MPLFrame(self.ui.plotframe)
        xdata = np.arange(0,10,0.01)
#        ydata = (2*np.sin(xdata),
#                 3*np.cos(xdata)+1,
#                 np.sqrt(xdata),
#                 xdata*0+3)
        ydata = (2*np.sin(xdata),
                 3*np.cos(xdata)+1)
        
        self.ui.plotframe.graph.update(xdata,ydata)
        
        

def main():
    faulthandler.enable()
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    #import pdb; pdb.set_trace()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
