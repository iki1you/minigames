from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
import paint

name = "NULL"

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, name):
        QtWidgets.QMainWindow.__init__(self)
        self.name = name
        self.setMinimumSize(QtCore.QSize(1000, 800))
        self.setWindowTitle("Главное меню")
        fontButton = QtGui.QFont() #Cтили текста для кнопок и лейблов
        fontButton.setPointSize(24)
        fontLabel1 = QtGui.QFont()
        fontLabel1.setPointSize(30)
        fontLabel2 = QtGui.QFont()
        fontLabel2.setPointSize(34)
        fontLabel3 = QtGui.QFont()
        fontLabel3.setPointSize(20)
        button1 = QtWidgets.QPushButton('Крокодил', self)
        button1.resize(250, 50)
        button1.move(25, 115)
        button1.setFont(fontButton)
        button1.clicked.connect(self.push)
        label1 = QtWidgets.QLabel("Список игр:", self)
        label1.resize(250,50)
        label1.setFont(fontLabel1)
        label1.move(25,50)
        label2 = QtWidgets.QLabel("Ваш ник: " + self.name, self)
        label2.resize(500,50)
        label2.setFont(fontLabel2)
        label2.move(380,350)
        label3 = QtWidgets.QLabel("Новости: Патч v0.001 добавлен интерфейс и возможность вводить ник", self)
        label3.resize(400,400)
        label3.move(450,-100)
        label3.setFont(fontLabel3)
        label3.setWordWrap(True)

    def push(self):
        ex.show()  # Переход в файл paint.py
        print(self.name)

class RunWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setMinimumSize(QtCore.QSize(500, 300))
        self.setWindowTitle("Введите ник")
        label1 = QtWidgets.QLabel("Введите свой ник:",self)
        font = QtGui.QFont()
        font.setPointSize(24)
        fontButton = QtGui.QFont()
        fontButton.setPointSize(16)
        label1.setFont(font)
        label1.resize(400,50)
        label1.move(50,50)
        self.lineEdit = QtWidgets.QLineEdit("",self)
        self.lineEdit.resize(400,30)
        self.lineEdit.move(50,120)
        button1 = QtWidgets.QPushButton("Вход", self)
        button1.setFont(fontButton)
        button1.move(200,200)
        button1.resize(100,50)
        button1.clicked.connect(self.push)
        self.name = "NULL"

    def push(self):
        if self.lineEdit.text() != "":
            self.name = self.lineEdit.text()

            ax.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex = paint.Window()
    runwindow = RunWindow()
    ax = MainWindow(runwindow.name)
    win = RunWindow()
    win.show()
    sys.exit(app.exec_())