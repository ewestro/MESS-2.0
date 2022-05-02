import os
import json
from windows.settings_window import *


class Monitor(QtCore.QThread):
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
        self.setting.pushButton_6.clicked.connect(self.save_function)
        self.setting.pushButton_7.clicked.connect(lambda: self.close())

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

    # Сохраняем настройки пользователя + делаем проверку того,что вводит пользователь
    def save_function(self):
        server_ip = self.setting.lineEdit_2.text()
        server_port = self.setting.lineEdit_3.text()
        nickname = self.setting.lineEdit_4.text()

        if 3 <= len(nickname) <= 20:
            with open(os.path.join("saved_parameters.json"), "w") as file:
                save = {"server_ip": server_ip, "server_port": server_port, "nick": nickname}
                json.dump(save, file)
            # Закрываем окно с настройками
            self.close()
        else:
            self.setting.lineEdit_4.setText("Ник должен состоять от 3 до 20 символов")
