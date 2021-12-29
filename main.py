from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
import paint


class Window(QMainWindow):
    def __init__(self, name):
        QMainWindow.__init__(self)
        self.name = name
        self.setMinimumSize(QtCore.QSize(1000, 800))
        self.setWindowTitle("Главное меню")
        fontButton = QtGui.QFont()  # Cтили текста для кнопок и лейблов
        fontButton.setPointSize(24)
        fontLabel1 = QtGui.QFont()
        fontLabel1.setPointSize(30)
        fontLabel2 = QtGui.QFont()
        fontLabel2.setPointSize(34)
        fontLabel3 = QtGui.QFont()
        fontLabel3.setPointSize(20)
        button1 = QPushButton('Крокодил', self)
        button1.resize(250, 50)
        button1.move(25, 115)
        button1.setFont(fontButton)
        button1.clicked.connect(self.push)
        label1 = QLabel("Список игр:", self)
        label1.resize(250, 50)
        label1.setFont(fontLabel1)
        label1.move(25, 50)
        label2 = QLabel("Ваш ник: " + self.name, self)
        label2.resize(500, 50)
        label2.setFont(fontLabel2)
        label2.move(380, 350)
        label3 = QLabel("Новости: Патч v0.001 добавлен интерфейс и возможность вводить ник", self)
        label3.resize(400, 400)
        label3.move(450, -100)
        label3.setFont(fontLabel3)
        label3.setWordWrap(True)

    def push(self):
        ex.show()  # Переход в файл paint.py


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    d, e = QInputDialog.getText(None, 'Login', 'Введите ник:', QLineEdit.Normal)
    if not d.split():
        e = False
    if not e:
        sys.exit(app.exec_())
    ex = paint.Window()
    w = Window(d)
    w.show()
    sys.exit(app.exec_())