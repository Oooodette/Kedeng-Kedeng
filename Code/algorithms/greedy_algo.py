from ..classes import Trajectory
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
        self.availables_copy = copy.copy(self.available_connections)


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

    def pick_start_station(self):
        """
        Picking start station either random or based on heuristic
        heuristic = pick start station with lowest number of connections
        Args:
        - trajectory(trajectory object)
        Returns:
        - start_station(station object)
        """
        Heuristic = False

        #with heuristic: pick start station of which the number of connection is lowest
        if Heuristic:
            l = list(self.availables_copy.values())

            lowest_len_connections = min(len(connections) for connections in l)

            for key, value in self.availables_copy.items():
                if len(value) == lowest_len_connections:
                    start_station = key

            #define attribute to reset if trajectory is rejected
            self.previous_start = (start_station, self.availables_copy[start_station])

            del self.availables_copy[start_station]            

        #without heuristic: random starting station
        else:
            start_station = self.network.stations[random.randint(0, len(self.network.stations) - 1)].name

        return start_station

    def determine_new_station(self, current_station, new_connection):
       
        if current_station == new_connection.station1:
            new_station = new_connection.station2

        elif current_station == new_connection.station2:
            new_station = new_connection.station1

        return new_station

    def look_forward(self, trajectory):
        """
        Look forward from the current station, gives score to a connection in the future if connection is undriven
        Args: 
        - trajectory(trajectory object)
        Returns:
        - connection_picked(connection object)
        """

        #retrieve the current station and its potential connections, init score list
        current_station = trajectory.stations[-1]
        potential_connections = self.available_connections[current_station]
        scores_list = []

        #copy the used_dict, keep track of potential use of connections
        used = copy.copy(self.network.used)

        #loop over all potential connections of the current station
        for potential in potential_connections:
            potential_time = trajectory.time + potential.time

            """if potential_time < self.network.max_trajectory_time:"""

            #keep track of the time the potential connections would add to the network, init score of one potential
            score = 0

            #check if potential is used, if not, set to True, check if time with this potential would not exceed max time 
            if used[potential] == 0 and potential_time <= self.network.max_trajectory_time:
                    score += 4
                    used[potential] += 1
        
            #retrieve the potentials of the potential, i.e. the first_gen_potentials
            first_gen_station = self.determine_new_station(current_station, potential)
            first_gen_potentials = self.available_connections[first_gen_station]

            #loop over the first_gen_potentials
            for first_gen_potential in first_gen_potentials:
                potential_time += first_gen_potential.time

                #check if potential is used, if not, set to True, check if time with this potential would not exceed max time 
                if used[first_gen_potential] == 0 and potential_time < self.network.max_trajectory_time:
                    score += 3
                    potential_time += potential_time
                    used[first_gen_potential] += 1


                """
                #retrieve potentials of potentials of potentials i.e. second_gen_potentials
                second_gen_station = self.determine_new_station(first_gen_station, first_gen_potential)
                second_gen_potentials = self.available_connections[second_gen_station]

                #loop over the second_gen_potentials
                for second_gen_potential in second_gen_potentials:
                    potential_time += second_gen_potential.time

                    #check if potential is used, if not, set to True, check if time with this potential would not exceed max time 
                    if used[second_gen_potential] == 0 and potential_time <= self.network.max_trajectory_time:
                        score += 2
                        used[second_gen_potential] += 1
                
                    #retrieve potentials of potentials of potentials of potentials, i.e. third_gen_potentials
                    thrird_gen_station = self.determine_new_station(second_gen_station, second_gen_potential)
                    third_gen_potentials = self.available_connections[thrird_gen_station]

                    #loop over third_gen_potentials
                    for third_gen_potential in third_gen_potentials:
                        potential_time += third_gen_potential.time

                        #check if potential is used, if not, set to True, check if time with this potential would not exceed max time 
                        if used[third_gen_potential] == 0 and potential_time <= self.network.max_trajectory_time:
                            score += 1
                            used[third_gen_potential] += 1
                        
                        #reset third_gen_potential attributes after checking 
                        used[third_gen_potential] = False
                        potential_time -= third_gen_potential.time
                    
                    #reset second_gen_potential attributes after checking branch
                    used[second_gen_potential] -= 1
                    potential_time -= second_gen_potential.time
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

        #TODO: check if connection with highest score does not make time in trajectory exceed max time
        if (trajectory.time + potential_connection.time) < self.network.max_trajectory_time:
            return potential_connection
        else:
            return None
        
    def pick_connection(self, available_connections, trajectory):
        """
        Pick connection based on criteria;
        - time of trajectory does not exceed max
        - picked connection is not the previous connection
        Args:
        - available_connections(list of connection object)
        - trajectory(trajectory object)
        Returns:
        - potential_connection(connection object)
        """

        #set chosen to False, make copy of available connections
        chosen = False
        available_connections_copy = copy.copy(available_connections)

        #loop over available connections until empty and pick random new connection
        while not chosen and (len(available_connections_copy)) > 0:
            potential_connection = available_connections_copy[random.randint(0, (len(available_connections_copy) - 1))]

            #remove option from availables list
            available_connections_copy.remove(potential_connection)

            #check criteria
            if (trajectory.time + potential_connection.time) < self.network.max_trajectory_time and potential_connection != trajectory.route[-1]:

                chosen = True
                return potential_connection

    def create_trajectory(self, trajectory_count):
        """
        Create a trajectory by sequencing connections
        Args:
        - trajectory_count(int)
        Returns:
        - trajectory(trajectory object)
        """
        
        #create an 'empty' instance of a trajectory and add to network
        trajectory = Trajectory(trajectory_count, [], 0)
        trajectory.route = [None]

        #add trajectory to the network
        self.network.add_trajectory(trajectory)

        #pick starting station and connection
        while len(trajectory.stations) == 0:

            start_station = self.pick_start_station()

            trajectory.stations.append(start_station)
            
            # start_available_connections = self.available_connections[start_station]
            # start_connection = self.pick_connection(start_available_connections, trajectory)
            
            start_connection = self.look_forward(trajectory)

            #update trajectory if startstation and connection are not None, else remove start station
            if start_connection != None:
                current_station = self.determine_new_station(start_station, start_connection)
                trajectory.stations.append(current_station)
                trajectory.route.append(start_connection)
                trajectory.time += start_connection.time
                self.network.used[start_connection] += 1

            else:
                trajectory.stations.remove(start_station)                

        #add new connection by looping while trajectory time does not exceed max time       
        while trajectory.time < self.network.max_trajectory_time:

            current_station = trajectory.stations[-1]

            # current_available_connections = self.available_connections[current_station]
            # new_connection = self.pick_connection(current_available_connections, trajectory)
            
            new_connection = self.look_forward(trajectory)

            #update trajectory if startstation and connection are not None, else remove start station
            if new_connection != None:
                new_station = self.determine_new_station(current_station, new_connection)
                trajectory.stations.append(new_station)
                trajectory.route.append(new_connection)
                trajectory.time += new_connection.time
                self.network.used[new_connection] += 1

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
                
        #loop while criteria for a new trajectory are fulfilled (iterations, max trajectories)
        while current_iteration < max_iterations and len(self.network.trajectories) < self.network.max_trajectories:
           
            #take score before, create and add a trajectory and take score after
            score_before = self.network.calculate_score()
            trajectory = self.create_trajectory(trajectory_count)
            score_after = self.network.calculate_score()

            #remove trajectory if score did not increase
            if score_before >= score_after:
                current_iteration += 1

                self.network.trajectories.remove(trajectory)
                # self.availables_copy[self.previous_start[0]] = self.previous_start[1]

                #reset the connections to unused when trajectory is removed
                for connection in trajectory.route:
                    self.network.used[connection] -= 1

            else:
                trajectory_count += 1

        return self.network

