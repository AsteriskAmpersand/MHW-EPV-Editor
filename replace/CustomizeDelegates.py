# -*- coding: utf-8 -*-
"""
Created on Sat May  2 14:25:19 2020

@author: AsteriskAmpersand
"""
from generic.RichTextDelegate import RichTextDisplay
from replace.CustomizeModel import FindRole,ReplaceRole,BasicTextEntry,TextEntry,ColorEntry,RGBAColorEntry
from PyQt5.QtWidgets import QPlainTextEdit,QColorDialog
from PyQt5.QtCore import Qt,QRect,QRectF,QSize
from PyQt5.QtGui import QColor,QPalette,QBrush,QFontMetrics,QPainterPath,QPainter
from PyQt5.QtWidgets import QStyledItemDelegate,QStyleOptionButton,QStyle,QApplication,QMessageBox

debug = lambda x: QMessageBox.critical(None,
                       "An exception was raised",
                       "Test %s"%(str(x)))

class CustomizeFindDelegate(QStyledItemDelegate):
    def getType(self,index):
        return index.model().entryType(index)
    #if t in [BasicTextEntry,TextEntry,ColorEntry,RGBAColorEntry]:
    def sizeHint(self, option, index):
        #debug(3)
        t = self.getType(index)
        if t in [BasicTextEntry,TextEntry]:
            return self.FTD_sizeHint(option,index)
        elif t in [ColorEntry,RGBAColorEntry]:
            return self.CFD_sizeHint(option,index)
        elif t is str:
            return self.text_sizeHint(option,index)
        else:
            return super().sizeHint(option,index)
    def paint(self, painter, option, index):
        #debug(4)
        t = self.getType(index)
        if t in [BasicTextEntry,TextEntry]:
            return RichTextDisplay.paint(self,painter,option,index)
        elif t in [ColorEntry,RGBAColorEntry]:
            return self.CFD_paint(painter,option,index,FindRole)
        elif t is str:   
            return self.text_paint(painter,option,index)
        else:
            return super().paint(painter,option,index)
    def initStyleOption(self,options,index):
        t = self.getType(index)
        #debug(2)
        if t in [BasicTextEntry,TextEntry]:
            return self.FTD_initStyleOption(options,index)
        elif t is str:
            return self.text_initStyleOption(options,index)
        else:
            return super().initStyleOption(options,index)        

#class TitleTextDelegate():
    def text_initStyleOption(self,option,index):
        super().initStyleOption(option,index)
        #option.font.setBold(True)
        #option.font.setPointSize(int(option.font.pointSize()*1.2))
        return 
        
    def text_paint(self,painter,option,index):
        #fontSize = int(option.font.pointSize())
        #print(fontSize)
        painter.save()
        self.initStyleOption(option, index)
        #text = index.data()
        obold = option.font.bold()
        opoint = option.font.pointSize()
        
        option.font.setBold(True)
        option.font.setPointSize(round(opoint*1.2))
        brush = QBrush(option.palette.window())
        brush.setColor(brush.color().darker(115))
        painter.fillRect(option.rect,brush)
        #option.palette.setColor(QPalette.Active,QPalette.Window,col)
        QStyledItemDelegate.paint(self,painter,option,index)
        
        option.font.setBold(obold)
        option.font.setPointSize(opoint)
        painter.restore()
        
    def text_sizeHint(self,option,index):
        #return super().sizeHint(option,index)
        text = index.data()
        self.initStyleOption(option,index)
        fm = QFontMetrics(option.font)
        w = fm.width(text)
        h = fm.height()*2
        return QSize(w, h)
        
#class FindTextDelegate(RichTextDisplay):
    #sizeHint, paint,initStyleOption
    def FTD_initStyleOption(self,options,index):
        QStyledItemDelegate.initStyleOption(self,options,index)
        options.text = index.data(FindRole).replace("\n","<br>")
        
    def FTD_sizeHint(self, option, index):
        count = index.model().data(index,FindRole).count("\n")+1
        text = index.model().data(index,FindRole)
        fm = QFontMetrics(option.font)
        w = fm.width(text)
        h = fm.height()*count
        return QSize(w, h)

