# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'adalm1000_mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import widgetbox

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
        self.frame = QtWidgets.QFrame(self.splitter)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.treeWidget = QtWidgets.QTreeWidget(self.splitter)
        self.treeWidget.setIndentation(0)
        self.treeWidget.setAnimated(True)
        self.treeWidget.setRootIsDecorated(False)
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setObjectName("treeWidget")
        self.treeSecs = treeSections(self.treeWidget)
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


class SectionExpandButton(QtWidgets.QPushButton):
    '''a QPushbutton that can expand or collapse its section
    '''
    def __init__(self, item, text = '', parent = None):
        super().__init__(text, parent)
        self.section = item
        self.clicked.connect(self.on_clicked)
        self.setStyleSheet("text-align: left;padding-left: 2px;")
        self.setFlat(True)

    def on_clicked(self):
        '''toggle expand/collapse of section by clicking
        '''
        if self.section.isExpanded():
            self.section.setExpanded(False)
        else:
            self.section.setExpanded(True)

class treeSections():
    def __init__(self,treeitem):
        self.tree = treeitem
        self.sections = []
        #self.define_sections()
        #self.add_sections()
        frame = QtWidgets.QFrame(self.tree)
        ch1 = treeScope(frame,"sch1")
        item = QtWidgets.QTreeWidgetItem()
        self.tree.addTopLevelItem(item)
        self.tree.setItemWidget(item,0,SectionExpandButton(item, text = "Scope Channel A"))
        section = QtWidgets.QTreeWidgetItem(item)
        section.setDisabled(True)
        self.tree.setItemWidget(section,0,frame)
        item.addChild(section)
        
        frame = QtWidgets.QFrame(self.tree)
        ch2 = treeAWG(frame,"schb")
        item = QtWidgets.QTreeWidgetItem()
        self.tree.addTopLevelItem(item)
        self.tree.setItemWidget(item,0,SectionExpandButton(item, text = "Scope Channel B"))
        section = QtWidgets.QTreeWidgetItem(item)
        section.setDisabled(True)
        self.tree.setItemWidget(section,0,frame)
        item.addChild(section)
        
        frame = QtWidgets.QFrame(self.tree)
        ch2 = treeAWG(frame,"fcha")
        item = QtWidgets.QTreeWidgetItem()
        self.tree.addTopLevelItem(item)
        self.tree.setItemWidget(item,0,SectionExpandButton(item, text = "Function Generator A"))
        section = QtWidgets.QTreeWidgetItem(item)
        section.setDisabled(True)
        self.tree.setItemWidget(section,0,frame)
        item.addChild(section)
        
        frame = QtWidgets.QFrame(self.tree)
        ch2 = treeScope(frame,"fchb")
        item = QtWidgets.QTreeWidgetItem()
        self.tree.addTopLevelItem(item)
        self.tree.setItemWidget(item,0,SectionExpandButton(item, text = "Function Generator B"))
        section = QtWidgets.QTreeWidgetItem(item)
        section.setDisabled(True)
        self.tree.setItemWidget(section,0,frame)
        item.addChild(section)
        
    def add_sections(self):
        for (title,widget) in self.sections:
            button1 = self.add_button(title)
            section1 = self.add_widget(button1,widget)
            button1.addChild(section1)
    
    def define_sections(self):
        '''reimplement this to define all your sections
        and add them as (title, widget) tuples to self.sections
        '''
        widget = QtWidgets.QFrame(self.tree)
        layout = QtWidgets.QHBoxLayout(widget)
        layout.addWidget(QtWidgets.QLabel('Bla'))
        layout.addWidget(QtWidgets.QLabel('Blubb'))
        title = 'Section 1'
        self.sections.append((title, widget))
        
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
    def __init__(self, par_widget,name_append):
        #Form.setObjectName("Form")
        #Form.resize(247, 136)
        #Form.setMinimumSize(QtCore.QSize(0, 0))
        self.formLayout = QtWidgets.QFormLayout(par_widget)
        self.formLayout.setVerticalSpacing(0)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout"+name_append)
        self.label = QtWidgets.QLabel(par_widget)
        self.label.setObjectName("label"+name_append)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label)
        self.label_2 = QtWidgets.QLabel(par_widget)
        self.label_2.setObjectName("label_2"+name_append)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(par_widget)
        self.label_3.setObjectName("label_3"+name_append)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_3)
        self.label_4 = QtWidgets.QLabel(par_widget)
        self.label_4.setObjectName("label_4"+name_append)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_4)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(par_widget)
        self.doubleSpinBox.setDecimals(3)
        self.doubleSpinBox.setObjectName("doubleSpinBox"+name_append)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.doubleSpinBox)
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(par_widget)
        self.doubleSpinBox_2.setDecimals(3)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2"+name_append)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.doubleSpinBox_2)
        self.doubleSpinBox_3 = QtWidgets.QDoubleSpinBox(par_widget)
        self.doubleSpinBox_3.setDecimals(3)
        self.doubleSpinBox_3.setObjectName("doubleSpinBox_3"+name_append)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.doubleSpinBox_3)
        self.doubleSpinBox_4 = QtWidgets.QDoubleSpinBox(par_widget)
        self.doubleSpinBox_4.setDecimals(3)
        self.doubleSpinBox_4.setObjectName("doubleSpinBox_4"+name_append)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.doubleSpinBox_4)

        self.label.setText("Volts/Div")
        self.label_2.setText("Vertical Offset")
        self.label_3.setText("Gain")
        self.label_4.setText("DC Offset")

