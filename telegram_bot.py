import requests
import time


class TelegramBot:

    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    def send_message(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={message}" \
              f"&parse_mode=markdown"
        requests.get(url)
        time.sleep(4)
