# -*- coding: utf-8 -*-
"""
Created on Fri May  1 21:49:34 2020

@author: AsteriskAmpersand
"""


import sys

from gui.CustomizeReplacement import Ui_Dialog
from replace.CustomizeModel import CustomizableResultsModel
from replace.CustomizeDelegates import CustomizeFindDelegate,CustomizeReplaceDelegate

#from PyQt5 import uic, QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QAbstractItemView,QMessageBox

def catch_exceptions(t, val, tb):
    QMessageBox.critical(None,
                       "An exception was raised",
                       "Exception type: {}".format(tb))
    old_hook(t, val, tb)


old_hook = sys.excepthook
sys.excepthook = catch_exceptions

test = lambda x:         QMessageBox.critical(None,
                           "Test",
                           "Test%d"%x)

class CustomizeReplacement(QDialog):
    def __init__(self, baseReplacements, *args):
        super().__init__(*args)
        self.model = CustomizableResultsModel(baseReplacements)
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.Before.setModel(self.model)
        self.ui.After.setModel(self.model)
        self.connectSignals()
        self.setDelegates()
        self.show()
        
    def connectSignals(self):
        self.ui.Cancel.pressed.connect(self.reject)
        self.ui.Accept.pressed.connect(self.replace)
        self.ui.Reset.pressed.connect(self.reset)
        self.ui.Remove.pressed.connect(self.remove)
        
        self.ui.Before.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ui.After.setSelectionModel(self.ui.Before.selectionModel())

        beforeBar = self.ui.Before.verticalScrollBar()
        afterBar = self.ui.After.verticalScrollBar()
        beforeBar.valueChanged.connect(afterBar.setValue)
        afterBar.valueChanged.connect(beforeBar.setValue)

        self.ui.Before.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.ui.Before.setWordWrap(False)
        self.ui.After.setWordWrap(False)

        self.ui.actionUndo.triggered.connect(self.undo)
        self.ui.actionRedo.triggered.connect(self.redo)
        self.ui.actionDelete.triggered.connect(self.remove)
        
    def setDelegates(self):
        self.ui.Before.setItemDelegate(CustomizeFindDelegate())
        self.ui.After.setItemDelegate(CustomizeReplaceDelegate())
    
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