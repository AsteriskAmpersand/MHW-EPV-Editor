# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 19:29:49 2020

@author: AsteriskAmpersand
"""
from generic.Queue import Queue,Stack
class CompositeUndo():
    def __init__(self,model):
        self.model = model
        self.redoActions = Queue() 
        self.undoActions = Stack()
    def __call__(self):
        self.do()
    def addAction(self,undoF,uparam,redoF,param):
        self.redoActions.put((redoF,param))
        self.undoActions.put((undoF,uparam))
        #print(uparam)
    def do(self,source):
        for f,p in source.consume():
            f(*p)
    def undo(self):self.do(self.undoActions)
    def redo(self):self.do(self.redoActions)