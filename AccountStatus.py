import sys
from AccountStatusUI import Ui_Form
from PyQt5.Qt import QWidget, QApplication, QTableWidgetItem
import pymysql



class myform(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton_2.clicked.connect(self.clear)
        self.pushButton.clicked.connect(self.load)
        self.show()

    def clear(self):
        pass

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


app = QApplication(sys.argv)
w = myform()
app.exec_()