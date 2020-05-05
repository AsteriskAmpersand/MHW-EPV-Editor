# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 16:45:22 2020

@author: AsteriskAmpersand
"""

from itertools import chain
from pathlib import Path
from generic.Queue import Queue,Stack
from model.EPV import EPV,EPVGroup,EPVRecord
from model.EPVCSlots import EPVCEntry
from model.utils import layout_widgets, qlistiter
from structs.epv import EPVExtraneousProperties
from gui.Forms import SelectForm
from gui.FileTab import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication
_translate = QtCore.QCoreApplication.translate

def functionChain(functionList):
    for function in functionList:
        function()
        
import sys 
def catch_exceptions(t, val, tb):
    QtWidgets.QMessageBox.critical(None,
                                   "An exception was raised",
                                   "Exception type: {}".format(tb))
    old_hook(t, val, tb)


old_hook = sys.excepthook
sys.excepthook = catch_exceptions

class EPVTab(QtWidgets.QWidget):
    tabNameChanged = QtCore.pyqtSignal(object,object)
    def __init__(self, parent = None, epvpath = None):
        super().__init__(parent)
        self.undoStack = Stack()
        self.redoStack = Stack()
        self.__changed__ = False
        self.path = epvpath
        self.changed = epvpath is None
        self.EPVModel = EPV(self,self.path)
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.setEPVSlots()
        self.setPropertySlots()
        
        self.connect()
        self.disableRecords()
        self.disableGroup()
        self.show()
        
    @property
    def changed(self): return self.__changed__
    @changed.setter
    def changed(self,value):
        if self.__changed__ != value:
            self.__changed__=value
            self.tabNameChanged.emit(self,"*"+(Path(self.path).stem if self.path else "New File"))
    
    def connect(self):
        self.ui.recordBrowser.setModel(self.EPVModel)
        self.connectSignals()   

    def connectSignals(self):
        self.ui.RecordIDs.undoableAction.connect(self.actionPushed)
        self.ui.efxPathsGroup.undoableAction.connect(self.actionPushed)
        self.EPVModel.undoableAction.connect(self.actionPushed)
        self.ui.recordBrowser.selectionModel().currentChanged.connect(self.selectionChanged)
        self.EPVModel.idEdited.connect(self.updateIDs)
        self.EPVModel.epvEdited.connect(self.updateEPVC)
        self.EPVModel.pathEdited.connect(self.updatePath)
        #Connect the view selection changes to update the pseudo-views
    
    def accessEPV(self,current):
        selected = self.EPVModel.access(current)
        if type(selected) is EPVGroup:
            group = selected
            record = None           
        elif type(selected) is EPVRecord:
            group = self.EPVModel.access(current.parent())
            record = selected
        else:
            group = None
            record = None
        return group,record
    
    def updateIDs(self,index):
        group,record = self.accessEPV(index)
        ix = self.ui.recordBrowser.selectionModel().currentIndex()
        self.ui.RecordIDs.IDUpdated(group,record,ix==index)
    
    def updateEPVC(self,index,rindex):
        if index == self.currentIndex():
            self.ui.efxSlots.itemWidget(self.ui.efxSlots.item(rindex)).fromModel()
    def updatePath(self,index,pindex):
        if index == self.currentIndex():
            self.ui.efxPathsGroup.fromModel()
    
    def selectionChanged(self,current,previous):
        selected = self.EPVModel.access(current)
        group,record = self.accessEPV(current)
        if type(selected) is EPVGroup:
            self.enableGroup()
            self.disableRecords()            
        elif type(selected) is EPVRecord:
            self.enableGroup()
            self.enableRecords()
        else:
            self.disableGroup()
            self.disableRecords()
        self.connectProperties(record)
        self.connectIDs(group,record)
    
    def connectProperties(self,record):
        if record:
            for slot,epvc in zip(qlistiter(self.ui.efxSlots),record.epvc):
                slot.connect(epvc)
        for widget in chain(qlistiter(self.ui.recordPropertiesL),
                          qlistiter(self.ui.recordPropertiesR)):
            widget.connect(record)
        self.ui.efxPathsGroup.connect(record)
        
    def connectIDs(self,group,record):
        self.ui.RecordIDs.connect(group,record)
    
    def setEPVSlots(self):
        for i in range(8):
            itemN = QtWidgets.QListWidgetItem()
            form = EPVCEntry()
            itemN.setSizeHint(form.sizeHint())            
            self.ui.efxSlots.addItem(itemN)
            self.ui.efxSlots.setItemWidget(itemN, form)
            form.undoableAction.connect(self.actionPushed)
    
    def setPropertySlots(self):
        propertyList = list(EPVExtraneousProperties.keys())
        self.ui.recordPropertiesL.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.ui.recordPropertiesR.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        for lprop in propertyList[:len(propertyList)//2+2]:
            form = SelectForm(lprop,EPVExtraneousProperties[lprop],self)
            itemN = QtWidgets.QListWidgetItem()
            itemN.setSizeHint(form.sizeHint())    
            self.ui.recordPropertiesL.addItem(itemN)
            self.ui.recordPropertiesL.setItemWidget(itemN, form)
            form.undoableAction.connect(self.actionPushed)
        for rprop in propertyList[len(propertyList)//2+2:]:
            form = SelectForm(rprop,EPVExtraneousProperties[rprop],self)
            itemN = QtWidgets.QListWidgetItem()
            itemN.setSizeHint(form.sizeHint())    
            self.ui.recordPropertiesR.addItem(itemN)
            self.ui.recordPropertiesR.setItemWidget(itemN, form)
            form.undoableAction.connect(self.actionPushed)
    
    def toggleRecords(self,val):
        self.ui.RecordIDs.toggleRecords(val)
        self.ui.efxSlots.setEnabled(val)
        self.ui.recordPropertiesL.setEnabled(val)
        self.ui.recordPropertiesR.setEnabled(val)
        self.ui.efxPathsGroup.setEnabled(val)
    def toggleGroup(self,val):
        self.ui.RecordIDs.toggleGroup(val)
         
    def disableRecords(self): self.toggleRecords(False)     
    def enableRecords(self): self.toggleRecords(True)
    def disableGroup(self): self.toggleGroup(False)
    def enableGroup(self): self.toggleGroup(True)
    
# =============================================================================
# Main - Search Functionality
# =============================================================================

    def getStringReferences(self,join=False):
        return self.EPVModel.getStringReferences(join)
    def getColorReferences(self,alpha=False):
        return self.EPVModel.getColorReferences(alpha)
    def replace(self,replacements):
        self.EPVModel.startReplace()
        for metaindex,content in replacements:
            metaindex.replace(content)
        self.EPVModel.endReplace()
    
# =============================================================================
# Main - Edit Functionality
# =============================================================================
    
    def actionPushed(self,responsible):
        self.changed = True
        self.undoStack.append(responsible)
        self.clearRedoStack()
    def undo(self):
        if self.undoStack.empty():
            return
        responsible = self.undoStack.pop()
        responsible.undo()
        self.redoStack.put(responsible)
    def redo(self):
        if self.redoStack.empty():
            return
        responsible = self.redoStack.get()
        responsible.redo()
        self.undoStack.append(responsible)
    def clearRedoStack(self):
        while(not self.redoStack.empty()):
            responsible = self.redoStack.get()
            responsible.clearRedoStack()
            
    def delete(self):self.EPVModel.removeRows(self.currentIndex().row(),1,self.currentIndex().parent())
    def duplicate(self):self.currentEntry().duplicate()
    def copy(self):QApplication.clipboard().setMimeData(self.EPVModel.mimeData([self.currentIndex()]))
    def paste(self):
        self.EPVModel.dropMimeData( QApplication.clipboard().mimeData(),
                                    QtCore.Qt.CopyAction,
                                    self.currentIndex().row(),
                                    0,
                                    self.currentIndex().parent())
    def copyProperties(self):return self.currentEntry()
    def pasteProperties(self,clipboard):self.currentEntry().pasteProperties(clipboard)
    def pushStack(self,mainCopyStack):mainCopyStack.put(self.currentEntry())
    def pasteStack(self,mainCopyStack):self.EPVModel.pasteStack(self.currentIndex(),mainCopyStack)
    def newGroup(self):
        index = self.currentIndex()
        if index.isValid():
            self.EPVModel.newGroup(index.row()+1)
            self.selectNextGroup()
        else:
            self.EPVModel.newGroup()            
        
    def newRecord(self):self.EPVModel.newRecord(self.currentIndex())
# =============================================================================
# Main - File Functionality
# =============================================================================
    def currentEntry(self):
        return self.EPVModel.access(self.currentIndex())
    def currentIndex(self):
        selection = self.ui.recordBrowser.selectedIndexes()
        if len(selection)==1:
            return selection[0]
        else:
            return QtCore.QModelIndex()
    def setCurrentIndex(self,index):
        self.ui.recordBrowser.setCurrentIndex(index)
    def selectNextGroup(self):
        current = self.currentIndex()
        if not current.isValid():
            return
        if current.internalPointer() is EPVGroup:
            current = current.parent()
        if current.row()+1 >= len(self.EPVModel):
            return
        self.ui.recordBrowser.setCurrentIndex(self.EPVModel.index(current.row()+1,current.column(),current.parent()))
        
    def SaveToFile(self,path):
        with open(path,"wb") as outf:
            outf.write(self.EPVModel.serialize())
        return
    def SaveAs(self):
        root = ""
        if self.path:
            root = str(Path(self.path).parent)
        filename = QFileDialog.getSaveFileName(self,_translate("EPVTab","Save EPV3"),root,_translate("EPVTab","MHW EPV3 (*.epv3)"))
        if filename[0]:
            filename = Path(filename[0])
            if filename.exists():
                self.SaveToFile(filename)
                self.path = filename
                self.tabNameChanged(self,Path(self.path).stem)
                return True
        return False    
    def Save(self):
        if not self.path:
            return self.SaveAs()
        else:
            self.SaveToFile(self.path)
            return True
            
    def RequestSave(self):
        if not self.changed:
            return True
        savePath = self.path if self.path else "New File"
        choice = QtWidgets.QMessageBox.question(self, 'Unsaved Changes on %s'%savePath,
                                            "Save Changes to %s?"%savePath,
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)
        if choice == QtWidgets.QMessageBox.Cancel:
            return False
        if choice == QtWidgets.QMessageBox.Yes:
            return self.Save()
        if choice == QtWidgets.QMessageBox.No:
            return True
        
if "__main__" in __name__:    
    app = QtWidgets.QApplication(sys.argv)
    window = EPVTab(None, r"E:\MHW\chunkG0\wp\rod\epv\hm_wp10_01.epv3")
    sys.exit(app.exec_())