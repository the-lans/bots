import requests  
import datetime

class BotHandler:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        resp = requests.get(self.api_url + 'getUpdates', {'timeout': timeout, 'offset': offset})
        return resp.json()['result']

    def send_message(self, chat_id, text):
        return requests.post(self.api_url + 'sendMessage', {'chat_id': chat_id, 'text': text})

    def get_last_update(self, offset=None, timeout=30):
        get_result = self.get_updates(offset, timeout)
        return (get_result[-1] if len(get_result) > 0 else None)

greet_bot = BotHandler("id_bot")
greetings = ('здравствуй', 'привет', 'ку', 'здорово', 'hello')

def run(new_offset):
    last_update = greet_bot.get_last_update(new_offset)
    if last_update == None:
        return new_offset

    last_update_id = last_update['update_id']
    last_chat_text = last_update['message']['text']
    last_chat_id = last_update['message']['chat']['id']
    last_chat_name = last_update['message']['chat']['first_name']

    now = datetime.datetime.now()
    lower_text = last_chat_text.lower()
    print(last_chat_text)

    if lower_text in greetings and 0 <= now.hour < 6:
        greet_bot.send_message(last_chat_id, 'Доброй ночи, {}'.format(last_chat_name))
    elif lower_text in greetings and 6 <= now.hour < 12:
        greet_bot.send_message(last_chat_id, 'Доброе утро, {}'.format(last_chat_name))
    elif lower_text in greetings and 12 <= now.hour < 18:
        greet_bot.send_message(last_chat_id, 'Добрый день, {}'.format(last_chat_name))
    elif lower_text in greetings and 18 <= now.hour < 24:
        greet_bot.send_message(last_chat_id, 'Добрый вечер, {}'.format(last_chat_name))

    return last_update_id + 1

if __name__ == '__main__':
    print("HelloBot run...")
    new_offset = None

    while True:
        try:
            new_offset = run(new_offset)
        except KeyboardInterrupt:
            print("HelloBot exit: KeyboardInterrupt")
            exit()
        except Exception:
            print("HelloBot exit: Exception")
            new_offset = None
            continue
