# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 02:51:53 2020

@author: AsteriskAmpersand
"""

from PyQt5.QtCore import Qt
from structs.epv import EPVExtraneousProperties
from model.EPVElements import (EPVC, objectType)
from structs.epv import record as binaryRecord
from structs.epv import extendedRecord as binaryExtendedRecord

class EPVRecord():
    def __init__(self,parent=None,record = None,trailID = 0):
        if record is None:
            self.recordID = 0
            self.path0,self.path1,self.path2,self.path3 = "","","",""
            self.boneID = 255
            self.epvc = [EPVC() for i in range(8)]
            self.trailID = trailID
            for prop in EPVExtraneousProperties:
                setattr(self,prop,objectType(EPVExtraneousProperties[prop])(None))
        else:
            self.recordID = record.recordID
            self.path0,self.path1,self.path2,self.path3 = record.packed_path
            self.boneID = record.boneID
            self.epvc = [EPVC(record.epvColor[i]) for i in range(8)]
            self.trailID = trailID
            for prop in EPVExtraneousProperties:
                setattr(self,prop,objectType(EPVExtraneousProperties[prop])(getattr(record,prop)))
        self.__parent__ = parent
        
    def serialize(self):
        export = {}
        export["packed_path"] = [str(self.path0).replace("\x00",""),str(self.path1).replace("\x00",""),
                                 str(self.path2).replace("\x00",""),str(self.path3).replace("\x00","")]
        export["recordID"] = self.recordID
        export["boneID"] = self.boneID
        export["trailID"] = self.trailID
        export["epvColor"] = [epvc.serialize() for epvc in self.epvc]
        for prop in EPVExtraneousProperties:
            sprop = getattr(self,prop)
            export[prop] = sprop.serialize() if hasattr(sprop,"serialize") else sprop
        return export
    def EPVSerialize(self,struct):return struct.build(self.serialize())
    def binarySerialize(self):return self.EPVSerialize(binaryRecord)
    def binaryExtendedSerialize(self):return self.EPVSerialize(binaryExtendedRecord)
    def getRole(self,role):
        if role == Qt.DisplayRole:
            Display = "Record ID: %s - %s"%(self.recordID,self.path0)
            return Display
        if role == Qt.EditRole:
            return self.recordID
        
    def setRole(self,value,role):
        if role == Qt.EditRole:
            self.recordID = value