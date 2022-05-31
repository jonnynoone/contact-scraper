import string
import time
import random
import requests
from bs4 import BeautifulSoup as bs
from openpyxl import Workbook

base_url = 'https://www.editus.lu/fr/particulier/lettre-'

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'adf_fpc=abf9740cd87b41c7b939d8f98f78a10c; .AspNetCore.Session=CfDJ8AF4duVEsu9JpRf2l5SbXVKEnOgjnj%2FISfi5X3JPZJqn1hLRU%2BH8p%2FcRoR4SmKOQr%2Bj0cMIVkvz0zQETCtSMMhrUcLeF8TTGnnH%2BcxxNKj6ZF2jA1XKXzQUqmSIL0QNhSd%2FG2gye6F4YkB8fpJqVLY2hU%2BN4M704DQqFYPyauYy3; datadome=vX21xY4sm1DzVp0b970~BMJwid6_uSV3rhfv6DZbzrBeUA2SF6~6fY4jpFYTPF-YrDdkbTn-lDj61Z6I3PC3JSAqzZDq.6c3ipjxEw8H_BNMnqgAD3RSj1bBuzPkXje; OptanonConsent=isGpcEnabled=0&datestamp=Tue+May+31+2022+12%3A58%3A25+GMT%2B0100+(British+Summer+Time)&version=6.35.0&isIABGlobal=false&consentId=1a703a73-6af1-4e41-82ae-dd8181c33348&interactionCount=1&landingPath=NotLandingPage&groups=1%3A1%2C2%3A1%2C4%3A1&hosts=H138%3A1%2CH82%3A1%2CH35%3A1%2CH146%3A1%2CH37%3A1%2CH38%3A1%2CH40%3A1%2CH42%3A1%2CH43%3A1%2CH45%3A1%2CH46%3A1%2CH47%3A1%2CH48%3A1%2CH5%3A1%2CH53%3A1%2CH147%3A1%2CH54%3A1%2CH57%3A1%2CH7%3A1%2CH59%3A1%2CH60%3A1%2CH62%3A1%2CH63%3A1%2CH64%3A1%2CH66%3A1%2CH68%3A1%2CH10%3A1%2CH70%3A1%2CH71%3A1%2CH164%3A1%2CH72%3A1%2CH74%3A1%2CH75%3A1%2CH78%3A1%2CH79%3A1%2CH81%3A1%2CH83%3A1%2CH84%3A1%2CH23%3A1%2CH87%3A1%2CH25%3A1%2CH91%3A1%2CH154%3A1%2CH28%3A1%2CH93%3A1%2CH94%3A1%2CH97%3A1%2CH99%3A1%2CH100%3A1%2CH102%3A1%2CH104%3A1%2CH105%3A1%2CH107%3A1&genVendors=&geolocation=GB%3BENG&AwaitingReconsent=false; OptanonAlertBoxClosed=2022-05-31T11:58:25.006Z',
    'Host': 'www.editus.lu',
    'Referer': 'https://www.editus.lu/fr/particulier/lettre-a?p=12',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
}

alphabet = list(string.ascii_lowercase)

# def getListings(soup):
#     results = soup.find(id = 'search-by-user-list').find_all('a')
#     for link in results:
#         links.append(link.get('href'))

for letter in alphabet:
    response = requests.get(base_url + letter, headers = headers)

    if response.status_code == 200:
        soup = bs(response.content, 'html.parser')

        # Get number of pages
        try:
            pagination = soup.find('ul', class_ = 'pagination').find_all('a')
            pages = int(pagination[-2].text.strip())
        except:
            pages = 1
            pass

        links = []

        # Get listings
        results = soup.find(id = 'search-by-user-list').find_all('a')
        for link in results:
            links.append(link.get('href'))

        if pages > 1:
            for i in range (2, pages + 1):
                response = requests.get(base_url + letter + '?p=' + str(i), headers = headers)

                results = soup.find(id = 'search-by-user-list').find_all('a')
                for link in results:
                    links.append(link.get('href'))

                time.sleep(random.randint(1, 3))

    time.sleep(random.randint(1, 3))


wb = Workbook()
ws = wb.active

for count, link in enumerate(links):
    ws['A{}'.format(count + 1)] = link 

wb.save('output.xlsx')