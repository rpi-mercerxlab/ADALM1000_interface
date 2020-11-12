# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
#import widgetbox
from adalm1000_osc_plots import MPLFrame
from adalm1000_cfgclasses import *
from adalm1000_controller import Waves

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1150, 722)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.plotframe = MPLFrame(self.splitter)
        self.plotframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.plotframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.plotframe.setObjectName("plotframe")
        self.ctlframe = QtWidgets.QFrame(self.splitter)
        self.ctlframe.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ctlframe.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ctlframe.setObjectName("ctlframe")
        self.splitter.setSizes([self.splitter.size().width()*.8,self.splitter.size().width()*.2])
        
        self.rightVLayout = QtWidgets.QVBoxLayout(self.ctlframe)
        
        self.runHLayout = QtWidgets.QHBoxLayout()
        self.runbutton = QtWidgets.QPushButton("Run")
        self.runHLayout.addWidget(self.runbutton)
        self.singlebutton = QtWidgets.QPushButton("Single")
        self.runHLayout.addWidget(self.singlebutton)
        self.rightVLayout.addLayout(self.runHLayout)
        
        self.treeWidget = QtWidgets.QTreeWidget()
        self.rightVLayout.addWidget(self.treeWidget)
        self.treeWidget.setIndentation(0)
        self.treeWidget.setAnimated(False)
        self.treeWidget.setRootIsDecorated(False)
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setObjectName("treeWidget")
        self.addControls(self.treeWidget)
#        self.treeSecs = treeSections(self.treeWidget)
        self.horizontalLayout.addWidget(self.splitter)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1150, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        #self.treeWidget.headerItem().setText(0, _translate("MainWindow", "Top"))
        #__sortingEnabled = self.treeWidget.isSortingEnabled()
        #self.treeWidget.setSortingEnabled(False)
        #self.treeWidget.topLevelItem(0).setText(0, _translate("MainWindow", "Item1"))
        #self.treeWidget.topLevelItem(1).setText(0, _translate("MainWindow", "Item2"))
        #self.treeWidget.topLevelItem(1).child(0).setText(0, _translate("MainWindow", "test"))
        #self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        
    def addControls(self, tree):
        self.allcfg = allCfg()
        
        self.allcfg.samp = SampCfg()
        frame = QtWidgets.QFrame(tree)
        tree.taxis = treeSampling(frame,"samp",self.allcfg.samp)
        item = QtWidgets.QTreeWidgetItem()
        tree.addTopLevelItem(item)
        tree.setItemWidget(item,0,SectionExpandButton(item, text = "Horizontal"))
        section = QtWidgets.QTreeWidgetItem(item)
        section.setDisabled(True)
        tree.setItemWidget(section,0,frame)
        item.addChild(section)
        
        self.allcfg.trig = TrigCfg()
        frame = QtWidgets.QFrame(tree)
        tree.triggering = treeTrigger(frame,"samp",self.allcfg.trig)
        item = QtWidgets.QTreeWidgetItem()
        tree.addTopLevelItem(item)
        tree.setItemWidget(item,0,SectionExpandButton(item, text = "Triggering"))
        section = QtWidgets.QTreeWidgetItem(item)
        section.setDisabled(True)
        tree.setItemWidget(section,0,frame)
        item.addChild(section)
        
        self.allcfg.chAV = ScopeCfg()
        frame = QtWidgets.QFrame(tree)
        tree.ch1 = treeScope(frame,"schav",self.allcfg.chAV)
        item = QtWidgets.QTreeWidgetItem()
        tree.addTopLevelItem(item)
        tree.setItemWidget(item,0,SectionExpandButton(item, text = "Scope Channel A"))
        section = QtWidgets.QTreeWidgetItem(item)
        section.setDisabled(True)
        tree.setItemWidget(section,0,frame)
        item.addChild(section)
        
        self.allcfg.chBV = ScopeCfg()
        frame = QtWidgets.QFrame(tree)
        tree.ch2 = treeScope(frame,"schbv",self.allcfg.chBV)
        item = QtWidgets.QTreeWidgetItem()
        tree.addTopLevelItem(item)
        tree.setItemWidget(item,0,SectionExpandButton(item, text = "Scope Channel B"))
        section = QtWidgets.QTreeWidgetItem(item)
        section.setDisabled(True)
        tree.setItemWidget(section,0,frame)
        item.addChild(section)
        
        self.allcfg.awgA = AWGCfg()
        frame = QtWidgets.QFrame(tree)
        tree.awgch1 = treeAWG(frame,"awga",self.allcfg.awgA)
        item = QtWidgets.QTreeWidgetItem()
        tree.addTopLevelItem(item)
        tree.setItemWidget(item,0,SectionExpandButton(item, text = "Function Generator A"))
        section = QtWidgets.QTreeWidgetItem(item)
        section.setDisabled(True)
        tree.setItemWidget(section,0,frame)
        item.addChild(section)
        
        self.allcfg.awgB = AWGCfg()
        frame = QtWidgets.QFrame(tree)
        tree.awgch2 = treeAWG(frame,"awgb",self.allcfg.awgB)
        item = QtWidgets.QTreeWidgetItem()
        tree.addTopLevelItem(item)
        tree.setItemWidget(item,0,SectionExpandButton(item, text = "Function Generator B"))
        section = QtWidgets.QTreeWidgetItem(item)
        section.setDisabled(True)
        tree.setItemWidget(section,0,frame)
        item.addChild(section)


