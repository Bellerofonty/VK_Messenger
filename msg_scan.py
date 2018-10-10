# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread, pyqtSignal

import vk

class MsgScan(QThread):
    ''' Запросы и извлечение информации из ответов'''

    # Сигналы, связывающие этот поток с GUI
    result_signal = pyqtSignal(str)
    success_signal = pyqtSignal()

    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.delay = 5

    def run(self):
        ''' Вызывается при запуске потока.
        Вызывать остальные методы отсюда.

        Вывод результата в лог:
            self.result_signal.emit(output)
        Сигнал о новом сообщении (окно разворачивается и всплывает):
            self.success_signal.emit()'''

    def read_token(self):
        ''' Прочитать из файла и вернуть токен для запросов'''

##        return token

    def get_conversations(self, token):
        ''' Получить последние диалоги,
        вернуть те, где есть непрочитанные сообщения'''

        ''' Если диалог с юзером (не чат), вернуть:
        "id"
        "unread_count"
        для каждого диалога
        '''

##        return unread_conv_list

    def get_history(self, id, unread_count, token):
        ''' Вернуть непрочитанные сообщения'''

##        return messages

    def get_name(self, id, token):
        ''' Вернуть имя и фамилию,
        (может работать как с ключом доступа пользователя,
        так и с сервисным ключом доступа)'''
        session = vk.Session(access_token=token)
        api = vk.API(session, v='5.85')
        user = api.users.get(user_id=id)
        name = user[0]['first_name'] + ' ' + user[0]['last_name']
        return name

#сервисный ключ доступа (постоянный)
token1 = 'b4c325c5b4c325c5b4c325c5f4b4a5a586bb4c3b4c325c5ef7d6e8321dd82c069e344a5'
#ключ доступа пользователя (временный)
token2 = 'a6a1493a15fca6c13035e79bd10bf039bde3526983a217cfb909b4364888a97b0451b68c01130369f2a2f'
my_id = 2318509

msg_scan = MsgScan()
print(msg_scan.get_name(my_id, token1))

















