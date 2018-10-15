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
import sys
from datetime import datetime


from PyQt5.QtWidgets import \
    QInputDialog,\
    QLineEdit,\
    QApplication

'''
Applications ID. Is necessary for auth procedure.
ID приложения. Необходим для процедуры авторизации.
'''
CLIENT_ID = '6713283'


class Token:
    '''
    Class giving file txt object with access_token inside.
    Класс, выдающий объект - файл txt с токеном.
    '''
    def __init__(self):

        self.app_dialog = QApplication(sys.argv)
        ''' Initialize QApp for QInputDialogs.
        Инициализация QApp сущности для QInputDialogs диалогов.'''

        self.write_token_to_file()

    def get_credentials(self):
        '''
        Method of getting VK user credentials.
        Метод получения имени и пароля пользователя VK.
        '''
        _login, ok = QInputDialog.getText(
            None,
            'VKMessenger Authorization',
            'type {}'.format('Login'),
            QLineEdit.Normal
        )

        _password, ok = QInputDialog.getText(
            None,
            'VKMessenger Authorization',
            'type {}'.format('Password'),
            QLineEdit.Password
        )

        return _login, _password

    def write_token_to_file(self):
        _login, _password = self.get_credentials()

        '''
        Start auth session by requests to VK API.
        Инициализация сессии авторизации запросами к VK API.
        '''
        self.session = vk.AuthSession(
            app_id=CLIENT_ID,
            user_login=_login,
            user_password=_password,
            scope='4096'
        )

        with open('token.txt', 'w+') as f:
            f.write(str(self.session.get_access_token() +
                        datetime.now().strftime('_%Y.%m.%d_%H:%M:%S_')))

        return sys.exit('That`s it: token is placed in a file!')
        '''
        Code freeze without that essential string. Need research.
        Надо выяснить, почему скрипт не завершается без этой строки.
        '''


if __name__ == '__main__':

    token = Token()
