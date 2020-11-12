
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtCore import pyqtSignal,pyqtSlot
import sys
sys.path.append("/usr/lib/python3.7/site-packages/")
from pysmu import *
from math import ceil,floor
from matplotlib import pyplot as plt
import numpy as np
from enum import Enum
#from adalm1000_cfgclasses import *


class Waves(Enum):
    OFF = 0
    DC = 1
    SINE = 2
    SAWTOOTH = 3
    SQUARE = 4

class ChanCfg(object):
    def __init__(self):
        self.per_samp = 0
        self.ph_samp = 0
        self.des_freq = 0
        self.des_phase = 0
        self.act_freq = 0
        self.act_phase = 0
        self.Vmin = 0
        self.Vmax = 0
        self.offset = 0
        self.amp = 0
        self.dc = 0
        self.mode = ''
        self.connectmode = 0
    
class AD1kController(QtCore.QObject):
    def __init__(self):
        super().__init__()
    
    def init(self):
        self.session = Session()
        if not self.session.devices:
            pass
        self.dev = self.session.devices[0]
        for dev in self.session.devices[1:]:         # Only use device 0 attached (remove others)
            self.session.remove(dev)
        self.ch = self.dev.channels
        #self.cha = self.dev.channels['A']
        #self.chb = self.dev.channels['B']
        self.__SAMPrate = 100000  # Sampling rate in Hz for both scope and AWG
        self.toffset = 0    # center of captured waveform will have trigger centered at middle when this is 0
        self.chcfg = {'A':ChanCfg(),'B':ChanCfg()}
        return self
    
        
        
    def setAWGMode(self,chan,connectmode):
        ''' mode:   0 - HI-Z (off)
                    1 - Source Voltage, Measure Current
                    2 - Source Current, Measure Voltage
                    3-5 == 0-3 with Voltage measurement split off
        '''
        self.chcfg[chan].connectmode = connectmode
        self.ch[chan].connectmode = Mode(connectmode)
    
    def setAWGOutput(self,chan,mode,offset,amp=0,freq=0,phase=0,dc=0):
        ''' mode should be text that matches the Enum Waves'''
        self.chcfg[chan].mode = mode
        self.chcfg[chan].des_freq = freq
        self.chcfg[chan].des_phase = phase
        mode = Waves[mode]
        if mode > 1:
            self.chcfg[chan].des_phase = self.chcfg[chan].des_phase-90    # By default, the wavegen will produce a COS wave, not a SIN wave.  Add offset
            if(self.chcfg[chan].phase < 0):
                self.chcfg[chan].phase += 360
            self.__calcSamps(chan)
            self.chcfg[chan].offset = offset
            self.chcfg[chan].amp = amp
            self.chcfg[chan].Vmin = offset-amp
            self.chcfg[chan].Vmax = offset+amp
        else:
            self.chcfg[chan].freq = self.chcfg[chan].per_samp = self.chcfg[chan].ph_phase = self.chcfg[chan].phase
                
        self.__setAWGOutput(chan)
            
        return (self.chcfg[chan].act_freq,self.chcfg[chan].act_phase)  # return the true frequency and phase used (correct sampling values)
    
    def __setAWGOutput(self,chan):
        chcfg = self.chcfg[chan]
        mode = Waves[chcfg.mode]
        if mode == 'OFF':
            self.setAWGMode(chan,0)
        else:
            self.setAWGMode(chan,chcfg.connectmode)
            if mode == 'DC':
                self.chcfg[chan].per_samp = 100
                self.ch[chan].constant(self.chcfg[chan].offset)
                print(offset)
            elif mode == 'SINE':
                self.ch[chan].sine(self.chcfg[chan].Vmin,self.chcfg[chan].Vmax,self.chcfg[chan].per_samp,self.chcfg[chan].ph_samp)
            elif mode == 'SAWTOOTH':
                self.ch[chan].sawtooth(self.chcfg[chan].Vmin,self.chcfg[chan].Vmax,self.chcfg[chan].chcfg[chan].per_samp,self.chcfg[chan].ph_samp)
            elif mode == 'SQUARE':
                self.ch[chan].square(self.chcfg[chan].Vmin,self.chcfg[chan].Vmax,amp,self.chcfg[chan].per_samp,self.chcfg[chan].ph_samp,self.chcfg[chan].dc)
                
    def __calcSamps(self,chan):
        ''' freq in Hz OR period in s
            phase in DEGREES
        '''
        period = 1/self.chcfg[chan].des_freq
        self.chcfg[chan].per_samp = round(self.__SAMPrate*period)
        self.chcfg[chan].ph_samp = round(phase*self.chcfg[chan].per_samp/360)
        self.chcfg[chan].act_freq = self.__SAMPrate/self.chcfg[chan].per_samp
        self.chcfg[chan].act_phase = self.chcfg[chan].ph_samp*360/self.chcfg[chan].per_samp
        
    def setSAMPRate(self,samprate):
        self.__SAMPrate = samprate
        self.__calcSamps('A')
        self.__setAWGOutput('A')
        self.__calcSamps('B')
        self.__setAWGOutput('B')
    
    def getSamples(self,samps):
        Adata = np.array([x[0][0] for x in self.session.get_samples(samps)[0]])
        Bdata = np.array([x[1][0] for x in self.session.get_samples(samps)[0]])
        
        #Adata = [x[0][0] for x in self.dev.read(samps)]
        #Bdata = [x[1][0] for x in self.dev.read(samps)]
        return (Adata,Bdata)
    
    def getSamplesAndInsert(self,samps,arrayA,arrayB,loc):
        data = self.session.get_samples(samps)[0]
        for ind in range(samps):
            arrayA[loc+ind] = data[ind][0][0]
            #arrayAI[loc+ind] = data[ind][0][1]
            arrayB[loc+ind] = data[ind][1][0]
            #arrayB[loc+ind] = data[ind][1][1]
        '''
        #Probably a much cleaner and pythonic way to do the above...
        #..something like this?
        for sample,ind in zip(data,range(loc,loc+samps)):
            arrayA[loc] = sample[0][0]
            arrayAI[loc] = sample[0][1]
            arrayB[loc] = sample[1][0]
            arrayBI[loc] = sample[1][1]
        '''
        
    
    def getSnapshot(self,time,start=0):     
        # Acquire a window of length time (in seconds) 
        # if 'start' is given, data from before start value is discarded
        timevector = np.arange(start,time,1/self.__SAMPrate)
        samps = ceil(time*self.__SAMPrate)
        data = self.getSamples(samps)
        if start:
            samps = floor(start*self.__SAMPrate)
            return (timevector,data[0][samps:],data[1][samps:])
        else:
            return (timevector,*data)
        
        
