import pygame, sys
from pygame.locals import *

from PyQt5 import QtCore, QtGui, QtWidgets

WIDTH = 1000
HEIGHT = 500
btn_1x = 10
btn_1y = 10
btn_size_x = 210
btn_size_y = 60
btn_2x = 0.3 * WIDTH
btn_2y = HEIGHT * 0.6

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.clicked.connect(self.push)
        self.toolButton.setGeometry(QtCore.QRect(0, 0, 151, 41))
        self.toolButton.setObjectName("toolButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def push(self):
        print("F")
        MainWindow.hide()
        pygame.init()
        screen = pygame.display.set_mode((1000, 500))
        pygame.display.set_caption('Test')

        COLOR = (49, 49, 255)
        while 1:
            pygame.time.delay(1)

            for event in pygame.event.get():
                if event.type == QUIT:
                    MainWindow.show()
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_1x <= event.pos[0] <= btn_size_x and btn_1y <= event.pos[1] <= btn_size_y:
                        MainWindow.show()
                    if 30 <= event.pos[0] <= 70 and 330 <= event.pos[1] <= 370:
                        COLOR = (24,17,219)
                    if 30 <= event.pos[0] <= 70 and 280 <= event.pos[1] <= 320:
                        COLOR = (219,4,0)
                    if 30 <= event.pos[0] <= 70 and 230 <= event.pos[1] <= 280:
                        COLOR = (200,219,30)
                    if 30 <= event.pos[0] <= 70 and 180 <= event.pos[1] <= 230:
                        COLOR = (30,219,56)

                draw(screen, btn_1x, btn_1y, btn_size_x, btn_size_y, '       BACK      ', (49,49,255), True)
                if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                    print(pygame.mouse.get_pos())
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]

                    pygame.draw.circle(screen, (COLOR), (x, y), 10)

                pygame.draw.rect(screen, (255,255,255), (10, 170, 90, 210))
                pygame.draw.circle(screen, (30,219,56), (50, 200), 20)
                pygame.draw.circle(screen, (200,219,30), (50, 250), 20)
                pygame.draw.circle(screen, (219,4,0), (50, 300), 20)
                pygame.draw.circle(screen, (24,17,219), (50, 350), 20)
                pygame.display.update()





    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolButton.setText(_translate("MainWindow", "Первая Миниигра"))

def draw(screen, x, y, btn_size_x, btn_size_y, text='', color=None, options=False):
    font = pygame.font.SysFont('arial', 25)
    text1 = font.render(text, 1, (0,0,0))
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

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())




windowHeight = 600
windowWidth = 900
