from PyQt5 import QtCore, QtGui, QtWidgets

import main


class Ui_RunWindow(object):
    def setupUi(self, RunWindow):
        RunWindow.setObjectName("RunWindow")
        RunWindow.resize(418, 278)
        self.centralwidget = QtWidgets.QWidget(RunWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 80, 341, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(30, 120, 351, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(140, 180, 121, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        RunWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(RunWindow)
        self.statusbar.setObjectName("statusbar")
        RunWindow.setStatusBar(self.statusbar)
        self.pushButton.clicked.connect(self.RUN)

        self.retranslateUi(RunWindow)
        QtCore.QMetaObject.connectSlotsByName(RunWindow)

    def RUN(self):
        ax.show()
        RunWindow.hide()

    def retranslateUi(self, RunWindow):
        _translate = QtCore.QCoreApplication.translate
        RunWindow.setWindowTitle(_translate("RunWindow", "MainWindow"))
        self.label_2.setText(_translate("RunWindow", "Введите свой ник:"))
        self.pushButton.setText(_translate("RunWindow", "Войти"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RunWindow = QtWidgets.QMainWindow()
    ax = main.MainWindow()
    ui = Ui_RunWindow()
    ui.setupUi(RunWindow)
    RunWindow.show()
    sys.exit(app.exec_())

