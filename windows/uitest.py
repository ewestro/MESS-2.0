import sys
from windows.main_window import *
from windows.settings_window_config import *


# Создаем интерфейс программы и обработчик событий
class Client(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Экземпляр класса для обработки соединений и сигналов
        self.connect_monitor = message_monitor()
        self.connect_monitor.mysignal.connect(self.signal_handler)

        # Функционал кнопок
        self.ui.pushButton_3.clicked.connect(lambda: self.close())
        self.ui.pushButton_5.clicked.connect(lambda: self.showMinimized())
        self.ui.pushButton_7.clicked.connect(self.settings_panel)

    # Функционал открытия панели настроек
    def settings_panel(self):
        setting_win = Settings(self, self.connect_monitor.mysignal)
        setting_win.show()

    # Обработчик сигналов из потока
    def signal_handler(self, value: list):
        if value[0] == "update_config":
            self.update_config()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = Client()
    myapp.show()
    sys.exit(app.exec_())
