import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import *
import qdarkstyle
from SignIn import SignInWidget
from SignUp import SignUpWidget
import sip

from Home import LRHomeWindow
from changePasswordDialog import changePasswordDialog


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.widget = SignInWidget()
        self.resize(900, 600)
        self.setWindowTitle("链润科技风控管理系统")
        self.setCentralWidget(self.widget)

        bar = self.menuBar()
        self.Menu = bar.addMenu("菜单栏")

        #self.signUpAction = QAction("注册", self)
        #self.changePasswordAction =QAction("修改密码",self)
        #self.signInAction = QAction("登录", self)
        self.quitSignInAction = QAction("退出登录", self)

        self.quitAction = QAction("退出", self)
        #self.Menu.addAction(self.signUpAction)
        #self.Menu.addAction(self.changePasswordAction)

        #self.Menu.addAction(self.signInAction)
        #self.Menu.addAction(self.quitSignInAction)
        self.Menu.addAction(self.quitAction)
        #self.signUpAction.setEnabled(True)
        #self.changePasswordAction.setEnabled(True)
        #self.signInAction.setEnabled(False)
        self.quitSignInAction.setEnabled(False)

        self.widget.signin_signal[str].connect(self.SignIn)
        self.Menu.triggered[QAction].connect(self.menuTriggered)


    def SignIn(self, studentId):
        sip.delete(self.widget)
        self.widget = LRHomeWindow()
        self.setCentralWidget(self.widget)
        #self.changePasswordAction.setEnabled(False)
        #self.signUpAction.setEnabled(True)
        #self.signInAction.setEnabled(False)
        self.quitSignInAction.setEnabled(True)

    def menuTriggered(self, q):
        if(q.text()=="修改密码"):
            changePsdDialog=changePasswordDialog(self)
            changePsdDialog.show()
            changePsdDialog.exec_()
        if (q.text() == "注册"):
            sip.delete(self.widget)
            self.widget = SignUpWidget()
            self.setCentralWidget(self.widget)
            self.widget.student_signup_signal[str].connect(self.studentSignIn)
            self.signUpAction.setEnabled(False)
            self.changePasswordAction.setEnabled(True)
            self.signInAction.setEnabled(True)
            self.quitSignInAction.setEnabled(False)
        if (q.text() == "退出登录"):
            sip.delete(self.widget)
            self.widget = SignInWidget()
            self.setCentralWidget(self.widget)
            self.widget.is_admin_signal.connect(self.adminSignIn)
            self.widget.is_student_signal[str].connect(self.studentSignIn)
            self.signUpAction.setEnabled(True)
            self.changePasswordAction.setEnabled(True)
            self.signInAction.setEnabled(False)
            self.quitSignInAction.setEnabled(False)
        if (q.text() == "登录"):
            sip.delete(self.widget)
            self.widget = SignInWidget()
            self.setCentralWidget(self.widget)
            self.widget.is_admin_signal.connect(self.adminSignIn)
            self.widget.is_student_signal[str].connect(self.studentSignIn)
            self.signUpAction.setEnabled(True)
            self.changePasswordAction.setEnabled(True)
            self.signInAction.setEnabled(False)
            self.quitSignInAction.setEnabled(False)
        if (q.text() == "退出"):
            qApp = QApplication.instance()
            qApp.quit()
        return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./images/MainWindow_1.png"))
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainwindow = Main()
    mainwindow.showMaximized()
    sys.exit(app.exec_())


