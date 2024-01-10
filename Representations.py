import pandas as pd

Class Dienstregeling(): 

    def __init__(self, verbindingsframe, stationsframe):
        self.verbindingsframe = verbindingsframe
        self.stationsframe = stationsframe
        self.verbindingen = []
        self.stations = []

    def maak_verbindingen(self):
    """Creëer instanties van verbinding class"""

        for verbinding in self.verbindingsframe.iterrows():
            tijd = verbinding['distance']
            station1 = verbinding['station1']
            station2 = verbinding['station2']
            nieuwe_verbinding = Verbinding(tijd, station1, station2)
            self.verbindingen.append(nieuwe_verbinding)
    
    def maak_stations(self):
    """"""

        for station in self.stationsframe.iterrows():
            x_cor = station['x']
            y_cor = station['y']
            nieuw_station = Station(x_cor, y_cor)
            self.stations.append(nieuw_station)
