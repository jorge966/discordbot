import requests
import json

url = 'https://www.pathofexile.com/character-window/get-characters?accountName=OkBread'
poe_web = requests.get(url)

json_data = json.loads(poe_web.text)
current_league = None
lastactive = None
league = None
name = None

user_name = None
ascendency = None
level = None
league = None
for character in json_data:
    for key, value in character.items():
        if key == 'lastActive':
            print(character)
            user_name = character['name']
            league = character['league']
            ascendency = character['class']
            level = str(character['level'])

print(type(user_name))
print(type(level))
print(type(ascendency))
print(type(league))






