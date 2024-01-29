from code.classes import Station, Connection, Trajectory, Network
from code.algorithms.random_algo import Random_algo
from code.algorithms.hillclimber import Hillclimber
# from code.visualize import visualize as vis
from code.visualize import new_visualize as vis
import pandas as pd
import matplotlib.pyplot as plt

#defining parameters for different datasets
max_trajectories_holland = 7
max_trajectory_time_holland = 120
max_trajectories_nl = 20
max_trajectory_time_nl = 180

if __name__ == "__main__":

    #define criteria
    minimal_score = 8000
    iterations = 0
    score = -1000

    connections_df = pd.read_csv('data\ConnectiesNationaal.csv')
    stations_df = pd.read_csv('data\StationsNationaal.csv')

    #looping until criteria are met
    # while score < minimal_score:
    network = Network(connections_df, stations_df, max_trajectories_nl, max_trajectory_time_nl)

    #looping until criteria are met
    # while score < minimal_score:
 
    # network = Network()
    
    # random_algo = Random_algo(network)
    # test_network = random_algo.create_network()
    # vis.plot_all(stations_df, connections_df, 'data\gadm41_NLD_1.json', test_network.used, test_network.trajectories, test_network.stations) 
    
    hillclimber_list = []
    count = 0
    for x in range(1000):
        print(count)
        network = Network(connections_df, stations_df, max_trajectories_nl, max_trajectory_time_nl)
        random_algo = Random_algo(network)
    
        test_network = random_algo.create_network()
    
        hillclimber = Hillclimber(test_network, 1000)

        newie = hillclimber.run() 

        score = newie.get_score()
     
        hillclimber_list.append(score)
    
        count += 1

    print(hillclimber_list)
    plt.hist(hillclimber_list, bins = 1000)
    plt.show()

  
    # hillclimber_solution = hillclimber.run()
    # # Create network from our data
    
    # score = test_network.get_score()
    # nr_traj = len(test_network.trajectories)

    # iterations += 1

    # #printing #iterations, number of trajectories and score of the network
    # print(f'number of iterations: {iterations}')
    # print(f'number of trajectories in network: {nr_traj}')
    # print(f'score of the network {score}')

    # #explicitly save the network that fulfills the criteria
    # network.save_network()
    # print(newie.trajectories[0].route, '1')
    # print(newie.trajectories[1].route, '2')
    
    #visualize
    
    # vis.plot_all(stations_df, connections_df, 'data\gadm41_NLD_1.json', newie.used, newie.trajectories, newie.stations)
    # # vis.visualize_stations_connections(test_network.stations_df, test_network.connections_df)
    # # vis.visualize_network(test_network.stations_df, test_network.connections_df, 'data\output.csv')

    # # vis.plot_netherlands()
    # # vis.plot_connections()
    

