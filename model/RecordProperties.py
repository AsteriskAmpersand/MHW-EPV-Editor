# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 23:55:32 2020

@author: AsteriskAmpersand
"""
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore
from generic.Queue import Queue,Stack

class RecordProperties(QWidget):
    undoableAction = QtCore.pyqtSignal(object)
    def __init__(self,parent=None):
        super().__init__(parent)
        self.undoStack = Stack()
        self.redoStack = Stack()
        self.setupUI()
        self.functors = []
    def setupUI(self):
        self.ui = self.ui_form()
        self.ui.setupUi(self)
    def connect(self,model):
        self.model = model
        if model:            
            self.fromModel()            
        else:
            self.disconnectSignals()
    def connectSignals(self):
        self.functors = [self.valueChangedGenerator(prop) for prop in self.properties]
        for f,prop in zip(self.functors,self.properties):
            getattr(self.ui,prop).valueChanged.connect(f)
    def disconnectSignals(self):
        for f,prop in zip(self.functors,self.properties):
            try:
                getattr(self.ui,prop).valueChanged.disconnect(f)
            except:
                pass
        self.functors=[]
    def fromModel(self,prop=None):
        self.disconnectSignals()
        if prop is None:
            for prop in self.properties:
                setattr(self,prop,getattr(self.model,prop))
        else:
            setattr(self,prop,self.model)
        self.connectSignals()
    def toModel(self,prop=None):
        if prop is None:
            for props in self.properties:
                setattr(self.model,props,getattr(self,props))
        else:
            setattr(self.model,prop,getattr(self,prop))
    def valueChangedGenerator(self,prop):
        def changed(newval):
            self.valueChanged(prop,newval)
        return changed
    def valueChanged(self,prop,newval):        
        if newval == getattr(self.model,prop):return
        self.recordState(prop)
        self.undoableAction.emit(self)
        self.toModel()
    def recordState(self,prop,target = None,model=None):
        #print("Event Recorded "+prop)
        if model is None:
            model = self.model
        propVal = getattr(model,prop)       
        if target is None: target = self.undoStack.append
        target((model,propVal,prop))        
    def consumeAction(self,action):
        model,value,propertyName = action()
        setattr(model,propertyName,value)
        if model == self.model:
            self.fromModel()
    def do(self,peek,inverse,source):
        model,val,name = peek
        self.recordState(name,inverse,model)
        self.consumeAction(source)        
    def undo(self):
        #if not self.undoStack.empty():
            self.do(self.undoStack.peek(),self.redoStack.put,self.undoStack.pop)
    def redo(self):
        #if not self.redoStack.empty():
            self.do(self.redoStack.peek(),self.undoStack.append,self.redoStack.get)  
    def clearRedoStack(self):
        if not self.redoStack.empty():
            self.redoStack.clear()