import requests
import json
import configparser as cfg


class telegram_chatbot():

    def __init__(self, config):
        self.token = self.read_token_from_config_file(config)
        self.base = "https://api.telegram.org/bot{}/".format(self.token)

    def get_updates(self, offset=None):
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url)
        return json.loads(r.content)

    def send_reply(self, msg, message_id, chat_id):
        url = self.base + "sendMessage?chat_id={}&reply_to_message_id={}&text={}".format(chat_id, message_id, msg)
        print(url)
        if msg is not None:
            requests.get(url)

    def send_message(self, chat_id, msg):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            requests.get(url)

    def read_token_from_config_file(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', 'token')

    def ban(self, user_id, chat_id):
        url = self.base + "banChatMember?chat_id={}&user_id={}".format(chat_id, user_id)
        print(url)
        requests.get(url)

    def user_restrict(self, user_id, chat_id):
        url = self.base + "getChatMember?chat_id={}&user_id={}".format(chat_id, user_id)
        print(url)
        r = requests.get(url)
        print(r.content)
        return json.loads(r.content)