class adalm1000CtlThread(QtCore.QObject):
    def __init__(self,ad1kctl):
        self.ad1kctl = ad1kctl
        self.acqtimer = QtCore.QTimer()
        self.acq = []
        self.acqtimer.timeout.connect(self.acquire)
        self.acqtimer.setSingleShot(True)
        self.maxwindowtime = 100 #ms
        self.continuous = 0
        self.run = 0
   
   
    data = pyqtSignal(tuple)
   
    @pyqtSlot(tuple)    # (sample rate,offset time)
    def setTiming(self,timing):
        if not self.__SAMPrate == timing[0]:
            self.__setSAMPRate(timing[0])
        self.toffset = timing[1]
        
    @pyqtSlot(object)
    def setTriggering(self,trigger):
        pass
    
    @pyqtSlot(object)
    def setAWGA(self,awg):
        #setAWGOutput(self,chan,mode,offset,amp=0,freq=0,phase=0,dc=0):
        ad1kctl.setAWGOutput('A',mode=awg.modesel,offset=awg.offset,amp=awg.amp,freq=awg.freq,phase=awg.phase,dc=awg.dutycycle)
    
    @pyqtSlot(object)
    def setAWGB(self,awg):
        ad1kctl.setAWGOutput('B',mode=awg.modesel,offset=awg.offset,amp=awg.amp,freq=awg.freq,phase=awg.phase,dc=awg.dutycycle)
    
    @pyqtSlot(tuple)    # tuple: (time to acquire for, time to ignore at beginning)
    def acquire(self,acq):
        self.run = 1
        if acq:
            self.acq = acq
        self.data.emit(self.getSnapshot(self,*self.acq))
        if self.continuous:
            self.acqtimer.start()   # Enforce hold-off time by running timer and then calling acquire again
        
    @pyqtSlot(tuple)    # tuple: (time to acquire for, time to ignore at beginning, hold-off time)
    def continuousAcquire(self,acq):
        self.continuous = 1
        self.run = 1
        self.acq = acq[0:2]
        self.acqtimer.setInterval(acq[2])
        self.acquire()
        
    @pyqtSlot()
    def stop(self):
        self.run = 0
        self.ad1kctl.setAWGMode('A',0)
        self.ad1kctl.setAWGMode('B',0)
        
    # Copied function from controller class, but with flag to make it cancellable
    def getSnapshot(self,time,start=0):
        samps = ceil(time*self.__SAMPrate)
        start_samps = floor(start*self.__SAMPrate)
        timevector = np.arange(start_samps,samps) / self.__SAMPrate
        windowlength = min(samps,self.__SAMPrate*1000/self.maxwindowtime)
        Adata = np.zeros(samps)
        Bdata = np.zeros(samps)
        
        loc = 0
        while samps > 0:
            if not self.run:
                return
            window = min(samps,windowlength)
            self.ad1kctl.getSamplesAndInsert(window,Adata,Bdata,loc)
            samps -= window
            loc += window
        
        return (timevector[start_samps:],Adata[start_samps:],Bdata[start_samps:])
        
        
if __name__ == "__main__":
    ad1kctl = AD1kController().init()
    ad1kctl.setAWGMode('A',1)
    ad1kctl.setAWGMode('B',1)
    ad1kctl.setAWGOutput('A',1,2.5,2.5)
    print(ad1kctl.setAWGOutput('B',2,2.5,1,109))
    
    #import pdb; pdb.set_trace()
    #data = ad1kctl.getSamples(1000)
    data = ad1kctl.getSnapshot(0.001,0.000)
    #print(data)
    
    plt.figure()
    plt.plot(data[0],data[1])
    plt.plot(data[0],data[2])
    plt.show()
