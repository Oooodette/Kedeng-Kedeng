from code.classes import Station, Connection, Trajectory, Network
from code.algorithms.random_algo import Random_algo
from code.algorithms.greedy_algo import Greedy_algo
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
    # network = Network(connections_df, stations_df, max_trajectories_nl, max_trajectory_time_nl)

    #looping until criteria are met
    # while score < minimal_score:
 
    # network = Network()
    
    # random_algo = Random_algo(network)
    # test_network = random_algo.create_network()
    # vis.plot_all(stations_df, connections_df, 'data\gadm41_NLD_1.json', test_network.used, test_network.trajectories, test_network.stations) 
    
    hillclimber_list = []
    count_list = []
    count = 0
    best_network= None
    previous_score = 0

    for x in range(10):
        print(count)
        network = Network(connections_df, stations_df, max_trajectories_nl, max_trajectory_time_nl)
        random_algo = Random_algo(network)
        test_network = random_algo.create_network()
        # vis.plot_all(stations_df, connections_df, 'data\gadm41_NLD_1.json', test_network.used, test_network.trajectories, test_network.stations) 
        hillclimber = Hillclimber(test_network, 400, 80)
        newie = hillclimber.run() 
    
        plt.plot(hillclimber.scorelist)
        plt.xlabel('iterations')
        plt.ylabel('score')
        
        score = newie.get_score()
        if score > previous_score: 
            best_network = newie
        hillclimber_list.append(score)

        count += 1
        count_list.append(count)
        previous_score = score
        
    plt.savefig('data/hillclimberplateau')
    plt.show()   
    # dictionary of lists
    # dict = {'count': count_list, 'score': hillclimber_list}
    # df = pd.DataFrame(dict)
        
    # # saving the dataframe
    # df.to_csv('data/histogram.csv')

    print(hillclimber_list)
    plt.hist(hillclimber_list, bins = 1000)
    plt.show()

    vis.plot_all(stations_df, connections_df, 'data\gadm41_NLD_1.json', best_network.used, best_network.trajectories, best_network.stations)
    
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
    
    
    # # vis.visualize_stations_connections(test_network.stations_df, test_network.connections_df)
    # # vis.visualize_network(test_network.stations_df, test_network.connections_df, 'data\output.csv')

    # # vis.plot_netherlands()
    # # vis.plot_connections()
    

