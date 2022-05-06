import sys
from windows.main_window import *
from windows.settings_window_config import *


# Создаем интерфейс программы и обработчики событий
class Client(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Убираем верхний системный трей
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.center()

        # Экземпляр класса для обработки соединений и сигналов
        self.connect_monitor = Monitor()

        # Данные из конфига
        self.nick = None
        self.ip = None
        self.port = None
        self.smile_type = None
        self.connect_status = False

        # Обработчики для кнопок
        # self.ui.pushButton.clicked.connect(self.send_message)
        # self.ui.pushButton_2.clicked.connect(self.connect_to_server)
        self.ui.pushButton_3.clicked.connect(lambda: self.close())
        self.ui.pushButton_5.clicked.connect(lambda: self.showMinimized())
        self.ui.pushButton_7.clicked.connect(self.settings_panel)

        # Обработчики для смайлов
        self.ui.pushButton_6.clicked.connect(lambda: self.send_smile('1'))
        self.ui.pushButton_8.clicked.connect(lambda: self.send_smile('2'))
        self.ui.pushButton_9.clicked.connect(lambda: self.send_smile('3'))
        self.ui.pushButton_10.clicked.connect(lambda: self.send_smile('4'))
        self.ui.pushButton_11.clicked.connect(lambda: self.send_smile('5'))
        self.ui.pushButton_12.clicked.connect(lambda: self.send_smile('6'))
        self.ui.pushButton_13.clicked.connect(lambda: self.send_smile('7'))
        self.ui.pushButton_14.clicked.connect(lambda: self.send_smile('8'))
        self.ui.pushButton_15.clicked.connect(lambda: self.send_smile('9'))
        self.ui.pushButton_16.clicked.connect(lambda: self.send_smile('10'))
        self.ui.pushButton_17.clicked.connect(lambda: self.send_smile('11'))
        self.ui.pushButton_18.clicked.connect(lambda: self.send_smile('12'))
        self.ui.pushButton_21.clicked.connect(lambda: self.send_smile('13'))
        self.ui.pushButton_22.clicked.connect(lambda: self.send_smile('14'))
        self.ui.pushButton_24.clicked.connect(lambda: self.send_smile('15'))

    # Функция отправления смайлов
    def send_smile(self, smile_number: str):
        buttons = {
            '1': self.ui.pushButton_6,
            '2': self.ui.pushButton_8,
            '3': self.ui.pushButton_9,
            '4': self.ui.pushButton_10,
            '5': self.ui.pushButton_11,
            '6': self.ui.pushButton_12,
            '7': self.ui.pushButton_13,
            '8': self.ui.pushButton_14,
            '9': self.ui.pushButton_15,
            '10': self.ui.pushButton_16,
            '11': self.ui.pushButton_17,
            '12': self.ui.pushButton_18,
            '13': self.ui.pushButton_21,
            '14': self.ui.pushButton_22,
            '15': self.ui.pushButton_24}

        change_style = """
        border-radius: 35px;
        border: 2px solid red;
        """

        default_style = """
        border: none;
        """

        if self.smile_type == None:
            buttons[smile_number].setStyleSheet(change_style)
            self.smile_type = smile_number

        elif self.smile_type != None and self.smile_type != smile_number:
            buttons[self.smile_type].setStyleSheet(default_style)
            buttons[smile_number].setStyleSheet(change_style)
            self.smile_type = smile_number

        elif self.smile_type != None and self.smile_type == smile_number:
            buttons[smile_number].setStyleSheet(default_style)
            self.smile_type = None

        print(f'SELF.SMILE_TYPE: {self.smile_type}')

    # Реализация открытия окна настроек
    def settings_panel(self):
        setting_win = Settings(self, self.connect_monitor.mysignal)
        setting_win.show()

    # Обновление конфигурации
    def update_config(self):
        if os.path.exists(os.path.join("saved_parameters.json")):
            with open(os.path.join("saved_parameters.json")) as file:
                data = json.load(file)
                self.nick = data['nick']
                self.ip = data['server_ip']
                self.port = int(data['server_port'])

        # Обработчик сигналов
    def signal_handler(self, value):
        if value[0] == "update_config":
            self.update_config()

    # Функции перетаскивания, передвижения окна настроек
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
