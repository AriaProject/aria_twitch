global config

config = {

    'server': 'irc.twitch.tv',
    'port': 6667,
    'username': 'username',
    'nickname': 'Nickname',

    'oauth_password': 'oauth',

    'channel': '#channel',

    'debug': True,

    'broadcast': {
        'active': False,
        'timesleep': 300 # time in second between each broadcast
    },

    'points': {
        'active': False,
        'timesleep': 60, # time in second between each point win
        'number': 1 # number of point win
    },

    'socket_buffer_size': 2048

}