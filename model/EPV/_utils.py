# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 00:50:07 2020

@author: AsteriskAmpersand
"""
from inspect import getmembers, isfunction

from model.EPV import _EPVUndo as E
from model.EPV import _EPVEditOperations as O
from model.EPV import _EPVCopyStack as C
print("\tfrom ._EPVEditOperations import ("+','.join(map(lambda x: x[0],getmembers(O, isfunction)))+")")
print("\tfrom ._EPVUndo import ("+','.join(map(lambda x: x[0],getmembers(E, isfunction)))+")")
print("\tfrom ._EPVCopyStack import ("+','.join(map(lambda x: x[0],getmembers(C, isfunction)))+")")