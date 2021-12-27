import sys
from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QMessageBox, QLabel, QPushButton, QLineEdit, QSpinBox
from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


class Dialogo(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi("login.ui", self)
        self.setWindowTitle("Авторизация")  # Title
        self.resize(250, 250)  # Размер окна
        self.setMinimumSize(250, 150)  # Минимальный размер окна
        self.setMaximumSize(250, 250)  # Максимальный размер окна
        self.db_ok.clicked.connect(self.getDb)  # Переход на getDb при нажатии на ОК
        self.db_cancel.clicked.connect(self.dbCancel)

    def getDb(self):
        useDb = self.db_combobox.currentText()  # Выбор базы
        login = self.db_login.text()  # Логин
        password = self.db_password.text()  # Пароль
        self.db = QSqlDatabase.addDatabase('QMYSQL')  # Драйвер для Mysql
        self.db.setHostName("localhost")
        self.db.setUserName("root")
        self.db.setPassword("root")
        self.db.setDatabaseName(useDb)
        self.db.open()
        query = QSqlQuery()
        query.prepare("SELECT * FROM users WHERE login = :login AND password = :password")
        query.bindValue(":login", login)
        query.bindValue(":password", password)
        query.exec_()
        if query.next():
            return True
        return False

    def dbCancel(self):
        self.close()


app = QApplication(sys.argv)
dialogo = Dialogo()
dialogo.show()
app.exec_()