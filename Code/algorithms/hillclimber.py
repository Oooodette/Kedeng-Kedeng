from ..algorithms.random_algo import Random_algo
from ..classes.network import Network, Trajectory
import matplotlib.pyplot as plt
import random


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
    
    def __init__(self, network: Network, attempts):
        self.network = network
        self.attempts = attempts
    
    def improving(self, previous_score):
        return self.network.get_score() > previous_score

    def update_used(self):
        pass

    def save_score_parts(self, fractionlist, subtractionlist):
        
        fraction, subtraction = self.network.calculate_score()
        fractionlist.append(fraction)
        subtractionlist.append(subtraction)

        return fractionlist, subtractionlist
    
    def plot_score_parts(fractionlist, subtractionlist):
        plt.plot(list(range(0,len(fractionlist))),fractionlist)
        plt.plot(list(range(0,len(fractionlist))),subtractionlist)
        plt.show()
    
    def add(self, new_trajectory):
        """
        Adds random trajectory to a network instance.
        Args: 
        - new_trajectory(instance of Trajectory class): trajectory needs to be added
        Returns:
        - new_trajectory(instance of Trajectory class): trajectory that was added.
        """
  
        self.network.add_trajectory(new_trajectory) 

        return new_trajectory
    
    def remove(self, trajectory: Trajectory , undo = False):
        """
        Removes trajectory from trajectory list of network instance. 
        Args:
         trajectory(instancee of Trajectory class): trajectory to be removed if not random (see below)
         undo(bool): represents whether the action was an initial action, or the consequence of an addition that gave no score improvement.
                    default = False, meaning it is an initial action. In that case, a random trajectory from the list is picked to be removed.
        Returns: 
        - trajectory(instance of Trajectory class): trajectory that was removed)
        """
        # check whether this action was because of an earlier addition
        if not undo:
            pick = random.randint(0,len(self.network.trajectories)-1)
            trajectory = self.network.trajectories[pick]

        self.network.remove_trajectory(trajectory)

        return trajectory
        

    def replace(self, add_trajectory, remove_trajectory):

        trajectory1 = self.remove(remove_trajectory)
        trajectory2 = self.add(add_trajectory)

        return trajectory1, trajectory2

    
    def pick_action(self):
        """
        Randomly select either add, remove or replace as next action to adapt network.
        Returns: 
        - action(str): name of action that is going to be performed.
        """
    
        actionlist = ['add', 'remove', 'replace']
        number = random.randint(0,1)

        return actionlist[number]
    
    def act(self, action, trajectory):
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

        # determine which action needs to be taken and if number of trajectories will stay between limits
        if action == 'add' and len(self.network.trajectories) < self.network.max_trajectories:
            self.add(trajectory)
            change = True
        elif action == 'remove' and len(self.network.trajectories) > 0:
            trajectory = self.remove(trajectory)   
            change = True
        elif action ==  'replace' :
            trajectory, changed_list = self.replace(trajectory)
            change = True

        if change:
            self.change_used_connections(action, trajectory.route)

        return trajectory, change

    def undo(self, action, trajectory):

        if action == 'add':
            trajectory = self.remove(trajectory, undo=True)
            self.change_used_connections('remove', trajectory.route)

        elif action == 'remove':
            trajectory = self.add(trajectory)
            self.change_used_connections('add', trajectory.route)

        else:
            trajectory = self.replace()
        
        return trajectory 

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
        print('old_score', self.network.get_score())
        tries = 0 
        previous_score = self.network.get_score()
        
        while tries < self.attempts: 
            new_trajectory = Random_algo.create_trajectory(self.network)  
            action = self.pick_action()
            trajectory, change = self.act(action, new_trajectory)
 
            if not self.improving(previous_score): 
                if change:
                    self.undo(action, trajectory)
                    tries += 1

            previous_score = self.network.get_score()
        print('new_score', self.network.get_score())
        return self.network

