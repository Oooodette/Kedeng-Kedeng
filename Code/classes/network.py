from .stations import Station
from .connection import Connection
from .trajectory import Trajectory
import pandas as pd
import random
class Network():
    def __init__(self, connections_file, stations_file):

        self.connections_df = self.load_data(connections_file)
        self.stations_df = self.load_data(stations_file)
        self.connections = []
        self.stations = []
        self.trajectories = []
        self.quality_network = None

    def load_data(self, filepath):
        return pd.read_csv(filepath)

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


    def pick_valid_connection(self, all_connections, previous_connection, time):

        chosen = False

        # if no valid connection exists, return None
        chosen_connection = None

        # keep picking a new connection until either a valid connection is found, or all connections have been tried
        while not chosen and len(all_connections) > 0:
            pick = random.randint(0, len(all_connections)-1)
            new_connection = all_connections[pick]
            all_connections.remove(all_connections[pick])


            # check to see if the connection is correct
            if time + new_connection.time < 120 and new_connection != previous_connection:
                chosen = True
                chosen_connection = new_connection

        return chosen_connection

    def create_trajectory(self):
        #TODO: Dit is een random algoritme, zet dit in mapje algoritme en roep hem aan. We willen geen algoritmes in de oplossing.
        # pick a random station from the list of stations
        previous_connection = None
        position = random.randint(0, len(self.stations)-1)
        current_station = self.stations[position].name
        time = 0
        trajectory_stations = [current_station]

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
            new_connection = self.pick_valid_connection(all_connections, previous_connection, time)

            # if valid connection is found, add it to the trajectory
            if new_connection != None:

                # pick correct station to move further with
                if current_station == new_connection.station1:
                    current_station = new_connection.station2
                    previous_station = new_connection.station1
                else:
                    current_station = new_connection.station1
                    previous_station = new_connection.station2
                time += new_connection.time
                trajectory_stations.append(current_station)
                new_connection.used = True
                previous_connection = new_connection


            # if no valid connection is found, break the loop
            else:
                break


        new_trajectory = Trajectory('x', trajectory_stations, time)

        return new_trajectory

    def is_valid(self):
        # if len(self.trajectories) <=7:
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
        fraction = sum([connection.used for connection in self.connections]) / len(self.connections)
        total_time = sum([trajectory.time for trajectory in self.trajectories])
        self.quality_network = fraction * 10000 - (len(self.trajectories) * 100 + total_time)

        # generate output
        data = {'train': [trajectory.name for trajectory in self.trajectories] + ['score'],
                'stations': [trajectory.stations for trajectory in self.trajectories] + [self.quality_network]}
        output_df = pd.DataFrame(data) # output geven zoals in voorbeeld

        output_df.to_csv('data\output.csv', index=False)

    def find_network(self):
        self.create_network()  
        counter = 0
        while len(self.trajectories) > 7:

            for connection in self.connections:
                connection.used = False
            self.trajectories = []
            counter +=1
            self.create_network()
            # if counter % 30 == 0 :
            #     print(counter)


    def get_score(self):
        print(f'the score of this network is {self.quality_network}')
        print('\n')
        print(len(self.trajectories))
