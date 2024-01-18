from ..classes import Trajectory
import pandas as pd
import random 
import pprint as pp 
import copy 

class Random_algo():

    def __init__(self, network):
        self.network = network
        self.station_list = self.network.stations 
        self.available_connections = {} 

    def create_available_connections(self, station_list, connection_list): 
        """Creates a list of all connections that have the current station as one of their stations

        Args: 
        - current_station(str): name of current station
        - connection_list(list): list of instances of connection class available for this network

        Returns: 
        - all_connections(list): list of instances of connection class that have current station as one of their stations.
        """
        
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

    def pick_valid_connection(self, all_connections, previous_connection, time):
        """"
        Pick a new connection to add to the trajectory that does not pass the time limit or is the same connection as the previous one (i.e.
        makes the train go back)

        Args: 
        - all_connections(list): list of instances of connection class that have current station as one of their stations.
        - previous_connection(instance of connection class): connection that brought us to current station.
        - time(int): total time of current trajectory (=sequence of connections) 

        Returns:
        - chosen_connection(instance of connection class): valid connection to add to trajectory. If no valid connection is found, 
            None is returned.
        """
        chosen = False

        # if no valid connection exists, return None
        chosen_connection = None
        connection_copy = copy.copy(all_connections)

        # keep picking a new connection until either a valid connection is found, or all connections have been tried
        while not chosen and len(connection_copy) > 0: 
            pick = random.randint(0, len(connection_copy)-1)
            new_connection = connection_copy[pick]
            connection_copy.remove(connection_copy[pick])

            # check to see if the connection is correct
            if time + new_connection.time < 120 and new_connection != previous_connection:
                chosen = True
                chosen_connection = new_connection
        
        return chosen_connection 

    def determine_station(self, current_station, new_connection):
        """
        Determine what next station will be, depending on whether previous station was station1 or station2.

        Args: 
        - current_station(str): name of current station
        - new_connection(instance of connection class): connection that was picked as the next connection

        Returns: 
        - current_station: name of new current station
        """
        # pick correct station to move further with (depending on whether previous station was station1 or station2 for this connection)
        if current_station == new_connection.station1:
            new_station = new_connection.station2
        else: 
            new_station = new_connection.station1
        
        return new_station

    def pick_random_station(self, station_list):
        """"
        Picks a starting station for a trajectory

        Args:
        - station_list(list of station objects)

        Returns:
        - randomly picked station from stations_list
        """
        position = random.randint(0, len(station_list)-1)
        current_station = station_list[position].name

        return current_station

    def create_trajectory(self, station_list):
        """
        Creates a new trajectory (i.e. a sequence of connections)

        Args:
        - station_list(list of station objects)

        Returns:
        - new_trajectory(trajectory object)
        """
        # initialize variables
        current_station = self.pick_random_station(station_list)
        previous_connection = None
        time = 0
        trajectory_stations = [current_station]
        trajectory_connections = []

        # only add more connections if total time is below 120
        while time < 120:
            new_connection = self.pick_valid_connection(self.available_connections[current_station], previous_connection, time) 
           
            # if a valid connection is found, change the current station to the next station of this connection
            if new_connection != None:
                
                current_station = self.determine_station(current_station, new_connection)
                time += new_connection.time 

                # add station and connection to trajectory	
                trajectory_stations.append(current_station)
                trajectory_connections.append(new_connection) 

                # update in used connections dictionary and update previous connection
                previous_connection = new_connection 
            
            # if no valid connection is found, break the loop
            else:
                break
            
        # create new trajectory instance
        new_trajectory = Trajectory('x', trajectory_stations, time) 
            
        # add used connections to route attribute of trajectory
        new_trajectory.route = set(trajectory_connections)
        
        
        return new_trajectory

    def create_network(self): 
        """
        Creates a network; consisting of trajectories
        
        Returns:
        - self.network(network object) - attribute of algorithm object
        """
        
        self.available_connections = self.create_available_connections(self.station_list, self.network.connections)
        self.network.connections_used()
        # new_trajectory = self.create_trajectory(self.station_list, self.connection_list)
        counter = 1
        
        # check if all connections are used and keep making trajectories 
        while not self.network.is_valid():
            
            new_trajectory = self.create_trajectory(self.station_list) 
            self.network.add_trajectory(new_trajectory)

            # update used connections
            # TODO: this can be done better with a different way to save used connectionss.
            for key, value in self.network.used.items(): 
                if key in new_trajectory.route:
                    value = True

            for connection in new_trajectory.route:
                
                self.network.used[connection] = True
            

            # change used connections based on new trajectory
            new_trajectory.name = counter
            counter += 1
        
        self.network.calculate_score()

        return self.network