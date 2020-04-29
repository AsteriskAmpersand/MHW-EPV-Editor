# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RecordIDs.ui'
#
# Created by: PyQt5 UI code generator 5.7.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(280, 45)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupMetadata = QtWidgets.QVBoxLayout()
        self.groupMetadata.setObjectName("groupMetadata")
        self.groupIDLabel = QtWidgets.QLabel(Form)
        self.groupIDLabel.setObjectName("groupIDLabel")
        self.groupMetadata.addWidget(self.groupIDLabel)
        self.groupID = QtWidgets.QSpinBox(Form)
        self.groupID.setMaximum(65535)
        self.groupID.setObjectName("groupID")
        self.groupMetadata.addWidget(self.groupID)
        self.horizontalLayout_2.addLayout(self.groupMetadata)
        self.recordMetadata = QtWidgets.QHBoxLayout()
        self.recordMetadata.setSpacing(0)
        self.recordMetadata.setObjectName("recordMetadata")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.recordIDLabel = QtWidgets.QLabel(Form)
        self.recordIDLabel.setObjectName("recordIDLabel")
        self.verticalLayout_2.addWidget(self.recordIDLabel)
        self.recordID = QtWidgets.QSpinBox(Form)
        self.recordID.setMaximum(65535)
        self.recordID.setObjectName("recordID")
        self.verticalLayout_2.addWidget(self.recordID)
        self.recordMetadata.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.trailIDLabel = QtWidgets.QLabel(Form)
        self.trailIDLabel.setObjectName("trailIDLabel")
        self.verticalLayout_3.addWidget(self.trailIDLabel)
        self.trailID = QtWidgets.QSpinBox(Form)
        self.trailID.setMinimum(-2147483647)
        self.trailID.setMaximum(2147483647)
        self.trailID.setProperty("value", 0)
        self.trailID.setObjectName("trailID")
        self.verticalLayout_3.addWidget(self.trailID)
        self.recordMetadata.addLayout(self.verticalLayout_3)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.boneIDLabel = QtWidgets.QLabel(Form)
        self.boneIDLabel.setObjectName("boneIDLabel")
        self.verticalLayout_8.addWidget(self.boneIDLabel)
        self.boneID = QtWidgets.QSpinBox(Form)
        self.boneID.setMinimum(-2147483647)
        self.boneID.setMaximum(2147483647)
        self.boneID.setObjectName("boneID")
        self.verticalLayout_8.addWidget(self.boneID)
        self.recordMetadata.addLayout(self.verticalLayout_8)
        self.horizontalLayout_2.addLayout(self.recordMetadata)
        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 3)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupIDLabel.setText(_translate("Form", "Group ID"))
        self.recordIDLabel.setText(_translate("Form", "Record ID"))
        self.trailIDLabel.setText(_translate("Form", "Trail ID"))
        self.boneIDLabel.setText(_translate("Form", "Bone ID"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

