# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 05:20:43 2020

@author: AsteriskAmpersand
"""
from copy import deepcopy

from ._EPVGroup import EPVGroup
from ._EPVRecord import EPVRecord

from PyQt5.QtWidgets import QMessageBox

def pasteStack(self,index,copyStack):
    if len(copyStack) == 0:
        return
    self.startRecording()
    if copyStack.pure():
        self.pastePureStack(index,copyStack)
    else:
        decision = self.mixedStackQuery().exec()
        for typingStack in copyStack.split():
            typing = next(copyStack.types())
            if typing is EPVRecord:
                if decision == QMessageBox.YesRole:
                    nindex = self.newGroup()
                    self.pastePureStack(nindex,typingStack)
                elif decision == QMessageBox.NoRole:
                    self.pastePureStack(index,typingStack)
            else:
                self.pastePureStack(index,typingStack)
    self.endRecording()
    return
    
def pastePureStack(self,index,copyStack):
    target = self.access(index)
    typing = next(copyStack.types())
    print(list(copyStack.types()))
    print(typing)
    print(typing is EPVGroup)
    if typing is EPVGroup:
        op = self.insertGroup
        if type(target) is EPVGroup:
            args = lambda entry: (deepcopy(entry),target.row()+1)
        elif type(target) is EPVRecord:
            args = lambda entry: (deepcopy(entry),target.__parent__.row()+1)
    elif typing is EPVRecord:
        op = self.insertRecord
        if type(target) is EPVGroup:
            args = lambda entry: (target,deepcopy(entry))
        elif type(target) is EPVRecord:
            args = lambda entry: (target.__parent__,deepcopy(entry),target.row()+1)            
    for entry in copyStack.consume():
        op(*args(entry))
        
def mixedStackQuery(self):
    qbox = QMessageBox()
    qbox.setWindowTitle("Orphan Records")
    qbox.setText("""There are orphan records on the stack.
Create a new group to hold them, parent them to current index or delete them?""")
    qbox.addButton("Create",QMessageBox.YesRole)
    qbox.addButton("Parent",QMessageBox.NoRole)
    qbox.addButton("Delete",QMessageBox.RejectRole)
    return qbox
