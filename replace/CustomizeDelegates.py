# -*- coding: utf-8 -*-
"""
Created on Sat May  2 14:25:19 2020

@author: AsteriskAmpersand
"""
from generic.RichTextDelegate import RichTextDisplay
from replace.CustomizeModel import FindRole,ReplaceRole,
from PyQt5.QtWidgets import QPlainTextEdit,QColorDialog
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyledItemDelegate

BasicTextEntry TextEntry ColorEntry RGBAColorEntry
 
class BasicReplaceText(ReplaceTextDelegate):
    BlockCountLimit = 1

class ReplaceTextDelegate(RichTextDisplay):
    BlockCountLimit = 4
    def initStyleOption(self,options,index):
        QtWidgets.QStyledItemDelegate.initStyleOption(self,options,index)
        options.text = index.data(ReplaceRole)
        
    def createEditor(self, parent, option, index):
        box = QPlainTextEdit(parent)
        box.maximumBlockCount = self.BlockCountLimit     
        return box

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        editor.setValue(value)

    def setModelData(self, editor, model, index):
        value = editor.value()
        model.setData(index, value, Qt.EditRole)

class FindTextDelegate(RichTextDisplay):
    def initStyleOption(self,options,index):
        RichTextDisplay.initStyleOption(self,options,index)
        options.text = index.data(FindRole)

class ColorReplaceDelegate(ColorFindDelegate):
    role = ReplaceRole
    def createEditor(self, parent, option, index):
        box = QColorDialog(parent)
        box.alpha = None      
        return box

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        if len(value) == 4:
            r,g,b,a = value
            editor.alpha = a
        else:
            r,g,b = value
            editor.alpha = None
        editor.setCurrentColor(QColor("%02X%02X%02X"%(r,g,b)))

    def setModelData(self, editor, model, index):
        value = editor.currentColor()
        if value.isValid():
            r,g,b = value.red(),value.green(),value.blue()
            if editor.alpha is not None:
                model.setData(index, (r,g,b,editor.alpha), Qt.EditRole)
            else:
                model.setData(index, (r,g,b), Qt.EditRole)
        
class ColorFindDelegate(QStyledItemDelegate):
    role = FindRole
    def paint(self, painter, option, index):
        QtGui.QStyledItemDelegate.paint(self, painter, option, index)
        rect = option.rect
        btn = QtGui.QStyleOptionButton()
        btn.rect = QtCore.QRect(rect.left() + rect.width() - 30, rect.top(), 30, rect.height())
        datum = index.data(self.role)
        if len(datum) == 4:
            t,r,g,b,a = datum,None
        if len(datum) == 5:
            t,r,g,b,a = datum
        btn.text = t       
        btn.setStyleSheet("background-color:rgb(%d,%d,%d);border:none"%(rgb))
        btn.state = QtGui.QStyle.State_Enabled|(QtGui.QStyle.State_MouseOver if option.state & QtGui.QStyle.State_MouseOver else QtGui.QStyle.State_None)
        QtGui.QApplication.style().drawControl(QtGui.QStyle.CE_PushButton, btn, painter)