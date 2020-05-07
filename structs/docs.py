# -*- coding: utf-8 -*-
"""
Created on Wed May  6 16:12:56 2020

@author: AsteriskAmpersand
"""


from structs.epv import group,record,parameterBlock1,parameterBlock2,epvc

print("Group:")
for prop in group.subcons:
    print("\t%s:%s"%(prop.name,prop.docs))
    
print("Record:")
for prop in record.subcons:
    print("\t%s:%s"%(prop.name,prop.docs))
print("\tParameter Block 1:")
for prop in parameterBlock1.subcons:
    print("\t\t%s:%s"%(prop.name,prop.docs))
print("\tParameter Block 2:")
for prop in parameterBlock2.subcons:
    print("\t\t%s:%s"%(prop.name,prop.docs))
    
print("EFX Slot:")
for prop in epvc.subcons:
    print("\t%s:%s"%(prop.name,prop.docs))