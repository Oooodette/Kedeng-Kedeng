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
        # previous_score = self.network.get_score() 
        # add_count = 0

        # # check if we are still under the attempt limit and under the maximum amount of trajectories
        # while add_count < self.attempts and len(self.network.trajectories) < self.network.max_trajectories:

        # create new trajectory and add it to network
        # new_trajectory = Random_algo.create_trajectory(self.network)    
        self.network.add_trajectory(new_trajectory) 
            
        # update used connections to enable score calculations
        # changed_list = [] 
        # for connection in new_trajectory.route:

        #     # save the changes you made so you can undo them when score doesn't improve
        #     if not self.network.used[connection]:
        #         changed_list.append(connection)
        #         self.network.used[connection] = True

            # # if score doesn't improve, remove trajectory and try again
            # if not self.improving(previous_score):
            #     self.network.trajectories.pop()

                # # change used connections back to false
                # for connection in changed_list:
                #     self.network.used[connection] = False
                # add_count += 1

            # else: 
            #     add_count = 0
            # previous_score = self.network.get_score()
        return new_trajectory
    
    def remove(self, trajectory):
        # pick = random.randint(0,len(self.network.trajectories)-1)
        # trajectory = self.network.trajectories[pick]
        self.network.trajectories.pop()
        
        # changed_list = [] 
        # for connection in trajectory.route:

        #     # save the changes you made so you can undo them when score doesn't improve
        #     if self.network.used[connection]:
        #         changed_list.append(connection)
        #         self.network.used[connection] = False

        return trajectory
        

    def replace(self, trajectory):

        trajectory1, changed_list1 = self.remove()
        trajectory2, changed_list2 = self.add(trajectory)

        return trajectory1, trajectory2, changed_list1, changed_list2

    
    def pick_action(self):
        
        actionlist = ['add', 'remove', 'replace']
        number = 0

        return actionlist[number]
    
    def act(self, action, trajectory):
        if action == 'add' and len(self.network.trajectories) < self.network.max_trajectories:
            changed_list = self.add(trajectory)
            print('add')
        elif action == 'remove':
            trajectory, changed_list = self.remove()   
        elif action ==  'replace' :
            trajectory, changed_list = self.replace(trajectory)
        
        return trajectory

    def unact(self,action, trajectory):
        if action == 'add':
            trajectory, _ = self.remove()
        elif action == 'remove':
            trajectory = self.add(trajectory)
        else:
            trajectory = self.replace()
        
        return trajectory

    def change_used_connections(self, action, connection_list):
        changed_list = []
        
        for connection in connection_list:
            
            if action == 'add':
                if self.network.used[connection] == False:  
                    changed_list.append(connection)
                    self.network.used[connection] = True
            
            if action == 'remove':
                if self.network.used[connection] == True:  
                    changed_list.append(connection)
                    self.network.used[connection] = False
    
        return changed_list
        
    def run(self):
        print('old_score', self.network.quality_network)
        print('trajectories', len(self.network.trajectories))
        tries = 0 
        previous_score = self.network.get_score()
        
        while tries < self.attempts: 
            new_trajectory = Random_algo.create_trajectory(self.network)  
            # action = self.pick_action()
            # trajectory = self.act(action, new_trajectory)
            trajectory = self.add(new_trajectory)
            # save changes so you can use them in used dictionary, to calculate correct score.
            changed_list = self.change_used_connections('add', trajectory.route)
            print(f'score after action:{self.network.quality_network} ')
            
            if not self.improving(previous_score):
                self.change_used_connections('remove', changed_list)
                self.remove(new_trajectory)
                print(f'score after opposite action: {self.network.quality_network}')
                tries += 1

            previous_score = self.network.get_score()
        
        return self.network

