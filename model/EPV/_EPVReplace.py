# -*- coding: utf-8 -*-
"""
Created on Mon May  4 11:18:33 2020

@author: AsteriskAmpersand
"""


def startReplace(self):
    self.startRecording()
    return

def _pathReplace(self,index,rindex,content):
    record = self.access(index)
    setattr(record,"path%d"%rindex,content)
    self.pathEdited.emit(index,rindex)
    
def pathReplace(self,index,rindex,content):
    record = self.access(index)
    if rindex == -1:
        paths = content.split("\n")
        paths = paths[:4] + [""]*max(0,(4-len(paths)))
        for ix,p in enumerate(paths):
            self.pathReplace(index,ix,p)
    else:
        path = "path%d"%rindex
        self.recordState(self._pathReplace,(index,rindex,getattr(record,path)),
                         self._pathReplace,(index,rindex,content))
        self._pathReplace(index,rindex,content)

def _colorReplace(self,index,rindex,content):
    colorSlot = self.access(index).epvc[rindex]
    r,g,b = content[:3]
    colorSlot.color = r,g,b
    if len(content) > 3:
        a = content[3]
        colorSlot.alpha = a    
    self.epvEdited.emit(index,rindex) 

def colorReplace(self,index,rindex,content):
    colorSlot = self.access(index).epvc[rindex]
    oldColor = tuple(list(colorSlot.color)+([] if len(content)==3 else [colorSlot.alpha]))
    self.recordState(self._colorReplace,(index,rindex,oldColor),self._colorReplace,(index,rindex,content))
    self._colorReplace(index,rindex,content)
    

def endReplace(self):
    self.endRecording()
    return