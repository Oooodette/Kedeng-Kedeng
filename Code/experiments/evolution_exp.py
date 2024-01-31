from ..algorithms.random_algo import Random_algo
from ..algorithms.greedy_algo import Greedy_algo
from ..algorithms.evolution_algo import Evolution_algo

from ..classes.network import Network, Trajectory
# from code.visualize import visualize as vis
from code.visualize import new_visualize as vis

import pandas as pd
import matplotlib.pyplot as plt

# defining parameters for different datasets
max_trajectories_holland = 7
max_trajectory_time_holland = 120
max_trajectories_nl = 20
max_trajectory_time_nl = 180

def run_experiment():
    """
    Function that runs an experiment for the evolution algorithm.
    Could either give plot with the score of the best network of every generation
    or a histogram showing the final network of ten generations running the algorithm 
    a number of iterations amount of time
    """
    # difine criteria
    generations_list = []
    iterations = []

    amount_of_generations = 10
    amount_of_iterations = 2 

    # decide if you want to plot the score of every generation 
    # or if you want to plot the score of the last generation after 
    # running the algorithm an amount of iterations times
    plot_generations_score = False

    connections_df = pd.read_csv('data\ConnectiesNationaal.csv')
    stations_df = pd.read_csv('data\StationsNationaal.csv')

    network = Network(connections_df, stations_df, max_trajectories_nl, max_trajectory_time_nl)
    
    if plot_generations_score:
        # third argument is true, so the best score of every generation is saved 
        evo_algo = Evolution_algo(network, amount_of_generations, "random", True)

        # Create network and call the list of scores of every generation
        test_network = evo_algo.last_man_standing()
        score_list = evo_algo.score_generations
        for i in range(1, amount_of_generations+1):
            generations_list.append(i)

        plt.plot(generations_list, score_list)
        plt.xlabel('generations')
        plt.ylabel('score network')

    else: 
        test_network_scores = []
        for i in range(1, amount_of_iterations+1):
            print("iteration:", i)
            evo_algo = Evolution_algo(network, amount_of_generations, "random")
            test_network = evo_algo.last_man_standing()
            test_network_scores.append(test_network.get_score)
        
        plt.hist(test_network_scores, bins = 1000)
        plt.xlabel("network score")
        plt.ylabel("iteraties")
        plt.xlim(4000, 7000)

