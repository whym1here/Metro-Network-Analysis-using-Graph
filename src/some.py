import requests
from bs4 import BeautifulSoup
import urllib.parse
import sys
import os.path

if os.path.exists("input.txt"):
    sys.stdin = open("input.txt", 'r')

sys.stdout = open("output.txt", 'w')

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

cnt  = 0
def display(name,lat,lon) :
    print("Station Name : ",name, end=" ")
    print("Latitude : ",lat, end=" ")
    print("Longitude : ",lon)

def Lat_Lon(name) :
    global cnt
    station_name = f"{name} Delhi "
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(station_name) +'?format=json'
    response = requests.get(url).json()
    #print(response)
    flag = True
    if(response != []) :
        for i in response :
            if(i["type"] == 'subway' and flag) :
                flag = False 
                display(station_name,i["lat"],i["lon"])
                break
        
        for i in response :
            if(i["type"] == 'station' and flag) :
                flag = False 
                display(station_name,i["lat"],i["lon"])
                break
        
        if(flag) :
            display(station_name,response[0]["lat"],response[0]["lon"])
    else :
        station_name = f"{name}"
        url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(station_name) +'?format=json'
        response = requests.get(url).json()
        #print(response)
        flag = True
        if(response != []) :
            for i in response :
                if(i["type"] == 'subway' and flag) :
                    flag = False 
                    display(station_name,i["lat"],i["lon"])
                    break
            
            for i in response :
                if(i["type"] == 'station' and flag) :
                    flag = False 
                    display(station_name,i["lat"],i["lon"])
                    break
            
            if(flag) :
                display(station_name,response[0]["lat"],response[0]["lon"])
        else :
            cnt+=1
            print("-"*100)
            print(station_name)
            print("Not Found!!!")
            print("-"*100)

# Main

n = int(input())
for i in range(n):
    s = input().lstrip('"').rstrip('"').rstrip('\n').rstrip(' ')
    # print(s)
    Lat_Lon(s)
print(cnt)