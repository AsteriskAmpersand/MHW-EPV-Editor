# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 16:45:22 2020

@author: AsteriskAmpersand
"""

from itertools import chain
from functools import partial
from pathlib import Path

from generic.Queue import Stack
from model.EPV import EPV,EPVGroup,EPVRecord
from model.EPVCSlots import EPVCEntry
from model.utils import qlistiter
from structs.epv import EPVExtraneousProperties
from gui.Forms import SelectForm
from gui.FileTab import Ui_Form

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QApplication,QAction,QMenu
from PyQt5.QtCore import QModelIndex, pyqtSignal, Qt, QCoreApplication
_translate = QCoreApplication.translate

"""       
import sys 
def catch_exceptions(t, val, tb):
    QtWidgets.QMessageBox.critical(None,
                                   "An exception was raised",
                                   "Exception type: {}".format(tb))
    old_hook(t, val, tb)


old_hook = sys.excepthook
sys.excepthook = catch_exceptions
"""

def defaultIfNone(function):
    def composite(self,*args):
        ix = None
        if len(args)>0:
            ix = args[0]
        if ix is None: 
            ix = self.currentIndex()
        #if not (ix and ix.isValid()):
        #    return False
        #print(function.__name__)
        #print(ix.row(),ix.internalPointer())
        result = function(self,ix)
        self.EPVModel.dataChanged.emit(ix,ix) #Might degrade performance compared to responsiveness
        return result
    return composite

def defaultIfClipboard(function):
    def composite(self,clipboard,ix = None):
        #print(function.__name__)
        #print(type(self))
        #print(type(clipboard))
        #print(type(ix))
        if ix is None: 
            ix = self.currentIndex()
        #if not (hasattr(ix,"isValid") and ix.isValid()):
        #    return False
        result = function(self,clipboard,ix)
        self.EPVModel.dataChanged.emit(ix,ix) #Might degrade performance compared to responsiveness
        return result
    return composite

class EPVTab(QtWidgets.QWidget):
    tabNameChanged = pyqtSignal(object,object)
    def __init__(self, parent = None, epvpath = None):
        super().__init__(parent)
        #self.__parent__ = parent
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
    
    def disableSelection(self):
        self.ui.recordBrowser.setCurrentIndex(QModelIndex())
    
    def connect(self):
        self.ui.recordBrowser.setModel(self.EPVModel)
        self.connectSignals()
        self.connectMenu()
        
    def connectMenu(self):
        view = self.ui.recordBrowser
        view.setContextMenuPolicy(Qt.CustomContextMenu)
        view.customContextMenuRequested.connect(self.customContextMenuRequested)
         
    def customContextMenuRequested(self, gp):
        view = self.ui.recordBrowser
        menu = QMenu(self)
        ix = view.indexAt(gp)
        record = [self.newRecord] if ix.row()!=-1 else []
        recordName = ["New Record"] if ix.row()!=-1 else []
        
        def setmenu(actionNames,methods,*args):
            for actionName,method in zip(actionNames,methods):
                action = QAction(actionName,view)
                action.triggered.connect(partial(method,*args))
                menu.addAction(action)
                
        setmenu(["New Group"]+recordName+["Paste"],[self.newGroup]+record+[self.paste],ix)
        if ix.isValid():
            setmenu(["Copy","Delete","Duplicate"],[self.copy,self.delete,self.duplicate],ix)
        clipboard = self.parentWidget().parentWidget().parentWidget().parentWidget().copyStack
        propclipboard = self.parentWidget().parentWidget().parentWidget().parentWidget().propertyClipboard
        if ix.isValid(): setmenu(["Push to Copy Stack"],[self.pushStack],clipboard,ix)
        setmenu(["Paste Copy Stack"],[self.pasteStack],clipboard,ix)
        if ix.isValid():
            setmenu(["Copy Properties"],[self.copyProperties,self.pasteProperties],propclipboard,ix)
            if propclipboard is not None and type(propclipboard) == type(self.EPVModel.access(ix)):
                setmenu(["Paste Properties"],[self.pasteProperties],propclipboard,ix)

        action = menu.exec_(view.viewport().mapToGlobal(gp))
        #print(ix.row(),ix.column(),ix.internalPointer())
        
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
# Main - Scripting Functionality
# =============================================================================
    
    def invalidateCaches(self):
        self.EPVModel.invalidateCaches()
    
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
    @defaultIfNone
    def delete(self,ix):
        r = ix.row()
        p = ix.parent()
        if r == -1: return False
        return self.EPVModel.removeRows(r,1,p)
    @defaultIfNone
    def duplicate(self,ix):
        if ix.row() == -1: return False
        return self.getEntry(ix).duplicate()
    @defaultIfNone
    def copy(self,ix):
        if not ix.isValid():
            return False
        QApplication.clipboard().setMimeData(self.EPVModel.mimeData([ix]))
    @defaultIfNone
    def paste(self,ix):
        self.EPVModel.dropMimeData( QApplication.clipboard().mimeData(),
                                    Qt.CopyAction,
                                    ix.row(),
                                    ix.column(),
                                    ix.parent())
    @defaultIfClipboard
    def copyProperties(self,clipboard,ix):
        if not ix.isValid():
            return False
        clipboard.set(self.getEntry(ix))
    @defaultIfClipboard
    def pasteProperties(self,clipboard,ix):
        if not ix.isValid():
            return
        self.getEntry(ix).pasteProperties(clipboard.get())
    @defaultIfClipboard
    def pushStack(self,mainCopyStack,ix):
        if not ix.isValid():
            return False
        mainCopyStack.put(self.getEntry(ix))
    @defaultIfClipboard
    def pasteStack(self,mainCopyStack,ix):
        self.EPVModel.pasteStack(ix,mainCopyStack)
    @defaultIfNone
    def newGroup(self, index):
        if index.isValid():
            self.EPVModel.newGroup(index.row()+1)
            self.selectNextGroup()
        else:
            self.EPVModel.newGroup()            
    @defaultIfNone
    def newRecord(self,ix):
        self.EPVModel.newRecord(ix)
# =============================================================================
# Main - File Functionality
# =============================================================================
    def getEntry(self,ix):
        return self.EPVModel.access(ix)
    def currentEntry(self):
        return self.getEntry(self.currentIndex())
    def currentIndex(self):
        selection = self.ui.recordBrowser.selectedIndexes()
        if len(selection)==1:
            return selection[0]
        else:
            return QModelIndex()
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
        try:
            with open(path,"wb") as outf:
                #print(path)
                data = self.EPVModel.serialize()
                #print(data)
                outf.write(data)
        except Exception as e:
            #print(e)
            return False
        return True
    def SaveAs(self):
        root = ""
        if self.path:
            root = str(Path(self.path).parent)
        filename = QFileDialog.getSaveFileName(self,_translate("EPVTab","Save EPV3"),root,_translate("EPVTab","MHW EPV3 (*.epv3)"))
        if filename[0]:
            filename = Path(filename[0])
            success = self.SaveToFile(filename)
            if not success: return False
            self.path = filename
            self.tabNameChanged.emit(self,Path(self.path).stem)
            return True
        return False    
    def Save(self):
        if not self.path:
            return self.SaveAs()
        else:
            return self.SaveToFile(self.path)
            
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
        
# =============================================================================
# Menu Bar Checks
# =============================================================================
            
    def undoable(self):
        return not self.undoStack.empty()
    
    def redoable(self):
        return not self.redoStack.empty()
    
        
if "__main__" in __name__:
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = EPVTab(None, r"E:\MHW\chunkG0\wp\rod\epv\hm_wp10_01.epv3")
    sys.exit(app.exec_())