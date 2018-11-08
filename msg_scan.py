# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread, pyqtSignal

import vk
import requests

class MsgScan(QThread):
    ''' Запросы и извлечение информации из ответов'''

    # Сигналы, связывающие этот поток с GUI
    result_signal = pyqtSignal(str)
    success_signal = pyqtSignal()

    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.delay = 5
        self.token_file = "token.txt"
        self.API_VERSION = 5.85

    def run(self):
        ''' Вызывается при запуске потока.
        Вызывать остальные методы отсюда.

        Вывод результата в лог:
            self.result_signal.emit(output)
        Сигнал о новом сообщении (окно разворачивается и всплывает):
            self.success_signal.emit()'''

        token = self.read_token()
        session = vk.Session(access_token=token)
        unread_conv_list = self.get_conversations(session)
        for dialog in unread_conv_list:
            history = self.get_history(dialog['id'], dialog['unread_count'], session)
            for messages in history.values():
                sender = self.get_name(messages[0], session)
                output = '{}: {}\n'.format(sender, messages[1])
                self.result_signal.emit(output)
                self.success_signal.emit()

    def read_token(self):
        ''' Прочитать из файла и вернуть токен для запросов'''

        try:
            with open(self.token_file) as file:
                return file.read().strip()
        except FileNotFoundError:
            self.result_signal.emit('File not found')
        except PermissionError:
            self.result_signal.emit("Permission problem")
        except IsADirectoryError:
            self.result_signal.emit("It's a directory")
        except:
            self.result_signal.emit("Something wrong")

    def get_conversations(self, session):
        ''' Получить последние диалоги,
        вернуть те, где есть непрочитанные сообщения'''

        ''' Если диалог с юзером (не чат), вернуть:
        "id"
        "unread_count"
        для каждого диалога
        '''
        unread_conv_list = []
        # Вероятно версию API стоит вынести в отдельную переменную для всех методов
        api = vk.API(session, v='5.85')
        # Получаем непрочитанные диалоги
        response_dialogs = api.messages.getConversations(filter='unread')
        for count in range(response_dialogs.get('count')):
            unread_count = ((response_dialogs.get('items')[count]).get('conversation')).get('unread_count')
            id = (((response_dialogs.get('items')[count]).get('conversation')).get('peer')).get('id')
            # Проверка на чат
            if ((response_dialogs.get('items')[count]).get('conversation')).get('chat_settings') is None:
                unread_conv_list.append({'id': id, 'unread_count': unread_count})
        # Возврат списка словарей в виде {id пользователя: Кол-во непрочитанных}
        return unread_conv_list

    def get_history(self, id, unread_count, session):
        ''' Вернуть непрочитанные сообщения'''
        api = vk.API(session, v='5.85')
        messages_history = api.messages.getHistory(count = unread_count, user_id = id)['items'][::-1]
        history = {messages['id']: [messages['from_id'], messages['text']] for messages in messages_history}
        return history

    def get_name(self, id, session):
        ''' Вернуть имя и фамилию,
        (может работать как с ключом доступа пользователя,
        так и с сервисным ключом доступа)'''
        api = vk.API(session, v='5.85')
        user = api.users.get(user_id=id)
        name = user[0]['first_name'] + ' ' + user[0]['last_name']
        return name

    def mark_as_read(self, id, token):

        base_string = "https://api.vk.com/method/{}?"
        params  = {'access_token' : token, 'v' : self.API_VERSION, 'peer_id' : id}
        method = "messages.markAsRead"
        try:
            #params.update('peer_id' : id)
            request = requests.get(base_string.format(method), params=params).json()
            #print(request)
            if 'response' in request:
                return request['response']
            elif 'error' in request:
                raise Exception(str(request['error']['error_msg']))
        except Exception as e:
            #print(e.args)
            self.result_signal.emit(str(e.args))
