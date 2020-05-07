# -*- coding: utf-8 -*-
"""
Created on Mon May  4 18:44:59 2020

@author: AsteriskAmpersand
"""

from singleton_decorator import singleton
from generic.UndoRedoController import InvertingUndoRedoController,DummyRedoController
from model.utils import qlistiter,layout_widgets
from model.EPV import EPVGroup
from model.EPV import EPVRecord
from generic.InteractiveConsole import InteractiveConsole
from structs.epv import record,epvc,parameterBlock2,parameterBlock1
   
class __ScriptMiniEngine__():
    def __init__(self):
        self.running = False
        self.UndoRedoController = DummyRedoController()
    #disable all indices when starting to avoid having to update views
    def start(self,app):
        self.app = app
        self.UndoRedoController.startRecording()
        self.running = True
        self.files = [ScriptEPV(self,self.app.ui.fileTabs.widget(ix).EPVModel ) for ix in range(self.app.ui.fileTabs.count())]
    def stop(self):
        self.running = False
        self.UndoRedoController.stopRecording()
        #Refresh Views
    def openFile(self,path):
        self.app.openFile(path)
        epv = ScriptEPV(self,self.app.ui.fileTabs.currentWidget())
        self.files.append(epv)
        return epv        
    def files(self):
        return self.files
    def current(self):
        return self.files[self.app.ui.fileTabs.currentWidget()]
    def interactiveMode(self,varDict):
        interactiveConsole = InteractiveConsole(varDict)
        interactiveConsole.exec()
    #def undo(self):
    #    self.UndoRedoController.undo()
    #def redo(self):
    #    self.UndoRedoController.redo()
    #include undoer stack

mse = __ScriptMiniEngine__()

class ScriptMetaClass():
    subcontainerName = ""
    primitiveName = ""
    primitiveType = None
    childrenType = None
    insertOperation = None
    removeOperation = None
    properties = {}
    omitted = []
    def __init__(self,parent=None,primitive=None):

        self.parent = parent
        if primitive is None:
            if self.primitiveType is not None:
                self.primitiveType(self.parent)
        setattr(self,self.primitiveName,primitive)
        setattr(self,self.subcontainerName,
                [self.childrenType(self,subelement) for subelement in primitive])
    def insertOperation(self,subelement,position):
        raise NotImplementedError()
    def removeOperation(self,position):
        raise NotImplementedError()
    def unimplemented(self,*kwargs):
        raise NotImplementedError("Function not implemented for class %s"%type(self).__name__)
    def Subcontainer(self):
        return getattr(self,self.subcontainerName)
    def AddSubelement(self,subelement = None, position = None):
        if position is None:
            position = len(getattr(self,self.subcontainerName))
        if type(subelement) is not self.childrenType:
            raise ValueError("Inserting Non %s Object: %s"%(self.childrenType.__name__,type(subelement)))
        mse.UndoRedoController.recordEvent(self.RemoveSubelement,(position))
        getattr(self,self.subcontainerName)[position:position] = [subelement]
        self.insertOperation(subelement,position)
    def RemoveSubelement(self,index):
        mse.UndoRedoController.recordEvent(self.AddSubelement,(self.GetSubelement(index),index))
        getattr(self,self.subcontainerName)[index:index+1] = []
        self.removeOperation(index)
    def SetParent(self,newparent):
        mse.UndoRedoController.recordEvent(self.SetParent,(self.parent))
        self.parent = newparent
        getattr(self,self.primitiveName).setParent(newparent)
    def GetSubelement(self,index):
        return getattr(self,self.subcontainerName)[index]
    def SetSubelement(self,index,subelement):
        if type(subelement) is not self.childrenType:
            raise ValueError("Setting Non %s Object: %s"%(self.childrenType.__name__,type(subelement)))
        mse.UndoRedoController.recordEvent(self.SetSubelement,(index,self.GetSubelement(index)))
        subelement.SetParent(self)
        
        
    def GetProperty(self,prop):
        if prop in self.properties:
            return getattr(self,self.primitiveName).__getattribute__(self.properties[prop])
        else:
            raise ValueError("%s is not a property of EPV %s. %s."%
                             (prop,type(self).__name__,",".join(self.properties.keys())))
    def SetProperty(self,prop,value):
        if prop in self.properties:
            mse.UndoRedoController.recordEvent(self.SetProperty,(prop,self.GetProperty(prop)))
            setattr(getattr(self,self.primitiveName),self.properties[prop],value)
        else:
            raise ValueError("%s is not a property of EPV %s. %s"%
                             (prop,type(self).__name__,",".join(self.properties.keys())))

    def __iter__(self):
        return iter(getattr(self,self.subcontainerName))
    def __len__(self):
        return len(getattr(self,self.subcontainerName))
    def __getitem__(self,i):
        if type(i) is int:
            return self.GetSubelement(i)
        elif type(i) is str:
            return self.GetProperty(i)
        else:
            raise TypeError("Access index can only be integers for positional access and string for accessing properties for scripting types.")
    def __setitem__(self,i,value):
        if type(i) is int:
            return self.SetSubelement(i,value)
        elif type(i) is str:
            return self.SetProperty(i,value)
        else:
            raise TypeError("Setting index can only be integers for positional access and string for accessing properties for scripting types.")

        