class SectionExpandButton(QtWidgets.QPushButton):
    '''a QPushbutton that can expand or collapse its section
    '''
    def __init__(self, item, text = '', parent = None):
        super().__init__(text, parent)
        self.section = item
        self.clicked.connect(self.on_clicked)
        self.setStyleSheet("text-align: left;padding-left: 2px;border-top: 2px solid #1e1b18")
        self.setFlat(True)

    def on_clicked(self):
        '''toggle expand/collapse of section by clicking
        '''
        if self.section.isExpanded():
            self.section.setExpanded(False)
        else:
            self.section.setExpanded(True)
            
class ComboBoxUnits(QtWidgets.QComboBox):
    def __init__(self,value=1,baseunit='',prefix='',suffix='',itemmin=0,itemmax=0,parent=None):
        super().__init__(parent)
        self.units = Units(value=value,baseunit=baseunit,prefix=prefix,suffix=suffix)
        self.setEditable(True)
        self.setInsertPolicy(0)
        self.lineEdit().editingFinished.connect(self.textChanged)
        self.currentIndexChanged.connect(self.textChanged)
        #self.currentIndexChanged.
        if itemmin == itemmax:
            if value:
                self.units.update(1,'')
            else:
                self.units.update(0,'')
            self.addItem(self.units.text)
        for i in range(itemmax-1,itemmin-1,-1):
            self.units.update(5*10**i,'')
            self.addItem(self.units.text)
            self.units.update(2*10**i,'')
            self.addItem(self.units.text)
            self.units.update(1*10**i,'')
            self.addItem(self.units.text)
        self.units.update(value,prefix) # revert to original
        self.setEditText(self.units.text)
    
    valueChanged = QtCore.pyqtSignal(float) # used to emit when the value, through either text or other method, changed
        
    def textChanged(self):
        self.units.setUnits(self.currentText())
        self.setEditText(self.units.text)
        self.valueChanged.emit(self.units.getFullValue())
        
    
