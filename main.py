from code.classes import Station, Connection, Trajectory, Network
from code.algorithms.random_algo import Random_algo
from code.algorithms.greedy_algo import Greedy_algo
from code.algorithms.hillclimber import Hillclimber
from code.algorithms.Evolution_algo import Evolution_algo
# from code.visualize import visualize as vis
from code.visualize import new_visualize as vis
import argparse
import pandas as pd

def main(output, area, start_network, algorithm):
    
    #defining parameters for different datasets
    if area == 'holland': 
        max_trajectories = 7
        max_trajectory_time = 120
        connections_df = pd.read_csv('data\ConnectiesHolland.csv')
        stations_df = pd.read_csv('data\StationsHolland.csv')

    if area == 'nederland':
        max_trajectories = 20
        max_trajectory_time = 180
        connections_df = pd.read_csv('data\ConnectiesNationaal.csv')
        stations_df = pd.read_csv('data\StationsNationaal.csv')
    

    network = Network(connections_df, stations_df, max_trajectories, max_trajectory_time)

    if start_network == 'random':
        print('Creating random network.')
        random_algo = Random_algo(network)
        # Create network from our data
        network = random_algo.create_network()

    else:
        print('Creating greedy network')
        greedy_algo = Greedy_algo(network)
        network = greedy_algo.create_network()

    if algorithm == 'hillclimber':
        print('Optimizing with hillclimber')
        hillclimber = Hillclimber(network, 1000)
        network = hillclimber.run()

    elif algorithm == 'evolution': 
        print('optimizing with evolutionary algorithm')
        evolution = Evolution_algo(network, 10)
        network = evolution.last_man_standing() 

    # get score of network and print result
    score = network.get_score()
    print(f'Score of this network = {score}')

    network.save(output)

    #visualize
    vis.plot_all(stations_df, connections_df, 'data\gadm41_NLD_1.json', network.used, network.trajectories, network.stations)

if __name__ == "__main__":

    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "find a great network")

    # Adding arguments
    parser.add_argument("output",nargs='?', help = "output file (csv)")
    parser.add_argument("-a", "--area",  nargs='?', type=str,  help="area to make network in (holland or nederland)")
    parser.add_argument("-sn", "--start_network", nargs='?',  type=str, help="algorithm to use for start network (random or greedy)")
    parser.add_argument("-algo", "--algorithm", nargs='?',  type = str, help = "algorithm to use for optimization (hillclimber or evolution)")
    # Read arguments from command line
    args = parser.parse_args()

    # Ask questions interactively
    if args.output is None:
        args.output = input("Enter output file (csv): ")

    if args.area is None:
        args.area = input("Enter area to make network in (holland or nederland): ")

    if args.start_network is None:
        args.start_network = input("Enter algorithm to use for start network (random or greedy): ")

    if args.algorithm is None:
        args.algorithm = input("Enter algorithm to use for optimization (hillclimber or evolution   ): ")

    # Run main with provide arguments
    main(args.output, args.area, args.start_network, args.algorithm)

    


