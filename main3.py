from code.classes import Station, Connection, Trajectory, Network
from code.algorithms.random_algo import Random_algo
from code.algorithms.greedy_algo import Greedy_algo
# from code.visualize import visualize as vis
from code.visualize import new_visualize as vis
import copy

#defining parameters for different datasets
max_trajectories_holland = 7
max_trajectory_time_holland = 120
max_trajectories_nl = 20
max_trajectory_time_nl = 180

if __name__ == "__main__":

    #difine criteria
    minimal_score = 8000
    iterations = 0
    score = 0

    #looping until criteria are met
    # while score < minimal_score:
    network = Network('data\ConnectiesNationaal.csv', 'data\StationsNationaal.csv', max_trajectories_nl, max_trajectory_time_nl)
    #network = Network()
    for i in range(10000):
        greedy = Greedy_algo(network)

        # Create network from our data
        test_network = greedy.create_network()
        new_score = test_network.get_score()

        if new_score > score:
            final_network = (test_network)
            score = new_score
            print('new high')

        print(i, new_score)
        iterations += 1

    nr_traj = len(final_network.trajectories)
    fraction = sum(final_network.used.values()) / len(final_network.used)

    #printing #iterations, number of trajectories and score of the network
    print(f'number of iterations: {iterations}')
    print(f'number of trajectories in network: {nr_traj}')
    print(f'score of the network {score}')
    print(f'fraction of driven connections: {fraction}')

    #explicitly save the network that fulfills the criteria
    final_network.save_network()

    #visualize
    vis.plot_all(final_network.stations_df, final_network.connections_df, 'data\gadm41_NLD_1.json', final_network.used, final_network.trajectories, final_network.stations)
    
    # vis.visualize_stations_connections(test_network.stations_df, test_network.connections_df)
    # vis.visualize_network(test_network.stations_df, test_network.connections_df, 'data\output.csv')

    # vis.plot_netherlands()
    # vis.plot_connections()
    

