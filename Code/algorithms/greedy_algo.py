from ..classes import Trajectory
import pandas as pd
import random 
import pprint as pp 
import copy 

class Greedy_algo():
    def __init__(self, network):
        self.network = network
        self.available_connections = self.create_available_connections(self.network.stations, self.network.connections)

    def create_driven_dict(self):
        driven_dict = {}
        for connection in self.network.connections:
            driven_dict[connection] = False
        return driven_dict

    def create_available_connections(self, station_list, connection_list): 
        
        available_connections_dict = {}
        for station in station_list:
            station_connections = [] 

            for connection in connection_list:
                if station.name == connection.station1 or station.name == connection.station2:
                    station_connections.append(connection)
            
            available_connections_dict[station.name] = station_connections
                   
        return available_connections_dict

    def pick_start_station(self, trajectory):

        start_station = self.network.stations[random.randint(0, len(self.network.stations) - 1)].name
        return start_station

    def determine_new_station(self, current_station, new_connection):
       
        if current_station == new_connection.station1:
            new_station = new_connection.station2
        else: 
            new_station = new_connection.station1
        return new_station

    def pick_connection(self, available_connections, trajectory):

        chosen = False

        available_connections_copy = copy.copy(available_connections)

        while not chosen and (len(available_connections_copy)) > 0:

            potential_connection = available_connections_copy[random.randint(0, (len(available_connections_copy) - 1))]
            available_connections_copy.remove(potential_connection)

            if (trajectory.time + potential_connection.time) < self.network.max_trajectory_time:
                if potential_connection != trajectory.route[-1]:

                    chosen = True
                    return potential_connection

    def remove_connection(self, trajectory, station, connection):
        trajectory.stations.remove(station)
        trajectory.connections.remove(connection)
        trajectory.time -= connection.time
        self.network.used[connection] = False

    def create_trajectory(self, trajectory_count):
        
        #create an 'empty' instance of a trajectory and add to network
        trajectory = Trajectory(trajectory_count, [], 0)
        trajectory.route = [None]
        self.network.add_trajectory(trajectory)

        while len(trajectory.stations) == 0:

            score_before = self.network.calculate_score()

            start_station = self.pick_start_station(trajectory)
            trajectory.stations.append(start_station)
            start_available_connections = self.available_connections[start_station]
            start_connection = self.pick_connection(start_available_connections, trajectory)

            if start_connection != None:
                trajectory.route.append(start_connection)
                current_station = self.determine_new_station(start_station, start_connection)
                trajectory.stations.append(current_station)
                trajectory.time += start_connection.time
                self.network.used[start_connection] = True

                score_after = self.network.calculate_score()

            else:
                trajectory.stations.remove(start_station)                

            # if score_before > score_after:
            #     trajectory.stations.remove(start_station)
            #     self.remove_connection(trajectory, current_station, start_connection)
                
        while trajectory.time < self.network.max_trajectory_time:

            current_station = trajectory.stations[-1]
            current_available_connections = self.available_connections[current_station]
            new_connection = self.pick_connection(current_available_connections, trajectory)

            if new_connection != None:

                score_before = self.network.calculate_score()

                new_station = self.determine_new_station(current_station, new_connection)
                trajectory.stations.append(new_station)
                trajectory.route.append(new_connection)
                
                trajectory.time += new_connection.time
                self.network.used[new_connection] = True

                score_after = self.network.calculate_score()

                # if score_before > score_after:
                #     self.remove_connection(trajectory, new_station, new_connection)

            else:
                break
    
        return trajectory

    def create_network(self):

        trajectory_count = 1
        max_iterations = 10
        current_iteration = 0
        best_network = self.network
        
        while current_iteration < max_iterations and len(self.network.trajectories) < self.network.max_trajectories:

            score_before = self.network.calculate_score()
            trajectory = self.create_trajectory(trajectory_count)
            score_after = self.network.calculate_score()

            if score_before >= score_after:
                current_iteration += 1
                self.network.trajectories.remove(trajectory)

                for connection in trajectory.route:
                    self.network.used[connection] = False

            else:
                best_network = copy.copy(self.network)
            
            trajectory_count += 1

        self.network = best_network
        return self.network

