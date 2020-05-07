# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 03:27:40 2020

@author: AsteriskAmpersand
"""
from PyQt5.QtCore import Qt, QMimeData, QModelIndex
from PyQt5.QtWidgets import QMessageBox
from ._EPVGroup import EPVGroup
from ._EPVRecord import EPVRecord
from ._EPVMimeTypes import EPVMETADATA,EPVGROUP,EPVRECORD,BINARY


def hexRepresent(binaryData):
    return  ' '.join(list(map(lambda x: "%02X"%x,binaryData)))

def flags(self, index):
    if not index.isValid():
        return Qt.ItemIsDropEnabled# | Qt.ItemIsDragEnabled #Qt.NoItemFlags
    if index.internalPointer() == self:
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsDragEnabled |Qt.ItemIsDropEnabled#Qt.NoItemFlags
    return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled 

def supportedDropActions(self):
    return Qt.MoveAction | Qt.CopyAction | Qt.IgnoreAction

def mimeTypes(self):
    return [EPVMETADATA,EPVGROUP,EPVRECORD,BINARY]

def mimeData(self,indices):
    if len(indices)>1:
        QMessageBox.critical(None,
                           "Multiselection not Implemented",
                           "Multiselection has not been implemented for EPV Selections yet.")
    mime = QMimeData()
    index = indices[0]
    
    focus = self.access(index)
    mime.setData(EPVMETADATA,b'')
    mime.internalPointer = focus
    mime.source = self
    if type(focus) is EPVGroup:
        datatype = EPVGROUP 
    elif type(focus) is EPVRecord:
        datatype = EPVRECORD
    else:
        raise ValueError("Unknown Type Exported %s"%type(focus))
    binaryData = focus.binarySerialize()
    mime.setData(BINARY,binaryData)
    mime.setText(hexRepresent(binaryData))
    extendedBinaryData = focus.binaryExtendedSerialize()
    mime.setData(datatype,extendedBinaryData)
    return mime
#QMimeData *QAbstractItemModel::mimeData(const QModelIndexList &indexes)

def canDropMimeData(self,data,action,row,column,parent):
    formats = set(data.formats())
    typings = self.mimeTypes()
    if EPVGROUP in formats and (
         ((row,column) == (-1,-1) and type(parent.internalPointer()) is EPVGroup) or
          (row != -1 and parent.row() != -1 )):
        return False
    if EPVRECORD in formats and not parent.isValid(): return False
    return any((typing in formats for typing in typings))
#if EPVRECORD in 
#print("%d:%d || %d:%d - %s"%(row,column,parent.row(),parent.column(),parent.internalPointer()))
#if row == -1 and column == -1: Disables moving on top but makes the whole thing SUPER HARD TO MOVE
#    return False
    
def dropIntoQuery(self,intoType):
    qbox = QMessageBox()
    if intoType is EPVGroup:
        qbox.setWindowTitle("Merge Group Contents?")
        qbox.setText("""This operation will merge the contents of both groups and
keep destination group id.
Are you sure you want to do this?""")
        qbox.setStandardButtons(QMessageBox.Yes)
        qbox.addButton(QMessageBox.Cancel)
    elif intoType is EPVRecord:
        qbox.setWindowTitle("Replace Record Contents?")
        qbox.setText("""This operation will replace this Record.
