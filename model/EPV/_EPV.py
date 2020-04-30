# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 21:54:37 2020

@author: AsteriskAmpersand
"""


from structs.epv import EPVFile
from model.Queue import Queue, Stack
from model.EPV._EPVGroup import EPVGroup
from model.EPV._EPVRecord import EPVRecord

from PyQt5.QtCore import Qt
from PyQt5 import QtCore,QtWidgets
import sys

def catch_exceptions(t, val, tb):
    QtWidgets.QMessageBox.critical(None,
                                   "An exception was raised",
                                   "Exception type: {}".format(tb))
    old_hook(t, val, tb)

old_hook = sys.excepthook
sys.excepthook = catch_exceptions
    
class EPV(QtCore.QAbstractItemModel):
    idEdited = QtCore.pyqtSignal(object)
    undoableAction = QtCore.pyqtSignal(object)
    
    from ._EPVEditOperations import (flags,supportedDropActions,mimeTypes,mimeData,
                                     canDropMimeData,dropIntoQuery,removeRows,_deleteRecord,
                                     _insertRecord,insertRecord,replaceRecord,moveinto,
                                     _internalMoveTo,dropMimeData)
    
    from ._EPVUndo import (startRecording,addEvent,endRecording,discardRecording,
                           recordState,undo,redo,)
    
    def __init__(self, parent = None, filepath = None):
        super().__init__(parent)
        self.undoStack = Stack()
        self.redoQueue = Queue()
        self.movePending = False
        self.__parent__ = parent
        self.children = []
        if filepath is None:
            self.signature = 219051094117
            self.epvPath = ""
            self.path = None
        else:
            f = EPVFile(filepath)
            self.signature = f.header.signature
            self.toBlocks(f.body,f.trail.trails)
            self.epvPath = f.trail.epvPath
            self.path = filepath
    
    def append(self,item):
        self.children.append(item)
    def __getitem__(self,key):
        return self.children[key]
    def __setitem__(self,key,value):
        self.children[key] = value
    def __len__(self):
        return len(self.children)
    def find(self,item):
        return self.children.index(item)
    def __iter__(self):
        return iter(self.children)    
    def __contains__(self, val):
        return val in self.children
    def pop(self,ix):
        return self.list.pop(ix)
    
    def serialize(self):
        header = {"signature":self.signature}
        blocks = {"count":len(self.blocks),"blocks":sum(map(lambda x: x.blockSerialize(),self.blocks),[])}
        trails = []
        for gix,group in enumerate(self.blocks):
            for rix,record in enumerate(group):
                trails.append({"blockID":gix,"recordID":rix,"trailID":record.trailID})
        trail = {"padding":0,"trailCount":self.blocks.recordCount(),
                 "trails":trails,"epvPath":self.epvPath,"ONE":1,"NULL":0}
        return EPVFile.file_serialize(header,blocks,trail)
               
    def addGroup(self, group):
        self.append(group)
    
    def newGroup(self):
        ngroup = EPVGroup()
        self.addGroup(ngroup)
    
    def toBlocks(self,body,trails):
        recordTrails = iter(trails)
        for group in body.blocks:
            self.addGroup(EPVGroup(self,group,recordTrails))
            
    def data(self, index, role):
        if not index.isValid():
            return None
        item = index.internalPointer()
#        print("%d %d %s"%(index.row(),index.column(),index.internalPointer()))
#        print(index.row())
#        print(len(item))
        return item[index.row()].getRole(role)
    
    def _setData(self,index,value,role):
        item = index.internalPointer()
        item[index.row()].setRole(value,role)
    
    def setData(self,index,value,role):
        if not index.isValid():
            return False
        item = index.internalPointer()
        prev = item[index.row()].getRole(role)
        
        def doSet(v):
            self._setData(index,v,role)
            self.idEdited.emit(index)            
            self.dataChanged.emit(index,index,[role])
            
        self.recordState(doSet,[prev],
                         doSet,[value])
        
        self._setData(index,value,role)
        
        self.idEdited.emit(index)            
        self.dataChanged.emit(index,index,[role])
        self.undoableAction.emit(self)
        return True
    
    def access(self,index):
        if not index.isValid():
            return self
        else:
            return index.internalPointer()[index.row()]
    
    def index(self, row, column, parent=QtCore.QModelIndex):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()
        if not parent.isValid():
            parentItem = self
        else:
            parentPointer = parent.internalPointer()
            try:
                parentItem = parentPointer[parent.row()]
            except:
                parentItem = None
        if parentItem:
            return self.createIndex(row, column, parentItem)
        else:
            return QtCore.QModelIndex()
        
    def parent(self, index=QtCore.QModelIndex()):
        if not index.isValid():
            return QtCore.QModelIndex()

        parent = index.internalPointer()

        if parent == self:
            return QtCore.QModelIndex()

        return self.createIndex(parent.row(), 0, parent.parent())

    def rowCount(self, parent):
        #print("%d %d %s"%(parent.row(),parent.column(),parent.internalPointer()))
        if not parent.isValid():
            parentItem = self
        else:
            parentItem = parent.internalPointer()[parent.row()]
        if not hasattr(parentItem,"__len__"):
            return 0
        return len(parentItem)

    def columnCount(self, parent):
        if type(parent.internalPointer) is EPVRecord:
            return 0
        return 1
    
    """
    def recordState(self,undoerFunction,undoerParameters):
        self.undoStack.put((undoerFunction,undoerParameters))
    def undo(self):
        func,param = self.undoStack.pop()
        func(*param)
        self.redoQueue.put(self.undoStack.pop())
    def redo(self):
        func,param = self.redoQueue.pop()
        func(*param)
    """