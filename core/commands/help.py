import requests,json

def help(username):
    response = requests.get('http://localhost:8000/api/commands')
    if response.status_code == 200:
        data = json.loads(response.content)
        commands = []
        for d in data['data']:
            commands.append(d['commands'])


    return "Voici la liste des commandes disponible sur le chat :" + ",".join(commands)