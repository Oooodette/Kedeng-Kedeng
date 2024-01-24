from .stations import Station
from .connection import Connection
from .trajectory import Trajectory
import pandas as pd
import random
class Network():
    """
    Class Network: create Network object;
        Attributes:
        - connections (list of connection objects)
        - stations (list of station objects)
        - trajectories (list of trajectory objects)
        - quality network (float) - quality specified as K = p * 10000 - (T * 100 + min); where:
          p = fraction of driven connections; T = number of trajectories; min = total used time of the network
        - used (dict) - dict that records whether connection has been used or not; in format connection: boolean

        Methods:
        - load_data - read in csv-files
        - load_connections - create connection objects
        - load_stations - create station objects
        - add_trajectory - add trajectory to the network
        - #remove_trajectory#
        - #change_trajectory#
        - get_score - retrieves the score of the network
    """
    def __init__(self, connections_file=None, stations_file=None, max_trajectories=None, max_trajectory_time=None):
        """
        Method that initializes attributes of the network object
        Args:
        - connections_file: the file containing the train connections
        - stations file: the file containing the train stations
        """
        if connections_file != None:
            self.connections_df = pd.read_csv(connections_file)
            self.connections = self.load_connections(self.connections_df)
            self.stations_df = pd.read_csv(stations_file)
            self.stations = self.load_stations(self.stations_df)
        self.max_trajectories = max_trajectories
        self.max_trajectory_time = max_trajectory_time
        self.trajectories = []
        self.quality_network = None
        self.used = self.connections_used() 

    def load_connections(self, connections_df):
        """
        Method to create a list of connection instances 
        Args:
        - connections_df: the dataframe containing the connections 
        Returns:
        - a list containing the connection instances 
        """
        connections = []

        # loop over dataframe rows, specify connection attributes
        for index, connection in connections_df.iterrows():
            time = connection.loc['distance']
            station1 = connection.loc['station1']
            station2 = connection.loc['station2']

            # create connection object, add connection to list, return list
            new_connection = Connection(time, station1, station2)
            connections.append(new_connection)
        return connections

    def load_stations(self, stations_df):
        """
        Method that creates a list of stations instances from a dataframe 
        containing the stations 
        Args: 
        - station_df: the dataframe containing the stations 
        Returns:
        - a list containing the stations instances 
        """
        stations = []

        # loop over dataframe rows, specify stations attributes
        for index, station in stations_df.iterrows():
            x_cor = station.loc['x']
            y_cor = station.loc['y']
            name = station.loc['station']

            # create station object, add connection to list, return list
            new_station = Station(name, x_cor, y_cor)
            stations.append(new_station)
        return stations
    
    def connections_used(self):
        """
        Method that creates a dictionary named 'used' with the connection instances as attribute 
        and whether the connection is already used or not as value with True and False 
        To start, the connections values are all set to False because no connections are used yet 
        Returns:
        - the completed dictionary 
        """
        used = {}
        for connection in self.connections:
            used[connection] = False 
        return used
 

    def add_trajectory(self, trajectory):
        """
        Method that adds a trajectory to the trajectory list 
        Args:
        - trajectory: an instance of the trajectory class 
        """
        self.trajectories.append(trajectory)

    def remove_trajectory(self, trajectory):
        """
        Method that removes a trajectory from the trajectory list 
        Args:
        - trajectory: an instance of the trajectory class 
        """
        self.trajectories.remove(trajectory)

    def is_valid(self):
        """
        Method that checks if all connections have been used
        Returns:
        - True; if all connections have been used
        - False; if not all connections have been used
        """
        if sum(self.used.values()) == len(self.used):
            return True
        else:
            return False
        
    def calculate_score(self):
        """
        Method that calculates the score of the network of trajectories 
        """
        # calculate score for this network
        fraction = sum(self.used.values()) / len(self.connections)
        total_time = sum([trajectory.time for trajectory in self.trajectories])
        self.quality_network = fraction * 10000 - (len(self.trajectories) * 100 + total_time) 
        return self.quality_network
    
    def save_network(self):
        """
        Method that saves the network to a csv file 
        """
        # generate output as dataframe
        data = {'train': [trajectory.name for trajectory in self.trajectories] + ['score'],
                'stations': [trajectory.stations for trajectory in self.trajectories] + [self.quality_network]}
        output_df = pd.DataFrame(data) # output geven zoals in voorbeeld

        #create csv-file from output
        output_df.to_csv('data\output.csv', index=False)
    

    def get_score(self):
        """
        Method that returns the score of the network
        """
        return self.quality_network

        
