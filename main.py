import pygame, sys
from pygame.locals import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QAction, qApp, QCheckBox
import paint

WIDTH = 1000
HEIGHT = 500
btn_1x = 10
btn_1y = 10
btn_size_x = 210
btn_size_y = 60
btn_2x = 0.3 * WIDTH
btn_2y = HEIGHT * 0.6
FPS = 6000
clock = pygame.time.Clock()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.clicked.connect(self.push)
        self.toolButton.setGeometry(QtCore.QRect(0, 0, 140, 40))
        self.toolButton.setObjectName("toolButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def push(self):
        ex.show()
        MainWindow.hide()
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolButton.setText(_translate("MainWindow", "Крокодил"))


def draw(screen, x, y, btn_size_x, btn_size_y, text='', color=None, options=False):
    font = pygame.font.SysFont('arial', 25)
    text1 = font.render(text, 1, (0, 0, 0))
    if text == '':
        pygame.draw.rect(screen, (0, 0, 0), (x, y, btn_size_x, btn_size_y))
    if options:
        pygame.draw.rect(screen, color, (x, y, btn_size_x, btn_size_y))
        screen.blit(text1, (x + 10, y + btn_size_y // 4))


def py_game():
    pass


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ex = paint.Window()
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

windowHeight = 600
windowWidth = 900
