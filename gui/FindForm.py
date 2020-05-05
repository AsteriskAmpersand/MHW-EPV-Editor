# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FindForm.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(484, 481)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Matches = QtWidgets.QListView(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Matches.sizePolicy().hasHeightForWidth())
        self.Matches.setSizePolicy(sizePolicy)
        self.Matches.setObjectName("Matches")
        self.verticalLayout.addWidget(self.Matches)
        self.FindForm = FindForm(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FindForm.sizePolicy().hasHeightForWidth())
        self.FindForm.setSizePolicy(sizePolicy)
        self.FindForm.setMinimumSize(QtCore.QSize(238, 148))
        self.FindForm.setMaximumSize(QtCore.QSize(16777215, 148))
        self.FindForm.setObjectName("FindForm")
        self.verticalLayout.addWidget(self.FindForm)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ApplyToAll = QtWidgets.QCheckBox(Dialog)
        self.ApplyToAll.setObjectName("ApplyToAll")
        self.horizontalLayout_2.addWidget(self.ApplyToAll)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.FindNext = QtWidgets.QPushButton(Dialog)
        self.FindNext.setObjectName("FindNext")
        self.horizontalLayout.addWidget(self.FindNext)
        self.FindAll = QtWidgets.QPushButton(Dialog)
        self.FindAll.setObjectName("FindAll")
        self.horizontalLayout.addWidget(self.FindAll)
        self.Cancel = QtWidgets.QPushButton(Dialog)
        self.Cancel.setObjectName("Cancel")
        self.horizontalLayout.addWidget(self.Cancel)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.ApplyToAll.setText(_translate("Dialog", "Apply to all Files"))
        self.FindNext.setText(_translate("Dialog", "Find Next"))
        self.FindAll.setText(_translate("Dialog", "Find All"))
        self.Cancel.setText(_translate("Dialog", "Cancel"))

from replace.FindSelector import FindForm

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

