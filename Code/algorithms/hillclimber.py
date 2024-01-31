from ..algorithms.random_algo import Random_algo
from ..algorithms.greedy_algo import Greedy_algo
from ..classes.network import Network, Trajectory
import matplotlib.pyplot as plt
import random
import pprint as pp
import math
import numpy as np
import copy


class Hillclimber():
    """
    Class Hillclimber: algorithm that keeps randomly changing a small part of a network until score doesn't improve anymore;
        Attributes:
        - random: an instance of the random_algo class that was created beforehand.
        - attempts: amount of times hillclimber tries to improve the score until stopping.

        Methods:
        - improving: determine whether current change improves total network score
        - add: add new trajectory to network while score is improving
        - replace: replace existing trajectory with new trajectory while score is improving
    """
    
    def __init__(self, network: Network, attempts) -> None:
        self.network = network
        self.attempts = attempts 
    
    def improving(self, previous_score):
        return self.network.get_score() > previous_score

    def save_score_parts(self, fractionlist, subtractionlist):
        
        fraction, subtraction = self.network.calculate_score()
        fractionlist.append(fraction)
        subtractionlist.append(subtraction)

        return fractionlist, subtractionlist
    
    def plot_score_parts(self, fractionlist, subtractionlist):
        plt.plot(list(range(0,len(fractionlist))),fractionlist)
        plt.plot(list(range(0,len(fractionlist))),subtractionlist)
        plt.show()  

    def remove_and_update(self, trajectory):
        """
        Remove a trajectory and update the used dictionary of the network accordingly.
        Args:
        - trajectory(instance of Trajectory class): trajectory to be removed.
        """
        
        self.network.remove_trajectory(trajectory) 
        self.change_used_connections('remove', trajectory.route)
   

    def add_and_update(self, trajectory):
        """
        Add a trajectory and update the used dictionary of the network accordingly.
        Args:
        - trajectory(instance of Trajectory class): trajectory to be added.
        """
        self.network.add_trajectory(trajectory)
        self.change_used_connections('add', trajectory.route)

    def replace(self, add_traj, remove_traj):
        self.remove_and_update(remove_traj)
        self.add_and_update(add_traj)
    
    def pick_action(self):
        """
        Randomly select either add, remove or replace as next action to adapt network.
        Returns: 
        - action(str): name of action that is going to be performed.
        """
    
        actionlist = ['add', 'remove', 'replace']
        number = random.randint(0,2)

        return actionlist[number]
    
    def pick_best_trajectory(self, heuristic):
        add_traj = {}

        for x in range(10):
            used_copy = self.network.used.copy()
            trajectory = Greedy_algo.create_trajectory(self.network, random.randint, used_copy) 
            used_connections_traj = [connection for connection in  trajectory.route if self.network.used[connection] == 0]
            used_connections_netw = [connection for connection, value in self.network.used.items() if value != 0] 
            all_connections = used_connections_traj + used_connections_netw 
            new_fraction = len(all_connections) / len(self.network.connections) 
            possible_score= new_fraction * 10000 - (100 + trajectory.time)
            
            
            if heuristic: 
                available_connections_start = self.network.available_connections[trajectory.stations[0]] 
                available_connections_end = self.network.available_connections[trajectory.stations[-1]]
                open_connections_start = [connection for connection in available_connections_start if self.network.used[connection] == 0]
                open_connections_end = [connection for connection in available_connections_end if self.network.used[connection] == 0] 
                if len(open_connections_start) % 2 != 0 or len(open_connections_end) % 2 != 0:
                    possible_score += 1000

            add_traj[trajectory] = possible_score

        best_trajectory =  max(add_traj, key=add_traj.get) 

        return best_trajectory

    def pick_random_trajectory(self):
        pick = random.randint(0,len(self.network.trajectories)-1)
        trajectory = self.network.trajectories[pick]
        return trajectory

    def act(self, action):
        """
        Add, remove or replace trajectories from a network instance. 
        Args: 
        - action(str): name of action that needs to be done
        - trajectory: trajectory that the change needs to be applied to
        Returns: 
        - trajectory(instance of Trajectory class): trajectory that was changed.
        - change(bool): variable to indicate whether anything was changed.
        """
        change = False
        # create random trajectory to add

        add_traj = self.pick_best_trajectory(True)
        # Random_algo.create_trajectory(self.network)
        #self.pick_best_trajectory(True)
        
        # select random trajectory to be removed
        if len(self.network.trajectories) > 0: 
            remove_traj = self.pick_random_trajectory() 
        else: 
            remove_traj = None

        # determine which action needs to be taken and if number of trajectories will stay between limits
        if action == 'add' and len(self.network.trajectories) < self.network.max_trajectories:
            self.add_and_update(add_traj)
            change = True
        elif action == 'remove' and len(self.network.trajectories) > 0:
            self.remove_and_update(remove_traj)   
            change = True
        elif action ==  'replace' and len(self.network.trajectories) > 0:
            self.replace(add_traj, remove_traj)
            change = True

        return add_traj, remove_traj, change

    def undo(self, action, add_traj, remove_traj):

        if action == 'add':
            self.remove_and_update(add_traj)   

        elif action == 'remove':
            self.add_and_update(remove_traj)

        else:
            self.replace(remove_traj, add_traj)

    def change_used_connections(self, action, connection_list):
        """
        Updates the used dictionary in network with the connections from the adapted trajectories list. 
        Args: 
        - action(str): name of action that was taken
        - connection_list(list): list of connections that was changed 
        """
        
        for connection in connection_list:
            if action == 'add': 
                self.network.used[connection] += 1
                
            if action == 'remove':
                self.network.used[connection] -= 1

    def calc_acception(self, previous_score, current_temp):
        diff = previous_score - self.network.get_score()
        print(diff, 'diff')
        # calculate metropolis acceptance criterion
        metropolis = np.exp(-(diff / current_temp))

        return metropolis
    
    def remove_connections(self, amount, trajectory): 
        
        shorter_traj = copy.deepcopy(trajectory)
        shorter_traj.route = shorter_traj.route[:-amount]
        self.replace(shorter_traj, trajectory) 

        return shorter_traj
    
    def add_connections(self, amount, trajectory):
        
        addition = 0
        new_trajectory = copy.deepcopy(trajectory)
        current_station = new_trajectory.stations[-1]
        previous_connection = new_trajectory.route[-1]
        # if new_trajectory.time < 120:
        print(new_trajectory.time)
        
        while new_trajectory.time < self.network.max_trajectory_time and addition <= amount:
            new_connection = Random_algo.pick_valid_connection(self.network, current_station, previous_connection, new_trajectory.time) 
            
            # if a valid connection is found, change the current station to the next station of this connection
            if new_connection != None:
                print('hi')

                current_station = Random_algo.determine_station(current_station, new_connection)
            
                # add station, connection and time to trajectory	
                new_trajectory.stations.append(current_station) 
                new_trajectory.route.append(new_connection) 
                new_trajectory.time += new_connection.time 
                
                previous_connection = new_connection 

            addition += 1
        print(len(new_trajectory.route), len(trajectory.route))
        self.replace(new_trajectory, trajectory) 

        return new_trajectory

    def run(self):
        print('old_score', self.network.get_score())

        tries = 0 
        previous_score = self.network.get_score()
        temp = 1000


        while tries < self.attempts:
            
            # calculate temperature for current try
            current_temp = temp / float(tries + 1)

            if tries < self.attempts/2:


                action = self.pick_action()
                add_traj, remove_traj, change = self.act(action)
                metropolis = self.calc_acception(previous_score, current_temp)

                
                if self.improving(previous_score) or random.random() < metropolis: 
                    pass

                else:
                    if change:
                        self.undo(action, add_traj, remove_traj)
                tries +=1 
                previous_score = self.network.get_score()
            
            else:

                # pick a random trajectory to adapt and select randomly whether it will be shortened, or lengthened
                trajectory_pick = self.pick_random_trajectory()
                amount = random.randint(1,3) 
                action = random.choice(['add', 'remove']) 

                # adapt the trajectory and calculate the acceptance chance
                if action == 'remove': 
                    print('remove')
                    new_trajectory = self.remove_connections(amount, trajectory_pick)

                else: 
                    print('add')
                    print('score before add', self.network.get_score())
                    new_trajectory = self.add_connections(amount, trajectory_pick)
                    print('score after add', self.network.get_score())

                # calculate acceptance possibility
                metropolis = self.calc_acception(previous_score, current_temp)
                print(metropolis)
                # check if score improves and undo your actions if it does not
                if self.improving(previous_score)  or random.random() < metropolis: 
                    pass
                else:
                    self.replace(trajectory_pick, new_trajectory)

                tries +=1 
            previous_score = self.network.get_score()

        print(previous_score)
        return self.network

        # while tries < self.attempts:
        #     trajectory_pick = self.pick_random_trajectory()
        #     amount = random.randint(1,3) 
        #     action = random.choice(['add', 'remove'])
            
        #     # calculate temperature for current epoch
        #     t = temp / float(tries + 1)


        #     # calculate metropolis acceptance criterion
        #     metropolis = np.exp(-diff / t)
            
        #     if action == 'remove' and len(trajectory_pick.route) > amount + 1:
                
        #         shorter_traj = copy.deepcopy(trajectory_pick)
        #         shorter_traj.route = shorter_traj.route[:-amount]
        #         self.replace(shorter_traj, trajectory_pick) 
        #         diff = previous_score - self.network.get_score() 
        #         if self.improving(previous_score): # or random.random() < metropolis: 
        #             pass
        #         else:
        #             self.replace(trajectory_pick, shorter_traj)

        #     if action == 'add':
        #         addition = 0
        #         new_trajectory = copy.deepcopy(trajectory_pick)
        #         current_station = new_trajectory.stations[-1]
        #         previous_connection = new_trajectory.route[-1]
                
        #         while new_trajectory.time < self.network.max_trajectory_time and addition <= amount:
        #             new_connection = Random_algo.pick_valid_connection(self.network.available_connections[current_station], previous_connection, trajectory_pick.time) 
                
        #             # if a valid connection is found, change the current station to the next station of this connection
        #             if new_connection != None:
                        
        #                 current_station = Random_algo.determine_station(current_station, new_connection)
        #                 new_trajectory.time += new_connection.time 

        #                 # add station and connection to trajectory	
        #                 new_trajectory.stations.append(current_station)
        #                 new_trajectory.route.append(new_connection) 
                        
        #                 previous_connection = new_connection 

        #             addition += 1

        #         for trajectory in self.network.trajectories:
        #             print(len(trajectory.route), 'before')
        #         self.replace(new_trajectory, trajectory_pick)
        #         for trajectory in self.network.trajectories:
        #             print(len(trajectory.route), 'after')
        #         diff = previous_score - self.network.get_score() 
        #         if self.improving(previous_score): # or random.random() < metropolis: 
        #             pass    
        #         else:
        #             self.replace(trajectory_pick, new_trajectory)
        #         previous_score = self.network.get_score()
        #     tries +=1 
        #     print(tries)

        #     previous_score = self.network.get_score()
       

