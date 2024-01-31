from .stations import Station
from .connection import Connection
from .trajectory import Trajectory
import pandas as pd
import random
class Network():
    """
    Class Network: create a network.

        Attributes:
        - connections (list): list of connection objects
        - stations (list): list of station objects
        - max_trajectories (int): max number of trajectories allowed in the network
        - max_trajectories (int): max length a trajectory can be
        - trajectories (list): list of trajectory objects
        - quality network (float): quality specified as K = p * 10000 - (T * 100 + min); where:
            p = fraction of driven connections; T = number of trajectories; min = total used time of the network
        - used (dict): dict that records whether connection has been used or not; (key=connection, value=int)
        - available_connections (dict): dict with connections of stations; (key=station.name, value=list of connections)
        
        Methods:
        - create_available_connections(): create the available connections dictionary
        - load_connections(): create connection objects
        - load_stations(): create station objects
        - connections_used(): create the used dictionary
        - add_trajectory(): add a trajectory to the network
        - remove_trajectory(): remove a trajectory from the network
        - is_valid(): checks if all connections are used
        - calculate_score(): calculates score of the network
        - save(): saves the networks trajectories and score to a csv
        - get_score ()- retrieves the score of the network
    """
    def __init__(self, connections, stations, max_trajectories, max_trajectory_time):
        """
        Initializes network and its attributes

        Args:
        - connections (pd.DataFrame or list): the dataframe or list containing the connections
        - stations (pd.DataFrame or list): the dataframe or list containing the stations
        - max_trajectories (int): max number of trajectories allowed in the network
        - max_trajectory_time (int): max time a trajectory is allowed to be
        """

        # check if connections (and stations) are a list or dataframe
        if type(connections) == list:
            self.connections = connections
            self.stations = stations
        else:
            self.connections = self.load_connections(connections)
            self.stations = self.load_stations(stations)
        
        # assign attributes
        self.max_trajectories = max_trajectories
        self.max_trajectory_time = max_trajectory_time
        self.trajectories = []
        self.quality_network = None
        self.used = self.connections_used() 
        self.available_connections = self.create_available_connections()

    def create_available_connections(self): 
        """Creates a list of all connections that have the current station as one of their stations.

        Returns: 
        - available_connections (dict): dict that has all available connections to a station; (key=station.name, value=list of connection objects)
        """

        station_list = self.stations
        connection_list = self.connections
        available_connections = {}
        for station in station_list:
            all_connections = [] 

            # loop through your list of connections and look for a connection that has the current station as station 1 or 2
            for connection in connection_list:
                if connection.station1 == station.name or connection.station2 == station.name:

                    # create list of all stations that have current station as station 1
                    all_connections.append(connection)
            
            # add the list of available connections to the dictionary of stations
            available_connections[station.name] = all_connections
            
                    #TODO: add which station was picked?
       
        return available_connections
    
    def load_connections(self, connections_df):
        """
        Create a list of connection instances from a dataframe containing the connections.

        Args:
        - connections_df (pd.DataFrame): the dataframe containing the connections 
        Returns:
        - connections (list): list containing the connection instances 
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
        Create a list of stations instances from a dataframe containing the stations.

        Args: 
        - station_df (pd.DataFrame): the dataframe containing the stations 
        Returns:
        - stations (list): list containing the stations instances 
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
        Create a dict that records how many times a connection is used.

        Returns:
        - used (dict): dict that for every connection records how many times it is used (key=connection object, value=int)
        """

        used = {}

        #loop over all connections and set default to 0 (unused)
        for connection in self.connections:
            used[connection] = 0

        return used
 
    def add_trajectory(self, trajectory):
        """
        Adds a trajectory to the trajectory list 

        Args:
        - trajectory (trajectory object): trajectory to append to the network
        """
        self.trajectories.append(trajectory)

    def remove_trajectory(self, trajectory):
        """
        Remove a trajectory from the trajectory list 

        Args:
        - trajectory (trajectory object): trajectory to remove from the network
        """
        self.trajectories.remove(trajectory)

    def is_valid(self):
        """
        Check if all connections have been used
        Returns:
        - True (boolean): if all connections have been used
        - False (boolean): if not all connections have been used
        """

        if sum(self.used.values()) == len(self.used):
            return True
        else:
            return False
        
    def calculate_score(self):
        """
        Calculates the score of the network of trajectories 
        """
        
        # all connections that are used in a list
        used_connections = [connection for connection, value in self.used.items() if value != 0]

        # calculate score for this network
        fraction = (len(used_connections)) / len(self.connections)
        total_time = sum([trajectory.time for trajectory in self.trajectories])
        self.quality_network = fraction * 10000 - (len(self.trajectories) * 100 + total_time) 
    
    def save(self, output_file):
        """
        Save the network to a csv file 

        Args:
        - output_file (string): filepath to save the csv-file to
        """

        # number every trajectory for output
        for index, trajectory in enumerate(self.trajectories):
            trajectory.name = index + 1

        # generate output as dataframe
        data = {'train': [trajectory.name for trajectory in self.trajectories] + ['score'],
                'stations': [trajectory.stations for trajectory in self.trajectories] + [self.quality_network]}
        output_df = pd.DataFrame(data) # output geven zoals in voorbeeld

        #create csv-file from output
        output_df.to_csv(output_file, index=False)
    
    def get_score(self):
        """
        Returns the score of the network
        Returns:
        - quality_network (float): the score of the network that is created
        """

        self.calculate_score()
        return self.quality_network

        
