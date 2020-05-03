# -*- coding: utf-8 -*-
"""
Created on Fri May  1 21:49:34 2020

@author: AsteriskAmpersand
"""


import sys

from gui.EPVCustomizeReplacement import Ui_Dialog
from replace.CustomizeModel import CustomizableResultsModel

#from PyQt5 import uic, QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QAbstractItemView
        
class CustomizeReplacement(QDialog):
    def __init__(self, baseReplacements, *args):
        super().__init__(*args)
        self.model = CustomizableResultsModel(baseReplacements)
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.connectSignals()        
        self.show()
        
    def connectSignals(self):
        self.ui.Cancel.connect(self.reject())
        self.ui.Accept.connect(self.replace)
        self.ui.Reset.connect(self.reset)
        self.ui.Remove.connect(self.remove)
        
        self.ui.After.setSelectionModel(self.ui.Before.selectionModel())
        self.ui.After.setSelectionMode(QAbstractItemView.ExtendedSelection)
        beforeBar = self.ui.Before.verticalScrollBar()
        afterBar = self.ui.After.verticalScrollBar()
        beforeBar.valueChanged.connect(afterBar.setValue)
        afterBar.valueChanged.connect(beforeBar.setValue)
        
        self.setDelegates()
        
        self.ui.actionUndo.connect(self.undo)
        self.ui.actionRedo.connect(self.redo)
        self.ui.actionDelete.connect(self.remove)
    
    def setDelegates(self):
        pass
    
    def undo(self):
        self.model.undo()
        
    def redo(self):
        self.model.redo()
    
    def replace(self):
        self._replace()
        self.accept()
        
    def _replace(self):
        self.results = self.model.compile()
    
    def reset(self):
        self.model.reset()
        
    def remove(self):
        self.model.removeMultindex(self.selection())
        
    def selection(self):
        return self.ui.Before.selectedIndexes()
    
if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = CustomizeReplacement(None)
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())