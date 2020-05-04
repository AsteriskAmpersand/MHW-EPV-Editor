# -*- coding: utf-8 -*-
"""
Created on Sun May  3 09:21:22 2020

@author: AsteriskAmpersand
"""

from ._EPVMetaIndex import PathIndex,ColorIndex,RGBAIndex

def getStringReferences(self,merge):
    entries = []
    for group in self:
        parent = self.index(group.row(),0)
        for record in group:
            child = self.index(record.row(),0,parent)
            paths = [record.path0,record.path1,record.path2,record.path3]
            if merge:
                path = '\n'.join(paths)
                ix = -1
                index = PathIndex(child,ix)
                entries.append((index,path))
            else:
                for ix,path in enumerate(paths):
                    index = PathIndex(child,ix)
                    entries.append((index,path))
    return entries
                    
def getColorReferences(self,alpha):
    entries = []
    for group in self:
        parent = self.index(group.row(),0)
        for record in group:
            child = self.index(record.row(),0,parent)
            for ix,epvc in enumerate(record.epvc):
                colors = list(epvc.color)
                if alpha:
                    colors += [epvc.alpha]
                    index = RGBAIndex(child,ix)
                else:
                    index = ColorIndex(child,ix)
                entries.append((index,colors))
    return entries

#for ref,string in reference.getStringReferences(self.ui.Group.checkState())
#for ref,color in reference.getColorReferences(self.ui.AlphaEnable.checkState()):