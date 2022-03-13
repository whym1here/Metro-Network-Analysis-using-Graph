import sys
import os.path
from collections import *
import pandas as pd

if os.path.exists("input.txt"):
    sys.stdin = open("input.txt", 'r')

station_names = []
city = "delhi"

def fetching():
    n = int(input())
    for i in range(n):
        station_name = input()
        station_names.append(station_name)
        # print(station_name)

if __name__=="__main__":
    fetching()
    dt = {"Station Names" : station_names}
    df = pd.DataFrame(dt)
    df.to_csv(f'{city.lower()}-metro-station-names.csv', index = False)