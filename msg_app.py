# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets

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
        self.login_thread = login.Login_Thread()

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
        ''' Вызов авторизации'''
        self.login_thread.start()