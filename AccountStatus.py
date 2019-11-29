import sys
import time
from AccountStatusUI import Ui_Form
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pymysql



class myform(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.clear)
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
        cursor.execute("SELECT * from account.accountstatus")
        data = cursor.fetchall()
        row = cursor.rowcount  # 取得记录个数，用于设置表格的行数
        vol = len(data[0])  # 取得字段数，用于设置表格的列数
        cursor.close()
        db.close()

        self.tableWidget.setRowCount(row)
        self.tableWidget.setColumnCount(vol)

        for i in range(row):
            for j in range(vol):
                temp_data = data[i][j]  # 临时记录，不能直接插入表格
                showdata = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                self.tableWidget.setItem(i, j, showdata)
class Thread(QThread):
    trigger = pyqtSignal(str)#注意pyqtSignal一定要实例到__init__前面
    def __init__(self):
        super(Thread, self).__init__()
        #定义的变量
        self.threadstartflag=True
        self.timecount=0
    #执行耗时操作
    def run(self):
        while self.threadstartflag == True:
            self.trigger.emit(u"计时%d"%self.timecount)#发送更新GUI的信号
            self.timecount+=1
            time.sleep(1)

app = QApplication(sys.argv)
w = myform()
app.exec_()