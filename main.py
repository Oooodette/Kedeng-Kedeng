from code.classes import Station, Connection, Trajectory, Network
from code.algorithms.random_algo import Random_algo
# from code.visualize import visualize as vis
from code.visualize import new_visualize as vis

#defining parameters for different datasets
max_trajectories_holland = 7
max_trajectory_time_holland = 120
max_trajectories_nl = 20
max_trajectory_time_nl = 180

if __name__ == "__main__":

    #difine criteria
    minimal_score = 8000
    iterations = 0
    score = -1000

    #looping until criteria are met
    # while score < minimal_score:
    network = Network('data\ConnectiesHolland.csv', 'data\StationsHolland.csv', max_trajectories_holland, max_trajectory_time_holland)
    random_algo = Random_algo(network)

    # Create network from our data
    test_network = random_algo.create_network()
    score = test_network.get_score()
    nr_traj = len(test_network.trajectories)

    iterations += 1

    #printing #iterations, number of trajectories and score of the network
    print(f'number of iterations: {iterations}')
    print(f'number of trajectories in network: {nr_traj}')
    print(f'score of the network {score}')

    #explicitly save the network that fulfills the criteria
    network.save_network()

    #visualize
    vis.plot_all(test_network.stations_df, test_network.connections_df, 'data\gadm41_NLD_1.json', test_network.used, test_network.trajectories, test_network.stations)
    
    # vis.visualize_stations_connections(test_network.stations_df, test_network.connections_df)
    # vis.visualize_network(test_network.stations_df, test_network.connections_df, 'data\output.csv')

    # vis.plot_netherlands()
    # vis.plot_connections()
    

