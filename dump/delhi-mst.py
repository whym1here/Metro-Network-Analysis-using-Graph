from math import *
import pandas as pd
import folium

class DSU(object):
    def __init__(self, n: int) -> None:
        self.p: list[int] = [i for i in range(n)]
        self.r: list[int] = [1 for i in range(n)]
        self.size: int = n
    
    def find(self, x: int) -> int:
        y = x
        while(x != self.p[x]):
            x = self.p[x]
        while(y != self.p[y]):
            z = self.p[y]
            self.p[y] = x
            y = z
        return x
    
    def join(self, x: int, y: int) -> None:
        x, y = self.find(x), self.find(y)

        if(self.r[x] > self.r[y]):
            x, y = y, x
        
        self.p[x] = y

        if(self.p[x] == self.p[y] and x != y):
            self.r[y] += 1

def distance(station1, station2):     
    
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lat1, lon1, lat2, lon2 = station1['Latitude'], station1['Longitude'], station2['Latitude'], station2['Longitude']

    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
 
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
      
    # calculate the result
    return(c * r)

if __name__ == "__main__":
    filename = r'../dataset/delhi-metro-data.csv'
    df = pd.read_csv(filename)
    name_to_int = dict()
    int_to_name = dict()
    cur = 0
    station_data = {}
    for index, row in df.iterrows():
        station_data[row['Station Name']] = {
            'Latitude': row['Latitude'],
            'Longitude': row['Longitude']
        }
        name_to_int[row['Station Name']] = cur
        int_to_name[cur] = row['Station Name']
        cur += 1
    
    edge_list = list()
    for i in range(len(station_data)):
        for j in range(len(station_data)):
            if(i != j):
                edge_list.append([
                    distance(
                        station_data[int_to_name[i]], 
                        station_data[int_to_name[j]]
                    ),
                    i, j, 
                    int_to_name[i],
                    int_to_name[j]
                ])
    
    edge_list.sort()
    print(edge_list)

    


    






# map = folium.Map(location=[28.7165805, 77.1704223], zoom_start=10)

# tooltip = "Click Here For More Info"

# def add_point(name, lat, lon, map):
#     marker = folium.CircleMarker(
#         location = [lat,lon],
#         popup = f"<stong>{name} Metro Sation</stong>",
#         radius = 1, weight = 2)
#     marker.add_to(map)

# for index, row in df.iterrows():
#     add_point(row['Station Name'], row['Latitude'], row['Longitude'], map)
    
# map.save('delhi-metro-station.html')