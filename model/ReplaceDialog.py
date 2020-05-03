# -*- coding: utf-8 -*-
"""
Created on Fri May  1 05:43:38 2020

@author: AsteriskAmpersand
"""

import sys
import os

from gui.EPVReplace import Ui_Dialog
from model.CustomizeReplacement import CustomizeReplacement
#from PyQt5 import uic, QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import Qt,QUrl
#from PyQt5.QtCore import QFile, QTextStream

class ReplaceDialog(QDialog):
    def __init__(self, reference, *args):
        super().__init__(*args)
        self.reference = reference
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.connectSignals()        
        self.show()
        
    def connectSignals(self):
        self.ui.Cancel.connect(self.reject())
        self.ui.Customize.connect()
        self.ui.Replace.connect(self.replace)
        
    def replace(self):
        self._replace()
        self.accept()
        
    def _replace(self):
        if self.ui.ApplyToAll.checkState():
            op = self.references.getFiles
        else:
            op = self.references.getCurrentFile
        self.results = {file:self.ui.ReplaceForm.evaluate(file) 
                for file in op()}
        return self.results
    
    def customize(self):
        results = self._replace()
        customize = CustomizeReplacement (results)
        result = customize.exec()
        if result == QDialog.Accepted():
           self.results = customize.results
           self.accept()
        
    
if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = ReplaceDialog(None)
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())