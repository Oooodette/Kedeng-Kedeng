from typing import List

from ..algorithms import random_algo
import random 
import copy 

from ..classes.network import Network
from itertools import combinations

class Evolution_algo():

    parents: List[Network]

    def __init__(self, network, number_of_iterations):
        self.size_generation = 96
        self.number_of_iterations = number_of_iterations
        self.parents = []
        for i in range(self.size_generation):
            network_copy = copy.deepcopy(network)
            random_algorithm = random_algo.Random_algo(network_copy)
            parent = random_algorithm.create_network()
            self.parents.append(parent)
             
    def create_groups(self):
        group_size = 8
        parents_copy = copy.deepcopy(self.parents)
        self.groups = []

        for i in range(12):
            group = random.sample(parents_copy, group_size)
            self.groups.append(group)
            for parent in group:
                parents_copy.remove(parent)

    def create_win_chances(self):
        p = 0.8
        number = 0

        self.win_chances = []

        for x in range(8):
            answer = p * ((1 - p)**x)
            number += answer 
            self.win_chances.append(number)
          
    def save_parents_scores(self, group):
        group_scores = {}
        for player in group:
            group_scores[player] = player.calculate_score()

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

    def choice_parents(self): 
        copy_survivors = copy.deepcopy(self.survivors)
        pick1 = random.randint(0, len(copy_survivors)-1)
        parent1 = copy_survivors[pick1]
        copy_survivors.remove(parent1)

        pick2 = random.randint(0, len(copy_survivors)-1)
        parent2 = copy_survivors[pick2]

        copy_survivors.remove(parent2)

        return parent1, parent2 
    
    def determine_half_trajectories(self, parent):
        vifty_chance = random.randint(1, 2)
        if len(parent.trajectories) % 2 == 0:
            pick = len(parent.trajectories) / 2 
        
        else:
            if vifty_chance == 1:
                pick = len(parent.trajectories) // 2
            else:
                pick = (len(parent.trajectories) // 2) + 1
        
        return int(pick)
    
    def create_possible_childs(self, all_trajectories, parent):
        self.possible_networks = []
        for r in range(2, len(all_trajectories)+1):
            for combi in combination(all_trajectories):
                possible_network = list(combi)
                self.possible_networks.append(possible_network)
            
    
    def create_offspring(self, parent1: Network, parent2: Network):
    
        pick1 = self.determine_half_trajectories(parent1)
        pick2 = self.determine_half_trajectories(parent2)

        parent1_trajectories = random.sample(parent1.trajectories, pick1)
        parent2_trajectories = random.sample(parent2.trajectories, pick2)

        combination_network = parent1_trajectories + parent2_trajectories

        final_network = Network(parent1.connections, parent1.stations, parent1.max_trajectories, parent1.max_trajectory_time)
        final_network.trajectories = combination_network

        return final_network 

    def create_generation(self):
        new_parents = []

        for i in range(self.size_generation):
            parent1, parent2 = self.choice_parents()
            offspring = self.create_offspring(parent1, parent2)
            new_parents.append(offspring)
        
        self.parents = new_parents

    def create_evolution(self):
        for i in range(self.number_of_iterations):
            self.create_groups()
            self.get_survivors()
            self.create_generation()

    def save_network_scores(self):
        self.network_scores = {}
        for network in self.parents: 
            self.network_scores[network] = network.calculate_score()
    
    def last_man_standing(self):
        self.create_win_chances()
        self.create_evolution()
        self.save_network_scores()

        sorted_networks = sorted(self.network_scores, key=lambda x: self.network_scores[x], reverse=True)
        self.best_network = sorted_networks[0]

        return self.best_network 


        


    

    
        




        






        
