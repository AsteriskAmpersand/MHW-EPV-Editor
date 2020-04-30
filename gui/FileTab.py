# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FileTab.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(663, 527)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(663, 527))
        Form.setBaseSize(QtCore.QSize(500, 500))
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.splitter_2 = QtWidgets.QSplitter(Form)
        self.splitter_2.setMinimumSize(QtCore.QSize(538, 482))
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setMinimumSize(QtCore.QSize(481, 341))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.recordBrowser = QtWidgets.QTreeView(self.splitter)
        self.recordBrowser.setMinimumSize(QtCore.QSize(237, 341))
        self.recordBrowser.setAcceptDrops(True)
        self.recordBrowser.setDragEnabled(True)
        self.recordBrowser.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.recordBrowser.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.recordBrowser.setHeaderHidden(True)
        self.recordBrowser.setObjectName("recordBrowser")
        self.frame = QtWidgets.QFrame(self.splitter)
        self.frame.setMinimumSize(QtCore.QSize(400, 341))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.RecordIDs = RecordIDs(self.frame)
        self.RecordIDs.setMinimumSize(QtCore.QSize(380, 45))
        self.RecordIDs.setObjectName("RecordIDs")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.RecordIDs)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_7.addWidget(self.RecordIDs)
        self.efxSlotGroup = QtWidgets.QGroupBox(self.frame)
        self.efxSlotGroup.setObjectName("efxSlotGroup")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.efxSlotGroup)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.efxSlots = QtWidgets.QListWidget(self.efxSlotGroup)
        self.efxSlots.setMinimumSize(QtCore.QSize(360, 0))
        self.efxSlots.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.efxSlots.setObjectName("efxSlots")
        self.verticalLayout_4.addWidget(self.efxSlots)
        self.verticalLayout_7.addWidget(self.efxSlotGroup)
        self.efxPathsGroup = EFXPaths(self.frame)
        self.efxPathsGroup.setMinimumSize(QtCore.QSize(380, 131))
        self.efxPathsGroup.setObjectName("efxPathsGroup")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.efxPathsGroup)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_7.addWidget(self.efxPathsGroup)
        self.recordPropertiesGroup = QtWidgets.QGroupBox(self.splitter_2)
        self.recordPropertiesGroup.setMinimumSize(QtCore.QSize(482, 133))
        self.recordPropertiesGroup.setObjectName("recordPropertiesGroup")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.recordPropertiesGroup)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.splitter_3 = QtWidgets.QSplitter(self.recordPropertiesGroup)
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.recordPropertiesL = QtWidgets.QListWidget(self.splitter_3)
        self.recordPropertiesL.setObjectName("recordPropertiesL")
        self.recordPropertiesR = QtWidgets.QListWidget(self.splitter_3)
        self.recordPropertiesR.setObjectName("recordPropertiesR")
        self.horizontalLayout_4.addWidget(self.splitter_3)
        self.verticalLayout_6.addWidget(self.splitter_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_6)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.efxSlotGroup.setTitle(_translate("Form", "EFX Slots"))
        self.recordPropertiesGroup.setTitle(_translate("Form", "Record Properties"))

from model.EFXPaths import EFXPaths
from model.RecordIDs import RecordIDs

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

