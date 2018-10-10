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
        # self.get_conversations(self.read_token())
        self.get_history(id, unread_count, self.read_token())
        # id - пользователя с кем выдать историю
        # unread_count получить откуда то или задать вручную

        Вывод результата в лог:
            self.result_signal.emit(output)
        Сигнал о новом сообщении (окно разворачивается и всплывает):
            self.success_signal.emit()'''

    def read_token(self):
        ''' Прочитать из файла и вернуть токен для запросов'''
        return 'token'
        # тут может быть ваш токен

##        return token

    def get_conversations(self, token):
        ''' Получить последние диалоги,
        вернуть те, где есть непрочитанные сообщения'''

        ''' Если диалог с юзером (не чат), вернуть:
        "id"
        "unread_count"
        для каждого диалога
        '''
        session = vk.Session(access_token=token)
        api = vk.API(session, v='5.85')
        # Получаем непрочитанные диалоги
        response_dialogs = api.messages.getConversations(filter='unread')
        for count in range(response_dialogs.get('count')):
            # print(response_dialogs)
            unread_count = ((response_dialogs.get('items')[count]).get('conversation')).get('unread_count')
            id = (((response_dialogs.get('items')[count]).get('conversation')).get('peer')).get('id')
            print(id)
            print(unread_count)

##        return unread_conv_list

    def get_history(self, id, unread_count, token):
        ''' Вернуть непрочитанные сообщения'''
        session = vk.Session(access_token=token)
        api = vk.API(session, v='5.85')
        messages_history = api.messages.getHistory(count = unread_count, user_id = id)['items'][::-1]
        my_name = self.get_name(None, token)
        id_name = self.get_name(id, token)
        for messages in messages_history:
            print((id_name if messages['from_id'] == id else my_name) + ': ' + messages['text'])

    def get_name(self, id, token):
        ''' Вернуть имя и фамилию'''
        session = vk.Session(access_token=token)
        api = vk.API(session, v='5.85')
        name = api.users.get(user_id = id)
        return name[0]['first_name'] + ' ' + name[0]['last_name']


msg_scan = MsgScan()
msg_scan.run()
