# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 03:27:40 2020

@author: AsteriskAmpersand
"""
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtWidgets import QMessageBox
from ._EPVGroup import EPVGroup
from ._EPVRecord import EPVRecord

EPVMETADATA = "application/x-mhw-epvmetadata"
EPVGROUP = "application/x-mhw-epvgroup"
EPVRECORD = "application/x-mhw-epvrecord"
BINARY = "application/octet-stream"
HEXTEXT = "text/plain"

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
    return any((typing in formats for typing in typings))
    #if EPVRECORD in 
    #print("%d:%d || %d:%d - %s"%(row,column,parent.row(),parent.column(),parent.internalPointer()))
    #if row == -1 and column == -1: Disables moving on top but makes the whole thing SUPER HARD TO MOVE
    #    return False
    
    # x  0 || -1:-1 None -> Moving before group x
    # x  0 || y:0 epv -> Moving before record y on group x
    #-1 -1 || x:0 epv -> Moving ontop of group x
    #-1 -1 || x:0 epvgroup y -> Moving ontop of record x on epvgroup y
    #
    return True

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

def removeRows(self,*kwargs):
    print("Oh Lawd")
    return False

def _deleteRecord(self,group,position):
    index = self.index(group.row(),0,group.parent())
    self.beginRemoveRows.emit(index,position,position)
    
    group[position:position+1] = []
    
    self.endRemoveRows.emit(index,position,position)

def _insertRecord(self,group,record,position):
    index = self.index(group.row(),0,group.parent())
    self.beginInsertRows(index,position,position)
    print(len(group))
    group[position:position] = [record]
    print(len(group))
    self.endInsertRow(index,position,position)
    return True

def insertRecord(self,group,record,position=None):
    if position is None:
        position = len(group)
    self.recordState(self._deleteRecord,[group,position],self._insertRecord,[group,record,position])
    self._insertRecord(group,record,position)
    pass

def replaceRecord(self,parent,record):
    pass

def moveinto(self,index,data):
    if data is EPVGroup:
        for children in data:
            self.insertRecord(index.internalPointer()[index.row()],children)#TODO - Think fully on how this works
    elif data is EPVRecord:
        self.replaceRecord(index,data)

def _internalMoveTo(self,target,data):
    row, col, parent = target
    typing = type(data)
    if (row,col) == (-1,-1):
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
    #TODO - Handle other cases
    return False

def dropMimeData(self, mimeData, dropAction, row, col, parent):
    if dropAction == Qt.IgnoreAction:
        return True
    if dropAction == Qt.MoveAction:
        if EPVMETADATA in mimeData.formats():
            if mimeData.source == self:
                self.movePending = True
                self.startRecording()
                result = self._internalMoveTo((row, col, parent),mimeData.internalPointer)
                if not result: 
                    self.discardRecording()
                    self.movePending = False
                return result
            
    #If row and col -1 ask user if they want to replace the data there or just throw it above or below
    return False 
#bool QAbstractItemModel::dropMimeData(const QMimeData *data, Qt::DropAction action, int row, int column, const QModelIndex &parent)