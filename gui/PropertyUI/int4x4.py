# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'int4x4.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(495, 108)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.valName = QtWidgets.QLabel(Form)
        self.valName.setMinimumSize(QtCore.QSize(225, 0))
        self.valName.setObjectName("valName")
        self.horizontalLayout.addWidget(self.valName)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.v00 = QtWidgets.QSpinBox(self.frame_2)
        self.v00.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.v00.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.v00.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.v00.setProperty("showGroupSeparator", False)
        self.v00.setObjectName("v00")
        self.horizontalLayout_2.addWidget(self.v00)
        self.v01 = QtWidgets.QSpinBox(self.frame_2)
        self.v01.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.v01.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.v01.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.v01.setProperty("showGroupSeparator", False)
        self.v01.setObjectName("v01")
        self.horizontalLayout_2.addWidget(self.v01)
        self.v02 = QtWidgets.QSpinBox(self.frame_2)
        self.v02.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.v02.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.v02.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.v02.setProperty("showGroupSeparator", False)
        self.v02.setObjectName("v02")
        self.horizontalLayout_2.addWidget(self.v02)
        self.v03 = QtWidgets.QSpinBox(self.frame_2)
        self.v03.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.v03.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.v03.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.v03.setProperty("showGroupSeparator", False)
        self.v03.setObjectName("v03")
        self.horizontalLayout_2.addWidget(self.v03)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.v10 = QtWidgets.QSpinBox(self.frame_3)
        self.v10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.v10.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.v10.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.v10.setProperty("showGroupSeparator", False)
        self.v10.setObjectName("v10")
        self.horizontalLayout_3.addWidget(self.v10)
        self.v11 = QtWidgets.QSpinBox(self.frame_3)
        self.v11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.v11.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.v11.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.v11.setProperty("showGroupSeparator", False)
        self.v11.setObjectName("v11")
        self.horizontalLayout_3.addWidget(self.v11)
        self.v12 = QtWidgets.QSpinBox(self.frame_3)
        self.v12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.v12.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.v12.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.v12.setProperty("showGroupSeparator", False)
        self.v12.setObjectName("v12")
        self.horizontalLayout_3.addWidget(self.v12)
        self.v13 = QtWidgets.QSpinBox(self.frame_3)
        self.v13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.v13.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.v13.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.v13.setProperty("showGroupSeparator", False)
        self.v13.setObjectName("v13")
        self.horizontalLayout_3.addWidget(self.v13)
        self.verticalLayout.addWidget(self.frame_3)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.v20 = QtWidgets.QSpinBox(self.frame_4)
        self.v20.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.v20.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.v20.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.v20.setProperty("showGroupSeparator", False)
        self.v20.setObjectName("v20")
        self.horizontalLayout_4.addWidget(self.v20)
        self.v21 = QtWidgets.QSpinBox(self.frame_4)
        self.v21.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.v21.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.v21.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.v21.setProperty("showGroupSeparator", False)
        self.v21.setObjectName("v21")
        self.horizontalLayout_4.addWidget(self.v21)
        self.v22 = QtWidgets.QSpinBox(self.frame_4)
        self.v22.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.v22.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.v22.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.v22.setProperty("showGroupSeparator", False)
        self.v22.setObjectName("v22")
        self.horizontalLayout_4.addWidget(self.v22)
        self.v23 = QtWidgets.QSpinBox(self.frame_4)
        self.v23.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.v23.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.v23.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.v23.setProperty("showGroupSeparator", False)
        self.v23.setObjectName("v23")
        self.horizontalLayout_4.addWidget(self.v23)
        self.verticalLayout.addWidget(self.frame_4)
        self.frame_5 = QtWidgets.QFrame(self.frame)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.v30 = QtWidgets.QSpinBox(self.frame_5)
        self.v30.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.v30.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.v30.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.v30.setProperty("showGroupSeparator", False)
        self.v30.setObjectName("v30")
        self.horizontalLayout_5.addWidget(self.v30)
        self.v31 = QtWidgets.QSpinBox(self.frame_5)
        self.v31.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.v31.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.v31.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.v31.setProperty("showGroupSeparator", False)
        self.v31.setObjectName("v31")
        self.horizontalLayout_5.addWidget(self.v31)
        self.v32 = QtWidgets.QSpinBox(self.frame_5)
        self.v32.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.v32.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.v32.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.v32.setProperty("showGroupSeparator", False)
        self.v32.setObjectName("v32")
        self.horizontalLayout_5.addWidget(self.v32)
        self.v33 = QtWidgets.QSpinBox(self.frame_5)
        self.v33.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.v33.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.v33.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.v33.setProperty("showGroupSeparator", False)
        self.v33.setObjectName("v33")
        self.horizontalLayout_5.addWidget(self.v33)
        self.verticalLayout.addWidget(self.frame_5)
        self.horizontalLayout.addWidget(self.frame)

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

