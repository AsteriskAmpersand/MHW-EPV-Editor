# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 21:54:37 2020

@author: AsteriskAmpersand
"""


from structs.epv import EPVFile, EPVExtraneousProperties
from model.Queue import Queue, Stack
from model.EPVElements import (EPVC, objectType)
from model.QList import QList
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QItemDelegate, QSpinBox
from PyQt5 import QtCore,QtWidgets
import sys

def catch_exceptions(t, val, tb):
    QtWidgets.QMessageBox.critical(None,
                                   "An exception was raised",
                                   "Exception type: {}".format(tb))
    old_hook(t, val, tb)

old_hook = sys.excepthook
sys.excepthook = catch_exceptions

class EPVRecord():
    def __init__(self,parent=None,record = None,trailID = 0):
        if record is None:
            self.recordID = 0
            self.path0,self.path1,self.path2,self.path3 = "","","",""
            self.boneID = 255
            self.epvc = [EPVC() for i in range(8)]
            self.trailID = trailID
            for prop in EPVExtraneousProperties:
                setattr(self,prop,objectType(EPVExtraneousProperties[prop])(None))
        else:
            self.recordID = record.recordID
            self.path0,self.path1,self.path2,self.path3 = record.packed_path
            self.boneID = record.boneID
            self.epvc = [EPVC(record.epvColor[i]) for i in range(8)]
            self.trailID = trailID
            for prop in EPVExtraneousProperties:
                setattr(self,prop,objectType(EPVExtraneousProperties[prop])(getattr(record,prop)))
        self.__parent__ = parent
        
    def serialize(self):
        export = {}
        export["packed_path"] = [str(self.path0).replace("\x00"),str(self.path1).replace("\x00"),
                                 str(self.path2).replace("\x00"),str(self.path3).replace("\x00")]
        export["recordID"] = self.recordID
        export["boneID"] = self.boneID
        export["epvColor"] = [epvc.serialize() for epvc in self.epvc]
        for prop in EPVExtraneousProperties:
            sprop = getattr(self,prop)
            export[prop] = sprop.serialize() if hasattr(sprop,"serialize") else sprop
    def getRole(self,role):
        if role == Qt.DisplayRole:
            Display = "Record ID: %s - %s"%(self.recordID,self.path0)
            return Display
        if role == Qt.EditRole:
            return self.recordID
        
    def setRole(self,value,role):
        if role == Qt.EditRole:
            self.recordID = value

class GroupRecordDelegate(QItemDelegate):
    def createEditor(self, parent, option, index):
        box = QSpinBox(parent)
        box.setMaximum(2**16-1)        
        return box

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        editor.setValue(value)

    def setModelData(self, editor, model, index):
        QtWidgets.QMessageBox.critical(None,
                               "No Error","No Error")
        value = editor.value()
        QtWidgets.QMessageBox.critical(None,
                               "No Error 2","No Error 2")
        model.setData(index, value, Qt.EditRole)

class EPVGroup(QList):
    def __init__(self,parent = None, group = None,trails = None):
        self.groupID = 0
        #self.records = QList()
        super().__init__(parent,[])
        if group is not None and trails is not None:
            self.fromBlock(group, trails)

    def fromBlock(self,group,trails):
        self.groupID = group.groupID
        for record,trail in zip(group.records,trails):
            self.append(EPVRecord(self,record,trail.trailID))
            
    def blockSerialize(self):
        return {"count":len(self),
                "records":[record.serialize() for record in self]}        
        
    def getRole(self,role):
        if role == Qt.DisplayRole:
            Display = "Group ID: %s - %s Record%s"%(self.groupID,len(self),"s" if len(self)>1 else "")
            return Display
        if role == Qt.EditRole:
            return self.groupID
    
    def setRole(self,value,role):
        if role == Qt.EditRole:
            self.groupID = value
        
    def row(self):
        if self.__parent__:
            return self.__parent__.find(self)
    
class EPV(QtCore.QAbstractItemModel):
    idEdited = QtCore.pyqtSignal(object)
    undoableAction = QtCore.pyqtSignal(object)
    def __init__(self, parent = None, filepath = None):
        super().__init__(parent)
        self.undoStack = Stack()
        self.redoQueue = Queue()
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
    
    def setData(self,index,value,role,supress=False):
        if not index.isValid():
            return False
        item = index.internalPointer()
        prev = item[index.row()].getRole(role)
        self.recordState(self.setData,[index,prev,role,True])
        item[index.row()].setRole(value,role)
        self.idEdited.emit(index)            
        self.dataChanged.emit(index,index,[role])
        if not supress:
            self.undoableAction.emit(self)
        return True
    
    def access(self,index):
        if not index.isValid():
            return None
        else:
            return index.internalPointer()[index.row()]
    
    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable
    
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
    
    def recordState(self,undoerFunction,undoerParameters):
        self.undoStack.put((undoerFunction,undoerParameters))
    def undo(self):
        func,param = self.undoStack.pop()
        func(*param)
        self.redoQueue.put(self.undoStack.pop())
    def redo(self):
        func,param = self.redoQueue.pop()
        func(*param)