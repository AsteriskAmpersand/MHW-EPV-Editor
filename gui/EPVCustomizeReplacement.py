# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EPVCustomizeReplacement.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(642, 660)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(Dialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.Before = QtWidgets.QListView(self.splitter)
        self.Before.setObjectName("Before")
        self.After = QtWidgets.QListView(self.splitter)
        self.After.setObjectName("After")
        self.verticalLayout.addWidget(self.splitter)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.Reset = QtWidgets.QPushButton(Dialog)
        self.Reset.setObjectName("Reset")
        self.horizontalLayout.addWidget(self.Reset)
        self.Remove = QtWidgets.QPushButton(Dialog)
        self.Remove.setObjectName("Remove")
        self.horizontalLayout.addWidget(self.Remove)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.Accept = QtWidgets.QPushButton(Dialog)
        self.Accept.setObjectName("Accept")
        self.horizontalLayout.addWidget(self.Accept)
        self.Cancel = QtWidgets.QPushButton(Dialog)
        self.Cancel.setObjectName("Cancel")
        self.horizontalLayout.addWidget(self.Cancel)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 200)
        self.actionUndo = QtWidgets.QAction(Dialog)
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QtWidgets.QAction(Dialog)
        self.actionRedo.setObjectName("actionRedo")
        self.actionDelete = QtWidgets.QAction(Dialog)
        self.actionDelete.setObjectName("actionDelete")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Reset.setText(_translate("Dialog", "Reset"))
        self.Remove.setText(_translate("Dialog", "Remove"))
        self.Accept.setText(_translate("Dialog", "Accept"))
        self.Cancel.setText(_translate("Dialog", "Cancel"))
        self.actionUndo.setText(_translate("Dialog", "Undo"))
        self.actionUndo.setShortcut(_translate("Dialog", "Ctrl+Z"))
        self.actionRedo.setText(_translate("Dialog", "Redo"))
        self.actionRedo.setShortcut(_translate("Dialog", "Ctrl+Y"))
        self.actionDelete.setText(_translate("Dialog", "Delete"))
        self.actionDelete.setShortcut(_translate("Dialog", "Del"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

