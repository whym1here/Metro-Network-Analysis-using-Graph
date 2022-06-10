import sys

city_name = 'mumbai'

# sys.stdout = open(f"{city_name}.txt", 'w')

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
    
    # lat1 = float(lat1)
    # lon1 = float(lon1)
    # lat2 = float(lat2)
    # lon2 = float(lon2)

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
    return (c * r)

def kruskal(edge_list, n, station_data):
    dsu = DSU(n)

    included_edges = []
    lat_long_included_edges = []

    total_length = 0

    for it in edge_list:
        wt = it[0]
        x = it[1]
        y = it[2]
        x_name = it[3]
        y_name = it[4]

        if(dsu.find(x) != dsu.find(y)):
            dsu.join(x, y)
            total_length += wt
            included_edges.append([x_name, y_name])
            lat_long_included_edges.append([
                [station_data[x_name]['Latitude'], station_data[x_name]['Longitude']],
                [station_data[y_name]['Latitude'], station_data[y_name]['Longitude']]
            ])
    
    # for ele in lat_long_included_edges:
    #     print(ele)

    return (total_length, included_edges, lat_long_included_edges)
        
def add_line(points, map_, color = 'red'):
    folium.PolyLine(
        points,
        color = color
    ).add_to(map_)

def add_point(name, lat, lon, map_):
    marker = folium.CircleMarker(
        location = [lat,lon],
        popup = f"<stong>{name} Metro Sation</stong>",
        radius = 1, weight = 2)
    marker.add_to(map_)

def gen_mst(city_name, df):
    name_to_int = dict()
    int_to_name = dict()
    cur = 0
    station_data = {}
    for index in df.index:
        station_data[df['Station Name'][index]] = {
            'Latitude': df['Latitude'][index],
            'Longitude': df['Longitude'][index]
        }
        name_to_int[df['Station Name'][index]] = cur
        cur += 1
    
    for key, val in name_to_int.items():
        int_to_name[val] = key
    
    edge_list = list()
    for i in range(len(station_data)):
        for j in range(len(station_data)):
            if(i in int_to_name.keys() and j in int_to_name.keys() and int_to_name[i] != int_to_name[j]):
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

    # for ele in edge_list:
    #     print(ele)
    
    total_length, included_edges, lat_long_included_edges = kruskal(edge_list, len(station_data), station_data)
    # df['Latitude'].mean()
    map_ = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=10)
        
    for it in lat_long_included_edges:
        add_line(it, map_)

    for index, row in df.iterrows():
        add_point(row['Station Name'], row['Latitude'], row['Longitude'], map_)

    print(f"total length of metro line = {total_length} km")
    # map.save(f'{city_name.lower()}-metro-station.html')
    return map_

def get_mutiple_mst(cityname, df_lst, colors):
    
    def get_geocoder(address):
        try:
            import geopy
            locator = geopy.geocoders.Nominatim(user_agent="myGeocoder")
            location = locator.geocode(address)
            # print(location)
            return [location.latitude, location.longitude]
        except:
            return [21.2379469, 81.6336833]

    map_ = folium.Map(location = get_geocoder(address = cityname), zoom_start = 10)

    for index, row in df_lst[0].iterrows():
        add_point(row['Station Name'], row['Latitude'], row['Longitude'], map_)

    def add_lines_points(df, color):
        name_to_int = dict()
        int_to_name = dict()
        cur = 0
        station_data = {}
        for index in df.index:
            station_data[df['Station Name'][index]] = {
                'Latitude': df['Latitude'][index],
                'Longitude': df['Longitude'][index]
            }
            name_to_int[df['Station Name'][index]] = cur
            cur += 1
        
        for key, val in name_to_int.items():
            int_to_name[val] = key
        
        edge_list = list()
        for i in range(len(station_data)):
            for j in range(len(station_data)):
                if(i in int_to_name.keys() and j in int_to_name.keys() and int_to_name[i] != int_to_name[j]):
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

        total_length, included_edges, lat_long_included_edges = kruskal(edge_list, len(station_data), station_data)
        
        for it in lat_long_included_edges:
            add_line(it, map_, color)

        for index, row in df.iterrows():
            add_point(row['Station Name'], row['Latitude'], row['Longitude'], map_)

        print(f'{color} metro network is of length: {total_length}')

    for i in range(len(df_lst)):
        add_lines_points(df_lst[i], colors[i])
    
    return map_
    

def get_edge_list(df):
    name_to_int = dict()
    int_to_name = dict()
    cur = 0
    station_data = {}
    for index in df.index:
        station_data[df['Station Name'][index]] = {
            'Latitude': df['Latitude'][index],
            'Longitude': df['Longitude'][index]
        }
        name_to_int[df['Station Name'][index]] = cur
        cur += 1
    
    for key, val in name_to_int.items():
        int_to_name[val] = key
    
    edge_list = list()
    for i in range(len(station_data)):
        for j in range(len(station_data)):
            if(i in int_to_name.keys() and j in int_to_name.keys() and int_to_name[i] != int_to_name[j]):
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
    total_length, included_edges, lat_long_included_edges = kruskal(edge_list, len(station_data), station_data)
    return {
        "total_length": total_length,
        "included_edges": included_edges,
        "lat_long_included_edges": lat_long_included_edges,
        "name_to_int": name_to_int,
        "int_to_name": int_to_name
    }