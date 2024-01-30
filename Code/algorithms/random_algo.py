from ..classes import Trajectory, Network
import pandas as pd
import random 
import pprint as pp 
import copy 

class Random_algo():

    def __init__(self, network: Network):
        self.network = network
        self.station_list = self.network.stations 
        self.available_connections = {} 

    @staticmethod
    def pick_valid_connection(all_connections, previous_connection, time):
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

    @staticmethod
    def determine_station(current_station, new_connection):
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
    
    @staticmethod
    def pick_station(station_list):
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
    
    @staticmethod
    def create_trajectory(network: Network):
        """
        Creates a new trajectory (i.e. a sequence of connections)

        Args:
        - station_list(list of station objects)

        Returns:
        - new_trajectory(trajectory object)
        """
        station_list = network.stations
        # initialize variables
        current_station = Random_algo.pick_station(station_list)
        previous_connection = None
        time = 0
        # trajectory_time = random.randint(0, network.max_trajectory_time)
        trajectory_stations = [current_station]
        trajectory_connections = []

        # only add more connections if total time is below 120
        while time < network.max_trajectory_time:
            new_connection = Random_algo.pick_valid_connection(network.available_connections[current_station], previous_connection, time) 
           
            # if a valid connection is found, change the current station to the next station of this connection
            if new_connection != None:
                
                current_station = Random_algo.determine_station(current_station, new_connection)
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
        new_trajectory.route = trajectory_connections

        return new_trajectory

    def create_network(self): 
        """
        Creates a network; consists of trajectories

        Returns:
        - network(network object) - attribute of algorithm object
        """
        nr_trajectories = random.randint(0, self.network.max_trajectories)
        # new_trajectory = self.create_trajectory(self.station_list, self.connection_list)
        counter = 1
        
        # check if all connections are used and keep making trajectories 
        while len(self.network.trajectories) < nr_trajectories:
            
            new_trajectory = Random_algo.create_trajectory(self.network) 
            self.network.add_trajectory(new_trajectory)

            # update used connections
            for connection in new_trajectory.route:
                self.network.used[connection] += 1
            
            # change used connections based on new trajectory
            new_trajectory.name = counter
            counter += 1
        
        self.network.calculate_score()

        return self.network