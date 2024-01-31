from ..algorithms.random_algo import Random_algo
from ..algorithms.greedy_algo import Greedy_algo
from ..algorithms.hillclimber import Hillclimber
from ..classes.network import Network, Trajectory
from ..visualize import new_visualize as vis
import  pandas as pd
import matplotlib.pyplot as plt

def run_experiment():
    """
    Runs our experiment for 10000 iterations. Saves histogram
    """

    #defining parameters for different datasets
    max_trajectories_holland = 7
    max_trajectory_time_holland = 120
    max_trajectories_nl = 20
    max_trajectory_time_nl = 180


    #read in data
    connections_df = pd.read_csv('data\ConnectiesNationaal.csv')
    stations_df = pd.read_csv('data\StationsNationaal.csv')
    network = Network(connections_df, stations_df, max_trajectories_nl, max_trajectory_time_nl)

    hillclimber_list = []
    count_list = []
    count = 0
    best_network= None
    previous_score = 0

    for x in range(10):
        print(f' current run: {count}')
        random_algo = Random_algo(network)
        test_network = random_algo.create_network()
        hillclimber = Hillclimber(test_network, 400, 'random')
        newie = hillclimber.run()        
        score = newie.get_score()
        if score > previous_score: 
            best_network = newie
        hillclimber_list.append(score)

        count += 1
        count_list.append(count)
        previous_score = score
    

    plt.hist(hillclimber_list, bins = 1000)
    plt.savefig('data/hill_histogram.png')
    plt.show()

    vis.plot_all(stations_df, connections_df, 'data\gadm41_NLD_1.json', best_network.used, best_network.trajectories, best_network.stations, 'data/experiment_results')
        