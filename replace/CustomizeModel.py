# -*- coding: utf-8 -*-
"""
Created on Sat May  2 14:08:05 2020

@author: AsteriskAmpersand
"""

from generic.QList import QList
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QColor
from replace.ReplaceEnums import BasicText,FullText,Color,RGBAColor
FindRole = 0+Qt.UserRole
ReplaceRole = 1+Qt.UserRole

#EditRole supplies the replaced values
#FindRole supplies the text for the find (including header)
#ReplaceRole 
#BasicTextEntry TextEntry ColorEntry RGBAColorEntry

import sys 
def catch_exceptions(t, val, tb):
    QMessageBox.critical(None,
                                   "An exception was raised",
                                   "Exception type: {}".format(tb))
    old_hook(t, val, tb)


old_hook = sys.excepthook
sys.excepthook = catch_exceptions

class ReplaceResultEntry():
    def __init__(self,file,dataIndex,replacementTarget):
        self.fileRef = file
        self.indexRef = dataIndex
        self.dataPath = dataIndex.dataPath()
        self.findValue =  dataIndex.findValue()
        self.replacedValue = replacementTarget
    def getRole(self,role):
        if role == FindRole:
            return self.displayFind(self.dataPath,self.findValue)
        if role == ReplaceRole:
            return self.displayReplace(self.replacedValue)
        if role == Qt.EditRole:
            return  self.replacedValue
    def setRole(self,value,role):
        self.replacedValue = self.validate(value)
        return True

class BasicTextEntry(ReplaceResultEntry):
    def validate(self,text):
        return text
    def displayFind(self,dataPath,findText):
        return "\t"+str(dataPath)+"\n"+findText
    def displayReplace(self,replaceText):
        return "\n"+replaceText    
        
class TextEntry(BasicTextEntry):
    def validate(self,text):
        results = text.split("\n")
        if len(results) > 4:
            results[:4]
        results = results + [""]*(4-len(results))
        return "\n".join(results)
    def displayReplace(self,replaceText):
        return "\n"+self.validate(replaceText)
    
class ColorEntry(ReplaceResultEntry):
    def validate(self,values):
        return values
    def displayFind(self,dataPath,findColor):
        return (dataPath,findColor)
    def displayReplace(self,replaceColor):
        return ("",replaceColor)
    def getRole(self,role):
        if role == Qt.BackgroundColorRole:
            color = QColor("FFFFFF")
            color.setAlpha(0)
            return color
        return super().getRole(role)
    
class RGBAColorEntry(ColorEntry):
    pass

class CustomizableResultsModel(QList):
    def __init__(self,data,*args,**kwargs):
        entries = []
        for file,datamass in data.items():
            entries.append(str(file.path))
            for index,replaceval in datamass:
                typing = index.getType()
                entryType = {BasicText:BasicTextEntry,FullText:TextEntry,
                Color:ColorEntry, RGBAColor:RGBAColorEntry}[typing]
                entries.append(entryType(file,index,replaceval))
        super().__init__(entries,*args,**kwargs)
    def compile(self):
        results = {}
        for entry in self:
            if type(entry) is not str:
                if entry.fileRef not in results:
                    results[entry.fileRef] = []
                results[entry.fileRef].append((entry.indexRef,entry.replacedValue))
        return results
    def removeMultindex(self,multindex):
        for index in multindex:
            if index.isValid():
                self.removeRow(index.row(),QModelIndex())
    def entryType(self,index):
        return type(self.__access__(index))
    def flags(self,index):
        obj = self.__access__(index)
        if type(obj) is str:
            return Qt.NoItemFlags
        else:
            return Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled
    def __access__(self,index):
        if not index.isValid():
            return self
        return self.list[index.row()]