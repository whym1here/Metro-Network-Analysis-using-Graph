import requests
from bs4 import BeautifulSoup
import sys
import os.path
import pandas as pd

if os.path.exists("input.txt"):
    sys.stdin = open("input.txt", 'r')
    sys.stdout = open("output.txt", 'w')

city_name = "Delhi"

URL = f"https://en.wikipedia.org/wiki/List_of_{city_name}_Metro_stations"
req = requests.get(URL)

soup = BeautifulSoup(req.content, 'html5lib')

station_names = []

table = soup.find('table', attrs = {
    'class' : 'wikitable sortable static-row-numbers',
    'style' : 'font-size:95%;',
    'width' : '100%'
})

station_name = []
flag = True

lines = [
    'Pink Line (Delhi Metro)',
    'Yellow Line (Delhi Metro)'
    'Violet Line (Delhi Metro)',
    'Red Line (Delhi Metro)',
    'Green Line (Delhi Metro)',
    'Magenta Line (Delhi Metro)',
    'Blue Line (Delhi Metro)',
    'Grey Line (Delhi Metro)'
]

lst = []

for row in table.find_all('tr'):
    if(flag):
        flag = False
        continue


    name = row.find_all('td')[0].find('a')['title']
    lst.append(name)

for i in lst:
    if(i == 'Yellow Line (Delhi Metro)'):
        continue
    if(i == 'Violet Line (Delhi Metro)'):
        continue
    if (i not in lines):
        station_names.append(i)

for val in station_names:
    print(val)
