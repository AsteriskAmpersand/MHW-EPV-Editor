# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 03:00:46 2020

@author: AsteriskAmpersand
"""

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import pyqtSignal

class saneQLineEdit(QLineEdit):
    valueChanged = pyqtSignal(object)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.textChanged.connect(self.valueChanged.emit)