class ScriptEPVC():
    primitiveName="epvc"
    def __init__(self,parent=None,primitive=None):
        self.parent = parent
        if primitive is None:
            raise ValueError("Content of EPVC Invalid")
        setattr(self,self.primitiveName,primitive)
    properties = {prop.name : prop.name for prop in epvc.subcons}
    GetProperty = ScriptMetaClass.GetProperty
    SetProperty = ScriptMetaClass.SetProperty
    def SetParent(self,*kwargs):pass
    def __getitem__(self,i):
        if type(i) is str:
            return self.GetProperty(i)
        else:
            raise TypeError("EFX Slot only allows access to named properties. %s."%(','.join(self.properties.keys())))
    def __setitem__(self,i,value):
        if type(i) is str:
            return self.SetProperty(i,value)
        else:
            raise TypeError("EFX Slot only allows setting to named properties. %s."%(','.join(self.properties.keys())))

class ScriptRecord(ScriptMetaClass):
    subcontainerName = "epvc"
    primitiveName="record"
    primitiveType = EPVRecord
    childrenType = ScriptEPVC
    properties = {"paths":"packed_path",**{prop.name:prop.name for prop in record.subcons if "parameterBlock" not in prop.name}}
    
    EFXS = ScriptMetaClass.Subcontainer
    AddSubelement = ScriptMetaClass.unimplemented
    RemoveSubelement = ScriptMetaClass.unimplemented
    GetEFXS = ScriptMetaClass.GetSubelement
    SetEFXS = ScriptMetaClass.SetSubelement
    
    pb1 = {prop.name:prop.name for prop in parameterBlock1.subcons}
    pb2 = {prop.name:prop.name for prop in parameterBlock2.subcons}
    
    def GetProperty(self,prop):
        if prop in self.pb1:
            return getattr(self,self.primitiveName).parameterBlock1.__getattr__(self.properties[prop])
        elif prop in self.pb2:
            return getattr(self,self.primitiveName).parameterBlock2.__getattr__(self.properties[prop])
        else:
            return super().GetProperty(self,prop)
    def SetProperty(self,prop,value):
        if prop in self.pb1:
            mse.UndoRedoController.recordEvent(self.SetProperty,(prop,self.GetProperty(prop)))
            setattr(getattr(self,self.primitiveName).parameterBlock1,self.properties[prop],value)
        if prop in self.pb2:
            mse.UndoRedoController.recordEvent(self.SetProperty,(prop,self.GetProperty(prop)))
            setattr(getattr(self,self.primitiveName).parameterBlock2,self.properties[prop],value)
        else:
            super().SetProperty(self,prop,value)
    
class ScriptGroup(ScriptMetaClass):
    subcontainerName = "records"
    primitiveName="group"
    primitiveType = EPVGroup
    childrenType = ScriptRecord
    properties = {"groupID":"groupID"}
    
    def insertOperation(self,subelement,position):
        self.epv._insertRecord(self.group,subelement.record,position)
    def removeOperation(self,position):
        self.epv._removeRecord(self.group,position)
    
    Records = ScriptMetaClass.Subcontainer
    AddRecord = ScriptMetaClass.AddSubelement
    RemoveRecord = ScriptMetaClass.RemoveSubelement
    GetRecord = ScriptMetaClass.GetSubelement
    SetRecord = ScriptMetaClass.SetSubelement

class ScriptEPV(ScriptMetaClass):
    subcontainerName = "groups"
    primitiveName="epv"
    primitiveType = None #EPV
    childrenType = ScriptGroup
    properties = {}
    
    def insertOperation(self,subelement,position):
        self.epv._insertGroup(subelement.group,position)
    def removeOperation(self,position):
        self.epv._removeGroup(position)
    Groups = ScriptMetaClass.Subcontainer
    AddGroup = ScriptMetaClass.AddSubelement
    RemoveGroup = ScriptMetaClass.RemoveSubelement
    GetGroup = ScriptMetaClass.GetSubelement
    SetGroup = ScriptMetaClass.SetSubelement
    
    GetProperty = ScriptMetaClass.unimplemented
    SetProperty = ScriptMetaClass.unimplemented