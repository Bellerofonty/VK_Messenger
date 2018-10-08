# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets

import gui
import msg_scan

class VkMessApp(QtWidgets.QWidget, gui.Ui_VkMessenger):
    '''GUI и управление потоком запросов'''

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_start.clicked.connect(self.start_scan)
        self.btn_stop.clicked.connect(self.stop_scan)
        self.btn_login.clicked.connect(self.login)
        self.thread = msg_scan.MsgScan() # Поиск в отдельном потоке
        self.thread.result_signal.connect(self.show_result)
        self.thread.success_signal.connect(self.success_alarm)

    def start_scan(self):
        self.thread.start()

    def stop_scan(self):
        self.thread.terminate()
        self.on_finished()

    def show_result(self, result):
        '''Добавляет запись в лог и проматывает его вниз'''
        pass

    def success_alarm(self):
        '''Окно разворачивается, всплывает'''
        pass

    def login(self):
        ''' Вызов авторизации'''
        pass