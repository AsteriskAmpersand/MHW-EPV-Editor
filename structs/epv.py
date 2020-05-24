# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 13:04:14 2020

@author: AsteriskAmpersand
"""
from construct import Int8sl as byte
from construct import Int8ul as ubyte
from construct import Int16sl as short
from construct import Int16ul as ushort
from construct import Int32sl as int32
from construct import Int32ul as uint32
from construct import Int64ul as uint64
from construct import Float32l as float32
from construct import CString as string
from construct import Struct,this,Probe
#from Chunk import chunkPath
from pathlib import Path
from collections import OrderedDict

epvc = Struct(
        "efxslot" / int32 *"int",#0
        "hexcolor" / ubyte[4] *"ubyte[4]",#255 255 255 255
        "saturation" / float32 *"float",#1
        "size" / int32 *"int",#1
        "frequency" / float32 *"float",#1
        )

parameterBlock1 = Struct(
    "paramU0" / int32[3] *"int[3]",#[1, 0, 0] normally
    "paramU1" / float32 *"float",#0 normally
    "paramU2" / int32[4] *"int[4]",#[0, 0, 1, 120] normally
    "EFXSubIndex" / short[2] *"short[2]",#[-1, -1, -1, -1] normally
    "paramU3" / short[2] *"short[2]",#[-1, -1, -1, -1] normally
    "EFXSubIndex2" / short[2] *"short[2]",
    "paramU4" / short[2] *"short[2]",#[0, 0] normally
)

parameterBlock2 = Struct(
    "f1" / float32 *"float",#1.0 normally
    "b1" / byte *"byte",#-128 normally
    "b2" / byte *"byte",#13 normally
    "b3" / byte *"byte",#1 normally
    "b4" / byte *"byte",#0 normally
    "i1" / int32 *"int",#6 normally
    "f2" / float32 *"float",#100 normally
    "i2" / int32 *"int",#512 normally
    "i3" / int32 *"int",#-1 normally
)

record = Struct(
    "packed_path" / string("utf-8")[4] *"string[4]",
    "padding" / int32 *"int",#0
    "unknownID" / int32 *"int",#0 or 5
    "recordID" / ushort *"ushort",    
    "parameterBlock1" / parameterBlock1 *"parameterBlock1",    
    "position" / float32[3] *"float[3]",#[0,0,0] normally
    "positionJitter" / float32[3] *"float[3]",#[0,0,0] normally
    "rotation" / float32[3] *"float[3]",#[0,0,0] normally
    "rotationJitter" / float32[3] *"float[3]",#[0,0,0] normally
    "paramW3"/ int32[2] *"int[2]",# normally 0,0 or 5,4 or 4,4
    "boneID" / int32 *"int",#tends to be -1
    "paramW4" / int32[3] *"int[3]",#confirmed cursed shit, tends to be [0,0,-1]
    "epvColor" / epvc[8] *"epvc[8]",
    "paramW5" / float32[2] *"float[2]",#tends to be [1,0]
    "parameterBlock2" / parameterBlock2 *"parameterBlock2",
    "paramV" / int32[4] *"int[4]",#[0, 0, 0, 0] normally
)

extendedRecord = record + Struct("trailID" / int32,)

EPVExtraneousProperties = OrderedDict([(i.name,i.docs) for i in record.subcons if i.name not in ["packed_path","recordID","epvColor","boneID"]])
def propDefault(prop,doc = None):
    if doc is None:
        doc = prop.docs
    return [0]*int(doc.split("[")[1].replace("]","")) if "[" in doc else 0
    
class parameterBlockDefault():
    def __init__(self):
        for prop in self.struct.subcons:
            setattr(self,prop.name, propDefault(prop))
class parameterBlock1Default(parameterBlockDefault):
    struct = parameterBlock1
class parameterBlock2Default(parameterBlockDefault):
    struct = parameterBlock2   
EPVExtraneousDefaults = OrderedDict([(prop,propDefault(prop,EPVExtraneousProperties[prop])) for prop in EPVExtraneousProperties if "parameterBlock" not in prop] + 
                                    [("parameterBlock1",parameterBlock1Default()),
                                     ("parameterBlock2",parameterBlock2Default())])

defaultRecord = {}
    
group = Struct(
    "recordCount" / uint32,
    "groupID" / ushort,
    "records" / record[this.recordCount],
)

extendedGroup = Struct(
    "recordCount" / uint32,
    "groupID" / ushort,
    "records" / extendedRecord[this.recordCount],     
)

trailRecord = Struct(
    "trailID" / int32,
    "blockID" / uint32,
    "recordID" / uint32,
)

trail = Struct(
    "padding" / uint64,
    "trailCount" / uint32,
    "trails" / trailRecord[this.trailCount],
    "epvPath" / string("utf-8"),
    "ONE" / byte,
    "NULL" / uint32,
)

blockSection = Struct(
    "count"  / uint32,
    "blocks" / group[this.count],        
)

header = Struct(
    "signature" / uint64,        
)

class EPVFile():
    headerStruct = header
    bodyStruct = blockSection
    trailStruct = trail
    def __init__(self,filepath):
        with open(filepath,"rb") as inf:
            self.header = self.headerStruct.parse_stream(inf)
            self.body = self.bodyStruct.parse_stream(inf)
            self.trail = self.trailStruct.parse_stream(inf)
            
    @staticmethod
    def file_serialize(header,body,trail):
        return EPVFile.headerStruct.build(header)+\
                EPVFile.bodyStruct.build(body)+\
                EPVFile.trailStruct.build(trail)
                
from pathlib import Path

"""
    "f1" / float32,
    "b1" / byte,
    "b2" / byte,
    "b3" / byte,
    "b4" / byte,
    "i1" / int32,
    "f2" / float32,
    "i2" / int32,
    "separator" / int32,
"""
if __name__=="__main__":
    for epv in Path(r"E:\MHW\chunkG0").rglob("*.epv3"):
        epvf = EPVFile(epv)
        for block in epvf.body.blocks:
            for group in block.records:
                #if group.blockParam1.paramU1 != 10:
                #    print(epv)
                #    print(group.blockParam1.paramU1)
                if list(group.paramV) != [0,1,0,0]:
                    print(epv)
                    print(list(group.paramV))
                #print(group.parameterBlock1.paramU0)