class treeAWG(object):
    def __init__(self, par_widget,name_append):
        #Form.setObjectName("Form")
        #Form.resize(247, 136)
        #Form.setMinimumSize(QtCore.QSize(0, 0))
        self.vLayout = QtWidgets.QVBoxLayout(par_widget)
        self.modesel = QtWidgets.QComboBox()
        self.vLayout.addWidget(self.modesel)
        self.modesel.addItem("OFF")
        self.modesel.addItem("DC")
        self.modesel.addItem("Sine")
        self.modesel.addItem("Sawtooth")
        self.modesel.addItem("Square")
        
        self.formLayout = QtWidgets.QFormLayout()
        self.vLayout.addLayout(self.formLayout)
        self.formLayout.setVerticalSpacing(0)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout"+name_append)
        self.label = QtWidgets.QLabel(par_widget)
        self.label.setObjectName("label"+name_append)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label)
        self.label_2 = QtWidgets.QLabel(par_widget)
        self.label_2.setObjectName("label_2"+name_append)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(par_widget)
        self.label_3.setObjectName("label_3"+name_append)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_3)
        self.label_4 = QtWidgets.QLabel(par_widget)
        self.label_4.setObjectName("label_4"+name_append)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.label_4)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(par_widget)
        self.doubleSpinBox.setDecimals(3)
        self.doubleSpinBox.setObjectName("doubleSpinBox"+name_append)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.doubleSpinBox)
        self.doubleSpinBox_2 = QtWidgets.QDoubleSpinBox(par_widget)
        self.doubleSpinBox_2.setDecimals(3)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox"+name_append)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.doubleSpinBox_2)
        self.doubleSpinBox_3 = QtWidgets.QDoubleSpinBox(par_widget)
        self.doubleSpinBox_3.setDecimals(3)
        self.doubleSpinBox_3.setObjectName("doubleSpinBox"+name_append)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.doubleSpinBox_3)
        self.doubleSpinBox_4 = QtWidgets.QDoubleSpinBox(par_widget)
        self.doubleSpinBox_4.setDecimals(3)
        self.doubleSpinBox_4.setObjectName("doubleSpinBox"+name_append)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.doubleSpinBox_4)

        self.label.setText("Volts/Div")
        self.label_2.setText("Vertical Offset")
        self.label_3.setText("Gain")
        self.label_4.setText("DC Offset")
