from ..algorithms.random_algo import Random_algo
from ..algorithms.greedy_algo import Greedy_algo
from ..classes.network import Network, Trajectory
import matplotlib.pyplot as plt
import random
import pprint as pp


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
            trajectory = Random_algo.create_trajectory(self.network) 
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
            pick = random.randint(0,len(self.network.trajectories)-1)
            remove_traj = self.network.trajectories[pick]
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

    def run(self):
        # print('old_score', self.network.get_score())
        score_list = []
        tries = 0 
        previous_score = self.network.get_score()
        while tries < self.attempts:
            # print('initial', self.network.get_score())    
            action = self.pick_action()
            add_traj, remove_traj, change = self.act(action)
            # print(f'after{action}: {self.network.get_score()}')    
            if not self.improving(previous_score): 
                
                if change:

                    self.undo(action, add_traj, remove_traj)
                    # print('after undo', self.network.get_score())
            tries +=1 
            previous_score = self.network.get_score()
            
            score_list.append(previous_score)
        # print('new_score', self.network.get_score())
        # plt.plot(score_list)
        # plt.show()

        return self.network

