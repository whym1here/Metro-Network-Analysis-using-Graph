from lib2to3.pgen2.grammar import opmap_raw
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
# import sys

# sys.stdout = open('hydrabad.html', 'w', encoding = 'utf-8')

city_name = "hyderabad"

# Main URL
URL = f'https://en.wikipedia.org/wiki/List_of_{city_name.capitalize()}_Metro_stations'
req = requests.get(URL)

soup = bs(req.content, 'html5lib')

# set of all the stations
station_names = set()

# print(soup)

html_table = soup.find('table', attrs = {
    'class' : 'wikitable sortable',
    'style' : 'text-align: center;',
    'width' : '100%'
})

redundent_station_list = []
for i, row in enumerate(html_table.find_all('tr')):
    if(i == 0): continue
    temp_name = row.find_all('td')[0].find('a')['title']
    redundent_station_list.append(temp_name)

for name in redundent_station_list:
    if('Line' in name.split()): continue
    station_names.add(name)

station_names = list(station_names)

temp_dict = {"Station Names" : station_names}
df = pd.DataFrame(temp_dict)
df.to_csv(f'../raw-data/{city_name.lower()}-metro-station-names.csv', index = False)