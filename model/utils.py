# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 06:21:22 2020

@author: AsteriskAmpersand
"""
from PyQt5.QtWidgets import QWidgetItem

def layout_widgets(layout):
   return (layout.itemAt(i).widget() if type(layout.itemAt(i)) is QWidgetItem else layout.itemAt(i) for i in range(layout.count()))

def qlistiter(qobject):
    return (qobject.itemWidget(qobject.item(i)) for i in range(qobject.count()))