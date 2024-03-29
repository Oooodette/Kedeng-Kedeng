from code.classes import Station, Connection, Trajectory, Network
from code.algorithms.random_algo import Random_algo
from code.algorithms.greedy_algo import Greedy_algo
from code.visualize import new_visualize as vis
import pandas as pd
import matplotlib.pyplot as plt


def run_experiment():
    """
    Run an experiment using the random algorithm.
    Runs 10,000 iterations

    Returns;
    - Variables of the best network of the 10,000
    - Averages of all 10,000 networks
    - Histogram of the scores of the 10,000 networks
    """
    
    # defining parameters for different datasets
    max_trajectories_holland = 7
    max_trajectory_time_holland = 120
    max_trajectories_nl = 20
    max_trajectory_time_nl = 180

    # initialize score and lists to append to 
    score = -100000
    scores = []
    nrs_trajectories = []
    fractions = []

    
    # read in data
    connections_df = pd.read_csv('data\ConnectiesNationaal.csv')
    stations_df = pd.read_csv('data\StationsNationaal.csv')


    # create 10000 networks
    for i in range(10000):
        print(f'current run: {i}')

        # initialize empty network
        network = Network(connections_df, stations_df, max_trajectories_nl, max_trajectory_time_nl)

        random_network = Random_algo(network)
        test_network = random_network.create_network()

        # retrieve score of new network
        new_score = test_network.get_score()

        # retrieve nr of trajectories, fraction
        used_connections = [connection for connection, value in test_network.used.items() if value != 0]
        fraction = (len(used_connections)) / len(test_network.connections)
        
        # append score, nr of trajectories, fraction of connections driven
        scores.append(new_score)
        nrs_trajectories.append(len(test_network.trajectories))
        fractions.append(fraction)

        # save network if new score is higher than previous network
        if new_score > score:
            final_network = test_network
            score = new_score

    # determining the fraction of driven connections
    used_connections = [connection for connection, value in final_network.used.items() if value != 0]
    fraction = (len(used_connections)) / len(final_network.connections)

    # print relevant oututs of best network
    print(f'Best network has score {final_network.get_score()}')
    print(f'Best network has {len(final_network.trajectories)} trajectories')
    print(f'Best network has fraction {fraction}')

    # print relevant averages of all 10,000 runs
    print(f'Average score is {sum(scores) / len(scores)}')
    print(f'Average number of trajectories is {sum(nrs_trajectories) / len(nrs_trajectories)}')
    print(f'Average fraction is {sum(fractions) / len(fractions)}')

    # creating histogram
    plt.hist(scores, bins=1000)
    plt.xlim(0, 10000)
    plt.show()

