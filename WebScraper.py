from bs4 import BeautifulSoup
import requests

poe_web = requests.get("https://www.pathofexile.com/account/view-profile/jorge9661/characters")

data = poe_web.text

soup = BeautifulSoup(data)

for item in soup:
    print()




#print(soup.prettify())