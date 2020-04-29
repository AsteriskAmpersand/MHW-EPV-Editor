# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 16:13:03 2020

@author: AsteriskAmpersand
"""

import sys
import os
from pathlib import Path

from gui.Main import Ui_MainWindow
from model.EPVTab import EPVTab

from PyQt5 import uic, QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QFile, QTextStream
_translate = QtCore.QCoreApplication.translate

def functionChain(functionList):
    for function in functionList:
        function()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, arguments):
        super().__init__()
        self.setAcceptDrops(True)        
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        elif __file__:
            application_path = os.path.dirname(__file__)
        self.setWindowIcon(QtGui.QIcon(application_path+r"\resources\DodoSama.png"))
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.fileTabs.setTabsClosable(True)
        
        #tab = EPVTab(self,r"E:\MHW\chunkG0\pl\f_equip\pl124_0000\body\epv\f_body124.epv3")
        #self.ui.fileTabs.addTab(tab,"Test") 
        
        self.setWindowTitle("Asterisk EPV Editor")
        self.connectMenus()
        self.connectSignals()
        self.show()
        
    def connectMenus(self):
        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionNew.triggered.connect(self.new)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionSave_As.triggered.connect(self.saveAs)
        self.ui.actionSave_All.triggered.connect(self.saveAll)
        self.ui.actionUndo.triggered.connect(self.undo)
        self.ui.actionRedo.triggered.connect(self.redo)
    
    def connectSignals(self):
        self.ui.fileTabs.tabCloseRequested.connect(self.closeTab)
        #connect changes in tab name
    
    def open(self):
        filename = QFileDialog.getOpenFileName(self,_translate("MainWindow","Open EPV3"),"",_translate("MainWindow","MHW EPV3 (*.epv3)"))
        if filename[0]:
            filename = Path(filename[0])
            if filename.exists():
                tab = EPVTab(self,filename)
                self.ui.fileTabs.addTab(tab,filename.stem)
                self.ui.fileTabs.setCurrentWidget(tab)
                tab.tabNameChanged.connect(self.renameTab)
            else:
                QtWidgets.QMessageBox.critical(None,
                       "File not found",
                       "File {} not found.".format(str(filename)))      
    def new(self):
        tab = EPVTab(self)
        self.ui.fileTabs.addTab(tab,"New EPV3")
        self.ui.fileTabs.setCurrentWidget(tab)
        tab.tabNameChanged.connect(self.renameTab)
    def save(self):
        ix = self.ui.fileTabs.currentIndex()
        tab = self.ui.fileTabs.widget(ix)
        tab.Save()
    def saveAs(self):
        ix = self.ui.fileTabs.currentIndex()
        tab = self.ui.fileTabs.widget(ix)
        tab.SaveAs()
    def saveAll(self):
        for tab in [self.ui.fileTabs.widget(i) for i in range(self.ui.fileTabs.count)]:
            tab.Save()
    def undo(self):
        widget = self.ui.fileTabs.currentWidget()
        widget.undo()
    def redo(self):
        widget = self.ui.fileTabs.currentWidget()
        widget.redo()
    def closeTab(self,ix):
        tab = self.ui.fileTabs.widget(ix)
        if tab.RequestSave():
            tab.tabNameChanged.disconnect(self.renameTab)
            self.ui.fileTabs.removeTab(ix)
    def renameTab(self,tab,name):
        ix = self.ui.fileTabs.indexOf(tab)
        self.ui.fileTabs.setTabText(ix,name)
    def closeEvent(self, event):
        for ix in range(self.ui.fileTabs.count):
            tab = self.ui.fileTabs.widget(ix) 
            if not tab.RequestSave():
                event.ignore()
            tab.tabNameChanged.disconnect(self.renameTab)
            self.ui.fileTabs.removeTab(ix)
        event.accept()
        
if __name__ == '__main__':
    #from pathlib import Path
    app = QtWidgets.QApplication(sys.argv)
    args = app.arguments()[1:]
    window = MainWindow(args)
    sys.exit(app.exec_())