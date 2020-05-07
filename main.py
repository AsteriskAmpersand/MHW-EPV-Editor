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
from model.AboutScripting import AboutScripting
from model.AboutHelp import AboutHelp
from generic.Queue import CopyStack
from scripting.scriptEngine import mse as MSE
from replace.ReplaceDialog import ReplaceDialog
from replace.FindDialog import FindDialog
from splash.Splash import SplashScreen

from PyQt5 import uic, QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QFileDialog, QMessageBox
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
        self.copyStack = CopyStack()
        self.propertyClipboard = None
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.fileTabs.setTabsClosable(True)
        
        self.setWindowTitle("Asterisk's Nebula Asterism")
        self.connectMenus()
        self.connectSignals()
        #self.disableMenus()
        self.show()
        
    def connectMenus(self):
        #File Menu
        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionNew.triggered.connect(self.new)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.actionSave_As.triggered.connect(self.saveAs)
        self.ui.actionSave_All.triggered.connect(self.saveAll)
        #Edit Menu
        self.ui.actionUndo.triggered.connect(self.undo)
        self.ui.actionRedo.triggered.connect(self.redo)
        
        self.ui.actionDelete.triggered.connect(self.delete)        
        self.ui.actionDuplicate.triggered.connect(self.duplicate)
        self.ui.actionCopy.triggered.connect(self.copy)
        self.ui.actionPaste.triggered.connect(self.paste)
        self.ui.actionCopy_Properties.triggered.connect(self.copyProperties)
        self.ui.actionPaste_Properties.triggered.connect(self.pasteProperties)
        
        self.ui.actionPush_To_Copy_Stack.triggered.connect(self.pushStack)
        self.ui.actionPaste_Copy_Stack.triggered.connect(self.pasteStack)
        self.ui.actionClear_Copy_Stack.triggered.connect(self.clearStack)
        
        self.ui.actionNew_Group.triggered.connect(self.newGroup)
        self.ui.actionNew_Record.triggered.connect(self.newRecord)
        
        #Find Menu
        self.ui.actionFind.triggered.connect(self.Find)
        self.ui.actionReplace.triggered.connect(self.Replace)
        
        #Script Menu
        self.ui.actionOpen_Interactive_Console.triggered.connect(self.loadInteractive)
        self.ui.actionLoad_Script.triggered.connect(self.loadScript)
        
        #Help Menu
        self.ui.actionScripting.triggered.connect(self.scriptingHelp)
        self.ui.actionAbout.triggered.connect(self.aboutHelp)
        
        #Debug Menu
        self.ui.actionShow_Undo_Stack.triggered.connect(self.showUndoStack)
        self.ui.actionShow_Redo_Stack.triggered.connect(self.showRedoStack)
        self.ui.menuDebug.setVisible(False)
        self.ui.menuDebug.menuAction().setVisible(False)
    
    def connectSignals(self):
        self.ui.fileTabs.tabCloseRequested.connect(self.closeTab)
        #connect changes in tab name
        
# =============================================================================
# File Operations
# =============================================================================
    def openFile(self,filename):
        tab = EPVTab(self,filename)
        self.ui.fileTabs.addTab(tab,filename.stem)
        self.ui.fileTabs.setCurrentWidget(tab)
        tab.tabNameChanged.connect(self.renameTab)        
        #self.enableMenus()
    def open(self):
        filename = QFileDialog.getOpenFileName(self,_translate("MainWindow","Open EPV3"),"",_translate("MainWindow","MHW EPV3 (*.epv3)"))
        if filename[0]:
            filename = Path(filename[0])
            if filename.exists():
                self.openFile(filename)
            else:
                QtWidgets.QMessageBox.critical(None,
                       "File not found",
                       "File {} not found.".format(str(filename)))      
    def new(self):
        tab = EPVTab(self)
        self.ui.fileTabs.addTab(tab,"New EPV3")
        self.ui.fileTabs.setCurrentWidget(tab)
        tab.tabNameChanged.connect(self.renameTab)
        #self.enableMenus()
    def save(self):
        ix = self.ui.fileTabs.currentIndex()
        tab = self.ui.fileTabs.widget(ix)
        tab.Save()
    def saveAs(self):
        ix = self.ui.fileTabs.currentIndex()
        tab = self.ui.fileTabs.widget(ix)
        tab.SaveAs()
    def saveAll(self):
        for tab in [self.ui.fileTabs.widget(i) for i in range(self.ui.fileTabs.count())]:
            tab.Save()

