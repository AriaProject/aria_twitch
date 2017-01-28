#!/usr/bin/env python

import logging,sys, argparse, signal
from core.main import AriaTwitch
from core.config import *

logger = logging.getLogger("aria_twitch")

def config_logger(debug=None):
    logger = logging.getLogger("aria_twitch")
    logger.propagate = False
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    ch.setFormatter(formatter)

    # add the handlers to logger
    logger.addHandler(ch)

    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)


    logger.debug("Logger ready")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Aria Twitch Bot')
    parser.add_argument("--debug", action='store_true', help="Show debug output")

    args = parser.parse_args()

    config_logger(args.debug)

    bot = AriaTwitch(config)

    def signal_handler(signal, frame):
        print "\n"
        logger.info("Ctrl+C pressed. Killing Aria Bot")
        bot.stop()
        sys.exit(0)

    # catch signal for killing on Ctrl+C pressed
    signal.signal(signal.SIGINT, signal_handler)

    bot.run();