from ..algorithms.random_algo import Random_algo
from ..algorithms.greedy_algo import Greedy_algo
from ..classes.network import Network, Trajectory
import matplotlib.pyplot as plt
import random

class Hillclimber():
    """
    Class Hillclimber: algorithm that keeps randomly changing a small part of a network until score doesn't improve anymore;
    
    Attributes:
    - network (Network instance): Network to be optimized
    - attempts (int): amount of times hillclimber tries to improve the score until stopping
    - scorelist (list): list of scores per iteration
    - algorithm (str): algorithm to be used for trajectory creation

    Methods:
    - improving - determine whether current change improves total network score
    - remove_and_update - removes a trajectory and update used dict of network
    - add_and_update - add new trajectory and update used dict of network
    - replace - replace a trajectory with another one
    - pick_action - choose an action (of the above 3) to perform
    - pick_best_trajectory - create group of 10 trajectories and pick the best one for this network
    - uneven_open_connections - check if trajectory has an uneven number of unused connections
    - pick_random_trajectory - pick a trajectory at random from the trajectories list of the network
    - run - run the hillclimber algorithm for an 'attempts' number of iterations
    """
    
    def __init__(self, network: Network, attempts: int, algorithm: str) -> None:
        self.network = network
        self.attempts = attempts 
        self.scorelist = []
        self.algorithm = algorithm

    def improving(self, previous_score: int) -> bool:
        return self.network.get_score() > previous_score

    def remove_and_update(self, trajectory: Trajectory):
        """
        Remove a trajectory and update the used dictionary of the network accordingly.

        Args:
        - trajectory (instance of Trajectory class): trajectory to be removed.
        """
        
        self.network.remove_trajectory(trajectory) 
        self.change_used_connections('remove', trajectory.route)
   

    def add_and_update(self, trajectory: Trajectory):
        """
        Add a trajectory and update the used dictionary of the network accordingly.

        Args:
        - trajectory (instance of Trajectory class): trajectory to be added.
        """
        self.network.add_trajectory(trajectory)
        self.change_used_connections('add', trajectory.route)

    def replace(self, add_traj: Trajectory, remove_traj: Trajectory):
        """
        Replace a trajectory with another trajectory in your network.

        Args:
        - trajectory (instance of Trajectory class): trajectory to be added.
        """
        self.remove_and_update(remove_traj)
        self.add_and_update(add_traj)
    
    def pick_action(self) -> str:
        """
        Randomly select either add, remove or replace as next action to adapt network.

        Returns: 
        - action (str): name of action that is going to be performed.
        """
    
        actionlist = ['add', 'remove', 'replace']
        number = random.randint(0,2)

        return actionlist[number]
    
    def pick_best_trajectory(self, heuristic:bool) -> Trajectory:
        """
        Creates 10 possible trajectories to add and selects the one that would improve the score most. Heuristic applied that if a start-
        or endstation is one that has an uneven number of open connections, it gets extra points.
        
        Args: 
        - heuristic (bool): value saying if heuristic should be applied
        Returns:
        - best_trajectory (trajectory instance): trajectory that would show the best score improvement if added.
        """
        add_traj = {}

        # create 10 trajectories
        for x in range(10):

            # use greedy algo to create trajectories
            if self.algorithm == 'greedy':
                used_copy = self.network.used.copy()
                trajectory = Greedy_algo.create_trajectory(self.network, random.randint, used_copy)
            else: 
                trajectory = Random_algo.create_trajectory(self.network) 

            # make a list of all connections that are used by this trajectory that were not already in the network 
            used_connections_traj = [connection for connection in  trajectory.route if self.network.used[connection] == 0]

            # list of all connections used by the network
            used_connections_netw = [connection for connection, value in self.network.used.items() if value != 0] 

            # calculate possible score if trajectory is added
            all_connections = used_connections_traj + used_connections_netw 
            new_fraction = len(all_connections) / len(self.network.connections) 
            possible_score= new_fraction * 10000 - (100 + trajectory.time)
            
            # check if begin- or endstation currently has uneven open connections and if so, add 1000 points
            if heuristic: 
                if self.uneven_open_connections(trajectory):
                    possible_score += 1000

            add_traj[trajectory] = possible_score

        # pick best fit
        best_trajectory =  max(add_traj, key=add_traj.get) 

        return best_trajectory
    def uneven_open_connections(self, trajectory: Trajectory) -> bool: 
        """
        Check if current open connections for end- and startstation is an uneven number. 
        
        Args: 
        - trajectory (Trajectory instance): trajectory that needs assessment
        Returns:
        - bool: true if either end- or startstation of trajectory has an uneven number of open connections.
        """

        # get start and end station of trajectory
        available_connections_start = self.network.available_connections[trajectory.stations[0]] 
        available_connections_end = self.network.available_connections[trajectory.stations[-1]]

        # collect open connections of both stations
        open_connections_start = [connection for connection in available_connections_start if self.network.used[connection] == 0]
        open_connections_end = [connection for connection in available_connections_end if self.network.used[connection] == 0] 

        return (len(open_connections_start) % 2 != 0) or (len(open_connections_end) % 2 != 0)

    def pick_random_trajectory(self) -> Trajectory:
        """
        Picks a random trajectory from the list of trajectories in network.
        
        Returns:
        - trajectory (Trajectory instance): trajectory to be used.
        """
        pick = random.randint(0,len(self.network.trajectories)-1)
        trajectory = self.network.trajectories[pick]

        return trajectory

    def act(self, action: str) -> tuple[Trajectory, Trajectory, bool]:
        """
        Add, remove or replace trajectories from a network instance. 
        Args: 
        - action (str): name of action that needs to be done
        - trajectory: trajectory that the change needs to be applied to
        Returns: 
        - trajectory (instance of Trajectory class): trajectory that was changed.
        - change (bool): variable to indicate whether anything was changed.
        """
        change = False

        # create group of 10 trajectories and pick the best one
        add_traj = self.pick_best_trajectory(True)
        
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

    def undo(self, action: str, add_traj: Trajectory, remove_traj: Trajectory):
        """
        Undo previous action. 
        
        Args:
        - action (str): previously performed action
        - add_traj: trajectory that was added
        - remove_traj: trajectory that was removed
        """
        if action == 'add':
            self.remove_and_update(add_traj)   

        elif action == 'remove':
            self.add_and_update(remove_traj)

        else:
            self.replace(remove_traj, add_traj)

    def change_used_connections(self, action:str, connection_list:list):
        """
        Updates the used dictionary in network with the connections from the adapted trajectories list. 
        Args: 
        - action (str): name of action that was taken
        - connection_list (list): list of connections that was changed 
        """
        
        for connection in connection_list:
            if action == 'add': 
                self.network.used[connection] += 1
                
            if action == 'remove':
                self.network.used[connection] -= 1

    def run(self) -> Network:
        """
        Run the hillclimber algorithm for 'attempts' iterations.

        Returns:
        - self.network (Network instance): network optimized with hillclimber network.
        """

        tries = 0 
        previous_score = self.network.get_score()

        # keep going until maximum attempts is reached
        while tries < self.attempts:

            # save score in the list of scores (for plotting)
            self.scorelist.append(previous_score)

            # update previous score for comparison
            previous_score = self.network.get_score()

            # pick action to perform and do it
            action = self.pick_action()
            add_traj, remove_traj, change = self.act(action)

            # if previous action did not improve the score, undo the action
            if self.improving(previous_score):
                pass
            else:
                if change:
                    self.undo(action, add_traj, remove_traj)
        
            tries +=1 
        
        return self.network
