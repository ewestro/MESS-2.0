import os
import json
from windows.settings_window import *
import re


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

        # Подргузка данных из .json
        if os.path.exists(os.path.join("saved_parameters.json")):
            with open(os.path.join("saved_parameters.json")) as file:
                data = json.load(file)
                self.setting.lineEdit_2.setText(data['server_ip'])
                self.setting.lineEdit_3.setText(data['server_port'])
                self.setting.lineEdit_4.setText(data['nick'])

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
        nick = self.setting.lineEdit_4.text()
        regular_ip = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"

        # Показываем пользователю неверно заполненные поля
        self.setting.lineEdit_2.setStyleSheet("border-radius: 7px;")
        self.setting.lineEdit_3.setStyleSheet("border-radius: 7px;")
        self.setting.lineEdit_4.setStyleSheet("border-radius: 7px;")

        # Проверяем правильность заполнения полей пользователем
        if 3 <= len(nick) <= 20:
            if not re.match(regular_ip, self.setting.lineEdit_2.text()) is None:
                if server_port.isdecimal() and int(server_port) <= 65535:

                    # Создаем конфиг, если его еще не существовало
                    if not os.path.exists(os.path.join("saved_parameters.json")):
                        with open(os.path.join("saved_parameters.json"), "w") as file:
                            data = {"nick": nick, "server_ip": server_ip, "server_port": server_port}
                            json.dump(data, file, indent=6)

                    # Если конфиг был создан ранее, то идет его перезапись
                    else:
                        with open(os.path.join("saved_parameters.json"), "w") as file:
                            data = {"nick": nick, "server_ip": server_ip, "server_port": server_port}
                            json.dump(data, file, indent=6)

                        # Закрываем окно с настройками
                    self.close()

                else:
                    self.setting.lineEdit_3.setStyleSheet("border: 2px solid red; border-radius: 7px;")
                    self.setting.lineEdit_3.setText("Вы неверно ввели Порт")
            else:
                self.setting.lineEdit_2.setStyleSheet("border: 2px solid red; border-radius: 7px;")
                self.setting.lineEdit_2.setText("Вы неверно ввели IP-адрес")
        else:
            self.setting.lineEdit_4.setStyleSheet("border: 2px solid red; border-radius: 7px;")
            self.setting.lineEdit_4.setText("Ник должен состоять от 3 до 20 символов")
