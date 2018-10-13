
    def get_history(self, id, unread_count, token):
        ''' Вернуть непрочитанные сообщения'''
        session = vk.Session(access_token=token)
        api = vk.API(session, v='5.85')
        messages_history = api.messages.getHistory(count = unread_count, user_id = id)['items'][::-1]
        history = {messages['id']:[messages['from_id'], messages['text']] for messages in messages_history}
        return history

