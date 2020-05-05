# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 06:34:47 2020

@author: AsteriskAmpersand
"""

from queue import Queue
from PyQt5 import QtCore, QtWidgets
from gui.RecordIDs import Ui_Form
from model.utils import layout_widgets
from model.RecordProperties import RecordProperties

class RecordIDs(RecordProperties):
    ui_form = Ui_Form
    undoableAction = QtCore.pyqtSignal(object)
    def __init__(self,parent=None):
        super().__init__(parent)
        self.rfunctors = []
        self.gfunctors = []
        
    def toggleGroup(self,val):
        for widget in layout_widgets(self.ui.groupMetadata):
            if type(widget) is not QtWidgets.QLabel:
                widget.setEnabled(val)
    def toggleRecords(self,val):
        for layout in layout_widgets(self.ui.recordMetadata):
            for widget in layout_widgets(layout):
                if type(widget) is not QtWidgets.QLabel:
                    widget.setEnabled(val)
    def connect(self,gmodel,rmodel=None):
        self.gmodel = gmodel
        self.rmodel = rmodel        
        if gmodel:            
            self.fromGModel()            
        else:
            self.disconnectGroupSignals()
        if rmodel:
            self.fromRModel()
        else:
            self.disconnectRecordSignals()
    rproperties = ["recordID","trailID","boneID"]
    gproperties = ["groupID"]
    
    @property
    def recordID(self):return self.ui.recordID.value()
    @recordID.setter
    def recordID(self,value):self.ui.recordID.setValue(value)
    @property
    def trailID(self):return self.ui.trailID.value()
    @trailID.setter
    def trailID(self,value):self.ui.trailID.setValue(value)
    @property
    def boneID(self):return self.ui.boneID.value()
    @boneID.setter
    def boneID(self,value):self.ui.boneID.setValue(value)
    @property
    def groupID(self):return self.ui.groupID.value()    
    @groupID.setter
    def groupID(self,value):self.ui.groupID.setValue(value)
    
    def IDUpdated(self,record,group,updatecurrent):
        self.fromModel(self.rmodel,prop="recordID")
        self.fromModel(self.gmodel,prop="groupID")
    
    def connectSignals(self,functors,listing):
        for f,prop in zip(functors,listing):
            getattr(self.ui,prop).valueChanged.connect(f)
    def disconnectSignals(self,functors,properties):
        for f,p in zip(functors,properties):
            try:
                getattr(self.ui,p).valueChanged.discconect(f)
            except:
                pass
        functors[:]=[]
    def fromModel(self,model=None,propList=None,prop=None):
        if model is not None and prop is not None:
            setattr(self,prop,getattr(model,prop))
        elif model is None or propList is None:
            if self.gmodel:
                self.fromModel(self.gmodel,self.gproperties)
            if self.rmodel:
                self.fromModel(self.rmodel,self.rproperties)    
        elif prop is None:
            for prop in propList:
                setattr(self,prop,getattr(model,prop))
    def toModel(self,model,propList,prop=None):
        if prop is None:
            for prop in propList:
                setattr(model,prop,getattr(self,prop))
        else:
            setattr(model,prop,getattr(self,prop))       
            
    def connectRecordSignals(self):
        self.rfunctors = []
        for prop in self.rproperties:
            self.rfunctors.append(self.valueChangedGenerator(prop))
        self.connectSignals(self.rfunctors,self.rproperties)
    def disconnectRecordSignals(self):self.disconnectSignals(self.rfunctors,self.rproperties)
    def fromRModel(self,prop=None):
        self.disconnectRecordSignals()
        self.fromModel(self.rmodel,self.rproperties,prop)
        self.connectRecordSignals()
    def toRModel(self,prop=None):self.toModel(self.rmodel,self.rproperties,prop)
    
    def connectGroupSignals(self):
        self.gfunctors = []
        for prop in self.gproperties:
            self.gfunctors.append(self.valueChangedGenerator(prop))
        self.connectSignals(self.gfunctors,self.gproperties)
    def disconnectGroupSignals(self):self.disconnectSignals(self.gfunctors,self.gproperties)
    def fromGModel(self,prop=None):
        self.disconnectGroupSignals()
        self.fromModel(self.gmodel,self.gproperties,prop)
        self.connectGroupSignals()
    def toGModel(self,prop=None):
        self.toModel(self.gmodel,self.gproperties,prop)

    def valueChangedGenerator(self,prop):
        def changed(newval):
            self.valueChanged(prop,newval)
        return changed
    def valueChanged(self,prop,newval):
        if prop in self.rproperties:
            model = self.rmodel
            pushModel = self.toRModel
        else:
            model = self.gmodel
            pushModel = self.toGModel
        if newval == getattr(model,prop):
            return
        self.recordState(prop)
        self.undoableAction.emit(self)
        pushModel(prop)
    
    def recordState(self,prop,target = None,model=None):
        if model is None:
            if prop in self.rproperties:
                model = self.rmodel
            else:
                model = self.gmodel
        propVal = getattr(model,prop)       
        if target is None: target = self.undoStack.append
        target((model,propVal,prop))        
    def consumeAction(self,action):
        model,value,propertyName = action()
        setattr(model,propertyName,value)
        if propertyName in self.rproperties:
            cmodel = self.rmodel
            proplist = self.rproperties
        else:
            cmodel = self.gmodel
            proplist = self.gproperties
        if model == cmodel:
            self.fromModel(cmodel,proplist)