#class ColorFindDelegate(QStyledItemDelegate):
    #role = FindRole
    def CFD_sizeHint(self,option,index):
        text,color = index.data(FindRole)
        fm = QFontMetrics(option.font)
        h = fm.height()*1.5
        w = fm.width(text) + h
        return QSize(w, h)
        
    def CFD_paint(self, painter, option, index,role):
        path,color =  index.data(role)
        painter.save()
        
        item = option.rect
        myOption = option
        #Highlighting
        if ((myOption.state & QStyle.State_Selected)):
            painter.fillRect(option.rect, option.palette.highlight());
        elif((myOption.state & QStyle.State_MouseOver)):
            painter.fillRect(option.rect, option.palette.midlight())
        
        #Text Rendering
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)     
        painter.drawText(item.left()+5, (item.top()+item.bottom()*2)/3, path)
        
        #Place Colour Sample
        fm = QFontMetrics(option.font)
        h = fm.height()*1.5
        w = max(180,fm.width(path) + h)
        #print(w)
        #print(h)
        
        x0 = item.left()+w+5
        y0 = item.top()+fm.height()*.15
        x1 = item.right()-5
        y1 = item.bottom()-fm.height()*.15
        
        #debug(str(color))
        brush = QBrush(QColor(*color))
        #debug(0)
        if not(x0>x1 or y0>y1):
            rect = QRectF(x0,y0,x1-x0,y1-y0)
            #debug(1)
            painter.setBrush(brush)
            #debug(2)
            painter.drawRect(rect);
            #debug(3)
        
        painter.restore()
        #super().paint(painter,option,index)
        return
        """
        super().paint(painter,option,index)
        QStyledItemDelegate.paint(self, painter, option, index)
        rect = option.rect
        btn = QStyleOptionButton()
        btn.rect = QRect(rect.left() + rect.width() - 30, rect.top(), 30, rect.height())
        datum = index.data(role)
        if len(datum) == 4:
            t,r,g,b,a = (*datum,None)
        if len(datum) == 5:
            t,r,g,b,a = datum
        btn.text = t       
        #btn.setStyleSheet("background-color:rgb(%d,%d,%d);border:none"%(r,g,b))
        btn.state = QStyle.State_Enabled|(QStyle.State_MouseOver if option.state & QStyle.State_MouseOver else QStyle.State_None)
        btn.palette.setBrush(QPalette.Button,QBrush(QColor("%02X%02X%02X"%(r,g,b))))
        QApplication.style().drawControl(QStyle.CE_PushButton, btn, painter)
        """
# =============================================================================
# Replace Delegate
# =============================================================================
class CustomizeReplaceDelegate(CustomizeFindDelegate):
    def initStyleOption(self,options,index):
        t = self.getType(index)
        if t in [BasicTextEntry,TextEntry]:
            return self.RTD_initStyleOption(options,index)
        else:
            return super().initStyleOption(options,index)   

    def paint(self, painter, option, index):
        #debug(4)
        t = self.getType(index)
        if t in [ColorEntry,RGBAColorEntry]:
            return self.CFD_paint(painter,option,index,ReplaceRole)
        else:
            return super().paint(painter,option,index)

    def createEditor(self, parent, option, index):
        t = self.getType(index)
        if t in [BasicTextEntry,TextEntry]:
            if t is BasicTextEntry:
                bcl = 1
            elif t is TextEntry:
                bcl = 4
            return self.RTD_createEditor( parent, option, index,bcl)
        elif t in [ColorEntry,RGBAColorEntry]:
            return self.CRD_createEditor( parent, option, index)
        else:   
            return None#super().createEditor( parent, option, index)
        
    def setEditorData(self, editor, index):
        t = self.getType(index)
        if t in [BasicTextEntry,TextEntry]:
            return self.RTD_setEditorData( editor, index)
        elif t in [ColorEntry,RGBAColorEntry]:
            return self.CRD_setEditorData( editor, index)
        else:
            return super().setEditorData(self, editor, index)
        
    def setModelData(self, editor, model, index):
        t = self.getType(index)
        if t in [BasicTextEntry,TextEntry]:
            return self.RTD_setModelData( editor, model, index)
        elif t in [ColorEntry,RGBAColorEntry]:
            return self.CRD_setModelData( editor, model,  index)
        else:
            return super().setModelData( editor, model,  index)
#class BasicReplaceText(ReplaceTextDelegate):
    #BlockCountLimit = 2
    
#class ReplaceTextDelegate(RichTextDisplay):
    #sizeHint, paint, initStyleOption
    #BlockCountLimit = 5
    def RTD_initStyleOption(self,options,index):
        QStyledItemDelegate.initStyleOption(self,options,index)
        options.text = index.data(ReplaceRole).replace("\n","<br>")
        
    def RTD_createEditor(self, parent, option, index, BlockCountLimit):
        box = QPlainTextEdit(parent)
        box.maximumBlockCount = BlockCountLimit     
        return box

    def RTD_setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        editor.setPlainText (value)

    def RTD_setModelData(self, editor, model, index):
        value = editor.toPlainText()
        model.setData(index, value, Qt.EditRole)

#class ColorReplaceDelegate(ColorFindDelegate):
    #paint CFD_paint
    role = ReplaceRole
    def CRD_createEditor(self, parent, option, index):
        value = index.data(Qt.EditRole)
        #debug("%d %d %s"%(index.row(),index.column(),index.parent()))
        if len(value) == 4:
            r,g,b,a = value
            #debug(a)
            colorPicker = QColorDialog(QColor(r,g,b,a),parent)
            colorPicker.setOption(QColorDialog.ShowAlphaChannel,True)
        else:
            r,g,b = value     
            a = None
            colorPicker = QColorDialog(QColor(r,g,b),parent)
        return colorPicker

    def CRD_setEditorData(self, editor, index):
        pass

    def CRD_setModelData(self, editor, model, index):
        color = editor.currentColor()
        if color.isValid():
            r,g,b = color.red(),color.green(),color.blue()
            if editor.testOption(QColorDialog.ShowAlphaChannel):
                index.model().setData(index,(r,g,b,color.alpha()), Qt.EditRole)
            else:
                index.model().setData(index,(r,g,b), Qt.EditRole)
