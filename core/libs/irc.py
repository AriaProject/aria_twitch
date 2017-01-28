# coding: utf8


import socket, re, time, sys, logging

logger = logging.getLogger("aria_twitch")

class irc:
    def __init__(self, config):
        self.config = config

    def check_for_message(self, data):
        if re.match(
                r'^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+(\.tmi\.twitch\.tv|\.testserver\.local) PRIVMSG #[a-zA-Z0-9_]+ :.+$',
                data):
            return True

    def get_message(self, data):
        return {
            'channel': re.findall(r'^:.+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+.+ PRIVMSG (.*?) :', data)[0],
            'username': re.findall(r'^:([a-zA-Z0-9_]+)\!', data)[0],
            'message': re.findall(r'PRIVMSG #[a-zA-Z0-9_]+ :(.+)', data)[0].decode('utf8')
        }

    def check_for_ping(self, data):
        if data[:4] == "PING":
            self.sock.send('PONG')

    def check_login_status(self, data):
        if re.match(r'^:(testserver\.local|tmi\.twitch\.tv) NOTICE \* :Login unsuccessful\r\n$', data):
            return False
        else:
            return True

    def send_message(self, message):
        self.sock.send('PRIVMSG %s :%s\n' % (self.config['channel'], message.encode('utf-8')))

    def get_irc_socket_object(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)

        self.sock = sock

        try:
            sock.connect((self.config['server'], self.config['port']))
        except:
            logger.info('Cannot connect to server (%s:%s).' % (self.config['server'], self.config['port']), 'error')
            sys.exit()

        sock.settimeout(None)

        sock.send('USER %s\r\n' % self.config['username'])
        sock.send('PASS %s\r\n' % self.config['oauth_password'])
        sock.send('NICK %s\r\n' % self.config['nickname'])

        if self.check_login_status(sock.recv(1024)):
            logger.info('Login successful.')
        else:
            logger.info('Login unsuccessful. (hint: make sure your oauth token is set in self.config/self.config.py).', 'error')
            sys.exit()


        self.join_channel()

        return sock

    def join_channel(self):
        logger.info('Joining channels %s.' % self.config['channel'])
        self.sock.send('JOIN %s\r\n' % self.config['channel'])
        logger.info('Joined channels.')

    def leave_channel(self):
        logger.info('Leaving chanels %s,' % self.config['channel'])
        self.sock.send('PART %s\r\n' % self.config['channel'])
        logger.info('Left channels.')