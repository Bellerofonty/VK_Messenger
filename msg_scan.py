# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread, pyqtSignal

class MsgScan(QThread):
    ''' Запросы и извлечение информации из ответов'''

    # Сигналы, связывающие этот поток с GUI
    result_signal = pyqtSignal(str)
    success_signal = pyqtSignal()

    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        self.delay = 5
        self.token_file = "token.txt"
        self.token = self.read_token()

    def run(self):
        ''' Вызывается при запуске потока.
        Вызывать остальные методы отсюда.

        Вывод результата в лог:
            self.result_signal.emit(output)
        Сигнал о новом сообщении (окно разворачивается и всплывает):
            self.success_signal.emit()'''

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
        ''' Вернуть имя и фамилию'''

##        return name

    

if __name__ == "__main__":
    pass
