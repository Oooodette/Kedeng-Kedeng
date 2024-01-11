from tkinter import W
import pandas as pd
import random


class Station():
    def __init__(self, name, x_cor, y_cor):
        self.name = name
        self.x_cor = x_cor
        self.y_cor = y_cor


class Connection():
    def __init__(self, time, station1, station2):
        self.time = time
        self.station1 = station1
        self.station2 = station2
        self.driven = False


class Trajectory():
    def __init__(self, stations, time):
        # add trajectory name
        self.stations = stations
        self.time = time



class Dienstregeling():
    def __init__(self, connections_df, stations_df):
        self.connections_df = connections_df
        self.stations_df = stations_df
        self.connections = []
        self.stations = []
        self.trajectories = []
        

    def create_connections(self):

        for connection in self.connections_df.iterrows():
            time = connection['distance']

            station1 = connection['station1']
            station2 = connection['station2']

            new_connection = Connection(time, station1, station2)
            self.connections.append(new_connection)

    def create_stations(self):

        for station in self.stations_df.iterrows():
            x_cor = station['x']
            y_cor = station['y']
            name = station['station']
            new_station = Station(name, x_cor, y_cor)
            self.stations.append(new_station)

    def create_network(self):
        # check if all connections are used
        if all ([connection.driven=True for connection in connections]):
            
            # calculate score for this network
            fraction = 
            total_time = sum([trajectory.time for trajectory in self.tractories])
            quality_network = fraction * 10000 - (len(self.trajectories) * 100 + total_time)

            # generate output
            data = {'train': self.trajectories.name
                    'stations': self.trajectories.stations}
            output_df = pd.DataFrame(data) # output geven zoals in voorbeeld
        else: 
            # create trajectory
       
    def create_trajectory(self):
        # pick a random station from the list of stations
        position = random.randint(0, len(self.stations))
        current_station = self.stations[position].name
        time = 0
        trajectory_stations = []

        # only add more connections if total time is below 120
        while time < 120:

            # create empty list to later select next connection from
            all_connections = []

            # loop through your list of connections and look for a connection that has the current station as station 1
            for connection in self.connections:
                if connection.station1 == current_station:

                    # create list of all stations that have current station as station 1
                    all_connections.append(connection)

            # pick one of the connections with correct station
            # LET OP!! Trajectory can now be longer than 120 minutes.
            pick = random.randint(0, len(all_connections))
            new_connection = all_connections[pick]
            if time + new_connection.time > 120:
                
            else: 

                time += new_connection.time

            if time > 120 and len(all_connections) > 1:

                time -= new_connection.time
                pick2 = random.randint(0, len(all_connections))
                new_connection2 = all_connections[pick2]
                time += new_connection2.time 

                current_station = new_connection2.station2
                trajectory_stations.append(new_connection2.station1)

                if time > 120 and len(all_connections) > 2:
                    time -= new_connection2.time 
                    pick3 = random.randint(0, len(all_connections))
                    new_connection3 = all_connections[pick3]
                    time += new_connection3.time 

                    current_station = new_connection3.station1
                    trajectory_stations.append(new_connection3.station1)
                
                else:
                    pass 

            else:
                current_station = new_connection.station2
                trajectory_stations.append(new_connection.station1)

        new_trajectory = Trajectory(trajectory_stations, time) 
        # TODO: add trajectories to list?
        