# =============================================================================
# Edit Block
# =============================================================================
    def undo(self):
        widget = self.ui.fileTabs.currentWidget()
        widget.undo()
    def redo(self):
        widget = self.ui.fileTabs.currentWidget()
        widget.redo()
        
    def delete(self):self.currentWidget().delete()
    def duplicate(self):self.currentWidget().duplicate()
    def copy(self):self.currentWidget().copy()
    def paste(self):self.currentWidget().paste()
    def copyProperties(self):self.propertyClipboard = self.currentWidget().copyProperties()
    def pasteProperties(self):
        if self.propertyClipboard: 
            self.currentWidget().pasteProperties(self.propertyClipboard)
    def pushStack(self):self.currentWidget().pushStack(self.copyStack)
    def pasteStack(self):self.currentWidget().pasteStack(self.copyStack)
    def clearStack(self):
        self.copyStack.clear()
    def newGroup(self):self.currentWidget().newGroup()
    def newRecord(self):self.currentWidget().newRecord()
      
# =============================================================================
# Find Block
# =============================================================================
    
    def Find(self):
        if self.ui.fileTabs.currentIndex() == -1:
            return
        findDialog = FindDialog(self,self.currentWidget().currentIndex(),self)
        metaIndex = findDialog.exec()
        if metaIndex:
            file,metaIndex = findDialog.results
            self.ui.fileTabs.setCurrentWidget(file)
            file.setCurrentIndex(metaIndex.index)
            
    def Replace(self):
        if self.ui.fileTabs.currentIndex() == -1:
            return
        replacementDialog = ReplaceDialog(self,self)
        replace = replacementDialog.exec()
        if replace:
            replacements = replacementDialog.results
            for file in replacements:
                file.replace(replacements[file])
    def BatchReplace(self):
        if not self.ui.fileTabs.currentIndex() == -1:
            return
    def getCurrentFile(self):
        return self.currentWidget()
    def getFiles(self):
        return [self.ui.fileTabs.widget(i) for i in range(self.ui.fileTabs.count())]
    
# =============================================================================
# Scripting Block
# =============================================================================
    
    def loadVarDict(self):
        return {"files":MSE.files,"current":MSE.current,"open":MSE.openFile}
    
    def loadInteractive(self):
        __qbox__ = QMessageBox()
        __qbox__.setText("Warning about loading Scripting:")
        __qbox__.setInformativeText("Undo and Redo functionality in all tabs will be be invalidated.\n Open the scripting console despite this?")
        __qbox__.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        __qbox__.setDefaultButton(QMessageBox.Ok)
        __response__ = __qbox__.exec()
        if __response__ == QMessageBox.Ok:
            self.invalidateCaches()
            MSE.start(self)
            MSE.interactiveMode(self.loadVarDict())
            MSE.stop()
        return

    def loadScript(self):
        __filepath__ = QFileDialog.getOpenFileName(
                self,_translate("MainWindow","Load Script"),
                "",
                _translate("MainWindow","Python Script File (*.py)"))[0]
        if not __filepath__:
            return
        __qbox__ = QMessageBox()
        __qbox__.setText("Warning about loading Scripts:")
        __qbox__.setInformativeText("Undo and Redo functionality in all tabs will be be invalidated.\n Load script despite this?")
        __qbox__.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        __qbox__.setDefaultButton(QMessageBox.Ok)
        __response__ = __qbox__.exec()
        if __response__ == QMessageBox.Ok:
            self.invalidateCaches()
            MSE.start(self)
            exec(open(__filepath__,"r").read(),{},self.loadVarDict())
            MSE.stop()
        return

    def invalidateCaches(self):
        for tab in [self.ui.fileTabs.widget(i) for i in range(self.ui.fileTabs.count())]:
            tab.invalidateCaches()
            tab.disableSelection()
            tab.changed = True

# =============================================================================
# Help Block
# =============================================================================
        
    def scriptingHelp(self):
        AboutScripting(self)
    
    def aboutHelp(self):
        AboutHelp(self)
    
# =============================================================================
#  Debug Block
# =============================================================================
    
    def showUndoStack(self):
        print(self.currentWidget().undoStack)
    def showRedoStack(self):
        print(self.currentWidget().redoStack)
        
