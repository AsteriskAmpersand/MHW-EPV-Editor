# -*- coding: utf-8 -*-
"""
Created on Sun May  3 08:55:29 2020

@author: AsteriskAmpersand
"""
from replace.ReplaceEnums import BasicText,FullText,Color,RGBAColor

class MetaIndex():
    def __init__(self,index,rindex):
        self.rindex = rindex
        self.index = index
    def dataPath(self):
        string = "" if self.rindex == -1 else "- Slot: %d"%self.rindex
        return "Group: %d - Record: %d%s"%(self.index.parent().row(),self.index.row(),string)
    def findValue(self):
        return NotImplementedError
    def getType(self):
        return NotImplementedError
    
class PathIndex(MetaIndex):
    def getType(self):
        return BasicText if self.rindex != -1 else FullText
    def findValue(self):
        record = self.index.model().access(self.index)
        if self.rindex == -1:
            path = '\n'.join([record.path0,record.path1,record.path2,record.path3])
        else:
            path = getattr(record,"path%d"%self.rindex)
        return path
class ColorIndex(MetaIndex):
    def getType(self):
        return Color
    def findValue(self):
        record = self.index.model().access(self.index)
        return record.epvc[self.rindex].color[:3]
class RGBAIndex(MetaIndex):
    def getType(self):
        return RGBAColor
    def findValue(self):
        record = self.index.model().access(self.index)
        epvc = record.epvc[self.rindex]
        return epvc.color