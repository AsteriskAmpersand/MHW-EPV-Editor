# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 21:54:37 2020

@author: AsteriskAmpersand
"""


from structs.epv import EPVFile
from generic.Queue import Queue, Stack

from ._EPVGroup import EPVGroup
from ._EPVRecord import EPVRecord

from PyQt5 import QtCore,QtWidgets
import sys

"""
def catch_exceptions(t, val, tb):
    QtWidgets.QMessageBox.critical(None,
                                   "An exception was raised",
                                   "Exception type: {}".format(tb))
    old_hook(t, val, tb)

old_hook = sys.excepthook
sys.excepthook = catch_exceptions
"""
 
class EPV(QtCore.QAbstractItemModel):
    idEdited = QtCore.pyqtSignal(object)
    epvEdited = QtCore.pyqtSignal(object,int)
    pathEdited = QtCore.pyqtSignal(object,int)
    undoableAction = QtCore.pyqtSignal(object)
    
    from ._EPVUndo import (clearRedoStack,discardRecording,endRecording,recordState,redo,startRecording,undo,invalidateCaches)
    from ._EPVEditOperations import (_deleteGroup,_deleteRecord,_dropData,_insertGroup,_insertRecord,_replaceRecord,canDropMimeData,deleteGroup,deleteRecord,dropIntoQuery,dropMimeData,flags,hexRepresent,insertGroup,insertRecord,mimeData,mimeTypes,moveinto,newGroup,newRecord,removeRows,replaceRecord,supportedDropActions)
    from ._EPVCopyStack import (deepcopy,mixedStackQuery,pastePureStack,pasteStack)
    from ._EPVSearchOperations import (getStringReferences,getColorReferences)
    from ._EPVReplace import (_colorReplace,_pathReplace,colorReplace,endReplace,pathReplace,startReplace)
    
    def __init__(self, parent = None, filepath = None):
        super().__init__(parent)
        self.undoStack = Stack()
        self.redoStack = Queue()
        self.movePending = False
        self.complexUndo = False
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
        blocks = {"count":len(self.children),"blocks":list(map(lambda x: x.blockSerialize(),self.children))}
        trails = []
        for gix,group in enumerate(self.children):
            for rix,record in enumerate(group):
                trails.append({"blockID":gix,"recordID":rix,"trailID":record.trailID})
        trail = {"padding":0,"trailCount":sum((len(c) for c in self.children)),
                 "trails":trails,"epvPath":self.epvPath,"ONE":1,"NULL":0}
        return EPVFile.file_serialize(header,blocks,trail)
               
    def addGroup(self, group):
        self.append(group)
    
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
    
    def index(self, row, column, parent=QtCore.QModelIndex()):
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
            parentObject = parent.internalPointer()
            #if len(parentObject)<=parent.row():
            #    print("Index invalidated at some point")
            #    return 0
            #This case should never happen but QT sometiems hickups on invalid indexes
            parentItem = parentObject[parent.row()]
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
        self.redoStack.put(self.undoStack.pop())
    def redo(self):
        func,param = self.redoStack.pop()
        func(*param)
    """