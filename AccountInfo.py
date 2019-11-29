import sys
import time
from AccountStatusUI import Ui_Form
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pymysql

class AccountInfo(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.threadstartslot()
        self.show()
    # 线程测试开始
    def threadstartslot(self):
        self.work = Thread()
        self.work.trigger.connect(self.load)  # 线程中的trigger与主类中的方法进行绑定
        self.work.start()  # 开启线程
    # 线程测试停止
    def threadstopslot(self):
        self.work.threadstartflag = False
    def clear(self):
        pass
    # 更新UI方法
    def load(self):
        db = pymysql.connect("localhost", "root", "Lianrun!@#", "posorders")
        cursor = db.cursor()
        cursor.execute("SELECT * from account.AccountInfo")
        data = cursor.fetchall()
        row = cursor.rowcount  # 取得记录个数，用于设置表格的行数
        vol = len(data[0])  # 取得字段数，用于设置表格的列数
        cursor.close()
        db.close()
        print(data[0])
        titles = ['账号', '余额', '入金', '出金', ' 已用保证金', '可用保证金', '保证金比率','账户盈利']
        self.tableWidget.setRowCount(row)
        self.tableWidget.setColumnCount(vol)
        self.tableWidget.setHorizontalHeaderLabels(titles)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i in range(row):
            for j in range(vol):
                temp_data = data[i][j]  # 临时记录，不能直接插入表格
                showdata = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                self.tableWidget.setItem(i, j, showdata)
class Thread(QThread):
    trigger = pyqtSignal()#注意pyqtSignal一定要实例到__init__前面
    def __init__(self):
        super(Thread, self).__init__()
        #定义的变量
        self.threadstartflag=True
    #执行耗时操作
    def run(self):
        while self.threadstartflag == True:
            self.trigger.emit()#发送更新GUI的信号
            time.sleep(5)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = AccountInfo()
    w.showMaximized()
    app.exec_()