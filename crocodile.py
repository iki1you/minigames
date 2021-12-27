import main
import pygame, sys
from pygame.locals import *
from PyQt5 import QtCore, QtGui, QtWidgets

def push(self):
    print("F")
    MainWindow.hide()
    pygame.init()
    screen = pygame.display.set_mode((1000, 500))
    pygame.display.set_caption('Test')

    COLOR = (49, 49, 255)
    while 1:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                MainWindow.show()
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_1x <= event.pos[0] <= btn_size_x and btn_1y <= event.pos[1] <= btn_size_y:
                    MainWindow.show()
                    pygame.quit()
                if 30 <= event.pos[0] <= 70 and 330 <= event.pos[1] <= 370:
                    COLOR = (24, 17, 219)
                if 30 <= event.pos[0] <= 70 and 280 <= event.pos[1] <= 320:
                    COLOR = (219, 4, 0)
                if 30 <= event.pos[0] <= 70 and 230 <= event.pos[1] <= 280:
                    COLOR = (200, 219, 30)
                if 30 <= event.pos[0] <= 70 and 180 <= event.pos[1] <= 230:
                    COLOR = (30, 219, 56)
            draw(screen, btn_1x, btn_1y, btn_size_x, btn_size_y, '       BACK      ', (49, 49, 255), True)
            if pygame.mouse.get_pressed(num_buttons=3) == (1, 0, 0):
                print(pygame.mouse.get_pos())
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]

                pygame.draw.circle(screen, (COLOR), (x, y), 10)

            pygame.draw.rect(screen, (255, 255, 255), (10, 170, 90, 210))
            pygame.draw.circle(screen, (30, 219, 56), (50, 200), 20)
            pygame.draw.circle(screen, (200, 219, 30), (50, 250), 20)
            pygame.draw.circle(screen, (219, 4, 0), (50, 300), 20)
            pygame.draw.circle(screen, (24, 17, 219), (50, 350), 20)
            pygame.display.update()