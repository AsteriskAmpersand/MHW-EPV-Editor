# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'int4.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(690, 38)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.valName = QtWidgets.QLabel(Form)
        self.valName.setMinimumSize(QtCore.QSize(225, 0))
        self.valName.setObjectName("valName")
        self.horizontalLayout.addWidget(self.valName)
        self.v0 = QtWidgets.QSpinBox(Form)
        self.v0.setMinimum(-127)
        self.v0.setMaximum(127)
        self.v0.setObjectName("v0")
        self.horizontalLayout.addWidget(self.v0)
        self.v1 = QtWidgets.QSpinBox(Form)
        self.v1.setMinimum(-127)
        self.v1.setMaximum(127)
        self.v1.setObjectName("v1")
        self.horizontalLayout.addWidget(self.v1)
        self.v2 = QtWidgets.QSpinBox(Form)
        self.v2.setMinimum(-127)
        self.v2.setMaximum(127)
        self.v2.setObjectName("v2")
        self.horizontalLayout.addWidget(self.v2)
        self.v3 = QtWidgets.QSpinBox(Form)
        self.v3.setMinimum(-127)
        self.v3.setMaximum(127)
        self.v3.setObjectName("v3")
        self.horizontalLayout.addWidget(self.v3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.valName.setText(_translate("Form", "fWaterCustomRefractionTangentNormalBlend"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

