# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EFXPaths.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(378, 131)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.efxPathsGroup = QtWidgets.QGroupBox(Form)
        self.efxPathsGroup.setObjectName("efxPathsGroup")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.efxPathsGroup)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.path0 = saneQLineEdit(self.efxPathsGroup)
        self.path0.setObjectName("path0")
        self.verticalLayout_5.addWidget(self.path0)
        self.path1 = saneQLineEdit(self.efxPathsGroup)
        self.path1.setObjectName("path1")
        self.verticalLayout_5.addWidget(self.path1)
        self.path2 = saneQLineEdit(self.efxPathsGroup)
        self.path2.setObjectName("path2")
        self.verticalLayout_5.addWidget(self.path2)
        self.path3 = saneQLineEdit(self.efxPathsGroup)
        self.path3.setObjectName("path3")
        self.verticalLayout_5.addWidget(self.path3)
        self.horizontalLayout.addWidget(self.efxPathsGroup)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.efxPathsGroup.setTitle(_translate("Form", "EFX Paths"))

from model.lineEditOverride import saneQLineEdit

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

