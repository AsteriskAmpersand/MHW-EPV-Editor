# -*- coding: utf-8 -*-
"""
Created on Mon May  4 16:09:20 2020

@author: AsteriskAmpersand
"""

from PyQt5.QtWidgets import QLabel,QWidget
from replace.ReplaceSelector import ReplaceForm
from gui.FindSubForm import Ui_Form

class FindForm(ReplaceForm):
    def __init__(self, *args):
        QWidget.__init__(self,*args)
        self.color1 = "#FFFFFFFFFF"
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.ui.Replace = QLabel(self.ui.Text)
        self.ui.Replace.setObjectName("Replace")
        self.ui.Replace.setText("")
        self.ui.verticalLayout_8.addWidget(self.ui.Replace)
        
        #self.ui.AlphaFind.setEnabled(False)
        #self.ui.AlphaReplace.setEnabled(False)
        
        self.connectSignals()
        
        self.show()
    
    def connectSignals(self):
        self.ui.ColorFind.pressed.connect(lambda: self.paletteChange(self.ui.ColorFind,"color1"))

    def colorReplace(self,find,replace,color):
        if self.colorDistance(color,find)<=self.ui.ColorTolerance.value():
            return (-1,-1,-1)
        return color