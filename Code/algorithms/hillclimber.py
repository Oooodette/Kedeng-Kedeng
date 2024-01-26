from ..algorithms.random_algo import Random_algo
from ..classes.network import Network
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
        Adds random trajectory to a network and checks whether score improves. If score does not improve, it removes the trajectory and
        tries another one, for self.attempts amount of times
        Returns:
        - self.network(instance of network class): adjusted network with added trajectories
        """
  
        self.network.add_trajectory(new_trajectory) 

        return new_trajectory
    
    def remove(self, trajectory, undo = False):
        if not undo:
            pick = random.randint(0,len(self.network.trajectories)-1)
            trajectory = self.network.trajectories[pick]

        self.network.trajectories.remove(trajectory)

        return trajectory
        

    def replace(self, trajectory):

        trajectory1, changed_list1 = self.remove()
        trajectory2, changed_list2 = self.add(trajectory)

        return trajectory1, trajectory2, changed_list1, changed_list2

    
    def pick_action(self):
        
        actionlist = ['add', 'remove', 'replace']
        number = random.randint(0,1)

        return actionlist[number]
    
    def act(self, action, trajectory):
        change = False

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

        for connection in connection_list:
            if action == 'add':
                self.network.used[connection] += 1
            
            if action == 'remove':
                self.network.used[connection] -= 1
    
        return 
        
    def run(self):
        print('old_score', self.network.quality_network)
        print('trajectories', len(self.network.trajectories))
        tries = 0 
        previous_score = self.network.get_score()
        
        while tries < self.attempts: 
            new_trajectory = Random_algo.create_trajectory(self.network)  
            action = self.pick_action()
            trajectory, change = self.act(action, new_trajectory)
            # save changes so you can use them in used dictionary, to calculate correct score.
            # self.change_used_connections(action, trajectory.route)
            print(f'score after {action}:{self.network.get_score()}')
            
            if not self.improving(previous_score):
                print('score not improved')
                if change:
                    self.undo(action, trajectory)
                    print(f'score after opposite action: {self.network.get_score()}')
                    tries += 1

            previous_score = self.network.get_score()
        
        return self.network

