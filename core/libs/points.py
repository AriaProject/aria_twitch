from threading import Thread
import time, requests, json, logging

logger = logging.getLogger("aria_twitch")

class PointsCRON(Thread):
    def __init__(self, config):

        self.number = config['points']['number']
        self.is_stop = False
        self.time_sleep = config['points']['timesleep']
        Thread.__init__(self)
        self.last_gain = time.time()
        logger.debug("Points CRON initialized")

    def run(self):
        logger.info("Start Points CRON")

        while not self.is_stop:
            if time.time() - self.last_gain  >= self.time_sleep:
                response = requests.get('https://tmi.twitch.tv/group/user/dtthibaud/chatters')
                viewers = []
                if response.status_code == 200:
                    data = json.loads(response.content)

                    for viewer in data["chatters"]["viewers"]:
                        viewers.append(viewer)
                    for viewer in data["chatters"]["moderators"]:
                        viewers.append(viewer)

                d = {
                    'number':self.number,
                    'viewers':viewers
                }

                response = requests.post('http://localhost:8000/api/viewers/increment', json=d)
                if response.status_code == 200:
                    logger.debug("Point CRON response : %s " % response.content)
                    logger.info("Point CRON increment success")
                else:
                    logger.error("Point CRON increment error")

                self.last_gain = time.time()

        logger.info("End Points CRON")

    def stop(self):
        logger.info("Stop Points CRON")
        self.is_stop=True