# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 05:20:43 2020

@author: AsteriskAmpersand
"""
from copy import deepcopy

from ._EPVGroup import EPVGroup
from ._EPVRecord import EPVRecord

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QModelIndex

def pasteStack(self,index,copyStack):
    if len(copyStack) == 0:
        return
    self.startRecording()
    if copyStack.pure():
        self.pastePureStack(index,copyStack)
    else:
        decision = self.mixedStackQuery().exec()
        stacks = copyStack.split()
        for typing in [EPVRecord,EPVGroup]:
            typingStack = stacks[typing]
            if typing is EPVRecord:
                if decision == 0:
                    group = self.newGroup()
                    nindex = self.index(group.row(),0,QModelIndex())
                    self.pastePureStack(nindex,typingStack)
                elif decision == 1:
                    self.pastePureStack(index,typingStack)
                else:
                    continue
            else:
                self.pastePureStack(index,typingStack)
    self.endRecording()
    return
    
def pastePureStack(self,index,copyStack):
    target = self.access(index)
    typing = next(copyStack.types())
    #print(list(copyStack.types()))
    #print(typing)
    #print(typing is EPVGroup)
    #It's failing for groups
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
            print(target.__parent__)
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
