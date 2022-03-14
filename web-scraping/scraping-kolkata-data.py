import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import sys

city_name = "kolkata"

sys.stdout = open("kolkata-metro.html", 'w', encoding='utf-8')

# Main URL
URL = f'https://en.wikipedia.org/wiki/List_of_Kolkata_Metro_stations'
req = requests.get(URL)

soup = bs(req.content, 'html5lib')

# set of all the stations
station_names = set()

print(soup)

html_table = soup.find('table', attrs = {
    'class' : 'wikitable sortable',
    'style' : 'font-size:95%;',
    'width' : '100%'
})

print(html_table)
redundent_station_list = []
for i, row in enumerate(html_table.find_all('tr')):
    if(i == 0 or i == 1): 
        continue
    temp_name = row.find_all('td')[0].find('a')['title']
    redundent_station_list.append(temp_name)

for name in redundent_station_list:
    if('Line' in name.split()): continue
    station_names.add(name)

station_names = list(station_names)

print(station_names)

temp_dict = {"Station Names" : station_names}
df = pd.DataFrame(temp_dict)
df.to_csv(f'../Raw-Data/{city_name.lower()}-metro-station-names.csv', index = False)