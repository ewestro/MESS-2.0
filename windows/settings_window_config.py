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

        # Обработчики кнопок
        self.setting.pushButton_7.clicked.connect(lambda: self.close())
        self.setting.pushButton_6.clicked.connect(self.save_function)

    # Сохранить настройки пользователя + делаем проверку того,что вводит пользователь
    def save_function(self):
        nick = self.setting.lineEdit_4.text()
        if len(nick) >= 3 and len(nick) <= 20:
            # Закрываем окно с настройками
            self.close()
            self.signal.emit(['update_config'])
        else:
            self.setting.lineEdit_4.setText("Ник должен состоять от 3 до 20 символов")
