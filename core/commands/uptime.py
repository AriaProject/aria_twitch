import requests, json, pprint, datetime


def uptime(username):
    response = requests.get("https://api.twitch.tv/kraken/streams/dtthibaud",
                            headers={'Client-ID': 'ptek5873bsbl4kp3ykgmofpdnh6mn6'})
    data = json.loads(response.content)

    if data['stream'] != 'null':
        timedelta = datetime.datetime.utcnow() - datetime.datetime.strptime(data['stream']['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        return "L'uptime est de "+str(timedelta).split('.')[0]
    else:
        return "Le stream est actuellement offline"