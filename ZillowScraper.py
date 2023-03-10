import requests
from time import sleep
from random import randint

urls = []
f = open('urls.txt', 'r')
Lines = f.readlines()

for line in Lines:
    urls.append(line.strip())

f.close()
from bs4 import BeautifulSoup

headers = {
    'accept': 'text/html',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0'
}

for url in urls:
    sleep(randint(1,2)) #Wait random time to avoid 'You are not human'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    def remove_tags(html):
        for data in html(['style', 'script']):
            data.decompose()

        return ' '.join(html.stripped_strings)

    soup = remove_tags(soup)
    soup = soup.replace(',', '')
    string = str(soup)
    string = string[string.index(" bd ") - 1:]
    index = string.index("Zestimate")
    string = string[:index + 22]
    house = {
        "address": string[(string.index("sqft") + 5):(string.index("IN") + 8)],
        "zestimate": string[(index + 15):len(string) + 1],
        "sqft": string[(string.index("ba") + 3):(string.index(" sqft"))],
        "bds": string[:string.index(" ")],
        "bths": string[(string.index("bd ") + 3):(string.index(" ba"))],
    }
    print(house["address"] + "," + house["zestimate"] + "," + house["sqft"] + "," + house["bds"] + "," + house["bths"])
