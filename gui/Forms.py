# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 05:48:36 2020

@author: AsteriskAmpersand
"""

from PyQt5 import QtWidgets, QtCore, QtGui
from model.utils import layout_widgets
from model.Queue import Queue
from model.RecordProperties import RecordProperties
from structs.epv import parameterBlock1, parameterBlock2
from collections import OrderedDict

def SelectForm(propertyName, propertyType,parent=None):
    if "parameterBlock1" in propertyType:
        return ParameterBlock1(parent)
    if "parameterBlock2" in propertyType:
        return ParameterBlock2(parent)
    if "vector" in propertyType:
        propertyType = "float[3]"
    if "[" in propertyType:
        typing = propertyType.split("[")[0]
        count = int(propertyType.split("[")[1].replace("]",""))
    else:
        typing = propertyType
        count = 1
    form = {"int":QtWidgets.QSpinBox,"uint":QtWidgets.QSpinBox,
            "byte":QtWidgets.QSpinBox,"ubyte":QtWidgets.QSpinBox,
            "short":QtWidgets.QSpinBox,"float":QtWidgets.QDoubleSpinBox,
            "vector":QVectorBox}
    args = {"byte":{"setMinimum":-128,"setMaximum":127},
            "ubyte":{"setMinimum":0,"setMaximum":255,"setValue":0},
            "short":{"setMinimum":-(2**15),"setMaximum":2**15-1},
            "int":{"setMinimum":-(2**31-1),"setMaximum":2**31-1},
            "uint":{"setMinimum":0,"setMaximum":(2**32-1)},
            "float":{"setDecimals":3,"setSingleStep":.001},
            }
    widget = PropertyWidget(count,form[typing],propertyName,parent,**args[typing])
    return widget

def iterable(prop):
    try:
        iter(prop)
        return True
    except:
        return False

class PropertyWidget(RecordProperties):
    def __init__(self,count,widgetType,propertyName,parent = None,**kwargs):
        super().__init__()
        self.rootLayout = QtWidgets.QHBoxLayout(self)
        self.rootLayout.setContentsMargins(0, 2, 0, 0)
        self.rootLayout.setSpacing(0)
        self.rootLayout.setObjectName("PropertyLayout")        
        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName("Label")
        self.label.setMinimumWidth(120)
        self.rootLayout.addWidget(self.label)   
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 2, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("EntryLayout")   
        for i in range(count):
            widget = widgetType(self)
            for val in kwargs:
                getattr(widget,val)(kwargs[val])      
            self.horizontalLayout.addWidget(widget)     
        self.rootLayout.addLayout(self.horizontalLayout)   
        self.rootLayout.setStretch(0,1)
        self.rootLayout.setStretch(1,3)
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Property", propertyName))
        self.propertyName = propertyName
    def setupUI(self):pass
    def connect(self,model):
        self.model = model
        if model:
            self.fromModel()       
            self.connectSignals()
        else:
            self.disconnectSignals()
            pass
    def fromModel(self):
        prop = getattr(self.model,self.propertyName)
        if not(iterable(prop)):
            prop = [prop]
            #print("%d/%d"%(len(prop),self.horizontalLayout.count()))
        for w,p in zip(layout_widgets(self.horizontalLayout),prop):
            w.setValue(p)
    def valueChanged(self):
        self.recordState(self.propertyName)
        self.undoableAction.emit(self)
        self.toModel()
    def toModel(self):
        prop = list(layout_widgets(self.horizontalLayout))
        if len(prop) == 1:
            prop = prop[0].value()
            setattr(self.model,self.propertyName,prop)
        else:
            for i,v in enumerate(prop):
                getattr(self.model,self.propertyName)[i]=v.value()
    def connectSignals(self):
        prop = list(layout_widgets(self.horizontalLayout))
        for w in prop:
            w.valueChanged.connect(self.valueChanged)
    def disconnectSignals(self):
        try:
            prop = list(layout_widgets(self.horizontalLayout))
            for w in prop:
                w.valueChanged.disconnect(self.valueChanged)
        except:
            pass

class QVectorBox(QtWidgets.QWidget):
    def __init__(self,parent = None,**kwargs):
        super().__init__(parent)

class PropBlock(QtWidgets.QWidget):
    undoableAction = QtCore.pyqtSignal(object)
    def __init__(self,parent = None,**kwargs):
        super().__init__(parent)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 3, 0, 3)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("PropertyLayout")
        for prop in self.propblock:
            widget = SelectForm(prop,self.propblock[prop],parent)
            self.verticalLayout.addWidget(widget)
    def connect(self,model):
        self.model = model
        root = getattr(self.model,self.propname) if model else None
        for widget in layout_widgets(self.verticalLayout):
            widget.connect(root)
        if model:      
            self.connectSignals()
        else:
            self.disconnectSignals()
    def connectSignals(self):
        for widget in layout_widgets(self.verticalLayout):
            widget.undoableAction.connect(self.passSignal)
    def disconnectSignals(self):        
        for widget in layout_widgets(self.verticalLayout):
            try:
                widget.undoableAction.disconnect(self.passSignal)
            except:
                pass
    def passSignal(self,responsible):
        self.undoableAction.emit(responsible)

class ParameterBlock1(PropBlock):
    propname = "parameterBlock1"
    propblock = OrderedDict([(i.name,i.docs) for i in parameterBlock1.subcons])

class ParameterBlock2(PropBlock):
    propname = "parameterBlock2"
    propblock = OrderedDict([(i.name,i.docs) for i in parameterBlock2.subcons])