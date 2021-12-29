from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import *
import crocodile




class Window(QMainWindow):
    def __init__(self, name):
        QMainWindow.__init__(self)
        self.name = name
        self.setMinimumSize(QtCore.QSize(1000, 800))
        self.setWindowTitle("Главное меню")
        self.setStyleSheet("background-color:#3771A1; color:white;border:none;")
        self.stop = False #Для работы кнопки



        frameTop = QFrame(self) #фрейм с надписью MiniGames
        frameTop.setFrameShape(QFrame.StyledPanel)
        frameTop.resize(1000,200)
        frameTop.move(0,0)
        frameTop.setStyleSheet("background-color:#3771A1;border:none;")


        frameBorder = QFrame(self) # горизонтальная палка
        frameBorder.setFrameShape(QFrame.StyledPanel)
        frameBorder.resize(1000,10)
        frameBorder.move(0,100)
        frameBorder.setStyleSheet("background-color:#000000;border:none;")

        frameBorder2 = QFrame(self)  # вертикальная палка
        frameBorder2.setFrameShape(QFrame.StyledPanel)
        frameBorder2.resize(10, 700)
        frameBorder2.move(250, 102)
        frameBorder2.setStyleSheet("background-color:#000000; border:1px solid #21222F;")


        frameMain = QFrame(self)
        frameMain.setFrameShape(QFrame.StyledPanel)
        frameMain.resize(700, 500)
        frameMain.setStyleSheet("background-color:#21222F;border:none;border-radius:15px;")
        frameMain.move(280,120)



        minigames = QLabel("MiniGames", self)
        minigames.resize(500,80)
        minigames.move(300,10)
        fontMinigames = QtGui.QFont()
        fontMinigames.setPointSize(60)
        minigames.setFont(fontMinigames)
        minigames.setStyleSheet("background-color:#3771A1;color:#FFFFFF;font-weight:bold;")



        fontButton = QtGui.QFont()
        fontButton.setPointSize(24)
        self.button1 = QPushButton('Крокодил', self)
        self.button1.setStyleSheet("background-color:#21222F;border:none;border-radius:15px;")
        self.button1.resize(200, 50)
        self.button1.move(25, 130)
        self.button1.setFont(fontButton)
        self.button1.clicked.connect(self.push)




        fontLabel2 = QtGui.QFont()
        fontLabel2.setPointSize(34)
        label2 = QLabel("   Ваш ник: " + self.name, self)
        label2.resize(600, 100)
        label2.setFont(fontLabel2)
        label2.setStyleSheet("background-color:#21222F;border:none;border-radius:15px;")
        label2.move(280, 650)

        self.info = "Новости: Патч v0.001. добавлен интерфейс и возможность вводить ник."
        fontLabel3 = QtGui.QFont()
        fontLabel3.setPointSize(20)
        self.label3 = QLabel(self.info, self)
        self.label3.resize(605, 400)
        self.label3.setStyleSheet("background:#21222F;")
        self.label3.move(300, 130)
        self.label3.setFont(fontLabel3)
        self.label3.setWordWrap(True)

        fontButton = QtGui.QFont()
        fontButton.setPointSize(24)
        self.button2 = QPushButton('Играть', self)
        self.button2.setStyleSheet("background-color:#3771A1;border:none;border-radius:15px;")
        self.button2.resize(250, 50)
        self.button2.move(500, 550)
        self.button2.setFont(fontButton)
        self.button2.clicked.connect(self.go)
        self.button2.hide()



    def push(self):
        if self.button1.text() == "Назад":
            self.button1.setText("Крокодил")
            self.label3.setText("Новости: Патч v0.001. добавлен интерфейс и возможность вводить ник.")
            self.button2.hide()

        elif self.button1.text() == "Крокодил":
            self.label3.setText("Правила этой игры очень просты и будут понятны даже ребенку. Один из игроков получает случайное слово или словосочетание"
                                ", и он должен нарисовать его. "
                                "Другие игроки должно догадаться, что за слово загадано и написать его в чат")
            self.button2.show()
            self.button1.setText("Назад")

    def go(self):
        CROCODILE.show()  # Переход в файл crocodile.py


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    nickname, e = QInputDialog.getText(None, 'Вход в систему', 'Введите ник:', QLineEdit.Normal)
    if not nickname.split():
        e = False
    if not e:
        sys.exit(app.exec_())
    nickname = "MyLongCode"
    CROCODILE = crocodile.Window() #крокодил
    win = Window(nickname) #главное меню
    win.show()
    sys.exit(app.exec_())