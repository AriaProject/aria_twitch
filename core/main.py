import libs.irc as irc_
import logging, pprint, thread
from core.commands_profider import CommandProvider
from core.libs.broadcast import Broadcast
from core.libs.points import PointsCRON

logger = logging.getLogger("aria_twitch")

class AriaTwitch:

    def __init__(self, config):
        self.config = config
        self.irc = irc_.irc(config)
        self.socket = self.irc.get_irc_socket_object()
        self.command_provider = CommandProvider()
        self.broadcast = Broadcast(self.irc, self.config)
        self.points = PointsCRON(self.config)

    def run(self):
        irc = self.irc
        sock = self.socket
        config = self.config

        irc.send_message("Bonjour DTThibaud.")

        if self.config['broadcast']['active']:
            self.broadcast.start()

        if self.config['points']['active']:
            self.points.start()

        while True:
            data = sock.recv(config['socket_buffer_size']).rstrip()

            if len(data) == 0:
                logger.info('Connection was lost, reconnecting.')
                sock = self.irc.get_irc_socket_object()

            if config['debug']:
                print data

            if irc.check_for_message(data):
                message_dict = irc.get_message(data)

                message = message_dict['message']
                username = message_dict['username']

                logger.info("Receive ["+username+" : "+message+"]")
                command = message.split(' ')

                if self.command_provider.exist(command[0]):

                    if len(command) > 1:
                        message_back = self.command_provider.run(command[0], username, command[1:])
                    else:
                        message_back = self.command_provider.run(command[0], username)

                    if message_back != None:
                        self.irc.send_message(message_back)

    def stop(self):
        self.irc.leave_channel()
        self.broadcast.stop()
        self.points.stop()