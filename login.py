#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Script wrote to get access_token for VkMessenger app.
Mostly code based on using vk module https://github.com/dimka665/vk
by https://pypi.org/user/dimka.dimka/.

Author: Ivan Kovalenko
Email:  kovalenko_ivan@hotmail.com
Last edited: October 2018
'''

import vk
from vk.exceptions import VkAuthError

import sys

from queue import Queue

from PyQt5.QtCore import \
    Qt, \
    QThread, \
    pyqtSignal

from PyQt5.QtWidgets import \
    QInputDialog,\
    QLineEdit,\
    QApplication,\
    QPushButton,\
    QMessageBox,\
    QWidget

'''
Applications ID. Is necessary for auth procedure.
ID приложения. Необходим для процедуры авторизации.
'''
CLIENT_ID = '6713283'

q = Queue()
'''Make a queue to exchange values between threads.
Создание очереди для обмена значениями между потоками.'''


class Test_GUI(QWidget):
    '''GUI class ONLY for TESTING login thread consistency.
    Создание GUI для ТЕСТИРОВАНИЯ потока идентификации.'''
    def __init__(self, parent=None):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Test_GUI')

        btn_login = QPushButton('Login', self)
        '''Minimalistic login button.
        Минималистичная кнопка залогинивания.'''
        btn_login.clicked.connect(self.login_clicked)

    def login_clicked(self):
        self.call_login_thread = Login_Thread()
        '''Use self.<> because of making reference for not being
        thrown away by garbage collector after handling __init__.
        Использовать self.<> в упоминании метода, чтобы сборщик
        мусора не выкинул поток после первого прохода __init__.'''

        '''Signals connected to internal methods.
        Сигналы, законнекченные к внутренним методам.'''
        self.call_login_thread.\
            success_signal.connect(self.show_signal)
        self.call_login_thread.\
            result_signal.connect(self.show_signal)
        self.call_login_thread.\
            login_signal.connect(self.login_signal)

        self.call_login_thread.start()

    def show_signal(self, text_arg):
        '''Notify about success/error in thread.
        Извещение о успехе/ошибке в потоке.'''
        self.display_msg = QMessageBox()
        self.display_msg.about(self, 'Notification', text_arg)

    def login_signal(self):
        '''Method of getting VK user credentials. Carried out to
        GUI to avoid QTimer error, because it is deprecated to call
        any GUI functions from thread other than the main thread.
        Метод получения имени и пароля пользователя VK;
        Вынесен в GUI, чтобы избежать ошибки QTimer error, потому
        как вызов функций GUI разрешён только из главного потока.'''
        login, ok = QInputDialog.getText(
            None,
            'VKMessenger Authorization',
            'type {}'.format('Login'),
            QLineEdit.Normal
        )

        password, ok = QInputDialog.getText(
            None,
            'VKMessenger Authorization',
            'type {}'.format('Password'),
            QLineEdit.Password
        )

        '''Put credentials to queue to get them from another thread.
        Кладём переменные в очередь, чтобы использовать их в
        другом потоке.'''
        q.put(login)
        q.put(password)

    def keyPressEvent(self, event):
        '''Simple method for usability. Press 'q' to quit GUI.
        Простой метод для использования кнопки для выхода из GUI.'''
        if event.key() == Qt.Key_Q:
            self.close()


class Login_Thread(QThread):
    '''QThread subclass, giving file object with access_token inside.
    Поток, выдающий объект - файл txt с токеном.'''

    success_signal = pyqtSignal(str)
    result_signal = pyqtSignal(str)
    login_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__()

    def run(self):
        '''Main method of thread.
        Основной метод потока.'''
        try:
            self._get_credentials()

            '''Geting values from queue.
            Получаем значения, отправленные раннее в очередь.'''
            _login = q.get()
            _password = q.get()

            token = self._request_token(_login, _password)

            self._write_token_to_file(token)

            self.success_signal.emit(
                'Token has been written\n'
                'Токен записан в файл')

        except VkAuthError:
            self.result_signal.emit(
                'Not valid login or password\n'
                'Неверный логин или пароль')

        self.exit()  # or could use sys.exit()
        '''Close Thread. Закрытие потока.'''

    def _get_credentials(self):
        '''Detach operations to main thread.
        Передача действий в главный поток.'''
        self.login_signal.emit()

    def _request_token(self, login, password):
        '''Start auth session by requests to VK API.
        Инициализация сессии авторизации запросами к VK API.'''
        self.session = vk.AuthSession(
            app_id=CLIENT_ID,
            user_login=login,
            user_password=password,
            scope='4096',
        )

        return self.session.get_access_token()

    def _write_token_to_file(self, token):

        with open('token.txt', 'w+') as f:
            f.write(token)

            '''TO-DO.
            Requesting to add as needed.
            Запрос на добавление записи timestamp о получении токена.
            + datetime.now().strftime('_%Y.%m.%d_%H:%M:%S_')))'''

        return None


if __name__ == '__main__':

    test_app = QApplication(sys.argv)

    test_login = Test_GUI()
    test_login.show()

    sys.exit(test_app.exec_())
