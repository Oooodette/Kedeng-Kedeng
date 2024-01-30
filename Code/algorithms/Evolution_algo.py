from typing import List

from ..algorithms import random_algo
import random 
import copy 
from ..classes.network import Network
from itertools import combinations

class Evolution_algo():
    """
    Class evolution algo that creates a Network using an evolution algorithm 

    Attributes:
    - size_generation (integer of the generation size)
    - group_size (integer of the group size)
    - number_of_iterations (float of the amount of iterations)
    - parents (list of networks)
    - connections (list of connections)
    - stations (list of stations)

    Methods:
    - create_groups - split list of networks in groups 
    - create_win_chances - creates a list of chances a network wins 
    - save_parents_scores - saves the scores of the parent networks 
    - survival_of_the_fittest - chooses the survivors based on the win chances 
    - get_survivors - adds all the survivors to a list 
    - choice_parent - chooses the parents that will reproduce 
    - make_possible_networks - creates all possible networks from the parents and saves the best 
    - create_offspring - creates offspring using the make_possible_networks method 
    - create_generation - creates a generation from the offsprings 
    - create_evolution - creates an evolution by making more generations 
    - save_network_scores - saves the scores of the networks derived from the evolution 
    - last_man_standing - picks the final best network 
    """
    parents: List[Network]

    
    def __init__(self, network, number_of_iterations):
        """
        Method that initializes the attributes network and number_of_iterations 
        and creates a first generation of parents by using the random algorithm 

        Args:
        - network (instance): network of the Network class 
        - number_of_iterations (integer): determines the amount of iterations 
        """
        self.size_generation = 24
        self.group_size = 2
        self.number_of_iterations = number_of_iterations
        self.parents = []
         
        # Make first generation of parents 
        for i in range(self.size_generation):
            network_copy = copy.deepcopy(network)
            # Create a network using the random algorithm 
            random_algorithm = random_algo.Random_algo(network_copy)
            parent = random_algorithm.create_network()
            self.parents.append(parent)

        self.connections = network.connections 
        self.stations = network.stations 

    def create_groups(self):
        """
        Method that divides the networks in groups 

        Args:
        """
        self.groups = []

        for i in range(12):
            group = random.sample(self.parents, self.group_size)
            self.groups.append(group)

            # Remove the chosen networks from the list to avoid duplicate networks 
            for network in group:
                self.parents.remove(network)

    def create_win_chances(self):
        p = 0.8
        number = 0

        self.win_chances = []

        for x in range(self.group_size):
            answer = p * ((1 - p)**x)
            number += answer 
            self.win_chances.append(number)
          
    def save_parents_scores(self, group):
        group_scores = {}
        for player in group:
            group_scores[player] = player.get_score()

        return group_scores 
    
    def survival_of_the_fittest(self, group_scores):
        sorted_networks = sorted(group_scores, key=lambda x: group_scores[x], reverse=True)
        random_float = round(random.uniform(0, 1), 10)

        survivor = None 
        if random_float <= self.win_chances[0]:
            survivor = sorted_networks[0]
        
        else:
            for i in range(len(self.win_chances)-1):
                if self.win_chances[i] <= random_float <= self.win_chances[i+1]:
                    survivor = sorted_networks[i+1]
                    break
        return survivor 
    
    def get_survivors(self):
        self.survivors = []

        for network_group in self.groups:
            
            group_scores = self.save_parents_scores(network_group)  
            survivor = self.survival_of_the_fittest(group_scores)
            self.survivors.append(survivor)
        print(self.survivors)

    def choice_parents(self): 
        parents = random.sample(self.survivors, 2)

        parent1 = parents[0]
        parent2 = parents[1]
        
        return parent1, parent2 
  
    def make_possible_networks(self, all_trajectories, max_trajectories, max_trajectory_time):
        highestScore = float("-inf")
        bestNetwork = None
        new_network = Network(self.connections, self.stations, max_trajectories, max_trajectory_time)
        
        if len(all_trajectories) > max_trajectories:
            max_amount = max_trajectories 
        else:
            max_amount = len(all_trajectories)

        for r in range(1, max_amount):
            print("Maximaal amount:", max_amount)
            print("We zijn nu bij aantal trajecten:", r)
            count = 0
            combination = (list(combi) for combi in combinations(all_trajectories, r))
            for comba in combination:
                new_network.trajectories = comba
                new_network.used = new_network.connections_used()

                for traject in new_network.trajectories:
                    for connection in traject.route:
                        
                        if connection in new_network.used:
                            new_network.used[connection] += 1
                        else:
                            new_network.used[connection] = 1
                
                current_score = new_network.get_score()

                if current_score > highestScore: 
                    #print(highestScore)
                    highestScore = current_score 
                    bestNetwork = new_network 
        print("FINAL SCORE:", bestNetwork.get_score())
        return bestNetwork
                                

    def create_offspring(self, parent1: Network, parent2: Network):
    
        all_trajectories = parent1.trajectories + parent2.trajectories
    
        final_network = self.make_possible_networks(all_trajectories, parent1.max_trajectories, parent1.max_trajectory_time)
                
        return final_network 

    def create_generation(self):
        
        new_parents = []

        for i in range(self.size_generation):
            parent1, parent2 = self.choice_parents()
            offspring = self.create_offspring(parent1, parent2)
            new_parents.append(offspring)
            print("lengte offsprings:", len(new_parents))

        self.parents = new_parents

    def create_evolution(self):
        count = 0
        for i in range(self.number_of_iterations):
            count += 1
            print("iteratie:", count)
            self.create_groups()
            self.get_survivors()
            self.create_generation()


    def save_network_scores(self):
        self.network_scores = {}
        for network in self.parents: 
            self.network_scores[network] = network.get_score()
    
    def last_man_standing(self):
        self.create_win_chances()
        self.create_evolution()
        self.save_network_scores()

        sorted_networks = sorted(self.network_scores, key=lambda x: self.network_scores[x], reverse=True)
        self.best_network = sorted_networks[0]

        return self.best_network 


        


    

    
        




        






        
