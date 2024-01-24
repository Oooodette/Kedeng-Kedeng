from ..algorithms import random_algo
from ..classes import Trajectory
import pandas as pd
import random 
import pprint as pp 
import copy 

class Evolution_algo():
    def __init__(self, network, number_of_iterations):
        self.size_generation = 96
        self.number_of_iterations = number_of_iterations
        self.parents = []
        for i in range(self.size_generation):
            parent = random_algo.Random_algo(network)
            self.parents.append(parent)
         
        self.network_scores = self.save_network_scores()
    
    def create_groups(self):
        group_size = 8 
        parents_copy = copy.copy(self.parents)
        self.groups = []

        for i in range(12):
            group = random.sample(parents_copy, group_size)
            self.groups.append(group)
            for parent in group:
                parents_copy.remove(parent)

    def create_win_chances(self):
        p = 0.8
        self.win_chances = []

        for x in range(8):
            answer = p * (1 - (1 - p)**x)
            self.win_chances.append(answer)
    
    def save_parents_scores(self, group):
        group_scores = {}
        for player in group:
            group_scores[player] = player.get_score()
            
        return group_scores 
    
    def survival_of_the_fittest(self, group_scores):
        sorted_networks = sorted(group_scores, key=lambda x: group_scores[x], reverse=True)
        
        random_float = round(random.uniform(0, 1), 10)

        if random_float < self.win_chances[0]:
            survivor = sorted_networks[0]
        elif self.win_chances[0] < random_float < self.win_chances[1]:
            survivor = sorted_networks[1]
        elif self.win_chances[1] < random_float < self.win_chances[2]:
            survivor = sorted_networks[2]
        elif self.win_chances[2] < random_float < self.win_chances[3]:
            survivor = sorted_networks[3]
        elif self.win_chances[3] < random_float < self.win_chances[4]:
            survivor = sorted_networks[4]
        elif self.win_chances[4] < random_float < self.win_chances[5]:
            survivor = sorted_networks[5]
        elif self.win_chances[5] < random_float < self.win_chances[6]:
            survivor = sorted_networks[6]
        elif self.win_chances[6] < random_float < self.win_chances[7]:
            survivor = sorted_networks[7]
        
        return survivor 
    
    def get_survivors(self):
        self.survivors = []
        for network_group in self.groups:
            group_scores = self.save_parents_scores(network_group)
            survivor = self.survival_of_the_fittest(group_scores)
            self.survivors.append(survivor)

    def choice_parents(self): 
        ## Steeds twee parents kiezen uit de survivors en deze gebruiken om nieuwe generaties te maken, vervolgens 
        ## deze generaties weer gebruiken om nieuwe generaties te maken als self.parents

    def two_random_numbers(self):
        pick1 = float("inf")
        pick2 = float("inf")

        ## TODO: Max trajectory time moet ook nog kloppen
        while pick1 + pick2 > self.network.max_trajectories:
            pick1 = random.randint(1, len(self.parent1.network.trajectories))
            pick2 = random.randint(1, len(self.parent2.network.trajectories))
        
        return pick1, pick2 
    
    def pick_random_trajectories(self, trajectories_list, pick_amount):
        trajectories = []
        trajectories_copy = copy.copy(trajectories_list)

        for i in range(pick_amount):
            trajectory = random.sample(trajectories_copy)
            trajectories.append(trajectory)
            for traject in trajectory:
                trajectories_copy.remove(traject)
            
        return trajectories 
    
    def create_generation(self, parent1, parent2):
        generation_network = []

        for i in range(self.size_generation):
            pick1, pick2 = self.two_random_numbers() 
            
            parent1_trajectories = self.pick_random_trajectories(self.parent1.network.trajectories, pick1)
            parent2_trajectories = self.pick_random_trajectories(self.parent2.network.trajectories, pick2)

            combination_network = parent1_trajectories + parent2_trajectories 
            generation_network.append(combination_network)

        return generation_network
    
    def create_evolution(self):
        ## TODO: kloppend maken 
        for i in range(self.number_of_iterations):
            best_network1, best_network2 = self.survival_of_the_fittest()
            self.create_generation(best_network1, best_network2)
        
        return best_network1 
    

    
        




        






        
