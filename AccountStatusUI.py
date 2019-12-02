# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AccountStatusUI.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui,QtWidgets,Qt


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        #self.pushButton = QtWidgets.QPushButton(Form)
        #self.pushButton.setObjectName("pushButton")
        self.radio_1 = QtWidgets.QRadioButton("显示所有账号状态")
        self.radio_1.setChecked(True)
        self.radio_2 = QtWidgets.QRadioButton("显示错误账号状态")
        self.horizontalLayout.addWidget(self.radio_1)
        #self.pushButton_2 = QtWidgets.QPushButton(Form)
        #self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.radio_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)

        QtCore.QMetaObject.connectSlotsByName(Form)





    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.radio_1.setText(_translate("Form", "显示所有账户状态"))
        self.radio_2.setText(_translate("Form", "显示错误账户状态"))


