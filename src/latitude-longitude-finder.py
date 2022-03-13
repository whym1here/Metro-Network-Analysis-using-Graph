import requests
import urllib.parse
import csv
import sys
import os.path

# for checking output
if os.path.exists("input.txt"):
    sys.stdin = open("input.txt", 'r')
sys.stdout = open("output.txt", 'w')

# CSV file fields
metro_fields = ["Station Name","Latitude","Longitude"]
metro_data = [] # list to store station data
city = "Delhi" # city name
filename = f"..\dataset\{city.lower()}-metro-data.csv" # filename

# cnt = 0
def display_save(name,lat,lon) :
    metro_data.append([name,lat,lon])
    print("Station Name : ",name, end=" ")
    print("Latitude : ",lat, end=" ")
    print("Longitude : ",lon)

def Lat_Lon(name) :
    global cnt
    station_name = f"{name} {city} "
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(station_name) +'?format=json'
    response = requests.get(url).json()
    #print(response)
    flag = True
    if(response != []) :
        for i in response :
            if(i["type"] == 'subway' and flag) :
                flag = False 
                display_save(station_name,i["lat"],i["lon"])
                break
        
        for i in response :
            if(i["type"] == 'station' and flag) :
                flag = False 
                display_save(station_name,i["lat"],i["lon"])
                break
        
        if(flag) :
            display_save(station_name,response[0]["lat"],response[0]["lon"])
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
                    display_save(station_name,i["lat"],i["lon"])
                    break
            
            for i in response :
                if(i["type"] == 'station' and flag) :
                    flag = False 
                    display_save(station_name,i["lat"],i["lon"])
                    break
            
            if(flag) :
                display_save(station_name,response[0]["lat"],response[0]["lon"])
        else :
            metro_data.append([station_name,"Not Found","Not Found"])
            # cnt+=1
            # print("-"*100)
            # print(station_name)
            # print("Not Found!!!")
            # print("-"*100)

# Main

n = int(input())
for i in range(n):
    s = input().lstrip('"').rstrip('"').rstrip('\n').rstrip(' ')
    # print(s)
    Lat_Lon(s)
# print(cnt)

# writing to csv file
with open(filename, 'w', newline='') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)
     
    # writing the fields
    csvwriter.writerow(metro_fields)
     
    # writing the data rows
    csvwriter.writerows(metro_data)