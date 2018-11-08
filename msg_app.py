# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QInputDialog as dialog
from PyQt5.QtWidgets import QLineEdit as input_field
from PyQt5.QtWidgets import QMessageBox as message_box

import gui
import msg_scan
import login


class VkMessApp(QtWidgets.QWidget, gui.Ui_VkMessenger):
    '''GUI и управление потоком запросов'''

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_start.clicked.connect(self.start_scan)
        self.btn_stop.clicked.connect(self.stop_scan)
        self.thread = msg_scan.MsgScan() # Поиск в отдельном потоке
        self.thread.started.connect(self.on_started)
        self.thread.finished.connect(self.on_finished)
        self.thread.result_signal.connect(self.show_result)
        self.thread.success_signal.connect(self.success_alarm)
        self.btn_login.clicked.connect(self.login)

    def start_scan(self):
        self.thread.start()

    def stop_scan(self):
        self.thread.terminate()
        self.on_finished()

    def show_result(self, result):
        '''Добавляет запись в лог и проматывает его вниз'''
        self.log.textCursor().insertText(result)
        self.log.ensureCursorVisible()

    def on_started(self):
        ''' Вынесено из start_scan, чтобы кнопка start блокировалась только
        когда фоновый поток успешно запущен'''
        self.btn_start.setDisabled(True)
        self.btn_stop.setDisabled(False)

    def on_finished(self):
        self.btn_start.setDisabled(False)
        self.btn_stop.setDisabled(True)

    def success_alarm(self):
        '''Окно разворачивается, всплывает'''
        self.showNormal()
        self.activateWindow()

    def login(self):
        '''Getting token.

        Ask user to authenticate.
        Deliver credentials to login thread.
        Send requset with credentials to API to get token.
        Write token to a file.
        Answer wirh result message.'''

        credentials = self.authenticate_dialog()

        self.login_thread = login.Login_Thread(credentials[0],
                                               credentials[1])

        self.login_thread.notification_string.connect(
            self.notification_window)
        '''Transmit notification message from login thread
        to main thread(GUI).'''

        self.login_thread.start()
        '''Request to API and write token to the file.'''

    def authenticate_dialog(self):
        '''Input login and password.'''

        _login, ok = dialog.getText(
            None,
            'VKMessenger Authorization',
            'Type login',
            input_field.Normal
        )

        _password, ok = dialog.getText(
            None,
            'VKMessenger Authorization',
            'Type password',
            input_field.Password
        )

        return _login, _password

    def notification_window(self, text_arg):
        '''Notify about success/errors in login thread.'''
        self.display_msg = message_box()
        self.display_msg.about(self, 'Notification', text_arg)
