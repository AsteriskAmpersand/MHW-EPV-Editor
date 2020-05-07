# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'InteractiveConsole.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(707, 661)
        Dialog.setModal(True)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(Dialog)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.Output = QtWidgets.QTextEdit(self.splitter)
        self.Output.setMinimumSize(QtCore.QSize(0, 0))
        self.Output.setAcceptDrops(False)
        self.Output.setUndoRedoEnabled(False)
        self.Output.setReadOnly(True)
        self.Output.setAcceptRichText(True)
        self.Output.setObjectName("Output")
        self.Input = QtWidgets.QTextEdit(self.splitter)
        self.Input.setReadOnly(False)
        self.Input.setObjectName("Input")
        self.horizontalLayout.addWidget(self.splitter)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

