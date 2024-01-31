from ..classes.network import Network, Trajectory

import pandas as pd
import random 
import pprint as pp 
import copy 

class Greedy_algo():
    """
    Greedy algorithm class.
    Attributes:
    - network (network object)

    Methods:
    - pick_start_station() - picking a starting station for a trajectory (random)
    - determine_new_station() - returns the connected station from using a connection
    - one_forward_look() - part of look_forward(); looks one connection ahead
    - look_forward() - looks two connections ahead, using one_look_forward(), and scores undriven connections respectively with 4 and 1
    - pick_connection() - picks a valid connection without looking forward
    - create_trajectory() - creates a trajectory based on either look_forward or pick_connection
    - create_network() - creates a network consisting of multiple trajectories
    """

    def __init__(self, network: Network):
        """
        Initializing the algorithm by adding an empty network, which will be modified
        """

        self.network = copy.deepcopy(network)

    @staticmethod
    def pick_start_station(network: Network):
        """
        Picking a start station randomly.

        Args:
        - network (network object): network that is being created
        Returns:
        - start_station(station object): station that is the start of a trajectory
        """

        start_station = network.stations[random.randint(0, len(network.stations) - 1)].name
        return start_station

    @staticmethod
    def determine_new_station(current_station, new_connection):
        """
        Determine new station based on current_station and new_connection.

        Args:
        - current_station (station object): station with which new_connection is connected
        - new_connection (connection object): the connection that is added to the trajectory
        Returns:
        - new_station (station object): the station at which we arrive by using new_connection
        """

        if current_station == new_connection.station1:
            new_station = new_connection.station2

        elif current_station == new_connection.station2:
            new_station = new_connection.station1

        return new_station
   
    @staticmethod
    def one_forward_look(network: Network, trajectory, current_station, potential, used, potential_time, score_potential, score_increase):
        """
        Looks one connection in the 'future' from current_station, evaluates all options;

        Args:
        - network (network object): the network that is being created
        - trajectory (trajectory object): trajectory that is being created
        - current_station (station object): station from which will be looked forward
        - potential (connection object): connection that will be scored
        - used (dict): dict that tracks usage of potentials
        - potential_time (int): current time of the potential
        - score (int): current score of the potential we are checking
        - score_increase (int): how much the score of the potential will increase if not used yet
        Returns:
        - x_gen_station (station object): the next station to check the potentials from
        - x_gen_potentials (list of connection objects): the list of potentials connected to x_gen_station
        - used(dict): tracks usage of potentials
        - potential_time (int): new_time of the potential
        - score (int): new score of the potential we are checking
        """

        #increase time of potential
        potential_time += potential.time

        #check if potential is used, if not, increase usage with 1, check if time with this potential would not exceed max time 
        if used[potential] == 0 and potential_time <= network.max_trajectory_time:
                score_potential += score_increase
                used[potential] += 1
    
        #retrieve the potentials of the potential, i.e. the first_gen_potentials
        x_gen_station = Greedy_algo.determine_new_station(current_station, potential)
        x_gen_potentials = network.available_connections[x_gen_station]

        return x_gen_station, x_gen_potentials, used, potential_time, score_potential

    @staticmethod
    def reset_forward_look(used, potential_time, potential):
        """
        Resetting the variables of the potentials

        Args:
        - used (dict): dict that tracks usage of potentials
        - potential_time (int): current time of the potential
        - potential (connection object) which potential to reset values for 
        Returns:
        - used(dict): dict that tracks usage of potentials
        - potential_time: (int): new time of the potential
        """

        #reset usage and decrease time of potentials
        used[potential] -= 1
        potential_time -= potential.time

        return used, potential_time

    @staticmethod
    def look_forward(network: Network, trajectory, used):
        """
        Look forward from the current station, gives score to a connection in the future if connection is undriven.

        Args: 
        - trajectory (trajectory object) trajectory for which we will look forward
        Returns:
        - connection_picked (connection object): new connection that is picked based on the scores
        """

        #retrieve the current station and its potential connections
        current_station = trajectory.stations[-1]
        potential_connections = network.available_connections[current_station]

        #initialize score list
        scores_list = []

        #copy the used connections dictionary to 
        used = copy.copy(used)

        #loop over all potential connections of the current station
        for potential in potential_connections:
            score_increase = 4
            
            # init score of one potential, retrieve trajectory time
            score_potential = 0
            potential_time = trajectory.time

            #look forward and return variables necessary to look forward further
            first_gen_station, first_gen_potentials, used, potential_time, score_potential = Greedy_algo.one_forward_look(network, trajectory, current_station, potential, used, potential_time, score_potential, score_increase)
        
            #loop over the first_gen_potentials
            for first_gen_potential in first_gen_potentials:
                score_increase = 1

                second_gen_station, second_gen_potentials, used, potential_time, score_potential = Greedy_algo.one_forward_look(network, trajectory, first_gen_station, first_gen_potential, used, potential_time, score_potential, score_increase)

                #reset first_gen_potential attributes after scoring branch
                used, potential_time = Greedy_algo.reset_forward_look(used, potential_time, first_gen_potential)

            #reset potential attributes after scoring branch
            used, potential_time = Greedy_algo.reset_forward_look(used, potential_time, potential)

            #adding the score of the potential to the list
            scores_list.append(score_potential)    

        #retrieving the potential with max score, picking connection
        index_max = max(range(len(scores_list)), key=scores_list.__getitem__)
        potential_connection = potential_connections[index_max]

        #check if connection with highest score does not make time in trajectory exceed max time
        if (trajectory.time + potential_connection.time) < network.max_trajectory_time:
            return potential_connection
        else:
            return None
    
    @staticmethod
    def update_trajectory(network: Network, trajectory, current_station, new_connection, used):
        """
        Updates attributes of a trajectory based on current_station and the new connection that will be added.

        Args:
        - network (network object): network that is being created
        - trajectory (trajectory object): trajectory to update the attributes of
        - current_station (station object): current station of the trajectory 
        - new_connection (connection object): new connection of the trajectory
        - used (dict): tracks connection usage
        Returns
        - used (dict): updated connection usage
        """

        #determine and append the new station, visited by using the new connection
        current_station = Greedy_algo.determine_new_station(current_station, new_connection)
        trajectory.stations.append(current_station)

        #append the trajectory, increase time of trajectory with time of connection
        trajectory.route.append(new_connection)
        trajectory.time += new_connection.time

        #increase the used count of the connection
        used[new_connection] += 1

        return used

    @staticmethod
    def create_trajectory(network: Network, trajectory_count, used):
        """
        Create a trajectory by sequencing connections.

        Args:
        - network (network object): network that is being created
        - trajectory_count (int): 'name' of the new trajectory
        - used (dict): tracks connection usage
        Returns:
        - trajectory (trajectory object): new trajectory that is created
        """
        
        #create an 'empty' instance of a trajectory and add to network
        trajectory = Trajectory(trajectory_count, [], [], 0)

        #init trajectory; pick starting station, add to trajectory, pick start connection
        start_station = Greedy_algo.pick_start_station(network)
        trajectory.stations.append(start_station)
        start_connection = Greedy_algo.look_forward(network, trajectory, used)

        #update trajectory if first connection is not None, else remove start station
        if start_connection != None:
            used = Greedy_algo.update_trajectory(network, trajectory, start_station, start_connection, used)

        else:
            trajectory.stations.remove(start_station)                

        #add new connection by looping while trajectory time does not exceed max time       
        while trajectory.time < network.max_trajectory_time:

            current_station = trajectory.stations[-1]
            new_connection = Greedy_algo.look_forward(network, trajectory, used)

            #update trajectory attributes if startstation and connection are not None
            if new_connection != None:
                used = Greedy_algo.update_trajectory(network, trajectory, current_station, new_connection, used)
            else:
                break
    
        return trajectory

    def create_network(self):
        """
        Create a network by combining multiple trajectories;
            greedy element: only add a trajectory if the newly created trajectory increases the score of the network.

        Returns:
        - self.network (network object): network that is created
        """

        #define trajectory name
        trajectory_count = 1

        #define how many times to keep trying to add a trajectory 
        current_iteration = 0
        max_iterations = 100
        traj_count = 0

        used = copy.copy(self.network.used)
                
        #loop while criteria for a new trajectory are fulfilled (iterations, max trajectories)
        while current_iteration < max_iterations and len(self.network.trajectories) < self.network.max_trajectories:
           
            #take score before, create a trajectory
            score_before = self.network.get_score()
            trajectory = Greedy_algo.create_trajectory(self.network, trajectory_count, used)

            #updating the used dict in the network
            for connection in trajectory.route:
                self.network.used[connection] += 1

            #add trajectory to network
            self.network.trajectories.append(trajectory)

            #take score after appending to network
            score_after = self.network.get_score()

            #remove trajectory if score did not increase, increase iteration
            if score_before >= score_after:
                current_iteration += 1
                self.network.trajectories.remove(trajectory)

                #reset the connections to be used one time less when trajectory is removed
                for connection in trajectory.route:
                    self.network.used[connection] -= 1

            else:
                #change name of next trajectory
                trajectory_count += 1

        return self.network
