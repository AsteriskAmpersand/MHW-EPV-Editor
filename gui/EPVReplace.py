# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EPVReplace.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(648, 259)
        Dialog.setModal(True)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.ReplaceForm = ReplaceForm(Dialog)
        self.ReplaceForm.setMinimumSize(QtCore.QSize(220, 185))
        self.ReplaceForm.setObjectName("ReplaceForm")
        self.verticalLayout_7.addWidget(self.ReplaceForm)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ApplyToAll = QtWidgets.QCheckBox(Dialog)
        self.ApplyToAll.setObjectName("ApplyToAll")
        self.horizontalLayout_2.addWidget(self.ApplyToAll)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Replace = QtWidgets.QPushButton(Dialog)
        self.Replace.setObjectName("Replace")
        self.horizontalLayout.addWidget(self.Replace)
        self.Customize = QtWidgets.QPushButton(Dialog)
        self.Customize.setObjectName("Customize")
        self.horizontalLayout.addWidget(self.Customize)
        self.Cancel = QtWidgets.QPushButton(Dialog)
        self.Cancel.setObjectName("Cancel")
        self.horizontalLayout.addWidget(self.Cancel)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_7.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.ApplyToAll.setText(_translate("Dialog", "Apply to all Files"))
        self.Replace.setText(_translate("Dialog", "Replace"))
        self.Customize.setText(_translate("Dialog", "Customize Replace"))
        self.Cancel.setText(_translate("Dialog", "Cancel"))

from replace.ReplaceSelector import ReplaceForm

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

