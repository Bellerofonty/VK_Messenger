import vk
from vk.exceptions import VkAuthError

from PyQt5.QtCore import \
    QThread, \
    pyqtSignal


CLIENT_ID = '6713283'  # Applications ID


class Login_Thread(QThread):

    notification_string = pyqtSignal(str)

    def __init__(self, _login, _password, parent=None):
        super(QThread, self).__init__()
        self._login = _login
        self._password = _password

    def run(self):
        '''Main method of thread.'''
        try:
            token = self._request_token(self._login,
                                        self._password)

            result_string = self._write_token_to_file(token)

            self.notification_string.emit(result_string)

        except VkAuthError:
            self.notification_string.emit(
                'Not valid login or password\n'
                'Неверный логин или пароль')

        self.exit()  # or could use sys.exit()
        '''Exit Thread.'''

    def _request_token(self, login, password):
        '''Start auth session, send request to API.'''

        self.session = vk.AuthSession(
            app_id=CLIENT_ID,
            user_login=login,
            user_password=password,
            scope='4096',
        )

        return self.session.get_access_token()

    def _write_token_to_file(self, token):

        with open('token.txt', 'w+') as f:
            f.write(token)

        return \
            'Token has been written\n'\
            'Токен записан в файл'
