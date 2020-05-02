# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 20:07:54 2020

@author: AsteriskAmpersand
"""
from ._ComplexUndo import CompositeUndo
from generic.Queue import Queue

def startRecording(self):
    if not self.complexUndo:
        self.complexUndo = CompositeUndo(self)
        
def endRecording(self):
    self.undoStack.put((self.complexUndo.undo,(),self.complexUndo.redo,()))
    self.undoableAction.emit(self)
    self.complexUndo = None
    
def discardRecording(self):
    self.complexUndo = None

def recordState(self,undoerFunction,undoerParameters,redoFunction,redoParameters):
    if self.complexUndo:
        self.complexUndo.addAction(undoerFunction,undoerParameters,redoFunction,redoParameters)
    else:
        self.undoStack.put((undoerFunction,undoerParameters,redoFunction,redoParameters))
        self.undoableAction.emit(self)
    
def undo(self):
    undofunc,undoparam,redo,rparam = self.undoStack.pop()
    undofunc(*undoparam)
    self.redoStack.put((redo,rparam,undofunc,undoparam))
    
def redo(self):
    redo,rparam,undofunc,undoparam = self.redoStack.pop()
    redo(*rparam)
    self.undoStack.put((undofunc,undoparam,redo,rparam))
    
def clearRedoStack(self):
    self.redoQueue = Stack()