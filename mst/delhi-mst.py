from math import *
import pandas as pd

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

def distance(lat1, lon1, lat2, lon2):     
    # The math module contains a function named
    # radians which converts from degrees to radians.
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

