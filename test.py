import requests

r = requests.get("https://api.opendota.com/api/players/92576390/matches")
t = requests.get("https://api.opendota.com/api/players/92576390/recentMatches")

print(t.text)