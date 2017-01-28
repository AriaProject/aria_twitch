import importlib, requests, json

class CommandProvider:

    def exist(self, command):
        response = requests.get("http://localhost:8000/api/commands/"+command)
        return response.status_code == 200

    def get_command(self, command):
        response = requests.get("http://localhost:8000/api/commands/" + command)
        if response.status_code == 200:
            return json.loads(response.content)['data']

    def has_args(self, command):
        return command['argc'] > 0

    def has_correct_argc(self, command, args):
        return len(args) == command['argc']

    def has_command_return(self, command):
        return command['return'] == 'command'

    def run(self, command, username, args=None):

        command = self.get_command(command)

        if self.has_command_return(command):
            command_clean = command['commands'].replace('!', '')

            module = importlib.import_module('core.commands.%s' % command_clean)
            function = getattr(module, command_clean)

            if args:
                if self.has_args(command) and self.has_correct_argc(command, args):
                    return function(args, username=username)
            else:
                return function(username=username)
        else:
            return command['return']
