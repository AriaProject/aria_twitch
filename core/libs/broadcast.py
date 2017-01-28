import time, logging, requests, json
from threading import Thread

logger = logging.getLogger("aria_twitch")

class Broadcast(Thread):
    def __init__(self, irc, config):
        self.messages = self.get_messages()

        self.time_sleep = config['broadcast']['timesleep']
        self.irc = irc
        self.counter = 0;
        self.last_broadcast=time.time()
        self.is_stop = False
        Thread.__init__(self)
        logger.debug("Broadcast initialized")

    def get_messages(self):
        response = requests.get('http://localhost:8000/api/broadcasts')

        messages = []

        if response.status_code == 200:
            data = json.loads(response.content)
            for d in data['data']:
                messages.append(d['message'])

        return messages

    def get_next_message(self):
        message = self.messages[self.counter]
        self.counter = (self.counter + 1) % len(self.messages)
        return message


    def run(self):
        logger.info("Start Broadcasting")
        print(len(self.messages))
        if len(self.messages) > 0:
            while not self.is_stop:
                if time.time() - self.last_broadcast >= self.time_sleep:
                    message = self.get_next_message()
                    logger.info("Broadcast: %s" % message)

                    self.irc.send_message(message)

                    self.last_broadcast = time.time()
                    self.messages = self.get_messages()

        logger.info("End Broadcasting")

    def stop(self):
        logger.info("Stop Broadcasting")
        self.is_stop=True
