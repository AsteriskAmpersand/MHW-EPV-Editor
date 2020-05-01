# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EPVElements.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from structs.epv import parameterBlock1,parameterBlock2

class EPVC():
    def __init__(self,record = None):
        if record is not None:
            self.efxslot = record.efxslot            
            self.r,self.g,self.b,self.alpha = record.hexcolor
            self.frequency = record.frequency
            self.size = record.size
            self.saturation = record.saturation
        else:
            self.efxslot = 0        
            self.r,self.g,self.b,self.alpha = 0,0,0,255
            self.frequency = 1
            self.size = 1
            self.saturation = 1
    def serialize(self):
        return {"efxslot":self.efxslot,
                "hexcolor":[self.r,self.g,self.b,self.alpha],
                "saturation":self.saturation,
                "size":self.size,
                "frequency":self.frequency
                }     
    @property
    def color(self):
        return (self.r,self.g,self.b)
    @color.setter
    def color(self,value):
        self.r,self.g,self.b = value

def emptyProp(propertyType):
    if "[" in propertyType:
        return [0]*int(propertyType.split("[")[1].replace("]",""))
    else:
        return 0
    
class ParameterBlock():
    def __init__(self,record=None):
        if record is None:
            for prop in self.struct.subcons:
                self.__setattr__(prop.name,emptyProp(prop.docs))
        else:
            for prop in self.struct.subcons:
                self.__setattr__(prop.name,getattr(record,prop.name))
    def serialize(self):
        return {prop.name:getattr(self,prop.name) for prop in self.struct.subcons}
            
class ParameterBlock1(ParameterBlock):
    struct = parameterBlock1
class ParamaterBlock2(ParameterBlock):
    struct = parameterBlock2

def objectType(entry):
    if "parameterBlock1" in entry:
        return ParameterBlock1
    if "parameterBlock2" in entry:
        return ParamaterBlock2
    return lambda x: x