# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 06:34:47 2020

@author: AsteriskAmpersand
"""

from gui.EPVSlot import Ui_Form as EPVForm
from model.RecordProperties import RecordProperties
#from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QWidget, QColorDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QColor

class colorMediator(QWidget):
    valueChanged = pyqtSignal(object)    
    
class EPVCEntry(RecordProperties):
    ui_form = EPVForm
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.ui.color = colorMediator()
        self.ui.colorTool.pressed.connect(self.paletteChange)    
    @property
    def efxslot(self): return self.ui.efxslot.value()
    @efxslot.setter
    def efxslot(self,value): self.ui.efxslot.setValue(value)
    @property
    def color(self): 
        color = self.ui.colorTool.palette().button().color()
        return color.red(),color.green(),color.blue()
    @color.setter
    def color(self,value):
        self.ui.colorTool.setStyleSheet("border: none; background-color: #%02X%02X%02X"%value)
    @property
    def alpha(self): return self.ui.alpha.value()
    @alpha.setter
    def alpha(self,value):self.ui.alpha.setValue(value)
    @property
    def saturation(self): return self.ui.saturation.value()
    @saturation.setter
    def saturation(self,value):self.ui.saturation.setValue(value)
    @property
    def frequency(self): return self.ui.frequency.value()
    @frequency.setter
    def frequency(self,value):self.ui.frequency.setValue(value)
    @property
    def size(self): return self.ui.size.value()
    @size.setter
    def size(self,value): return self.ui.size.setValue(value)
    properties = ["efxslot","color","alpha","saturation","frequency","size"]
    
    def paletteChange(self):
        color = QColorDialog.getColor(QColor("#%X%X%X"%self.color))
        if color.isValid():
            self.color = color.red(),color.green(),color.blue()
            self.ui.color.valueChanged.emit("color")