#    def valueChanged(self):
        
        
#class treeSections():
#    def __init__(self,treeitem):
#        self.tree = treeitem
#        self.sections = []
#        self.define_sections()
#        self.add_sections()
#        
#        self.sampcfg = SampCfg()
#        frame = QtWidgets.QFrame(self.tree)
#        self.taxis = treeSampling(frame,"samp",self.sampcfg)
#        item = QtWidgets.QTreeWidgetItem()
#        self.tree.addTopLevelItem(item)
#        self.tree.setItemWidget(item,0,SectionExpandButton(item, text = "Horizontal"))
#        section = QtWidgets.QTreeWidgetItem(item)
#        section.setDisabled(True)
#        self.tree.setItemWidget(section,0,frame)
#        item.addChild(section)
#        
#        self.trigcfg = TrigCfg()
#        frame = QtWidgets.QFrame(self.tree)
#        self.triggering = treeTrigger(frame,"samp",self.trigcfg)
#        item = QtWidgets.QTreeWidgetItem()
#        self.tree.addTopLevelItem(item)
#        self.tree.setItemWidget(item,0,SectionExpandButton(item, text = "Triggering"))
#        section = QtWidgets.QTreeWidgetItem(item)
#        section.setDisabled(True)
#        self.tree.setItemWidget(section,0,frame)
#        item.addChild(section)
#        
#        self.ch1scope = ScopeCfg()
#        frame = QtWidgets.QFrame(self.tree)
#        self.ch1 = treeScope(frame,"sch1",self.ch1scope)
#        item = QtWidgets.QTreeWidgetItem()
#        self.tree.addTopLevelItem(item)
#        self.tree.setItemWidget(item,0,SectionExpandButton(item, text = "Scope Channel A"))
#        section = QtWidgets.QTreeWidgetItem(item)
#        section.setDisabled(True)
#        self.tree.setItemWidget(section,0,frame)
#        item.addChild(section)
#        
#        self.ch2scope = ScopeCfg()
#        frame = QtWidgets.QFrame(self.tree)
#        self.ch2 = treeScope(frame,"schb",self.ch2scope)
#        item = QtWidgets.QTreeWidgetItem()
#        self.tree.addTopLevelItem(item)
#        self.tree.setItemWidget(item,0,SectionExpandButton(item, text = "Scope Channel B"))
#        section = QtWidgets.QTreeWidgetItem(item)
#        section.setDisabled(True)
#        self.tree.setItemWidget(section,0,frame)
#        item.addChild(section)
#        
#        self.ch1awg = AWGCfg()
#        frame = QtWidgets.QFrame(self.tree)
#        self.awgch1 = treeAWG(frame,"fcha",self.ch1awg)
#        item = QtWidgets.QTreeWidgetItem()
#        self.tree.addTopLevelItem(item)
#        self.tree.setItemWidget(item,0,SectionExpandButton(item, text = "Function Generator A"))
#        section = QtWidgets.QTreeWidgetItem(item)
#        section.setDisabled(True)
#        self.tree.setItemWidget(section,0,frame)
#        item.addChild(section)
#        
#        self.ch2awg = AWGCfg()
#        frame = QtWidgets.QFrame(self.tree)
#        self.awgch2 = treeAWG(frame,"fchb",self.ch2awg)
#        item = QtWidgets.QTreeWidgetItem()
#        self.tree.addTopLevelItem(item)
#        self.tree.setItemWidget(item,0,SectionExpandButton(item, text = "Function Generator B"))
#        section = QtWidgets.QTreeWidgetItem(item)
#        section.setDisabled(True)
#        self.tree.setItemWidget(section,0,frame)
#        item.addChild(section)
        
    def add_button(self, title):
        '''creates a QTreeWidgetItem containing a button
        to expand or collapse its section
        '''
        item = QtWidgets.QTreeWidgetItem()
        self.tree.addTopLevelItem(item)
        self.tree.setItemWidget(item, 0, SectionExpandButton(item, text = title))
        return item

    def add_widget(self, button, widget):
        '''creates a QWidgetItem containing the widget,
        as child of the button-QWidgetItem
        '''
        section = QtWidgets.QTreeWidgetItem(button)
        section.setDisabled(True)
        self.tree.setItemWidget(section, 0, widget)
        return section
    
class treeScope(object):
    def __init__(self, par_widget,name_append,cfgobj):
        #Form.setObjectName("Form")
        #Form.resize(247, 136)
        #Form.setMinimumSize(QtCore.QSize(0, 0))
        self.formLayout = QtWidgets.QFormLayout(par_widget)
        self.formLayout.setVerticalSpacing(0)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout"+name_append)
        
        self.label = QtWidgets.QLabel(par_widget)
        self.label.setObjectName("label"+name_append)
        self.label.setText("Volts/Div")
        cfgobj.scale = ComboBoxUnits(1,'V','','/div',-3,1,parent=par_widget)
        cfgobj.scale.setObjectName("scale"+name_append)
        
        self.label_2 = QtWidgets.QLabel(par_widget)
        self.label_2.setObjectName("label_2"+name_append)
        self.label_2.setText("Vertical Offset")
        cfgobj.voff = ComboBoxUnits(0,'V','','',-3,1,parent=par_widget)
        cfgobj.voff.setObjectName("voff"+name_append)
        
        self.label_3 = QtWidgets.QLabel(par_widget)
        self.label_3.setObjectName("label_3"+name_append)
        self.label_3.setText("Gain")
        cfgobj.chgain = ComboBoxUnits(1,'','','',parent=par_widget)
        cfgobj.chgain.setObjectName("chgain"+name_append)
        
        self.label_4 = QtWidgets.QLabel(par_widget)
        self.label_4.setObjectName("label_4"+name_append)
        self.label_4.setText("DC Offset")
        cfgobj.choff = ComboBoxUnits(0,'V','','',parent=par_widget)
        cfgobj.choff.setObjectName("choff"+name_append)
        
        self.label_5 = QtWidgets.QLabel(par_widget)
        self.label_5.setObjectName("label_5"+name_append)
        self.label_5.setText("Measure Source")
        cfgobj.measawg = QtWidgets.QCheckBox(par_widget)
        cfgobj.measawg.setObjectName("measawg"+name_append)
        
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, cfgobj.scale)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, cfgobj.voff)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, cfgobj.chgain)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, cfgobj.choff)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, cfgobj.measawg)

