# -*- coding: utf-8 -*-
"""
Created on Fri May  1 03:32:47 2020

@author: AsteriskAmpersand
"""


import sys
import re
from math import sqrt

from replace.ReplaceEnums import TEXT,COLOR
from gui.ReplaceForm import Ui_Form

from PyQt5.QtWidgets import QWidget, QColorDialog, QApplication
from PyQt5.QtGui import QColor

class ReplaceForm(QWidget):
    def __init__(self, *args):
        super().__init__(*args)
        self.color1 = "#FFFFFFFF"
        self.color2 = "#FFFFFFFF"
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        #self.ui.AlphaFind.setEnabled(False)
        #self.ui.AlphaReplace.setEnabled(False)
        
        self.connectSignals()
        
        self.show()
    
    def connectSignals(self):
        self.ui.ColorFind.pressed.connect(lambda: self.paletteChange(self.ui.ColorFind,"color1"))
        self.ui.ColorFind_2.pressed.connect(lambda: self.paletteChange(self.ui.ColorFind_2,"color2"))
        #self.ui.AlphaEnable.stateChanged.connect(self.alphaToggled)
        #ColorFind2
    #ColorFind ColorFind2
    
    #def alphaToggled(self):
    #    self.ui.AlphaFind.setEnabled(self.ui.AlphaEnable.checkState())
    #    self.ui.AlphaReplace.setEnabled(self.ui.AlphaEnable.checkState())
    
    def paletteChange(self,finder,prop):
        alpha = self.ui.AlphaEnable.checkState()
        if alpha:
            color = QColorDialog.getColor(QColor(getattr(self,prop)),options = QColorDialog.ShowAlphaChannel)
        else:
            color = QColorDialog.getColor(QColor(getattr(self,prop)))
        if color.isValid():
            stylesheetColor = color.name(QColor.HexRgb if not alpha else QColor.HexArgb)
            finder.setStyleSheet("border: none; background-color: %s"%stylesheetColor)
            setattr(self,prop,stylesheetColor)
            
    def colorDistance(self,c1,c2):
        if len(c1)>3:
            if c1[3]!=c2[3]: return 767
        rmean = ( c1[0] + c2[0] ) // 2;
        r = c1[0] - c2[0]
        g = c1[1] - c2[1]
        b = c1[2] - c2[2]
        return sqrt((((512+rmean)*r*r)>>8) + 4*g*g + (((767-rmean)*b*b)>>8))
    
    def replace(self):
        find = self.ui.Find.text()
        replace = self.ui.Replace.text()
        def externalReplace(string):
            return string.replace(find,replace)
        return externalReplace

    def regexReplace(self):
        find = self.ui.Find.text()
        replace = self.ui.Replace.text()
        matcher = re.compile(find)
        def externalReplace(string):
            return matcher.sub(replace,string)
        return externalReplace
    
    def evaluateText(self,reference):
        results = []
        op = self.regexReplace() if self.ui.Regex.checkState() else self.replace()
        for ref,string in reference.getStringReferences(self.ui.Group.checkState()):
            stringbefore = string
            stringafter = op(string)
            if stringbefore != stringafter:
                results.append((ref,stringafter))
        return results
    
    def colorReplace(self,find,replace,color):
        if self.colorDistance(color,find)<=self.ui.ColorTolerance.value():
            return replace
        return color
    
    def evaluateColor(self,reference):
        results = []
        if self.ui.AlphaEnable.checkState():
            prism = lambda x: (x.red(),x.green(),x.blue(),x.alpha())
        else:
            prism = lambda x: (x.red(),x.green(),x.blue())
        colorFind = prism(QColor(self.color1))
        colorReplace = prism(QColor(self.color2))
        for ref,color in reference.getColorReferences(self.ui.AlphaEnable.checkState()):
            colorbefore = color
            colorafter = self.colorReplace(colorFind,colorReplace,color)
            #print(colorbefore)
            #print(colorafter)
            if list(colorbefore) != list(colorafter):
                results.append((ref,colorafter))
        return results            
        
    def evaluate(self,reference):
        if not reference:
            return []
        #currentMode = self.ui.tabWidget.currentWidget()
        mode = {"Text":TEXT,"Color":COLOR}[self.ui.tabWidget.tabText(self.ui.tabWidget.currentIndex())]
        if mode == TEXT: return self.evaluateText(reference)
        elif mode == COLOR: return self.evaluateColor(reference)

if "__main__" in __name__:    
    app = QApplication(sys.argv)
    window = ReplaceForm(None)
    sys.exit(app.exec_())