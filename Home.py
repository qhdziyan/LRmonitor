
import sys
import time
from CheckOrder import CheckOrder
from AccountStatus import AccountStatus
from AccountInfo import AccountInfo
from EAControl import EAControl
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *
import qdarkstyle

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(889, 533)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.AccountStatusButton = QtWidgets.QPushButton(Form)
        self.AccountStatusButton.setObjectName("AccountStatusButton")
        self.horizontalLayout.addWidget(self.AccountStatusButton)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_6 = QtWidgets.QPushButton(Form)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout.addWidget(self.pushButton_6)
        self.pushButton_4 = QtWidgets.QPushButton(Form)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.pushButton_5 = QtWidgets.QPushButton(Form)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout.addWidget(self.pushButton_5)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.AccountStatus = AccountStatus()
        self.verticalLayout.addWidget(self.AccountStatus)
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.AccountStatusButton.setText(_translate("Form", "账号状态"))
        self.pushButton_2.setText(_translate("Form", "跟单信息"))
        self.pushButton_3.setText(_translate("Form", "持仓信息"))
        self.pushButton_6.setText(_translate("Form", "风控设置"))
        self.pushButton_4.setText(_translate("Form", "资金状态"))
        self.pushButton_5.setText(_translate("Form", "EA控制"))
class LRHomeWindow(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(LRHomeWindow, self).__init__(parent)
        self.setupUi(self)
        self.checkinstance = CheckOrder()
        for account in self.checkinstance.SourceAccountList:
            self.checkinstance.InitCurOrders(account)
        self.threadstartslot()
        self.checkinstance.AlertSignal.connect(self.ShowMessage)
        self.AccountInfoWindow = AccountInfo()
        self.pushButton_3.clicked.connect(self.AccountInfoWindow.showMaximized)
        self.EAControlWindow = EAControl()
        self.pushButton_6.clicked.connect(self.EAControlWindow.show)

    # 线程测试开始
    def threadstartslot(self):
        self.work = Thread()
        self.work.trigger.connect(self.deal)  # 线程中的trigger与主类中的方法进行绑定
        self.work.start()  # 开启线程
    # 线程测试停止
    def threadstopslot(self):
        self.work.threadstartflag = False
    # 更新UI方法
    def deal(self):
        #检查新订单
        for account in self.checkinstance.SourceAccountList:
            self.checkinstance.SearchNewOrders(account)
        #检查跟单账户跟单状态
        self.checkinstance.SearchFollowOpenOrders(self.checkinstance.NewOpenTicket)
        self.checkinstance.SearchFollowCloseOrders(self.checkinstance.NewCloseTicket)
    #显示信息
    def ShowMessage(self,contents):
        self.textBrowser.append(contents)
        self.textBrowser.append("-----------------------------------------------------------------------------------------------")


class Thread(QThread):
    trigger = pyqtSignal()#注意pyqtSignal一定要实例到__init__前面
    def __init__(self):
        super(Thread, self).__init__()
        #定义的变量
        self.threadstartflag=True
        self.timecount=0
    #执行耗时操作
    def run(self):
        while self.threadstartflag == True:
            self.trigger.emit()#发送更新GUI的信号
            time.sleep(3)

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    #mainWindow = QtWidgets.QMainWindow()
    ui = LRHomeWindow()
    #ui.setupUi(mainWindow)
    ui.showMaximized()
    #ui.threadstartslot()
    #mainWindow.show()
    sys.exit(app.exec_())
