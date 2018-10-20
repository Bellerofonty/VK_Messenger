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

        token = self.read_token()
        session = vk.Session(access_token=token)
        unread_conv_list = self.get_conversations(token, session)
        for dialog in unread_conv_list:
            history = self.get_history(dialog['id'], dialog['unread_count'], token, session)
            sender = self.get_name(dialog['id'], token, session)
            output = '{}\n'.format(history)
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

    def get_conversations(self, token, session):
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

    def get_history(self, id, unread_count, token, session):
        ''' Вернуть непрочитанные сообщения'''
        api = vk.API(session, v='5.85')
        messages_history = api.messages.getHistory(count = unread_count, user_id = id)['items'][::-1]
        history = {messages['id']: [messages['from_id'], messages['text']] for messages in messages_history}
        return history

    def get_name(self, id, token, session):
        ''' Вернуть имя и фамилию,
        (может работать как с ключом доступа пользователя,
        так и с сервисным ключом доступа)'''
        api = vk.API(session, v='5.85')
        user = api.users.get(user_id=id)
        name = user[0]['first_name'] + ' ' + user[0]['last_name']
        return name