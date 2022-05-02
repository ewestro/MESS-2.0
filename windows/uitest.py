import sys
from windows.main_window import *
from windows.settings_window_config import *


# Создаем интерфейс программы и обработчик событий
class Client(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #Убираем  верхний системный трей
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.center()

        # Экземпляр класса для обработки соединений и сигналов
        self.connect_monitor = message_monitor()

        # Функционал кнопок
        self.ui.pushButton_3.clicked.connect(lambda: self.close())
        self.ui.pushButton_5.clicked.connect(lambda: self.showMinimized())
        self.ui.pushButton_7.clicked.connect(self.settings_panel)

    # Реализация открытия окна настроек
    def settings_panel(self):
        setting_win = Settings(self, self.connect_monitor.mysignal)
        setting_win.show()


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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = Client()
    myapp.show()
    sys.exit(app.exec_())
