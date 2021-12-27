from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RunWindow(object):
    def setupUi(self, RunWindow):
        RunWindow.setObjectName("RunWindow")
        RunWindow.resize(961, 808)
        self.centralwidget = QtWidgets.QWidget(RunWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(590, 650, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 650, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 10, 691, 601))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("DWGQtQDWsAAX-KB.jpg"))
        self.label.setIndent(-2)
        self.label.setObjectName("label")
        RunWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(RunWindow)
        self.statusbar.setObjectName("statusbar")
        RunWindow.setStatusBar(self.statusbar)

        self.retranslateUi(RunWindow)
        QtCore.QMetaObject.connectSlotsByName(RunWindow)

    def retranslateUi(self, RunWindow):
        _translate = QtCore.QCoreApplication.translate
        RunWindow.setWindowTitle(_translate("RunWindow", "MainWindow"))
        self.pushButton.setText(_translate("RunWindow", "Войти"))
        self.pushButton_2.setText(_translate("RunWindow", "Хост"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RunWindow = QtWidgets.QMainWindow()
    ui = Ui_RunWindow()
    ui.setupUi(RunWindow)
    RunWindow.show()
    sys.exit(app.exec_())
