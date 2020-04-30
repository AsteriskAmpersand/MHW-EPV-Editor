# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 19:29:49 2020

@author: AsteriskAmpersand
"""
from model.Queue import Queue,Stack
class CompositeUndo():
    def __init__(self,model):
        self.model = model
        self.redoActions = Queue() 
        self.undoActions = Stack()
    def __call__(self):
        self.do()
    def addAction(self,func,param,undo,uparam):
        self.redoActions.put((func,param))
        self.undoAction.put((undo,uparam))
    def do(self):
        pass