# =============================================================================
# Housekeeping Blcok
# =============================================================================
    def currentWidget(self):return self.ui.fileTabs.widget(self.ui.fileTabs.currentIndex())
    def closeTab(self,ix):
        tab = self.ui.fileTabs.widget(ix)
        if tab.RequestSave():
            tab.tabNameChanged.disconnect(self.renameTab)
            self.ui.fileTabs.removeTab(ix)
    def renameTab(self,tab,name):
        ix = self.ui.fileTabs.indexOf(tab)
        self.ui.fileTabs.setTabText(ix,name)
    def closeEvent(self, event):
        for ix in range(self.ui.fileTabs.count()):
            tab = self.ui.fileTabs.widget(ix) 
            if not tab.RequestSave():
                event.ignore()
                return
        for ix in range(self.ui.fileTabs.count()-1,-1,-1):
            tab = self.ui.fileTabs.widget(ix) 
            tab.tabNameChanged.disconnect(self.renameTab)
            self.ui.fileTabs.removeTab(ix)
        event.accept()

# =============================================================================
# Dark Theming
# =============================================================================

def setStyle(app):
    from PyQt5.QtCore import Qt
    app.setStyle("Fusion")
    darkPalette = QPalette()
    darkPalette.setColor(QPalette.Window,QColor(53,53,53));
    darkPalette.setColor(QPalette.WindowText,Qt.white);
    darkPalette.setColor(QPalette.Disabled,QPalette.WindowText,QColor(127,127,127));
    darkPalette.setColor(QPalette.Base,QColor(42,42,42));
    darkPalette.setColor(QPalette.AlternateBase,QColor(66,66,66));
    darkPalette.setColor(QPalette.ToolTipBase,Qt.white);
    darkPalette.setColor(QPalette.ToolTipText,Qt.white);
    darkPalette.setColor(QPalette.Text,Qt.white);
    darkPalette.setColor(QPalette.Disabled,QPalette.Text,QColor(127,127,127));
    darkPalette.setColor(QPalette.Dark,QColor(35,35,35));
    darkPalette.setColor(QPalette.Shadow,QColor(20,20,20));
    darkPalette.setColor(QPalette.Button,QColor(53,53,53));
    darkPalette.setColor(QPalette.ButtonText,Qt.white);
    darkPalette.setColor(QPalette.Disabled,QPalette.ButtonText,QColor(127,127,127));
    darkPalette.setColor(QPalette.BrightText,Qt.red);
    darkPalette.setColor(QPalette.Link,QColor(42,130,218));
    darkPalette.setColor(QPalette.Highlight,QColor(42,130,218));
    darkPalette.setColor(QPalette.Disabled,QPalette.Highlight,QColor(80,80,80));
    darkPalette.setColor(QPalette.HighlightedText,Qt.white);
    darkPalette.setColor(QPalette.Disabled,QPalette.HighlightedText,QColor(127,127,127));
    app.setPalette(darkPalette)

if __name__ == '__main__':
    #from pathlib import Path
    app = QtWidgets.QApplication(sys.argv)
    args = app.arguments()[1:]
    splash = SplashScreen()
    response = splash.exec()
    
    if not response:
        sys.exit(app.exec_())
    
    setStyle(app)
    """
    file = QFile("./dark.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())
    """
    """
    app.setStyle("Fusion")

    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(42, 43, 46))
    palette.setColor(QPalette.WindowText, QColor(224, 224, 224))
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(42, 43, 46))
    palette.setColor(QPalette.ToolTipBase, QColor(224, 224, 224))
    palette.setColor(QPalette.ToolTipText, QColor(224, 224, 224))
    palette.setColor(QPalette.Text, QColor(224, 224, 224))
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QColor(224, 224, 224))
    palette.setColor(QPalette.BrightText, QtCore.Qt.red)
    palette.setColor(QPalette.Link, QColor(117, 115, 164))
    palette.setColor(QPalette.Highlight, QColor(105, 125, 135))
    palette.setColor(QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(palette)
    """
    window = MainWindow(args)
    #tab = EPVTab(self,r"E:\MHW\chunkG0\pl\f_equip\pl124_0000\body\epv\f_body124.epv3")
    #self.ui.fileTabs.addTab(tab,"Test") 
    window.openFile(Path(r"E:\MHW\chunkG0\wp\rod\epv\hm_wp10_01.epv3"))
    sys.exit(app.exec_())