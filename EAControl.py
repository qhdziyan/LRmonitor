import sys
import time
from EAControlUi import Ui_Dialog
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pymysql

class EAControl(QWidget, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #self.show()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = EAControl()
    app.exec_()