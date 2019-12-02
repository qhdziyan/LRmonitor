import sys
import time
from AccountStatusUI import Ui_Form
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pymysql
import qdarkstyle



class AccountStatus(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.threadstartslot()
        self.show()
    # 线程测试开始
    def threadstartslot(self):
        self.work = Thread()
        self.work.trigger.connect(self.loaddata)  # 线程中的trigger与主类中的方法进行绑定
        self.radio_1.toggled.connect(self.loaddata)
        self.radio_2.toggled.connect(self.loaddata)
        self.work.start()  # 开启线程
    # 线程测试停止
    def threadstopslot(self):
        self.work.threadstartflag = False
    def clear(self):
        pass
    # 更新UI方法
    def loaddata(self):
        db = pymysql.connect("localhost", "root", "Lianrun!@#", "posorders")
        cursor = db.cursor()
        cursor.execute("SELECT * from account.accountstatus")
        data = cursor.fetchall()
        row = cursor.rowcount  # 取得记录个数，用于设置表格的行数
        vol = len(data[0])  # 取得字段数，用于设置表格的列数
        cursor.close()
        db.close()

        errorlist = []
        Nerrorlist=[]
        AllList=[]
        for i in range(row):
            AllList.append(data[i])
            for j in range(vol):
                if (j == 1 or j == 2 or j == 4 or j == 5 or j == 6 or j == 7 or j == 8) and data[i][j]!= 1:
                    errorlist.append(data[i])
                    break
                elif j == 3 and time.time() - (data[i][j] - 28800) > 30:
                    errorlist.append(data[i])
                    break
        Nerrorlist=[ i for i in AllList if i not in errorlist ]
        AllList=errorlist+Nerrorlist
        titles = ['账号', 'MT4连接状态', '客户端繁忙', 'EA当前时间', ' 订单数量', '允许交易', 'DLLs', '库文件', '允许EA','报警操作']
        if self.radio_2.isChecked():
            self.tableWidget.setRowCount(len(errorlist))
            if errorlist!=[]:
                self.tableWidget.setColumnCount(len(errorlist[0])-1)
            self.tableWidget.setHorizontalHeaderLabels(titles)
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            for i in range(len(errorlist)):
                for j in range(len(errorlist[i])):
                    if j < len(errorlist[i]):
                        if j==3:
                            temp_data=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(errorlist[i][j]-60*60*8))
                        elif j==0:
                            temp_data=errorlist[i][j]
                        else:
                            if errorlist[i][j]==1:
                                temp_data = "正常" # 临时记录，不能直接插入表格
                            else:
                                temp_data="异常"
                        showdata = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                        if (j==1 or j==2 or j==4 or j==5 or j==6 or j==7 or j==8) and temp_data!="正常" and errorlist[i][9]!=1:
                            showdata.setBackground(QBrush(QColor(255,0,0)))
                        if j == 3 and time.time()-(errorlist[i][j]-28800)>30 and errorlist[i][9]!=1:
                            showdata.setBackground(QBrush(QColor(255, 0, 0)))
                        self.tableWidget.setItem(i, j, showdata)
                    if j==len(AllList[i])-2:
                        self.tableWidget.setCellWidget(i, j, self.buttonForRow(str(AllList[i][0]),str(AllList[i][9])))
        if self.radio_1.isChecked():
            self.tableWidget.setRowCount(len(AllList))
            if AllList!=[]:
                self.tableWidget.setColumnCount(len(AllList[0])-1)
            self.tableWidget.setHorizontalHeaderLabels(titles)
            self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            for i in range(len(AllList)):
                for j in range(len(AllList[i])):
                    if j<len(AllList[i]):
                        if j==3:
                            temp_data=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(AllList[i][j]-60*60*8))
                        elif j==0:
                            temp_data=str(AllList[i][j])
                        else:
                            if AllList[i][j]==1:
                                temp_data = "正常"  # 临时记录，不能直接插入表格
                            else:
                                temp_data="异常"
                        showdata = QTableWidgetItem(temp_data)  # 转换后可插入表格
                        if (j==1 or j==2 or j==4 or j==5 or j==6 or j==7 or j==8) and temp_data!="正常"  and AllList[i][9]!=1:
                            showdata.setBackground(QBrush(QColor(255,0,0)))
                        if j == 3 and time.time()-(AllList[i][j]-28800)>30 and AllList[i][9]!=1:
                            showdata.setBackground(QBrush(QColor(255, 0, 0)))
                        self.tableWidget.setItem(i, j, showdata)
                    if j==len(AllList[i])-2:
                        self.tableWidget.setCellWidget(i, j, self.buttonForRow(str(AllList[i][0]),str(AllList[i][9])))

        # 列表内添加按钮
    def buttonForRow(self,id,alert):

            widget = QWidget()
            # 清除警报
            viewBtn = QPushButton('清除警报')
            viewBtn.setStyleSheet(''' text-align : center;
                                      background-color : DarkSeaGreen;
                                      height : 30px;
                                      border-style: outset;
                                      font : 13px; ''')
            viewBtn.clicked.connect(lambda: self.clearAlert(id,alert))
            #恢复警报
            viewBtn1 = QPushButton('恢复警报')
            viewBtn1.setStyleSheet(''' text-align : center;
                                                  background-color : Red;
                                                  height : 30px;
                                                  border-style: outset;
                                                  font : 13px; ''')
            viewBtn1.clicked.connect(lambda: self.recoveryAlert(id, alert))
            viewBtn.clicked.connect(self.loaddata)
            viewBtn1.clicked.connect(self.loaddata)
            # 删除
            deleteBtn = QPushButton('删除账户')
            deleteBtn.setStyleSheet(''' text-align : center;
                                        background-color : LightCoral;
                                        height : 30px;
                                        border-style: outset;
                                        font : 13px; ''')
            deleteBtn.clicked.connect(lambda:self.deleteTable(id))
            deleteBtn.clicked.connect(self.loaddata)
            hLayout = QHBoxLayout()
            if alert!="1":
                hLayout.addWidget(viewBtn)
            else:
                hLayout.addWidget(viewBtn1)

            hLayout.addWidget(deleteBtn)
            hLayout.setContentsMargins(5, 2, 5, 2)
            widget.setLayout(hLayout)
            return widget
    def updateTable(self,id):
        print("updateTable",id)
    def clearAlert(self,id,alert):
        db = pymysql.connect("localhost", "root", "Lianrun!@#", "posorders")
        cursor = db.cursor()
        cursor.execute("UPDATE account.accountstatus SET isalert = 1 WHERE accountid = %s" %(id))
        db.commit()
        cursor.close()
        db.close()
    def recoveryAlert(self,id,alert):
        db = pymysql.connect("localhost", "root", "Lianrun!@#", "posorders")
        cursor = db.cursor()
        cursor.execute("UPDATE account.accountstatus SET isalert = 0 WHERE accountid = %s" %(id))
        db.commit()
        cursor.close()
        db.close()
    def deleteTable(self,id):
        db = pymysql.connect("localhost", "root", "Lianrun!@#", "posorders")
        cursor = db.cursor()
        cursor.execute("delete from account.accountstatus WHERE accountid = %s" % (id))
        db.commit()
        cursor.close()
        db.close()
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
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    w = AccountStatus()
    app.exec_()