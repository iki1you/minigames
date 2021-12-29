import sys
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import QPropertyAnimation, pyqtProperty
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QApplication, QMainWindow


class PushButton(QtWidgets.QPushButton):
    hover = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(PushButton, self).__init__(parent)
        pass

    def enterEvent(self, event):
        self.hover.emit("enterEvent")

    def leaveEvent(self, event):
        self.hover.emit("leaveEvent")


class AnimationShadowEffect(QGraphicsDropShadowEffect):

    def __init__(self, color, *args, **kwargs):
        super(AnimationShadowEffect, self).__init__(*args, **kwargs)
        self.setColor(color)
        self.setOffset(0, 0)
        self.setBlurRadius(0)
        self._radius = 0
        self.animation = QPropertyAnimation(self)
        self.animation.setTargetObject(self)
        self.animation.setDuration(1500)            # Время одного цикла
        self.animation.setLoopCount(-1)             # Постоянный цикл
        self.animation.setPropertyName(b'radius')
        self.animation.setKeyValueAt(0.5, 15)

    def start(self):
        self.animation.start()

    def stop(self, r=0):
        # Остановить анимацию и изменить значение радиуса
        self.animation.stop()
        self.radius = r

    @pyqtProperty(int)
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, r):
        self._radius = r
        self.setBlurRadius(r)


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        uic.loadUi("main.ui", self)

        #Инифицализация анимации
        self.aniButton = AnimationShadowEffect(QtCore.Qt.white, self.designer_button)
        self.designer_button.setGraphicsEffect(self.aniButton)

        #Добавление эффекта к кнопке
        self.designer_button = PushButton(self.designer_button)
        self.designer_button.setCheckable(True)
        self.designer_button.hover.connect(self.button_hover)


    def button_hover(self, hover):
        if hover == "enterEvent":
            self.aniButton.start()
        elif hover == "leaveEvent":
            self.aniButton.stop()


if __name__ == '__main__':

    app = QApplication(sys.argv)

    ex = App()
    ex.show()
    sys.exit(app.exec_())