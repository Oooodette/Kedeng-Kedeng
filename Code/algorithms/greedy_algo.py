from ..classes import Station, Connection, Trajectory, Network
import pandas as pd
import random 
import pprint as pp 
import copy 

class Greedy_algo():
    """
    Greedy algorithm class;
    Attrs:
    - self.network(network object)
    - self.available_connections(dict)
    - self.available_connections_copy(dict)

    Methods:
    - create_available_connections() - creates dict; key=station, value=list of connection object
    - pick_start_station() - picking a starting station for a trajectory (random or heuristic)
    - determine_new_station() - returns the connected station from using a connection
    - look_forward() - looks four connections ahead to and scores undriven connections with 1
    - pick_connection() - picks a valid connection without looking forward
    - create_trajectory() - creates a trajectory based on either look_forward or pick_connection
    - create_network() - creates a network consisting of multiple trajectories
    """
    def __init__(self, network):
        """
        initializing the algorithm by adding a network
        """
        self.network = copy.deepcopy(network)
        self.available_connections = self.create_available_connections(self.network.stations, self.network.connections)

    def create_available_connections(self, station_list, connection_list): 
        """
        Creates a dict of available connections for each station
        Args:
        - station list(list)
        - connection_list(list)
        Returns:
        - available_connections_dict(dict; key=name of the station, value=list of connection objects)
        """

        #initialize dict and loop over all stations, create a list for each station
        available_connections_dict = {}
        for station in station_list:
            station_connections = [] 

            #loop over all connections, check if station is in the connection
            for connection in connection_list:
                if station.name == connection.station1 or station.name == connection.station2:
                    station_connections.append(connection)
            
            #add connections to the dict
            available_connections_dict[station.name] = station_connections
                   
        return available_connections_dict

    @staticmethod
    def pick_start_station(network):
        """
        Picking start station randomly
        Args:
        - trajectory(trajectory object)
        Returns:
        - start_station(station object)
        """

        start_station = network.stations[random.randint(0, len(network.stations) - 1)].name
        return start_station

    @staticmethod
    def determine_new_station(current_station, new_connection):
        """
        Determine new station based on current_station and new_connection
        Args:
        - current_station(station object)
        - new_connection(connection object)
        Returns:
        - new_station(station object)
        """
       
        if current_station == new_connection.station1:
            new_station = new_connection.station2

        elif current_station == new_connection.station2:
            new_station = new_connection.station1

        return new_station
   
    @staticmethod
    def one_forward_look(network, trajectory, current_station, potential, available_connections, used, score):

        potential_time = trajectory.time + potential.time

        #check if potential is used, if not, set to True, check if time with this potential would not exceed max time 
        if used[potential] == 0 and potential_time <= network.max_trajectory_time:
                score += 4
                used[potential] += 1
    
        #retrieve the potentials of the potential, i.e. the first_gen_potentials
        x_gen_station = Greedy_algo.determine_new_station(current_station, potential)
        x_gen_potentials = available_connections[x_gen_station]

        return x_gen_station, x_gen_potentials, used, potential_time, score


    @staticmethod
    def look_forward(network, trajectory, available_connections):
        """
        Look forward from the current station, gives score to a connection in the future if connection is undriven
        Args: 
        - trajectory(trajectory object)
        Returns:
        - connection_picked(connection object)
        """

        #retrieve the current station and its potential connections, init score list
        current_station = trajectory.stations[-1]
        potential_connections = available_connections[current_station]
        scores_list = []

        #copy the used_dict, keep track of potential use of connections
        used = copy.copy(network.used)

        #loop over all potential connections of the current station
        for potential in potential_connections:
            
            #keep track of the time the potential connections would add to the network, init score of one potential
            score = 0

            #look forward and return variables necessary to look forward further
            first_gen_station, first_gen_potentials, used, potential_time, score = Greedy_algo.one_forward_look(network, trajectory, current_station, potential, available_connections, used, score)
        

            #loop over the first_gen_potentials
            for first_gen_potential in first_gen_potentials:

                # second_gen_station, second_gen_potentials, used, potential_time, score = Greedy_algo.one_forward_look(network, trajectory, current_station, potential, available_connections, used, score)


                potential_time += first_gen_potential.time

                #check if potential is used, if not, set to True, check if time with this potential would not exceed max time 
                if used[first_gen_potential] == 0 and potential_time < network.max_trajectory_time:
                    score += 3
                    potential_time += potential_time
                    used[first_gen_potential] += 1


                """
                # #retrieve potentials of potentials of potentials i.e. second_gen_potentials
                # second_gen_station = Greedy_algo.determine_new_station(first_gen_station, first_gen_potential)
                # second_gen_potentials = available_connections[second_gen_station]

                # #loop over the second_gen_potentials
                # for second_gen_potential in second_gen_potentials:
                #     potential_time += second_gen_potential.time

                #     #check if potential is used, if not, set to True, check if time with this potential would not exceed max time 
                #     if used[second_gen_potential] == 0 and potential_time <= network.max_trajectory_time:
                #         score += 2
                #         used[second_gen_potential] += 1
                
                #     #retrieve potentials of potentials of potentials of potentials, i.e. third_gen_potentials
                #     thrird_gen_station = Greedy_algo.determine_new_station(second_gen_station, second_gen_potential)
                #     third_gen_potentials = available_connections[thrird_gen_station]

                #     #loop over third_gen_potentials
                #     for third_gen_potential in third_gen_potentials:
                #         potential_time += third_gen_potential.time

                #         #check if potential is used, if not, set to True, check if time with this potential would not exceed max time 
                #         if used[third_gen_potential] == 0 and potential_time <= network.max_trajectory_time:
                #             score += 1
                #             used[third_gen_potential] += 1
                        
                #         #reset third_gen_potential attributes after checking 
                #         used[third_gen_potential] = False
                #         potential_time -= third_gen_potential.time
                    
                #     #reset second_gen_potential attributes after checking branch
                #     used[second_gen_potential] -= 1
                #     potential_time -= second_gen_potential.time
                """  


                #reset first_gen_potential attributes after checking branch
                used[first_gen_potential] -= 1
                potential_time -= first_gen_potential.time

            #reset potential attributes after checking branch
            used[potential] -= 1
            potential_time -= potential.time
        
            #adding the score of the potential to the list
            scores_list.append(score)    

        #retrieving the potential with max score, picking connection
        index_max = max(range(len(scores_list)), key=scores_list.__getitem__)
        potential_connection = potential_connections[index_max]

        #check if connection with highest score does not make time in trajectory exceed max time
        if (trajectory.time + potential_connection.time) < network.max_trajectory_time:
            return potential_connection
        else:
            return None
    
    @staticmethod
    def update_trajectory(network, trajectory, current_station, new_connection):
        """
        Updates attributes of a trajectory based on current_station and a new connection
        Args:
        - network(network object)
        - trajectory(trajectory object)
        - current_station(station object)
        - new_connection(connection object)
        Returns:
        - Nothing, but updates attributes of trajectory
        """

        #determine and append the new station, visited by using the new connection
        current_station = Greedy_algo.determine_new_station(current_station, new_connection)
        trajectory.stations.append(current_station)

        #append the trajectory, increase time of trajectory with time of connection
        trajectory.route.append(new_connection)
        trajectory.time += new_connection.time

        #increase the used count of the connection
        network.used[new_connection] += 1

    @staticmethod
    def create_trajectory(network, trajectory_count):
        """
        Create a trajectory by sequencing connections
        Args:
        - trajectory_count(int)
        Returns:
        - trajectory(trajectory object)
        """
        
        #create an 'empty' instance of a trajectory and add to network
        trajectory = Trajectory(trajectory_count, [], [], 0)
        network.add_trajectory(trajectory)

        #retrieve available connections
        available_connections = network.available_connections

        count = 0
        #init trajectory; pick starting station, add to trajectory, pick start connection
        start_station = Greedy_algo.pick_start_station(network)
        trajectory.stations.append(start_station)
        start_connection = Greedy_algo.look_forward(network, trajectory, available_connections)

        #update trajectory if first connection is not None, else remove start station
        if start_connection != None:
            Greedy_algo.update_trajectory(network, trajectory, start_station, start_connection)

        else:
            trajectory.stations.remove(start_station)                

        #add new connection by looping while trajectory time does not exceed max time       
        while trajectory.time < network.max_trajectory_time:

            current_station = trajectory.stations[-1]
            new_connection = Greedy_algo.look_forward(network, trajectory, available_connections)

            #update trajectory attributes if startstation and connection are not None
            if new_connection != None:
                Greedy_algo.update_trajectory(network, trajectory, current_station, new_connection)
            else:
                break
    
        return trajectory

    def create_network(self):
        """
        Create a network by combining multiple trajectories;
            - only add if trajectory increases the score
        Args: None
        Returns:
        - self.network(network object)
        """

        #define trajectory name
        trajectory_count = 1

        #define how many times to keep trying to add a trajectory 
        current_iteration = 0
        max_iterations = 10
        traj_count = 0
        available_connections = self.network.available_connections
                
        #loop while criteria for a new trajectory are fulfilled (iterations, max trajectories)
        while current_iteration < max_iterations and len(self.network.trajectories) < self.network.max_trajectories:
           
            #take score before, create and add a trajectory and take score after
            score_before = self.network.get_score()
            trajectory = Greedy_algo.create_trajectory(self.network, trajectory_count)
            score_after = self.network.get_score()

            #remove trajectory if score did not increase, increase iteration
            if score_before >= score_after:
                current_iteration += 1
                self.network.trajectories.remove(trajectory)

                #reset the connections to unused when trajectory is removed
                for connection in trajectory.route:
                    self.network.used[connection] -= 1

            else:
                trajectory_count += 1

        return self.network

