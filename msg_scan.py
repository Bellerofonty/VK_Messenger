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
        unread_conv_list = []
        session = vk.Session(access_token=token)
        # Вероятно версию API стоит вынести в отдельную переменную для всех методов
        api = vk.API(session, v='5.85')
        # Получаем непрочитанные диалоги
        response_dialogs = api.messages.getConversations(filter='unread')
        for count in range(response_dialogs.get('count')):
            unread_count = ((response_dialogs.get('items')[count]).get('conversation')).get('unread_count')
            id = (((response_dialogs.get('items')[count]).get('conversation')).get('peer')).get('id')
            # Проверка на чат
            if ((response_dialogs.get('items')[count]).get('conversation')).get('chat_settings') is None:
                unread_conv_list.append({id: unread_count})
        # Возврат списка словарей в виде {id пользователя: Кол-во непрочитанных}
        return unread_conv_list

    def get_history(self, id, unread_count, token):
        ''' Вернуть непрочитанные сообщения'''
        session = vk.Session(access_token=token)
        api = vk.API(session, v='5.85')
        messages_history = api.messages.getHistory(count = unread_count, user_id = id)['items'][::-1]
        history = {messages['id']:[messages['from_id'], messages['text']] for messages in messages_history}
        return history

    def get_name(self, id, token):
        ''' Вернуть имя и фамилию,
        (может работать как с ключом доступа пользователя,
        так и с сервисным ключом доступа)'''
        session = vk.Session(access_token=token)
        api = vk.API(session, v='5.85')
        user = api.users.get(user_id=id)
        name = user[0]['first_name'] + ' ' + user[0]['last_name']
        return name