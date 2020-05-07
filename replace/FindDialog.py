# -*- coding: utf-8 -*-
"""
Created on Mon May  4 14:55:55 2020

@author: AsteriskAmpersand
"""


import sys
import os

from gui.FindForm import Ui_Dialog
from replace.CustomizeDelegates import CustomizeFindDelegate
from replace.CustomizeModel import CustomizableResultsModel
#from PyQt5 import uic, QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QAbstractItemView
from PyQt5.QtCore import Qt,QUrl
from collections import OrderedDict
#from PyQt5.QtCore import QFile, QTextStream

class FindDialog(QDialog):
    def __init__(self, reference, startIndex, *args):
        super().__init__(*args)
        self.reference = reference
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.Matches.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.results = None
        self.setIndex(startIndex)
        self.model = None
        
        self.connectSignals()        
        self.show()
        
    def setIndex(self,index):
        if not index.isValid():
            self.group = -1
            self.record = -1
        else:
            if not index.parent().isValid():
                self.group = index.row()
                self.record = -1
            else:
                self.group = index.parent().row()
                self.record = index.row()
        
    def connectSignals(self):
        self.ui.FindNext.pressed.connect(self.findNext)
        self.ui.FindAll.pressed.connect(self.findAll)
        self.ui.Cancel.pressed.connect(self.reject)
        self.ui.Matches.doubleClicked.connect(self.goTo)
    
    def goTo(self,viewIndex):
        if not viewIndex.isValid():
            return
        if self.model is None:
            return
        if self.model[viewIndex.row()] is str:
            return
        else:
            metaIndex = self.model[viewIndex.row()].metaIndex()
            file = self.model[viewIndex.row()].fileRef
            self.results = file,metaIndex
            self.accept()
    
    def findAll(self):
        results = self.find()
        if not results:
            QMessageBox.critical(None,
                       "No Match Found",
                       "No matches for the query were found. Try again with different values")  
            return
        self.model = CustomizableResultsModel(results)
        self.ui.Matches.setModel(self.model)
        self.ui.Matches.setItemDelegate(CustomizeFindDelegate())
    
    def findSuccesor(self,results):
        current = self.reference.getCurrentFile()
        fakeNext = None
        startTrue = False
        for file,matches in results.items():
            if file is current and not matches:
                startTrue = True
            for imatch,_ in matches:
                group,record = imatch.IDPair()
                if file is current and group >= self.group and record > self.record:
                    startTrue = True
                if startTrue:
                    self.results = file,imatch
                    self.accept()
                    return
                else:
                    if fakeNext is None:
                        fakeNext = file,imatch
        self.results = fakeNext
        self.accept()  
        return 
            
    
    def findNext(self):
        results = self.find()
        if not results:
            QMessageBox.critical(None,
                       "No Match Found",
                       "No matches for the query were found. Try again with different values")      
            return
        return self.findSuccesor(results)
        
    def find(self):
        if self.ui.ApplyToAll.checkState():
            op = self.reference.getFiles
        else:
            op = lambda: [self.reference.getCurrentFile()]
        results = OrderedDict([(file,self.ui.FindForm.evaluate(file) )
                for file in op()])
        return results
            
if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = FindDialog(None)
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())