from windows.settings_window import *


class message_monitor(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(list)


# Окно с настройками клиента
class Settings(QtWidgets.QWidget):
    def __init__(self, parent=None, signal=None):
        super().__init__(parent, QtCore.Qt.Window)
        self.setting = Ui_Form()
        self.setting.setupUi(self)
        self.setWindowModality(2)

        # Убираем  верхний системный трей
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.center()

        # Обработчики кнопок
        self.setting.pushButton_7.clicked.connect(lambda: self.close())
        self.setting.pushButton_6.clicked.connect(self.save_function)


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


    # Сохранить настройки пользователя + делаем проверку того,что вводит пользователь
    def save_function(self):
        server_ip = self.setting.lineEdit_2.text()
        server_port = self.setting.lineEdit_3.text()
        nick = self.setting.lineEdit_4.text()
        
        if len(nick) >= 3 and len(nick) <= 20:

            # Закрываем окно с настройками
            self.close()
        else:
            self.setting.lineEdit_4.setText("Ник должен состоять от 3 до 20 символов")