Are you sure you want to do this?""")
        qbox.setStandardButtons(QMessageBox.Yes)
        qbox.addButton(QMessageBox.Cancel)
    return qbox

def removeRows(self,row,count,parent):
    parentObj = self.access(parent)
    #if not self.movePending:
    self.startRecording()
    if type(parentObj) is EPVGroup:
        op = lambda x: self.deleteRecord(parentObj,x)
    elif type(parentObj) is type(self):
        op = self.deleteGroup
    else: return False
    if row+count > len(parentObj):return False
    for ix in range(row,row+count):
        op(ix)
    self.endRecording()
    #self.movePending = False
    return True

def deleteGroup(self,groupIndex):
    self.recordState(self._insertGroup,[self[groupIndex],groupIndex],self._deleteGroup,[groupIndex])
    return self._deleteGroup(groupIndex)

def _deleteGroup(self,groupIndex):
    index = QModelIndex()#self.createIndex(groupIndex,0,self)
    self.beginRemoveRows(index,groupIndex,groupIndex)    
    self[groupIndex:groupIndex+1] = []
    self.endRemoveRows()
    return True

def _insertGroup(self,group,groupIndex):
    index = QModelIndex()
    self.beginInsertRows(index,groupIndex,groupIndex)  
    group.setParent(self)
    self[groupIndex:groupIndex] = [group]
    self.endInsertRows()
    return True

def _replaceGroup(self,group,groupIndex):
    self._removeGroup(groupIndex)
    self._insertGroup(group,groupIndex)
    return True

def insertGroup(self,group,groupIndex = None):
    if groupIndex == None:
        groupIndex = len(self)
    self.recordState(self._deleteGroup,[groupIndex],self._insertGroup,[group,groupIndex])
    return self._insertGroup(group,groupIndex)

def newGroup(self,groupIndex = None):
    ngroup = EPVGroup(self)
    self.insertGroup(ngroup,groupIndex)
    return ngroup
    
def newRecord(self,recordIndex):
    if not recordIndex.isValid():
        recordIndex = self.index(len(self)-1,0,QModelIndex())
    if type(self.access(recordIndex)) is EPVRecord:
        recordIndex = recordIndex.parent()
    group = self.access(recordIndex)
    self.insertRecord(group,EPVRecord(group))
    
def _deleteRecord(self,group,position):
    index = self.createIndex(group.row(),0,group.parent())
    self.beginRemoveRows(index,position,position)    
    group[position:position+1] = []    
    self.endRemoveRows()
    return True

def deleteRecord(self,group,position):
    self.recordState(self._insertRecord,[group,group[position],position],self._deleteRecord,[group,position])
    return self._deleteRecord(group,position)

def _insertRecord(self,group,record,position):
    index = self.createIndex(group.row(),0,group.parent())
    self.beginInsertRows(index,position,position)
    record.setParent(group)
    group[position:position] = [record]
    self.endInsertRows()
    return True

def insertRecord(self,group,record,position=None):
    if position is None:
        position = len(group)
    self.recordState(self._deleteRecord,[group,position],self._insertRecord,[group,record,position])
    return self._insertRecord(group,record,position)
    
def _replaceRecord(self,index,record):
    self.deleteRecord(index.internalPointer(),index.row())
    self.insertRecord(index.internalPointer(),record,index.row())
    
def replaceRecord(self,index,record):
    self.startRecording()
    self.deleteRecord(index.internalPointer(),index.row())
    self.insertRecord(index.internalPointer(),record,index.row())
    self.endRecording()

def moveinto(self,index,data):
    if type(data) is EPVGroup:
        for children in data:
            self.insertRecord(index.internalPointer()[index.row()],children)
    elif type(data) is EPVRecord:
        self._replaceRecord(index,data)
        
    
# x  0 || -1:-1 None -> Moving before group x
# x  0 || y:0 epv -> Moving before record y on group x
#-1 -1 || x:0 epv -> Moving ontop of group x
#-1 -1 || x:0 epvgroup y -> Moving ontop of record x on epvgroup y

#TODO - Missing one case the one where it drops into the open space
    
def _dropData(self,target,data):
    row, col, parent = target
    typing = type(data)
    #print("%d %d || %d %d %s"%(row,col,parent.row(),parent.column(),parent.internalPointer()))
    if (row,col) == (-1,-1):
        if not parent.isValid():
            if typing is EPVRecord:
                return False
            elif typing is EPVGroup:
                self.insertGroup(data,len(self))
                return True
        if typing is EPVRecord and type(self.access(parent)) is EPVGroup:
            self.insertRecord(self.access(parent),data)
            return True
        prompt = self.dropIntoQuery(typing)
        result = prompt.exec()
        if result == QMessageBox.Cancel:
            return False
        elif result == QMessageBox.Yes:
            self.moveinto(parent,data)
            return True
    elif not parent.isValid():
        self.insertGroup(data,row)
        return True
    else:
        parent = self.access(parent)
        if type(parent) is EPVGroup:
            self.insertRecord(parent,data,row)
            return True
    return False

def dropMimeData(self, mimeData, dropAction, row, col, parent):
    print("%d - %d | %d %d %s"%(row,col,parent.row(),parent.column(),parent.internalPointer()))
    if dropAction == Qt.IgnoreAction:
        return True
    if dropAction == Qt.MoveAction:
        if EPVMETADATA in mimeData.formats():
            if mimeData.source == self:
                #self.movePending = True
                self.startRecording()
                result = self._dropData((row, col, parent),mimeData.internalPointer)
                if not result: 
                    self.discardRecording()
                    #self.movePending = False
                return result
    if dropAction == Qt.CopyAction:
        if EPVMETADATA  in mimeData.formats():
            if EPVGROUP in mimeData.formats():
                data = EPVGroup.fromExtendedBinary(mimeData.data(EPVGROUP))
                if parent.isValid():
                    row = parent.row()
                    parent = QModelIndex()
            elif EPVRECORD in mimeData.formats():
                data = EPVRecord.fromExtendedBinary(mimeData.data(EPVRECORD))
            self.startRecording()
            result = self._dropData((row, col, parent),data)
            if not result: 
                self.discardRecording()
                return False
            self.endRecording()
                
    #If row and col -1 ask user if they want to replace the data there or just throw it above or below
    return False 
#bool QAbstractItemModel::dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent)