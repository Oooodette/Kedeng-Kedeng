from ..algorithms.random_algo import Random_algo
from ..classes.network import Network


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

        
    def add(self):
        """
        Adds random trajectory to a network and checks whether score improves. If score does not improve, it removes the trajectory and
        tries another one, for self.attempts amount of times
        Returns:
        - self.network(instance of network class): adjusted network with added trajectories
        """
        previous_score = self.network.get_score() 
        add_count = 0
 
        # check if we are still under the attempt limit and under the maximum amount of trajectories
        while add_count < self.attempts and len(self.network.trajectories) < self.network.max_trajectories:
            
            # create new trajectory and add it to network
            new_trajectory = Random_algo.create_trajectory(self.network)
            
            self.network.add_trajectory(new_trajectory)
            
            # update used connections to enable score calculations
            changed_list = [] 
            for connection in new_trajectory.route:

                # save the changes you made so you can undo them when score doesn't improve
                if not self.network.used[connection]:
                    changed_list.append(connection)
                    self.network.used[connection] = True

            # if score doesn't improve, remove trajectory and try again
            if not self.improving(previous_score):
                self.network.trajectories.pop()

                # change used connections back to false
                for connection in changed_list:
                    self.network.used[connection] = False
                add_count += 1

            else: 
                add_count = 0

            previous_score = self.network.get_score()
        
        return self.network
        
    # def replace(self):
    #     replace_count = 0
    #     previous_score = 0 

    #     while replace_count < self.attempts:
    #         #TODO: save trajectory before removing in case it doesn't improve score 
    #         self.network.remove_trajectory()

    #         #TODO: create greedy trajectory
    #         self.network.add_trajectory
    #         if not self.improving(previous_score):
            
            
                
                
        
            # #TODO: create greedy trajectory 
            # self.network.add_trajectory
            # if not self.improving(previous_score):
            #     #TODO: remove trajectory
            #     add_count += 1



    # def change_network(self, method = 'add'):
        
    #     self.network.add_trajectory


    # def run(self):
    #     count = 0
    #     #TODO: calculate score
    #     while count < self.attempts:
    #         self.change_network()
    #         count = 
    #     self.add()
    #     self.replace()



     

