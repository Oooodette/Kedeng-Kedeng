from code.classes import Station, Connection, Trajectory, Network
from code.algorithms.random_algo import Random_algo
from code.algorithms.greedy_algo import Greedy_algo
from code.algorithms.hillclimber import Hillclimber
from code.algorithms.Evolution_algo import Evolution_algo
from code.visualize import new_visualize as vis
import code.experiments.greedy_exp as greedy_exp
import code.experiments.evolution_exp as evol_exp
import code.experiments.random_exp as random_exp
import code.experiments.hillclimber_exp as hill_exp
import argparse
import pandas as pd

def main(output, vis_output, area, start_network, algorithm):
    
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
        trajectory_maker = input("use random or greedy for making new trajectories?" )
        print('Optimizing with hillclimber')
        hillclimber = Hillclimber(network, 1000, trajectory_maker)
        network = hillclimber.run()

    elif algorithm == 'evolution': 
        print('optimizing with evolutionary algorithm')
        evolution = Evolution_algo(network, 10, start_network)
        network = evolution.last_man_standing() 

    # get score of network and print result
    score = network.get_score()
    print(f'Score of this network = {score}')

    network.save(output)

    #visualize
    vis.plot_all(stations_df, connections_df, 'data\gadm41_NLD_1.json', network.used, network.trajectories, network.stations, vis_output)

if __name__ == "__main__":

    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "find a great network")

    # Adding arguments
    parser.add_argument("-o", "--output", nargs='?', default = 'output.csv', type=str , help = "output file (csv). default = %(default)s")
    parser.add_argument("-vo", "--visualize_output", nargs='?',default = 'visualize.png', type=str,  help = "filename for the visualization of the network. default = %(default)s")
    parser.add_argument("-a", "--area",  nargs='?', default = 'nederland', type=str,  help="area to make network in (holland or nederland). default = %(default)s")
    parser.add_argument("-sn", "--start_network", nargs='?', default = 'random', type=str, help="algorithm to use for start network (random, greedy or hillclimber). default = %(default)s")
    parser.add_argument("-algo", "--algorithm", nargs='?', default = 'hillclimber',  type = str, help = "algorithm to use for optimization (hillclimber, greedy or evolution). default = %(default)s")
    parser.add_argument("-exp", "--experiment", action='store_true')
    args = parser.parse_args()
    
    if args.experiment:
        experiment = input("which experiment do you want to run?")
        if experiment == 'random':
            random_exp.run_experiment()
        elif experiment == 'greedy':
            greedy_exp.run_experiment()
        elif experiment == 'evolution':
            evol_exp.run_experiment()
        else:
            hill_exp.run_experiment()
            
        exit()
    # Ask questions interactively
    if args.output is None:
        args.output = input("Enter output file (csv): ")
    
    if args.visualize_output is None:
        args.visualize_output = input("Enter filename for your visualization (png): ")

    if args.area is None:
        args.area = input("Enter area to make network in (holland or nederland): ")

    if args.start_network is None:
        args.start_network = input("Enter algorithm to use as start network (random, greedy or hillclimber): ")

    if args.algorithm is None:
        args.algorithm = input("Enter algorithm to use for optimization (greedy, hillclimber or evolution): ")

    # Run main with provide arguments
    main(args.output, args.visualize_output, args.area, args.start_network, args.algorithm)

    


