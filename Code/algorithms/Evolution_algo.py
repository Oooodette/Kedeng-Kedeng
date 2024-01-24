from ..classes import Trajectory
import pandas as pd
import random 
import pprint as pp 
import copy 

class Evolution_algo():
    def __init__(self, parent1, parent2, size_generation, number_of_iterations):
        self.parent1 = parent1 ## nog geen idee hoe ik dat moet doen met hillclimber aanroepen 
        self.parent2 = parent2 ## nog geen idee hoe ik dat moet doen met hillclimber aanroepen 
        self.size_generation = size_generation
        self.number_of_iterations = number_of_iterations
        self.network_scores = self.save_network_scores()
    
    def two_random_numbers(self):
        pick1 = float("inf")
        pick2 = float("inf")

        ## Max trajectory time moet ook nog kloppen
        while pick1 + pick2 > self.network.max_trajectories:
            pick1 = random.randint(1, len(parent1.network.trajectories))
            pick2 = random.randint(1, len(parent2.network.trajectories))
        
        return pick1, pick2 
    
    def pick_random_trajectories(self, trajectories_list, pick_amount):
        trajectories = []
        trajectories_copy = copy.copy(trajectories_list)

        for i in range(pick_amount):
            trajectory = random.choice(trajectories_copy)
            trajectories_copy.remove(trajectory)
            trajectories.append(trajectory)
            
            pick_amount -= 1
        
        return trajectories 
    
    def create_generation(self, parent1, parent2):
        generation_network = []

        for i in range(self.size_generation):
            pick1, pick2 = self.two_random_numbers() 
            
            parent1_trajectories = self.pick_random_trajectories(parent1.network.trajectories, pick1)
            parent2_trajectories = self.pick_random_trajectories(parent2.network.trajectories, pick2)

            combination_network = parent1_trajectories + parent2_trajectories 
            generation_network.append(combination_network)

        return generation_network
    
    def save_network_scores(self):
        generation_network = self.create_generation()

        network_scores = {}
        for network in generation_network:
            network_scores[network] = network.get_score()

        return network_scores 

    def survival_of_the_fittest(self):
        highest_score = 0
        second_highest_score = 0

        for score, network in self.network_scores.items():
            if score > highest_score:
                highest_score = score 
                best_network1 = network 
        
        for score, network in self.network_scores.items():
            if score > second_highest_score and score < highest_score:
                second_highest_score = score 
                best_network2 = network 
        
        return best_network1, best_network2 
    
    def create_evolution(self):
        for i in range(self.number_of_iterations):
            best_network1, best_network2 = self.survival_of_the_fittest()
            self.create_generation(best_network1, best_network2)
        
        return best_network1 
    

    
        




        






        
