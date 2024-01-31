from code.classes import Station, Connection, Trajectory, Network
from code.algorithms.random_algo import Random_algo
from code.algorithms.greedy_algo import Greedy_algo
from code.visualize import new_visualize as vis
import copy
import pandas as pd
import random
import matplotlib.pyplot as plt
import time

# random.seed(2)

#defining parameters for different datasets
max_trajectories_holland = 7
max_trajectory_time_holland = 120
max_trajectories_nl = 20
max_trajectory_time_nl = 180

if __name__ == "__main__":

    #difine criteria
    score = 0

    connections_df = pd.read_csv('data\ConnectiesNationaal.csv')
    stations_df = pd.read_csv('data\StationsNationaal.csv')

    network = Network(connections_df, stations_df, max_trajectories_nl, max_trajectory_time_nl)
    

    scores = []

    start = time.time()
    for i in range(10000):
        greedy = Greedy_algo(network)

        # Create network from our data
        test_network = greedy.create_network()
        new_score = test_network.get_score()

        scores.append(new_score)

        if new_score > score:
            final_network = test_network
            score = new_score
            print('new high')

        print(i, new_score)

    end = time.time()
    nr_traj = len(final_network.trajectories)
    used_connections = [connection for connection, value in final_network.used.items() if value != 0]
    fraction = (len(used_connections)) / len(final_network.connections)
    times_used_list = list(final_network.used.values())


    #printing #iterations, number of trajectories and score of the network
    print(f'number of trajectories in network: {nr_traj}')
    print(f'score of the network: {score}')
    print(f'average score is: {sum(scores) / len(scores)}')
    print(f'fraction of driven connections: {fraction}')

    print(f'times connections are used: {times_used_list})')
    print(f'most times one connectionis used: {max(times_used_list)}')
    print(f'this is connection: {final_network.connections[times_used_list.index(max(times_used_list))].station1, final_network.connections[times_used_list.index(max(times_used_list))].station2}')

    #explicitly save the network that fulfills the criteria
    final_network.save('data/output.csv')
    
    print(f'10000 it took {end - start}')
    #visualize
    vis.plot_all(stations_df, connections_df, 'data\gadm41_NLD_1.json', final_network.used, final_network.trajectories, final_network.stations)
    
    plt.hist(scores, bins=1000)
    plt.xlim(4000, 7000)
    plt.show()
