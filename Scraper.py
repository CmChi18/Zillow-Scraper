import requests
from bs4 import BeautifulSoup
from time import sleep
import random

counter = 0

userAgents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0.2",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0.3 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/77.0.4054.277",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.62",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Mozilla/5.0 (X11; Ubuntu; Linux aarch64; rv:109.0) Gecko/20100101 Firefox/114.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/96.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/96.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/97.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/97.0",
]


f = open('Addresses.csv', 'r')

current = open('start-num.txt', 'r')
currentNum = int(current.readline())
current.close()
print(currentNum)

lines = f.readlines()

headers = {
        'Accept': 'text/html',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'www.zillow.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': random.choice(userAgents)
    }

def nextAgent(): #Cycles to the next agent in the list
   index = userAgents.index(headers['User-Agent'])
   if index == (len(userAgents) - 1):
       index = 0
   else:
       index += 1
   headers['User-Agent'] = userAgents[index]
   print(headers['User-Agent'])

while currentNum < len(lines):

    try:
        sleep(random.randint(1,2)) #Wait random time to avoid 'You are not human'
        headers['User-Agent'] = random.choice(userAgents) #Chooses random agent to avoid denied access
        
        parsed = lines[currentNum].replace('\n', '')
        parsed = parsed.replace('"', '')
        
        parsed = parsed.split(',')
        print(parsed)
        print(headers['User-Agent'])
        
        search_query = parsed[0].replace(' ', '-')
        
        url = f"https://www.zillow.com/homes/{search_query}-Carmel-IN-{parsed[1]}_rb/"
        print(url)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        
        if 'denied' in str(soup):
            continue
            nextAgent()
            counter += 1
            if counter == len(userAgents):
                print('abort')
                break
            continue
            
        counter = 0
        
        print(currentNum)
        currentNum += 1
        numf = open('start-num.txt', 'w')
        numf.write(f'{currentNum}')
        numf.close()
        
        
        zest = soup.find('span', class_='Text-c11n-8-89-0__sc-aiai24-0 cfmKEe')
        if zest == None:
            zest = soup.find('span', class_='Text-c11n-8-84-0__sc-aiai24-0 gTVYcr')
        zest = zest.text.replace(',', '')
        bby = soup.find('span', {'data-testid': 'bed-bath-beyond'})
        bby = bby.find_all('span', 'Text-c11n-8-89-0__sc-aiai24-0 UtIzR')
        if bby == []:
           bby = soup.find('span', {'data-testid': 'bed-bath-beyond'})
           bby = bby.find_all('span', 'Text-c11n-8-84-0__sc-aiai24-0 fsXIkY')
        
        if 'None' in zest or not '$' in zest:
            print('Nothing here')
            continue
        
        bd = bby[0].text.replace(' bd', '')
        bth = bby[1].text.replace(' ba', '')
        sqft = bby[2].text.replace(',', '')
        sqft = sqft.replace(' sqft', '')
        addr = parsed[0] + '., Carmel IN ' + parsed[1]
        for p, r in rules.items():
                addr = addr.replace(p, r)
        print(f'{addr} {zest} {bd} {bth} {sqft}')  
        
        listings = open('listings.csv', 'a')
        listings.write(f'{addr},{zest},{bd},{bth},{sqft},{parsed[2]},{url}' + '\n')
    except (IndexError, AttributeError) as e:
        print(f'Data could not be found: {e}')
        continue
    except ConnectionError:
    	print('connection reset trying again')
    	continue
    except KeyboardInterrupt:
    	print('\n' + 'Stopping scraper..' + '\n')
    	break

file = open('listings.csv', 'r')
lines = file.readlines()

for i in range(len(lines)): #Split listings into files of size 2000 to import to google maps if desired
    if i % 2000 == 0:
    	file.close()
    	file = open(f'Saved-Urls/listings-zone{int((i / 2000) + 1)}.csv', 'w')
    	file.write('Address,Location,Zestimate,Bd,Bth,Sqft,Subdivision,Url' + '\n')
    file.write(lines[i])
    
file.close()