class treeAWG(object):
    def __init__(self, par_widget,name_append,cfgobj):
        #Form.setObjectName("Form")
        #Form.resize(247, 136)
        #Form.setMinimumSize(QtCore.QSize(0, 0))
        self.formLayout = QtWidgets.QFormLayout(par_widget)
        self.formLayout.setVerticalSpacing(0)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout"+name_append)
        cfgobj.modesel = QtWidgets.QComboBox()
        self.formLayout.setWidget(0,QtWidgets.QFormLayout.SpanningRole,cfgobj.modesel)
        for wave in Waves:
            cfgobj.modesel.addItem(wave.name)
        cfgobj.modesel.setObjectName("modesel"+name_append)
        
        self.label = QtWidgets.QLabel(par_widget)
        self.label.setObjectName("label"+name_append)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(par_widget)
        self.label_2.setObjectName("label_2"+name_append)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(par_widget)
        self.label_3.setObjectName("label_3"+name_append)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtWidgets.QLabel(par_widget)
        self.label_4.setObjectName("label_4"+name_append)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        cfgobj.amp = ComboBoxUnits(1,'V','','',-3,1,parent=par_widget)
        cfgobj.amp.setObjectName("AWGamp"+name_append)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, cfgobj.amp)
        cfgobj.offset = ComboBoxUnits(0,'V','','',parent=par_widget)
        cfgobj.offset.setObjectName("AWGoffset"+name_append)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, cfgobj.offset)
        cfgobj.freq = ComboBoxUnits(1,'Hz','k','',-1,5,parent=par_widget)
        cfgobj.freq.setObjectName("AWGfreq"+name_append)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, cfgobj.freq)
        cfgobj.phase = ComboBoxUnits(0,'deg','','',parent=par_widget)
        cfgobj.phase.setObjectName("AWGphase"+name_append)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, cfgobj.phase)

        self.label.setText("Amplitude")
        self.label_2.setText("DC Offset")
        self.label_3.setText("Frequency")
        self.label_4.setText("Phase")

class treeSampling(object):
    def __init__(self, par_widget,name_append,cfgobj):
        #Form.setObjectName("Form")
        #Form.resize(247, 136)
        #Form.setMinimumSize(QtCore.QSize(0, 0))
        self.formLayout = QtWidgets.QFormLayout(par_widget)
        self.formLayout.setVerticalSpacing(0)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout"+name_append)
        self.label = QtWidgets.QLabel(par_widget)
        self.label.setObjectName("label"+name_append)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        cfgobj.hscale = ComboBoxUnits(value=1,baseunit='s',prefix='',suffix='/div',itemmin=-6,itemmax=1)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, cfgobj.hscale)
        
        self.label_2 = QtWidgets.QLabel(par_widget)
        self.label_2.setObjectName("label_2"+name_append)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        cfgobj.position = ComboBoxUnits(value=0,baseunit='s',prefix='',suffix='')
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, cfgobj.position)

        self.label.setText("Scale")
        self.label_2.setText("Position")

class treeTrigger(object):
    def __init__(self, par_widget,name_append,cfgobj):
        #Form.setObjectName("Form")
        #Form.resize(247, 136)
        #Form.setMinimumSize(QtCore.QSize(0, 0))
        self.formLayout = QtWidgets.QFormLayout(par_widget)
        self.formLayout.setVerticalSpacing(0)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout"+name_append)
        self.label = QtWidgets.QLabel(par_widget)
        self.label.setObjectName("label"+name_append)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        cfgobj.source = QtWidgets.QComboBox()
        cfgobj.source.addItem("Channel A")
        cfgobj.source.addItem("Channel B")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, cfgobj.source)
        
        self.label_2 = QtWidgets.QLabel(par_widget)
        self.label_2.setObjectName("label_2"+name_append)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        cfgobj.edge = QtWidgets.QComboBox()
        cfgobj.edge.addItem("Rising")
        cfgobj.edge.addItem("Falling")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, cfgobj.edge)
        
        self.label_3 = QtWidgets.QLabel(par_widget)
        self.label_3.setObjectName("label_2"+name_append)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        cfgobj.level = ComboBoxUnits(0,'V','','',0,0,par_widget)
        cfgobj.level.setObjectName("doubleSpinBox"+name_append)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, cfgobj.level)

        self.label.setText("Source")
        self.label_2.setText("Edge")
        self.label_3.setText("Level")
