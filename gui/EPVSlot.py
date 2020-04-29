# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EPVSlot.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(358, 40)
        Form.setMinimumSize(QtCore.QSize(0, 40))
        Form.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setContentsMargins(0, 2, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.efxslot = QtWidgets.QSpinBox(Form)
        self.efxslot.setMaximum(255)
        self.efxslot.setObjectName("efxslot")
        self.verticalLayout.addWidget(self.efxslot)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.colorTool = QtWidgets.QToolButton(Form)
        self.colorTool.setText("")
        self.colorTool.setObjectName("colorTool")
        self.horizontalLayout.addWidget(self.colorTool)
        self.alpha = QtWidgets.QDoubleSpinBox(Form)
        self.alpha.setDecimals(1)
        self.alpha.setMaximum(100.0)
        self.alpha.setProperty("value", 100.0)
        self.alpha.setObjectName("alpha")
        self.horizontalLayout.addWidget(self.alpha)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.saturation = QtWidgets.QDoubleSpinBox(Form)
        self.saturation.setDecimals(3)
        self.saturation.setMinimum(-99.99)
        self.saturation.setSingleStep(0.001)
        self.saturation.setProperty("value", 1.0)
        self.saturation.setObjectName("saturation")
        self.verticalLayout_3.addWidget(self.saturation)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.size = QtWidgets.QSpinBox(Form)
        self.size.setMinimum(-999)
        self.size.setMaximum(999)
        self.size.setProperty("value", 1)
        self.size.setObjectName("size")
        self.verticalLayout_4.addWidget(self.size)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_5.addWidget(self.label_5)
        self.frequency = QtWidgets.QDoubleSpinBox(Form)
        self.frequency.setDecimals(3)
        self.frequency.setMinimum(-99.99)
        self.frequency.setProperty("value", 1.0)
        self.frequency.setObjectName("frequency")
        self.verticalLayout_5.addWidget(self.frequency)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.horizontalLayout_2.setStretch(0, 5)
        self.horizontalLayout_2.setStretch(1, 5)
        self.horizontalLayout_2.setStretch(2, 5)
        self.horizontalLayout_2.setStretch(3, 5)
        self.horizontalLayout_2.setStretch(4, 5)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "EFX Slot"))
        self.label_2.setText(_translate("Form", "Color - Alpha"))
        self.label_3.setText(_translate("Form", "Saturation"))
        self.label_4.setText(_translate("Form", "Size"))
        self.label_5.setText(_translate("Form", "Frequency"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
