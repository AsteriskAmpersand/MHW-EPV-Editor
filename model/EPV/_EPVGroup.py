# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 02:52:33 2020

@author: AsteriskAmpersand
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QItemDelegate, QSpinBox
from PyQt5 import QtWidgets

from model.QList import QList
from model.EPV._EPVRecord import EPVRecord
from structs.epv import group as binaryGroup
from structs.epv import extendedGroup as binaryExtendedGroup

class GroupRecordDelegate(QItemDelegate):
    def createEditor(self, parent, option, index):
        box = QSpinBox(parent)
        box.setMaximum(2**16-1)        
        return box

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        editor.setValue(value)

    def setModelData(self, editor, model, index):
        value = editor.value()
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
        return {"groupID" : self.groupID,
                "recordCount":len(self),
                "records":[record.serialize() for record in self]}        
    def EPVSerialize(self,struct):return struct.build(self.blockSerialize())
    def binarySerialize(self):return self.EPVSerialize(binaryGroup)
    def binaryExtendedSerialize(self):return self.EPVSerialize(binaryExtendedGroup)
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