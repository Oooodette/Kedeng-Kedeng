from ..classes import Trajectory
import pandas as pd
import random 

class Random_algo():

    def __init__(self, network):
        self.network = network
        self.connection_list = self.network.connections
        self.station_list = self.network.stations 
        self.available_connections = {} 

    def create_available_connections(self, station_list, connection_list): 
        """Creates a list of all connections that have the current station as one of their stations
        Args: 
            current_station(str): name of current station
            connection_list(list): list of instances of connection class available for this network
        Returns: 
            all_connections(list): list of instances of connection class that have current station as one of their stations.
        """
        all_connections = []
        available_connections = {}
        for station in station_list:
            # loop through your list of connections and look for a connection that has the current station as station 1 or 2
            for connection in connection_list:

                if connection.station1 == station or connection.station2 == station:

                    # create list of all stations that have current station as station 1
                    all_connections.append(connection)
            
            # add the list of available connections to the dictionary of stations
            available_connections[station] = all_connections
                    #TODO: add which station was picked?

        return available_connections

    def pick_valid_connection(self, all_connections, previous_connection, time):
        """"
        Pick a new connection to add to the trajectory that does not pass the time limit or is the same connection as the previous one (i.e.
        makes the train go back)
        Args: 
            all_connections(list): list of instances of connection class that have current station as one of their stations.
            previous_connection(instance of connection class): connection that brought us to current station.
            time(int): total time of current trajectory (=sequence of connections) 
        Returns:
            chosen_connection(instance of connection class): valid connection to add to trajectory. If no valid trajectory is found, 
            None is returned.
        """
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

    def determine_station(self, current_station, new_connection):
        """
        Determine what next station will be, depending on whether previous station was station1 or station2.
        Args: 
            current_station(str): name of current station
            new_connection(instance of connection class): connection that was picked as the next connection
        Returns: 
            current_station: name of new current station
        """
        # pick correct station to move further with (depending on whether previous station was station1 or station2 for this connection)
        if current_station == new_connection.station1:
            new_station = new_connection.station2
        else: 
            new_station = new_connection.station1
        
        return new_station

    def pick_random_station(self, station_list):
        """"
        Picks a starting station for a trajectory.
        """
        position = random.randint(0, len(station_list)-1)
        current_station = station_list[position].name

        return current_station

    def create_trajectory(self, station_list, connection_list):
        
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
            new_trajectory.route = trajectory_connections
            
            return new_trajectory

    def create_network(self): 
        """"""
        self.available_connections = self.create_available_connections(self.station_list, self.connection_list)
        new_trajectory = self.create_trajectory(self.station_list, self.connection_list)
        counter = 1
        
        # check if all connections are used and keep making trajectories 
        while not self.network.is_valid():
            
            new_trajectory = self.create_trajectory(self.station_list, self.connection_list)
            self.network.add_trajectory(new_trajectory)

            # update used connections
            # TODO: this can be done better with a different way to save used connectionss.
            for connection, value in new_trajectory.connections:
                self.network.used[connection] = value

            # change used connections based on new trajectory
            new_trajectory.name = counter
            counter += 1
        return self.network

       
    


# ############################################################## OLD FUNCTIONS START HERE
         
# def create_trajectory(station_list,  ):
#         #TODO: Dit is een random algoritme, zet dit in mapje algoritme en roep hem aan. We willen geen algoritmes in de oplossing. 
#         # pick a random station from the list of stations
#         previous_connection = None
#         position = random.randint(0, len(station_list)-1)
#         current_station = station_list[position].name
#         time = 0

#         # save first station as starting station for this trajectory
#         trajectory_stations = [current_station]

#         # only add more connections if total time is below 120
#         while time < 120:
            
#             create_station_list(current_station, connection_list)
#             # create empty list to later select next connection from
#             all_connections = []

#             # loop through your list of connections and look for a connection that has the current station as station 1 or 2
#             for connection in self.connections:
               
#                 if connection.station1 == current_station or connection.station2 == current_station:

#                     # create list of all stations that have current station as station 1
#                     all_connections.append(connection)
            
#             # pick one of the connections with correct station
#             new_connection = pick_valid_connection(all_connections, previous_connection, time) 
            
#             # if valid connection is found, add it to the trajectory
#             if new_connection != None:

#                 # pick correct station to move further with
#                 if current_station == new_connection.station1:
#                     current_station = new_connection.station2
#                     previous_station = new_connection.station1
#                 else: 
#                     current_station = new_connection.station1
#                     previous_station = new_connection.station2
#                 time += new_connection.time 
#                 trajectory_stations.append(current_station)
#                 new_connection.used = True
#                 previous_connection = new_connection 
         

#             # if no valid connection is found, break the loop
#             else:
#                 break
            
#         new_trajectory = Trajectory('x', trajectory_stations, time) 
        
#         return new_trajectory

#     def create_network(connections_file, stations_file):
#         #TODO: This should be a function that calls on an algorithm
#         new_network = Network(connections_file, stations_file) 
#         new_trajectory = create_trajectory()

#         counter = 1
#         # check if all connections are used and keep making trajectories 
#         while not self.is_valid():
            
#             new_trajectory = self.create_trajectory()
#             new_trajectory.name = counter
#             counter += 1
#             self.trajectories.append(new_trajectory)

#         # calculate score for this network
#         fraction = sum([connection.used for connection in self.connections]) / len(self.connections)
#         total_time = sum([trajectory.time for trajectory in self.trajectories])
#         self.quality_network = fraction * 10000 - (len(self.trajectories) * 100 + total_time)

#         # generate output
#         data = {'train': [trajectory.name for trajectory in self.trajectories] + ['score'], 
#                 'stations': [trajectory.stations for trajectory in self.trajectories] + [self.quality_network]} 
#         output_df = pd.DataFrame(data) # output geven zoals in voorbeeld

#         output_df.to_csv('data\output.csv', index=False) 
        
