


class Units(object):
    def __init__(self,value=1,baseunit='',prefix='',suffix=''):
        self.value = value
        self.baseunit = baseunit
        self.prefix = prefix
        self.prefix,self.prefixexp = self.get_prefix_exp(self.prefix)
        self.suffix = suffix
        self.text = self.makeText()
    
    def update(self,value='',prefix=''): 
        self.value = value
        self.prefix = prefix
        self.prefix,self.prefixexp = self.get_prefix_exp(self.prefix)
        self.adjustPrefix()
        self.makeText()
    
    def get_prefix_exp(self,prefix):
        try:
            prefixexp = {'G':9,'M':6,'k':3,'':0,'m':-3,'u':-6,'n':-9,'p':-12}[prefix]
            return (prefix,prefixexp)
        except KeyError:
            return ('',0)
    
    def setUnits(self,text):
        unit = text.lstrip('-1234567890. ')
        try:
            self.value = float(text.rstrip(unit))
        except ValueError:
            return #don't change units
        self.prefix = ''
        if unit:
            self.prefix = unit[0]
        self.prefix,self.prefixexp = self.get_prefix_exp(self.prefix)
        self.adjustPrefix()
        self.makeText()
    
    def makeText(self):
        self.text = '{0:1.3f} {1}{2}{3}'.format(self.value,self.prefix,self.baseunit,self.suffix)
        
    def adjustPrefix(self):
        if self.value == 0: return
        while self.value >= 1000 and self.prefixexp < 1e9:
            self.prefixexp += 3
            self.value /=1000
        while self.value < 1 and self.prefixexp > -12:
            self.prefixexp -= 3
            self.value *= 1000
        self.prefix = {9:'G',6:'M',3:'k',0:'',-3:'m',-6:'u',-9:'n',-12:'p'}[self.prefixexp]
        
    def getFullValue(self):
        return self.value * 10**self.prefixexp
        
class allCfg(object):
    def __init(object):
        self.chAV = []
        self.chBV = []
        self.chAA = []
        self.chBA = []
        self.chm1 = []
        self.chm2 = []
        self.trig = []
        self.samp = []
        self.awgA = []
        self.awgB = []
        
class SampCfg(object):
    def __init__(self):
        self.hscale = []
        self.position = []
        
class TrigCfg(object):
    def __init__(self):
        self.source = []
        self.edge = []
        self.level = []
            
class ScopeCfg(object):
    def __init__(self):
        self.scale = []
        self.voff = []
        self.chgain = []
        self.choff = []
        self.measawg = []
        
class AWGCfg(object):
    def __init__(self):
        self.modesel = []
        self.amp = []
        self.offset = []
        self.freq = []
        self.phase = []
        self.dutycyle = []
        
