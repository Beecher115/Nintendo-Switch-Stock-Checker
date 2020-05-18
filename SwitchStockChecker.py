import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Littlewoods robots.txt allows scraping but not without a User Agent
headers = {
    "User-Agent": "" # Removed for privacy
}

# Web pages on Smyths website for Nintendo Switch
smyths = {
    'Grey' : 'https://www.smythstoys.com/ie/en-ie/video-games-and-tablets/nintendo-gaming/nintendo-switch/nintendo-switch-consoles/nintendo-switch-grey-with-improved-battery-life/p/182023',
    'Neon' : 'https://www.smythstoys.com/ie/en-ie/video-games-and-tablets/nintendo-gaming/nintendo-switch/nintendo-switch-consoles/nintendo-switch-neon-red-blue-with-improved-battery-life/p/182022',
    'Animal Crossing' : 'https://www.smythstoys.com/ie/en-ie/video-games-and-tablets/nintendo-gaming/nintendo-switch/nintendo-switch-consoles/nintendo-switch-animal-crossing-limited-edition-console/p/187118'
    }

# Web pages on GameStop website for Nintendo Switch
gamestop = {
    'Grey (used)' : 'https://www.gamestop.ie/Switch/Games/51568/nintendo-switch-grey-console',
    'Neon (used)' : 'https://www.gamestop.ie/Switch/Games/62061/nintendo-switch-red-blue-console',
    'Grey' : 'https://www.gamestop.ie/Switch/Games/73198/nintendo-switch-1-1-grey-console',
    'Neon' : 'https://www.gamestop.ie/Switch/Games/73274/nintendo-switch-1-1-red-blue-console',
    'Animal Crossing' : 'https://www.gamestop.ie/Switch/Games/74210/nintendo-switch-animal-crossing-new-horizons-console-bundle'
}

# Web page on Littlwoods listing Nintendo products
littlewoods = {
    'Listing' : 'https://www.littlewoodsireland.ie/gaming-dvd/nintendo-switch-consoles/e/b/127568.end?sort=price,0'
}

# Smyths website parser
# Will parse each page of Switch type and check if in stock
print("Smyths")
for switch,pg in smyths.items():
    html = urllib.request.urlopen(pg, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    stock = soup.find(class_=' deliveryType homeDelivery js-stockStatus')
    try:
        status = stock.get_text().strip()
        print(switch + " console status: " + status)
    except:
        print(switch + " console status: No stock listed")
print("")

# GameStop website parser
# Will parse each page of Switch type and check if in stock
print("GameStop")
for switch,pg in gamestop.items():
    html = urllib.request.urlopen(pg, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    page = soup.find(class_='bigBuyButtons SPNOpenMap').find_all('a')
    for stock in page:
        if stock.get('style') == 'display: block;':
            status = stock.get_text()
            print(switch + " console status: " + status)
print("")

# Littlewoods website parser
# Littlewoods do not have the Switch listed, will check if a Switch has been listed
print("Littlewoods")
for pg in littlewoods.values():
    req = urllib.request.Request(pg, headers=headers)
    html = urllib.request.urlopen(req, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    page = soup.find_all(class_='productBrand')
    status = False
    for stock in page:
        if stock.get_text().strip() == 'Nintendo Switch':
            status = True
            print('Switch available')
    if status == False:
        print('No stock listed')
