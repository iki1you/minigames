import sys
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QPen, QIcon, QImage, QCursor, QColor, QBrush, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QAction, qApp, QCheckBox
from PyQt5.QtWidgets import QVBoxLayout, QFileDialog, QColorDialog, QPushButton, QSlider, QLineEdit, QMessageBox
import main


class DrawWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 800)
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.instrument = 'brush'
        self.draw = False
        self.brushColor1 = Qt.black
        self.brushColor = Qt.black
        self.brushColor2 = Qt.white
        self.brushSize = 3
        self.zl = False
        self.text = ''
        self.txt = Text(self)
        self.lastPoint = 0, 0
        self.toolbar = ToolBar(self)
        self.setContextMenuPolicy(Qt.PreventContextMenu)
        self.setCursor(QCursor(Qt.CrossCursor))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton or event.button() == Qt.RightButton:
            if event.button() == Qt.LeftButton:
                self.brushColor = self.brushColor1
            elif event.button() == Qt.RightButton:
                self.brushColor = self.brushColor2
            self.draw = True
            self.lastPoint = event.pos()
            if self.instrument == 'brush':
                painter = QPainter(self.image)
                painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                painter.drawPoint(event.pos())
                self.update()
            else:
                self.firstPoint = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() and (Qt.LeftButton or Qt.RightButton) and self.draw:
            if event.button == Qt.LeftButton:
                self.brushColor = self.brushColor1
            elif event.button == Qt.RightButton:
                self.brushColor = self.brushColor2
            if self.instrument == 'brush' or self.instrument == 'eraser':
                self.drawer(event)
            elif self.instrument == 'malarwing':
                painter = QPainter(self.image)
                painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                painter.drawLine(self.lastPoint, event.pos())
                self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.draw = False
            self.brushColor = self.brushColor1
            self.drawer(event)
        elif event.button() == Qt.RightButton:
            self.draw = False
            self.brushColor = self.brushColor2
            self.drawer(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.begin(self)
        painter.drawImage(self.rect(), self.image, self.image.rect())
        painter.end()

    def drawer(self, event):
        painter = QPainter(self.image)
        painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        if self.instrument == 'line':
            painter.drawLine(self.lastPoint, event.pos())
        elif self.instrument == 'brush':
            painter.drawLine(self.lastPoint, event.pos())
        elif self.instrument == 'circle':
            if self.zl:
                painter.setPen(QPen(self.brushColor, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
                painter.setBrush(QBrush(self.brushColor))
            radius = ((self.lastPoint.x() - event.x()) ** 2 + (self.lastPoint.y() - event.y()) ** 2) ** 0.5
            painter.drawEllipse(self.lastPoint, radius, radius)
        elif self.instrument == 'triangle':
            if self.zl:
                painter.setPen(QPen(self.brushColor, 1, Qt.SolidLine, Qt.SquareCap))
                painter.setBrush(QBrush(self.brushColor))
            triangle = Triangle(self.lastPoint, event, self.image, self.brushColor, self.brushSize)
            triangle.drawT(painter)
        elif self.instrument == 'square':
            if self.zl:
                painter.setPen(QPen(self.brushColor, 1, Qt.SolidLine, Qt.SquareCap))
                painter.setBrush(QBrush(self.brushColor))
            square = Square(self.lastPoint, event, self.image, self.brushColor, self.brushSize)
            square.drawT(painter)
        elif self.instrument == 'eraser':
            painter.setPen(QPen(self.brushColor2, self.brushSize, Qt.SolidLine, Qt.RoundCap))
            painter.drawLine(self.lastPoint, event.pos())
        elif self.instrument == 'text':
            painter.drawText(self.lastPoint, self.text)
        self.lastPoint = event.pos()
        self.update()


class ToolBar(QWidget):
    def __init__(self, e):
        super(ToolBar, self).__init__()
        self.e = e
        self.toolbar = e.addToolBar('Панель инструментов')
        self.toolbar.setMovable(False)
        self.toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.slider = QSlider(self.toolbar)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(50)
        self.slider.setTickPosition(50)
        self.slider.setTickInterval(2)
        self.slider.valueChanged.connect(self.setSize)
        self.slider.move(620, 2)
        self.open = QAction(QIcon('icons/открыть.png'), 'open', self)
        self.toolbar.addAction(self.open)
        self.open.triggered.connect(self.openn)
        self.toolbar.setAutoFillBackground(True)
        self.earaser = QAction(QIcon('icons/earaser.png'), 'eraser', self)
        self.toolbar.addAction(self.earaser)
        self.earaser.triggered.connect(self.eraser)
        self.brushAction = QAction(QIcon('icons/brush.png'), 'Brush', self)
        self.toolbar.addAction(self.brushAction)
        self.brushAction.triggered.connect(self.setBrush)
        self.triangleAction = QAction(QIcon('icons/triangle.png'), 'Triangle', self)
        self.toolbar.addAction(self.triangleAction)
        self.triangleAction.triggered.connect(self.setTriangle)
        self.circleAction = QAction(QIcon('icons/circle.png'), 'Circle', self)
        self.toolbar.addAction(self.circleAction)
        self.circleAction.triggered.connect(self.setCircle)
        self.squareAction = QAction(QIcon('icons/rectangle.png'), 'Rectangle', self)
        self.toolbar.addAction(self.squareAction)
        self.squareAction.triggered.connect(self.setSquare)
        self.malarwingAction = QAction(QIcon('icons/malarwing.png'), 'Malarwing', self)
        self.toolbar.addAction(self.malarwingAction)
        self.malarwingAction.triggered.connect(self.setmalarwing)
        self.textAction = QAction(QIcon('icons/text.png'), 'Text', self)
        self.toolbar.addAction(self.textAction)
        self.textAction.triggered.connect(self.text)
        self.clearAction = QAction(QIcon('icons/clear.png'), 'Clear', self)
        self.toolbar.addAction(self.clearAction)
        self.clearAction.triggered.connect(self.clear)
        self.lineAction = QAction(QIcon('icons/line.png'), 'Line', self)
        self.toolbar.addAction(self.lineAction)
        self.lineAction.triggered.connect(self.setLine)
        self.zalifk_text = QLabel(e)
        self.zalifk_text.move(728, 2)
        self.zalifk_text.setText('Заливка')
        self.zalifk = QCheckBox(e)
        self.zalifk.move(775, 2)
        self.zalifk.stateChanged.connect(self.checkbox)
        self.setcoloraction = QPushButton(e)
        self.setcoloraction.setText('Выбрать цвет 1(ПКМ)')
        self.setcoloraction.move(350, 2)
        self.setcoloraction.clicked.connect(self.run)
        self.setcoloraction.resize(120, 30)
        self.setcoloraction2 = QPushButton(e)
        self.setcoloraction2.setText('Выбрать цвет 2(ЛКМ)')
        self.setcoloraction2.move(470, 2)
        self.setcoloraction2.clicked.connect(self.run2)
        self.setcoloraction2.resize(120, 30)
        self.sizeview = QLabel(self.toolbar)
        self.sizeview.move(593, 2)
        self.sizeview.setText(f'{e.brushSize}px')
        self.sizeview.resize(30, 15)

    def setSize(self):
        self.e.brushSize = self.slider.value()
        self.sizeview.setText(f'{self.e.brushSize}px')

    def setBrush(self):
        self.e.instrument = 'brush'

    def setLine(self):
        self.e.instrument = 'line'

    def setCircle(self):
        self.e.instrument = 'circle'

    def setTriangle(self):
        self.e.instrument = 'triangle'

    def setmalarwing(self):
        self.e.instrument = 'malarwing'

    def setSquare(self):
        self.e.instrument = 'square'

    def checkbox(self):
        if self.zalifk.checkState():
            self.e.zl = True
        else:
            self.e.zl = False


    def eraser(self):
        self.e.instrument = 'eraser'

    def run(self):
        color2 = QColorDialog.getColor()
        if color2.isValid():
            r, g, b = color2.getRgb()[1], color2.getRgb()[2], color2.getRgb()[3]
            r, g, b = 255 - r, 255 - g, 255 - b
            color3 = QColor(r, g, b)
            self.setcoloraction.setStyleSheet(f'background-color: {color2.name()}; color: {color3.name()}')
            self.e.brushColor1 = color2

    def run2(self):
        color2 = QColorDialog.getColor()
        if color2.isValid():
            r, g, b = color2.getRgb()[1], color2.getRgb()[2], color2.getRgb()[3]
            r, g, b = 255 - r, 255 - g, 255 - b
            color3 = QColor(r, g, b)
            self.setcoloraction2.setStyleSheet(f'background-color: {color2.name()}; color: {color3.name()}')
            self.e.brushColor2 = color2

    def clear(self):
        self.e.image.fill(self.e.brushColor2)
        self.e.update()

    def text(self):
        self.e.txt.show()

    def openn(self):
        fname = QFileDialog.getOpenFileName(
            self, 'Выбрать картинку', '',
            'Картинка (*.jpg);;Картинка (*.jpg);;Все файлы (*)')[0]
        painter = QPainter(self.e.image)
        painter.drawImage(QPoint(0, 0), QImage(fname))


class Triangle:
    def __init__(self, start_pos, event_pos, image, brushColor, brushSize):
        self.brushColor = brushColor
        self.brushSize = brushSize
        self.image = image
        self.start = start_pos
        self.event = event_pos
        self.radius = ((self.start.x() - event_pos.x())**2 + (self.start.y() - event_pos.y())**2)**0.5
        self.poligon = [
            QPoint(start_pos.x(), start_pos.y() - self.radius),
            QPoint(start_pos.x() - self.radius, start_pos.y() + self.radius),
            QPoint(start_pos.x() + self.radius, start_pos.y() + self.radius)
        ]

    def drawT(self, painter):
        painter.drawPolygon(*self.poligon)


class Square:
    def __init__(self, start_pos, event_pos, image, brushColor, brushSize):
        self.brushColor = brushColor
        self.brushSize = brushSize
        self.image = image
        self.poligon = [
            QPoint(start_pos.x(), start_pos.y()),
            QPoint(event_pos.x(), start_pos.y()),
            QPoint(event_pos.x(), event_pos.y()),
            QPoint(start_pos.x(), event_pos.y())
        ]

    def drawT(self, painter):
        painter.drawPolygon(*self.poligon)


class AboutWindow(QWidget):
    def __init__(self):
        super(AboutWindow, self).__init__()

        self.setWindowTitle('Справка')
        self.setFixedSize(270, 200)
        self.circle = QPixmap('icons/s.png')
        self.info = QLabel(self)
        self.info.setPixmap(self.circle)
        self.info.move(0, 50)
        self.txt = QLabel(self)
        self.txt.move(5, 5)
        self.txt.setText('"Paint 2.4" - растровый графический редактор, \nс расширенными возможностями для рисования.')
        self.txt2 = QLabel(self)
        self.txt2.move(5, 160)
        self.txt2.setText('создано на pyqt5')


class Question(QWidget):
    def __init__(self):
        super(Question, self).__init__()

        self.setWindowTitle('Справка')
        self.setFixedSize(770, 230)
        self.circle = QPixmap('icons/circleh.png')
        self.info = QLabel(self)
        self.info.setPixmap(self.circle)
        self.txt = QLabel(self)
        self.txt.move(5, 200)
        self.txt.setText('Точка O, где x1,y1 - начальные координаты; B, где x2,y2 - конечные.')






class Text(QWidget):
    def __init__(self, e):
        super(Text, self).__init__()

        self.e = e
        self.setWindowTitle('Ввод текста.')
        self.setFixedSize(270, 30)
        self.info = QLabel(self)
        self.info.setText('Введите текст:')
        self.info.move(6, 10)
        self.inpt = QLineEdit(self)
        self.inpt.move(100, 3)
        self.inpt.resize(50, 25)
        self.accept = QPushButton(self)
        self.accept.move(170, 3)
        self.accept.resize(70, 25)
        self.accept.setText('Принять')
        self.accept.clicked.connect(self.accepted)

    def accepted(self):
        self.e.text = self.inpt.text()
        self.e.instrument = 'text'
        self.close()


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle('Крокодил')
        self.setCentralWidget(DrawWidget())
        self.setFixedSize(800, 800)
        self.about_window = AboutWindow()
        self.question = QAction(self)
        self.question.setText('Сгенерировать слово')
        self.question.triggered.connect(self.randomWord)
        self.menuBar().addAction(self.question)
        self.question = Question()


    def randomWord(self):
        import random
        words = ["подпись", "вырез", "гранит", "кругозор", "блузка", "фараон", "клапан", "ёж", "вымя", "турист",
                 "колготки", "стоп", "кран", "питание",
                 "свёрток", "дочь", "шампунь", "броня", "зайчатина", "гимназист", "стелька", "подделка", "виза",
                 "затычка", "решение", "алкоголь", "шуруп",
                 "воровка", "колодец", "кабан", "команда", "бордель", "ловушка", "буква", "опера", "сектор",
                 "математика", "пароварка", "невезение", "глубина",
                 "штука", "справочник", "вождь", "хобот", "ширинка", "усталость", "служитель", "жар", "спальная",
                 "видео", "рот", "просьба", "фишка", "рукопись",
                 "ракетчик", "каблук", "шрифт", "палец", "ножка", "халва", "черника", "незнайка", "компания",
                 "работница", "мышь", "исследование", "кружка", "мороженое",
                 "сиденье", "пулемёт", "печь", "солист", "свёкла", "стая", "зелье", "дума", "посылка", "коготь",
                 "семафор", "брат", "различие", "плоскостопие", "двигатель",
                 "сфера", "тюльпан", "затвор", "внедорожник", "самурай", "стан", "алгоритм", "параграф", "глаз",
                 "медалист", "пульт", "поводок", "подлежащее", "ор", "бунт",
                 "удочка", "лес", "диспетчер", "монитор", "вдова", "пиратство", "астролог", "сосед", "пуп",
                 "изобретатель", "чума", "танец", "затишье", "пластилин", "йог",
                 "маска", "блоха", "судьба", "сияние", "рукавица", "филе", "заплыв", "сёмга", "гиппопотам", "мастер",
                 "походка", "ландыш", "яблоня", "кляча", "лиса",
                 "свёртываемость", "раствор", "соты", "солод", "спорт", "шифер", "прощение", "стопка", "побег"]
        self.word = words[random.randint(0, len(words) - 1)]
        msg = QMessageBox()
        msg.setText("Вам выпало слово: " + self.word)
        font = QtGui.QFont()
        font.setPointSize(20)
        msg.setFont(font)
        msg.setFixedSize(250, 250)
        msg.exec_()

    def question_show(self):
        self.question.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    ex.show()
    sys.exit(app.exec_())