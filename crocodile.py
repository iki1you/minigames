import sys
from PyQt5.QtCore import Qt, QPoint, QRectF
from PyQt5.QtGui import QPainter, QPen, QIcon, QImage, QCursor, QColor, QBrush
from PyQt5.QtWidgets import *

import socket
from des import *

from methods.SettingsPanel import *
from methods.ConnectThreadMonitor import *

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


class Chat(QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Данные из конфига (симметричный ключ получаем в ответе от сервера)
        self.nick = None
        self.ip = None
        self.port = None
        self.smile_type = None
        self.connect_status = False

        # Экземпляр класса для обработки соединений и сигналов
        self.connect_monitor = message_monitor()
        self.connect_monitor.mysignal.connect(self.signal_handler)

        # Отключаем стандартные границы окна программы
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.center()

        # Обработчики основных кнопок + кнопок с панели
        self.ui.pushButton.clicked.connect(self.send_message)
        self.ui.pushButton_2.clicked.connect(self.connect_to_server)
        self.ui.pushButton_4.clicked.connect(lambda: self.ui.listWidget.clear())
        self.ui.pushButton_7.clicked.connect(self.setting_panel)


    # Перетаскивание безрамочного окна
    # ==================================================================
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        try:
            delta = QtCore.QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        except AttributeError:
            pass



    # Открыть окно для настройки клиента
    def setting_panel(self):
        setting_win = SettingPanel(self, self.connect_monitor.mysignal)
        setting_win.show()


    # Обновление конфигов клиента
    def update_config(self):
        """
        Используется для обновления значений на лету, без необходимости
        перезапускать клиент (В случае если пользователь отредактировал настройки
        либо же запустил софт и необходимо проинициализировать значения)
        """
        # Если конфиг уже был создан
        if os.path.exists(os.path.join("data", "config.json")):
            with open(os.path.join("data", "config.json")) as file:
                data = json.load(file)
                self.nick = data['nick']
                self.ip = data['server_ip']
                self.port = int(data['server_port'])


    # Обработчик сигналов из потока
    def signal_handler(self, value: list):
        # Обновление параметров конфига
        if value[0] == "update_config":
            self.update_config()

        # Обновление симметричного ключа
        elif value[0] == "SERVER_OK":
            self.connect_status = True
            item = QtWidgets.QListWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignHCenter)
            item.setText(f"SERVER: {value[1]}\n")
            self.ui.listWidget.addItem(item)
            print(value)


        # Обработка сообщений других пользователей
        # ['ENCRYPT_MESSAGE', self.nick, smile_num, message_text.encode()]
        elif value[0] == "ENCRYPT_MESSAGE":
            item = QtWidgets.QListWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignRight)

            if value[2] != None:
                size = QtCore.QSize(45, 45)
                icon = QtGui.QIcon(os.path.join("icons", f"smile{value[2]}.png"))
                self.ui.listWidget.setIconSize(size)
                item.setIcon(icon)

            item.setText(f"{value[1]}:\n{value[-1]}")
            self.ui.listWidget.addItem(item)
            print(value)


    # Отправить сообщение на сервер
    def send_message(self):
        if self.connect_status:
            message_text = self.ui.lineEdit.text()
            smile_num = self.smile_type

            # Если поле с текстом не пустое шифруем сообщение и передаем на сервер
            if len(message_text) > 0:
                payload = ['ENCRYPT_MESSAGE', self.nick, smile_num, message_text.encode()]
                print(payload)
                self.connect_monitor.send_encrypt(payload)

                # Добавляем свое сообщение в ListWidget
                item = QtWidgets.QListWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignLeft)
                size = QtCore.QSize(45, 45)

                if smile_num != None:
                    icon = QtGui.QIcon(os.path.join("icons", f"smile{smile_num}.png"))
                    self.ui.listWidget.setIconSize(size)
                    item.setIcon(icon)
                item.setText(f"{self.nick} (ВЫ):\n{message_text}")
                self.ui.listWidget.addItem(item)

        else:
            message = "Проверьте соединение с сервером"
            QtWidgets.QMessageBox.about(self, "Оповещение", message)


    # Покдлючаемся к общему серверу
    def connect_to_server(self):
        self.update_config()    # Обновляем данные пользователя

        if self.nick != None:
            try:
                self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client.connect((self.ip, self.port))

                # Запускаем мониторинг входящих сообщений
                self.connect_monitor.server_socket = self.client
                self.connect_monitor.start()

                # Блокируем кнопки
                self.btn_locker(self.ui.pushButton_2, True)
                self.btn_locker(self.ui.pushButton_7, True)

            except Exception as err:
                message = "Ошибка соединения с сервером.\nПроверьте правильность ввода данных"
                QtWidgets.QMessageBox.about(self, "Оповещение", message)
        else:   # Если пользователь не заполнил данные
            message = "Для начала заполните данные во вкладке 'Настройки'"
            QtWidgets.QMessageBox.about(self, "Оповещение", message)


    # Блокировщик кнопок
    def btn_locker(self, btn: object, lock_status: bool) -> None:
        default_style = """
        QPushButton{
            color: white;
            border-radius: 7px;
            background-color: #595F76;
        }
        QPushButton:hover{
            background-color: #50566E;
        }      
        QPushButton:pressed{
            background-color: #434965;
        }
        """

        lock_style = """
        color: #9EA2AB;
        border-radius: 7px;
        background-color: #2C313C;
        """

        if lock_style:
            btn.setDisabled(True)
            btn.setStyleSheet(lock_style)
        else:
            btn.setDisabled(False)
            btn.setStyleSheet(default_style)


    # Обработчик события на выход из клиента
    def closeEvent(self, value: QtGui.QCloseEvent) -> None:
        try:
            payload = ['EXIT', f'{self.nick}', 'вышел из чата!'.encode()]
            self.connect_monitor.send_encrypt(payload); self.hide()
            time.sleep(3); self.client.close()
            self.close()
        except Exception as err:
            print(err)



class Window(QMainWindow):
    def __init__(self):

        super(Window, self).__init__()
        self.setWindowTitle('Крокодил')
        self.setCentralWidget(DrawWidget())
        self.setFixedSize(1500, 800)
        self.question = QAction(self)
        self.question.setText('Сгенерировать слово')
        self.question.triggered.connect(self.randomWord)
        self.menuBar().addAction(self.question)


        self.scene = QGraphicsScene()                   #НЕ ТРОГАТЬ Я ПОСТАВИЛ СВЕЧКУ ЗА ЭТИ СТРОКИ
        self.view = QGraphicsView(self.scene)
        self.view.setSceneRect(0, 0, 1500, 756)
        self.setCentralWidget(self.view)
        line = QLineEdit()
        ChatWidget = self.scene.addWidget(Chat())
        Draw = self.scene.addWidget(DrawWidget())
        ChatWidget.setGeometry(QRectF(790,-10,600,800))




    def randomWord(self): #генерация рандомного слова
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