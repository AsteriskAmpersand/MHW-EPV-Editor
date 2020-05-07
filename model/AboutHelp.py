# -*- coding: utf-8 -*-
"""
Created on Wed May  6 17:03:14 2020

@author: AsteriskAmpersand
"""

#from gui.HelpAbout import Ui_Dialog as Help_Dialog
from PyQt5.QtWidgets import QDialog

class AboutHelp(QDialog):
    def __init__(self, *args):
        super().__init__(*args)

        #self.ui = Help_Dialog()
        #self.ui.setupUi(self)
        
        self.show()