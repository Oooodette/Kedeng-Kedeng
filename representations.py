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
        self.used= False

class Trajectory():
    def __init__(self, name, stations, time):
        self.name = name
        self.stations = stations
        self.time = time



class Network():
    def __init__(self, connections_file, stations_file):
        self.connections_df = load_data(connections_file)
        self.stations_df = load_data(stations_file)
        self.connections = [] #TODO: call function here
        self.stations = [] # TODO: call function here
        self.trajectories = []
        self.quality_network = None
        
    def load_data(self, filepath): 
        return pd.read_csv(filepath, index_col=False)
        
    
    def load_connections(self):

        for index, connection in self.connections_df.iterrows():
            time = connection.loc['distance']

            station1 = connection.loc['station1']
            station2 = connection.loc['station2']

            new_connection = Connection(time, station1, station2)
            self.connections.append(new_connection)

    def load_stations(self):

        for index, station in self.stations_df.iterrows():
            x_cor = station.loc['x']
            y_cor = station.loc['y']
            name = station.loc['station']
            new_station = Station(name, x_cor, y_cor)
            self.stations.append(new_station)
    
    def pick_valid_connection(self, all_connections, time):
     
        chosen = False

        # if no valid connection exists, return None
        chosen_connection = None

        # keep picking a new connection until either a valid connection is found, or all connections have been tried
        while not chosen and len(all_connections) > 0: 
            pick = random.randint(0, len(all_connections)-1)
            new_connection = all_connections[pick]
            all_connections.remove(all_connections[pick])

            # check to see if the connection is correct
            if time + new_connection.time < 120:
                chosen = True
                chosen_connection = new_connection
        
        return chosen_connection 

    def create_trajectory(self):
        # pick a random station from the list of stations
        previous_connection = None
        position = random.randint(0, len(self.stations)-1)
        current_station = self.stations[position].name
        time = 0
        trajectory_stations = []

        # only add more connections if total time is below 120
        while time < 120:

            # create empty list to later select next connection from
            all_connections = []

            # loop through your list of connections and look for a connection that has the current station as station 1 or 2
            for connection in self.connections:
               
                if connection.station1 == current_station or connection.station2 == current_station:

                    # create list of all stations that have current station as station 1
                    all_connections.append(connection)
            
            # pick one of the connections with correct station
            new_connection = self.pick_valid_connection(all_connections, time) 
            
            # if valid connection is found, add it to the trajectory
            if new_connection != None and new_connection != previous_connection: 

                # pick correct station to move further with
                if current_station == new_connection.station1:
                    current_station = new_connection.station2
                    next_station = new_connection.station1
                else: 
                    current_station = new_connection.station1
                    next_station = new_connection.station2
                time += new_connection.time 
                trajectory_stations.append(current_station)
                new_connection.used = True
                previous_connection = new_connection 
         
            # if no valid connection is found, break the loop
            else:
                # when only one connection has been driven, we also want to add the next station  
                if len(trajectory_stations) == 1:
                    trajectory_stations.append(next_station)
                break
            
        new_trajectory = Trajectory('x', trajectory_stations, time) 
        return new_trajectory
    def is_valid(self):
        if all ([connection.used==True for connection in self.connections]):
            return True
        else:
            return False
    
    def create_network(self):
        counter = 1
        # check if all connections are used and keep making trajectories 
        while not self.is_valid():
            
            new_trajectory = self.create_trajectory()
            new_trajectory.name = counter
            counter += 1
            self.trajectories.append(new_trajectory)

        # calculate score for this network
        fraction = 1 #TODO: calculate total number of connections used
        total_time = sum([trajectory.time for trajectory in self.trajectories])
        self.quality_network = fraction * 10000 - (len(self.trajectories) * 100 + total_time)

        # generate output
        data = {'train': [trajectory.name for trajectory in self.trajectories] + ['score'], 
                'stations': [trajectory.stations for trajectory in self.trajectories] + [quality_network]} 
        output_df = pd.DataFrame(data) # output geven zoals in voorbeeld

        output_df.to_csv('output.csv', index=False)

    def get_score(self):
        print(f'the score of this network = {self.quality_network}')

