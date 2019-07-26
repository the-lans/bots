from flask import Flask, request, Response

from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage

from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest

import time
import logging
import sched
import threading

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask(__name__)
viber = Api(BotConfiguration(
    name='ChickenStoreBot',
    avatar='https://iplaces.ru/AvatarChicken.jpg',
    auth_token='49fe7d423d67d422-31dda79e9d6248e7-300c2231ba176c71'
))

@app.route('/deploy', methods=['POST'])
def incoming():
    logger.debug("received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # this library supplies a simple way to receive a request object
    viber_request = viber.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message
        # lets echo back
        viber.send_messages(viber_request.sender.id, [
            message
        ])
    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.get_user.id, [
            TextMessage(text="Спасибо за подписку!")
        ])
    elif isinstance(viber_request, ViberFailedRequest):
        logger.warning("Клиент не получил сообщение. Отказ: {0}".format(viber_request))

    return Response(status=200)

def set_webhook(viber):
    event_types = viber.set_webhook('https://iplaces.ru:443/deploy')
    print("Webhook")
    print(event_types)

if __name__ == "__main__":
    print("Bot run...")
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(5, 1, set_webhook, (viber,))
    t = threading.Thread(target=scheduler.run)
    t.start()

    context = ('server.crt', 'server.key')
    app.run(host='176.57.216.209', port=443, debug=True, ssl_context=context)
    print("End bot!")
