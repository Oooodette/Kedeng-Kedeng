import pandas as pd

class Verbinding():
    def __init__(self, time, station1, station2):
        self.time = time
        self.station1 = station1 
        self.station2 = station2
        self.driven = False
 
class Station():
    def __init__(self, name, x_cor, y_cor):
        self.name = name
        self.x_cor = x_cor 
        self.y_cor = y_cor 

class Traject():
    def __init__(self, stations, time):
        self.stations = stations 
        self.time = time 

class Dienstregeling(): 
    def __init__(self, verbindingsframe, stationsframe):
        self.verbindingsframe = verbindingsframe
        self.stationsframe = stationsframe
        self.verbindingen = []
        self.stations = []

    def create_connections(self):
    
    for verbinding in self.verbindingsframe.iterrows():
            tijd = verbinding['distance']

            
            station1 = verbinding['station1']
            station2 = verbinding['station2']

            nieuwe_verbinding = Verbinding(tijd, station1, station2)
            self.verbindingen.append(nieuwe_verbinding)
   
    def create_stations(self):
    
    for station in self.stationsframe.iterrows():
        x_cor = station['x']
        y_cor = station['y']
        name = station['station']
        nieuw_station = Station(name, x_cor, y_cor)
        self.stations.append(nieuw_station)

    


       
    
