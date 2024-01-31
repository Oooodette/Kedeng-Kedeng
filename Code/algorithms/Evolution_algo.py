from typing import List

from ..algorithms import random_algo
from ..algorithms import hillclimber
from ..classes.network import Network

import random 
import copy 
import math
from itertools import combinations, islice

class Evolution_algo():
    """
    Class evolution algo that creates a Network using an evolution algorithm. 

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
    - update_used_dictionary - updates the used dictionary of a given network  
    - amount_of_possible_combinations - calculates the possible amount of combinations
    - make_possible_networks - creates all possible networks from the parents and saves the best 
    - create_offspring - creates offspring using the make_possible_networks method 
    - create_generation - creates a generation from the offsprings 
    - create_evolution - creates an evolution by making more generations 
    - save_network_scores - saves the scores of the networks derived from the evolution 
    - last_man_standing - picks the final best network 
    """
    parents: List[Network]
    parent: Network 

    def __init__(self, network, number_of_iterations):
        """
        Method that initializes the attributes network and number_of_iterations. 
        Creates a first generation of parents by using the random algorithm. 

        Args:
        - network (instance): network of the Network class 
        - number_of_iterations (integer): determines the amount of iterations 
        """
        self.size_generation = 96
        self.group_size = 8
        self.number_of_iterations = number_of_iterations
        self.parents = []
        
        # Make first generation of parents 
        for i in range(self.size_generation):
            network_copy = copy.deepcopy(network)

            # Create a network using the random algorithm 
            hill_algorithm = random_algo.Random_algo(network_copy)
            parent = hill_algorithm.create_network()

            self.parents.append(parent)

        self.connections = network.connections 
        self.stations = network.stations 

    def create_groups(self):
        """
        Method that divides the network parents in groups.
        """
        self.groups = []

        for i in range(12):
            group = random.sample(self.parents, self.group_size)
            self.groups.append(group)

            # Remove the chosen networks from the list to avoid duplicate networks 
            for network in group:
                self.parents.remove(network)

    def create_win_chances(self):
        """
        Method that creates a list of the chances a survivor wins.
        The best network wins with 80%, the second best with 16%, the third best with 8% etc. 
        """
        p = 0.8
        number = 0

        self.win_chances = []

        for x in range(self.group_size):

            # Calculate the correct values 
            answer = p * ((1 - p)**x)

            # Add the value to 'number' so we get a range of 0.800, 0.960, 0.992 etc
            number += answer 
            self.win_chances.append(number)

    def save_parents_scores(self, group):
        """
        Method that saves the scores of the networks in the parents list. 
        This is necessary to pick the best network in further steps.

        Args:
        - group(list of networks): group of networks that compete against each other in further steps 
        Returns:
        - group_scores: dictionary with the scores of the networks in a group as key and the score as value
        """
        group_scores = {}
        for player in group:

            # Reset and update the used dictionary before calculating the score 
            player.used = player.connections_used()
            player.used = self.update_used_dictionary(player)

            group_scores[player] = player.get_score()

        return group_scores 
    
    def survival_of_the_fittest(self, group_scores):
        """
        Method that picks one network from one group. 
        The win_chances list determines which one will survive. 

        Args:
        - group_scores(dictionary): dictionary with the network scores of each network in a group
        Returns:
        - survivor: the network that wins the tournament 
        """
        # Create a list with networks descending sorted on scores 
        sorted_networks = sorted(group_scores, key=lambda x: group_scores[x], reverse=True)
        survivor = None 

        # Pick a random float with ten decimals 
        random_float = round(random.uniform(0, 1), 10)

        # With 80% chance the best network wins 
        if random_float <= self.win_chances[0]:
            survivor = sorted_networks[0]
        
        # With smaller chances choose networks with lower values 
        else:
            for i in range(len(self.win_chances)-1):
                if self.win_chances[i] <= random_float <= self.win_chances[i+1]:
                    survivor = sorted_networks[i+1]
                    break
        print(survivor.get_score())
        return survivor 
    
    def get_survivors(self):
        """
        Method that picks a survivor(network) from each group and creates a list of survivors(networks).
        """
        self.survivors = []

        for network_group in self.groups:
            
            group_scores = self.save_parents_scores(network_group)  
            survivor = self.survival_of_the_fittest(group_scores)
            self.survivors.append(survivor)
        
    def choice_parents(self): 
        """
        Method that chooses two random parents from the list of survivors. 
        """
        parents = random.sample(self.survivors, 2)

        parent1 = parents[0]
        parent2 = parents[1]
        
        return parent1, parent2 
    
    def update_used_dictionary(self, network):
        """
        Method that updates the dictionary with used connections.

        Args:
        - network(instance): the network for which the dictionary has to be updated 
        Returns:
        - the dictionary with the correct values 
        """
        for traject in network.trajectories:
            for connection in traject.route:
                network.used[connection] += 1

        return network.used 
    
    def amount_of_possible_combinations(self, n, r):
        """
        Method that calculates the possible amount of combinations.

        Args:
        - n(int): the length of the combinated trajectories from the parents 
        - r(int): the amount of trajectories the combination consists of 
        """
        return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))
       
    def make_possible_networks(self, all_trajectories, max_trajectories, max_trajectory_time):
        """
        Method that makes possible combinations of trajectories of different lengths. 
        Creates 27 amount of combinations for each length and saves the one that creates a network 
        with the highest score. 

        Args:
        - all_trajectories(list of trajectories): list of trajectories to make the combinations from 
        - max_trajectories(int): maximum amount of trajectories in a network 
        - max_trajectory_time(int): maximum amount of time a network is allowed to have 

        Returns:
        - the network with the best combination of trajectories
        """
        highest_score = float("-inf")
        best_trajectories = None

        best_network = Network(self.connections, self.stations, max_trajectories, max_trajectory_time)
        
        # If the length of all_trajectories is bigger than the maximum: set max_amount to the maximum 
        if len(all_trajectories) > max_trajectories:
            max_amount = max_trajectories 
        
        # If smaller, set the max_amount to the length of all_trajectories
        else:
            max_amount = len(all_trajectories)

        # Determine the smallest possible amount of combinations consisting of one traject
        smallest_combination_size = self.amount_of_possible_combinations(len(all_trajectories), 1)

        for r in range(1, max_amount):
            # Shuffle the trajectories so it won't make the same combination each iteration 
            random.shuffle(all_trajectories)

            # Create a list of combinations for each length
            # Generate amount of combinations of the smallest combination size 
            combination = (list(combi) for combi in islice(combinations(all_trajectories, r), smallest_combination_size))

            for comb in combination:
                best_network.trajectories = comb

                # Reset and update the used dictionary so the score can be calculated
                best_network.used = best_network.connections_used()
                best_network.used = self.update_used_dictionary(best_network)

                current_score = best_network.get_score()

                if current_score > highest_score :
                    highest_score = current_score 
                    best_trajectories = comb 

        best_network.trajectories = best_trajectories

        return best_network
                                

    def create_offspring(self, parent1: Network, parent2: Network):
        """
        Method that combines the trajectories from the parents to create an offspring

        Args:
        - parent1(network): one network from the survivors 
        - parent2(network): another network from the survivors 
        Returns:
        - offspring: the best network, so the network with the best combination of trajectories
        """
        all_trajectories = parent1.trajectories + parent2.trajectories
        offspring = self.make_possible_networks(all_trajectories, parent1.max_trajectories, parent1.max_trajectory_time)
                
        return offspring

    def create_generation(self):
        """
        Method that creates a new generation by creating a size_generation amount of offsprings 
        Replaces self.parents with this generation for further evolution 
        """
        new_parents = []

        for i in range(self.size_generation):
            parent1, parent2 = self.choice_parents()
            offspring = self.create_offspring(parent1, parent2)
            new_parents.append(offspring)
        
        self.parents = new_parents

    def create_evolution(self):
        """
        Method that creates an evolution by creating multiple generations
        """
        count = 0
        for i in range(self.number_of_iterations):
            count += 1
            print("iteratie:", count)
            # Create new groups and survivors to use in the create_generation function
            self.create_groups()
            self.get_survivors()
            self.create_generation()

    def save_network_scores(self):
        """
        Method that saves the scores of the parents in a dictionary to pick the best network 
        """
        self.network_scores = {}
        for network in self.parents: 
            network.used = network.connections_used()
            network.used = self.update_used_dictionary(network)

            self.network_scores[network] = network.get_score()
    
    def last_man_standing(self):
        """
        Method that picks the network with the highest score of the last generation of parents

        Returns:
        - The network with the highest score 
        """
        self.create_win_chances()
        self.create_evolution()
        self.save_network_scores()

        # Create a list with networks descending sorted on scores 
        sorted_networks = sorted(self.network_scores, key=lambda x: self.network_scores[x], reverse=True)
        self.best_network = sorted_networks[0]

        return self.best_network 


        


    

    
        




        






        
