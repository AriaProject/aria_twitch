import requests, json


def banque(username):
    response = requests.get('http://localhost:8000/api/viewers/'+username)
    if response.status_code == 200:
        data = json.loads(response.content)

        return "@"+username +" vous avez actuellement "+str(data['data']['points'])+" point(s)."