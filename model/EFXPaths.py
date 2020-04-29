# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 06:34:47 2020

@author: AsteriskAmpersand
"""

from model.RecordProperties import RecordProperties
from gui.EFXPaths import Ui_Form
from PyQt5.QtCore import pyqtSignal

class EFXPaths(RecordProperties):        
    ui_form = Ui_Form
    @property
    def path0(self):return self.ui.path0.text()
    @path0.setter
    def path0(self,value):self.ui.path0.setText(value)
    @property
    def path1(self):return self.ui.path1.text()
    @path1.setter
    def path1(self,value):self.ui.path1.setText(value)
    @property
    def path2(self):return self.ui.path2.text()
    @path2.setter
    def path2(self,value):self.ui.path2.setText(value)
    @property
    def path3(self):return self.ui.path3.text()
    @path3.setter
    def path3(self,value):self.ui.path3.setText(value)
    properties = ["path0","path1","path2","path3"]